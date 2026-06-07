import os
import sqlite3
import json
import logging
from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
import httpx
import tempfile
import aiofiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="IPFS PyPI Proxy")

# Configuration
PYPI_SIMPLE_URL = "https://pypi.org/simple"
IPFS_API_URL = os.getenv("IPFS_API_URL", "http://127.0.0.1:5001")
IPFS_GATEWAY_URL = os.getenv("IPFS_GATEWAY_URL", "http://127.0.0.1:8080")
DB_PATH = os.getenv("DB_PATH", "/data/cache.db")
PROXY_BASE_URL = os.getenv("PROXY_BASE_URL", "http://127.0.0.1:3141")

# Initialize SQLite database
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS package_cache (
            filename TEXT PRIMARY KEY,
            cid TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_cid_for_filename(filename: str) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT cid FROM package_cache WHERE filename = ?", (filename,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_cid_for_filename(filename: str, cid: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO package_cache (filename, cid) VALUES (?, ?)", (filename, cid))
    conn.commit()
    conn.close()

@app.get("/")
def index():
    return {"status": "ok", "service": "IPFS PyPI Proxy"}

@app.get("/simple/")
async def simple_index():
    # Pip usually doesn't request the root /simple/ with JSON, but we forward it just in case
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PYPI_SIMPLE_URL}/")
        return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type"))

@app.get("/simple/{package}/")
async def package_index(package: str, request: Request):
    headers = {"Accept": "application/vnd.pypi.simple.v1+json"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{PYPI_SIMPLE_URL}/{package}/", headers=headers)

        if resp.status_code != 200:
            return Response(content=resp.content, status_code=resp.status_code)

        data = resp.json()

        # Rewrite URLs in the files list
        for file_info in data.get("files", []):
            original_url = file_info["url"]
            filename = file_info["filename"]
            # Save original URL in fragment so we know where to fetch it from
            file_info["url"] = f"{PROXY_BASE_URL}/download/{filename}?source={original_url}"

        return JSONResponse(content=data, media_type="application/vnd.pypi.simple.v1+json")

@app.get("/download/{filename}")
async def download_package(filename: str, source: str):
    cid = get_cid_for_filename(filename)

    if cid:
        logger.info(f"Cache hit for {filename}: CID {cid}")
        # Ensure it is available locally via gateway
        try:
            # We must not use `async with` for the client if we are returning a StreamingResponse
            # that will consume it after the function returns, or we need to manage the lifecycle in the generator.
            # A cleaner way is to let StreamingResponse manage it by yielding from a generator that manages the client.
            async def stream_from_ipfs():
                async with httpx.AsyncClient(timeout=30.0) as ipfs_client:
                    req = ipfs_client.build_request("GET", f"{IPFS_GATEWAY_URL}/ipfs/{cid}")
                    r = await ipfs_client.send(req, stream=True)
                    if r.status_code != 200:
                        raise Exception(f"IPFS Gateway returned status {r.status_code}")
                    async for chunk in r.aiter_raw():
                        yield chunk

            # Since we can't easily catch an exception raised inside the generator *before* returning the response
            # to fall back, let's just make a HEAD or initial GET request to verify it's there.
            async with httpx.AsyncClient(timeout=5.0) as check_client:
                check_r = await check_client.head(f"{IPFS_GATEWAY_URL}/ipfs/{cid}")
                if check_r.status_code == 200:
                    return StreamingResponse(stream_from_ipfs(), media_type="application/octet-stream")
                else:
                    logger.warning(f"CID {cid} not found on gateway (status {check_r.status_code}), falling back to download")
        except Exception as e:
            logger.error(f"Failed to stream from IPFS gateway for {cid}: {e}")
            # Fall back to downloading

    logger.info(f"Cache miss for {filename}, downloading from {source}")

    # Download from PyPI to a temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("GET", source) as response:
                response.raise_for_status()
                async with aiofiles.open(tmp_path, 'wb') as f:
                    async for chunk in response.aiter_bytes():
                        await f.write(chunk)

            # Add to IPFS
            logger.info(f"Adding {filename} to IPFS")
            with open(tmp_path, "rb") as f:
                add_resp = await client.post(
                    f"{IPFS_API_URL}/api/v0/add",
                    files={"file": (filename, f)},
                    timeout=60.0
                )
                add_resp.raise_for_status()
                ipfs_data = add_resp.json()
                cid = ipfs_data["Hash"]

                logger.info(f"Added {filename} to IPFS with CID {cid}")
                save_cid_for_filename(filename, cid)

        # Stream the file back to the client
        async def stream_file():
            try:
                async with aiofiles.open(tmp_path, 'rb') as f:
                    while chunk := await f.read(8192):
                        yield chunk
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        return StreamingResponse(stream_file(), media_type="application/octet-stream")

    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        logger.error(f"Error processing {filename}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

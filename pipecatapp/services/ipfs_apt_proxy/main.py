import os
import sqlite3
import logging
import asyncio
from aiohttp import web
import aiohttp
import tempfile
import aiofiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
IPFS_API_URL = os.getenv("IPFS_API_URL", "http://127.0.0.1:5001")
IPFS_GATEWAY_URL = os.getenv("IPFS_GATEWAY_URL", "http://127.0.0.1:8080")
DB_PATH = os.getenv("DB_PATH", "/data/cache.db")
PORT = int(os.getenv("PORT", "3142"))

# Initialize SQLite database
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS package_cache (
            url TEXT PRIMARY KEY,
            cid TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_cid_for_url(url: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT cid FROM package_cache WHERE url = ?", (url,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_cid_for_url(url: str, cid: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO package_cache (url, cid) VALUES (?, ?)", (url, cid))
    conn.commit()
    conn.close()

async def handle(request):
    target_url = str(request.url)

    # Check if this is just a healthcheck
    if request.path == "/" and len(request.query) == 0 and "ubuntu" not in target_url:
        return web.json_response({"status": "ok", "service": "IPFS APT Proxy"})

    # Fast path: check if it's an InRelease or Release file (we shouldn't cache these as they change)
    is_metadata = any(x in target_url for x in ["InRelease", "Release", "Packages.xz", "Packages.gz", "Packages.bz2", "Packages.lzma", "Translation"])

    if is_metadata:
        logger.info(f"Passing through metadata request: {target_url}")
        return await fetch_and_stream(target_url, request.headers, request, cache=False)

    cid = get_cid_for_url(target_url)

    if cid:
        logger.info(f"Cache hit for {target_url}: CID {cid}")
        try:
            # Check if it's accessible via IPFS Gateway
            async with aiohttp.ClientSession() as session:
                async with session.head(f"{IPFS_GATEWAY_URL}/ipfs/{cid}", timeout=5.0) as check_r:
                    if check_r.status == 200:
                        response = web.StreamResponse()
                        response.headers['Content-Type'] = 'application/octet-stream'
                        await response.prepare(request)

                        async with session.get(f"{IPFS_GATEWAY_URL}/ipfs/{cid}", timeout=30.0) as r:
                            if r.status == 200:
                                async for chunk in r.content.iter_chunked(8192):
                                    await response.write(chunk)
                                await response.write_eof()
                                return response
                    else:
                        logger.warning(f"CID {cid} not found on gateway (status {check_r.status}), falling back to download")
        except Exception as e:
            logger.error(f"Failed to stream from IPFS gateway for {cid}: {e}")

    logger.info(f"Cache miss for {target_url}")
    return await fetch_and_stream(target_url, request.headers, request, cache=True)


async def fetch_and_stream(url: str, headers, request, cache: bool = True):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        # Filter headers
        proxy_headers = {k: v for k, v in headers.items() if k.lower() not in ["host", "connection", "proxy-connection"]}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=proxy_headers) as response:
                if response.status != 200:
                    os.unlink(tmp_path)
                    res = web.StreamResponse(status=response.status)
                    for k, v in response.headers.items():
                        if k.lower() not in ["connection", "transfer-encoding"]:
                            res.headers[k] = v
                    await res.prepare(request)
                    async for chunk in response.content.iter_chunked(8192):
                        await res.write(chunk)
                    await res.write_eof()
                    return res

                async with aiofiles.open(tmp_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)

            if cache:
                filename = url.split("/")[-1]
                logger.info(f"Adding {url} to IPFS")
                try:
                    with open(tmp_path, "rb") as f:
                        data = aiohttp.FormData()
                        data.add_field('file', f, filename=filename)
                        async with session.post(f"{IPFS_API_URL}/api/v0/add", data=data, timeout=120.0) as add_resp:
                            add_resp.raise_for_status()
                            ipfs_data = await add_resp.json()
                            cid = ipfs_data["Hash"]

                            logger.info(f"Added {url} to IPFS with CID {cid}")
                            save_cid_for_url(url, cid)
                except Exception as e:
                    logger.error(f"Failed to add to IPFS: {e}")

        res = web.StreamResponse()
        res.headers['Content-Type'] = 'application/octet-stream'
        await res.prepare(request)

        async with aiofiles.open(tmp_path, 'rb') as f:
            while chunk := await f.read(8192):
                await res.write(chunk)
        await res.write_eof()
        return res

    except Exception as e:
        logger.error(f"Error processing {url}: {e}")
        return web.Response(text=str(e), status=500)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

app = web.Application()
app.router.add_route('*', '/{tail:.*}', handle)

if __name__ == '__main__':
    web.run_app(app, port=PORT)

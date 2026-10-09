import gzip
import subprocess
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "/srv/tftp/debian-installer/amd64/initrd.gz"
with open(path, "rb") as f:
    data = f.read()

import io
import gzip
import subprocess
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "/srv/tftp/debian-installer/amd64/initrd.gz"
with open(path, "rb") as f:
    bio = io.BytesIO(f.read())

stream_idx = 0
while bio.tell() < len(bio.getvalue()):
    start_pos = bio.tell()
    try:
        gz = gzip.GzipFile(fileobj=bio)
        content = gz.read()
        print(f"Stream {stream_idx}: start={start_pos}, decompressed={len(content)}B")
        out = subprocess.check_output(["cpio", "-t"], input=content, stderr=subprocess.DEVNULL).decode().splitlines()
        print(f"  Files: {len(out)}")
        lib_entries = [x for x in out if x == "lib" or x.startswith("lib/")]
        if lib_entries:
            print(f"  WARNING: stream {stream_idx} has 'lib' entries: {lib_entries[:5]}")
        else:
            print(f"  OK: stream {stream_idx} has zero 'lib' collisions.")
        has_realtek = [x for x in out if "rtl8168g-2.fw" in x]
        if has_realtek:
            print(f"  SUCCESS: Found Realtek firmware: {has_realtek}")
        stream_idx += 1
    except Exception as e:
        print(f"Stream {stream_idx} ended at {start_pos}: {e}")
        break

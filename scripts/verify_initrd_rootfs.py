import io
import gzip
import os
import shutil
import subprocess

initrd_path = "/srv/tftp/debian-installer/amd64/initrd.gz"
orig_path = "/srv/tftp/debian-installer/amd64/initrd.gz.orig"

with open(initrd_path, "rb") as f:
    data = f.read()

test_root = "/tmp/test_rootfs"
shutil.rmtree(test_root, ignore_errors=True)
os.makedirs(test_root, exist_ok=True)

orig_size = os.path.getsize(orig_path)
s1 = data[:orig_size]
s2 = data[orig_size:]

print(f"Stream 1 size: {len(s1)}B, Stream 2 size: {len(s2)}B")

# Unpack stream 1
subprocess.run(["cpio", "-idmu"], input=gzip.decompress(s1), cwd=test_root, check=True, stderr=subprocess.DEVNULL)
# Unpack stream 2
subprocess.run(["cpio", "-idmu"], input=gzip.decompress(s2), cwd=test_root, check=True, stderr=subprocess.DEVNULL)

# Verify lib symlink
lib_path = os.path.join(test_root, "lib")
is_symlink = os.path.islink(lib_path)
symlink_target = os.readlink(lib_path) if is_symlink else None
print(f"lib is symlink: {is_symlink}, target: {symlink_target}")
assert is_symlink, "FATAL: lib was overwritten and is not a symlink!"
assert symlink_target == "usr/lib", f"FATAL: lib does not point to usr/lib! points to {symlink_target}"

# Verify init-debug exists and is readable through /lib
init_debug = os.path.join(test_root, "lib/debian-installer/init-debug")
assert os.path.exists(init_debug), f"FATAL: {init_debug} not found!"
print("Verified: /lib/debian-installer/init-debug exists and is readable.")

# Verify Realtek firmware exists through both /lib and /usr/lib
fw_lib = os.path.join(test_root, "lib/firmware/rtl_nic/rtl8168g-2.fw")
fw_usr = os.path.join(test_root, "usr/lib/firmware/rtl_nic/rtl8168g-2.fw")
assert os.path.exists(fw_lib), f"FATAL: {fw_lib} not found!"
assert os.path.exists(fw_usr), f"FATAL: {fw_usr} not found!"
print("Verified: rtl_nic/rtl8168g-2.fw exists and is readable via both paths!")

# Clean up
shutil.rmtree(test_root)
print("ALL VERIFICATIONS PASSED! Root filesystem will NOT panic.")

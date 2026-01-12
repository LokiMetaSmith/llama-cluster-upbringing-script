#!/usr/bin/env python3
import os
import sys
import errno
import time
import stat
import json
import logging
import base64
import requests
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from threading import Lock

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('unified_fs')

class DataCache:
    """Helper to cache API responses to ensure consistency between getattr and read."""
    def __init__(self, ttl=5):
        self.ttl = ttl
        self.cache = {}
        self.lock = Lock()

    def get(self, key):
        with self.lock:
            if key in self.cache:
                timestamp, data = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    return data
                else:
                    del self.cache[key]
        return None

    def set(self, key, data):
        with self.lock:
            self.cache[key] = (time.time(), data)

class Backend:
    def getattr(self, path):
        raise FuseOSError(errno.ENOENT)

    def readdir(self, path):
        return []

    def read(self, path, size, offset):
        raise FuseOSError(errno.ENOENT)

class ConsulBackend(Backend):
    def __init__(self, base_url="http://localhost:8500/v1"):
        self.base_url = base_url
        self.services_cache = DataCache(ttl=10)
        self.file_cache = DataCache(ttl=5) # Short TTL for dynamic content
        self.kv_cache = DataCache(ttl=5)

    def _get_services_list(self):
        cached = self.services_cache.get('list')
        if cached:
            return cached

        try:
            resp = requests.get(f"{self.base_url}/catalog/services", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                self.services_cache.set('list', data)
                return data
        except Exception as e:
            logger.error(f"Consul list error: {e}")
        return {}

    def _get_service_file(self, service_name, fname):
        key = f"{service_name}/{fname}"
        cached = self.file_cache.get(key)
        if cached:
            return cached

        data_str = ""
        if fname == 'nodes.json':
            try:
                resp = requests.get(f"{self.base_url}/catalog/service/{service_name}", timeout=2)
                if resp.status_code == 200:
                    data_str = json.dumps(resp.json(), indent=2) + "\n"
            except Exception as e:
                data_str = json.dumps({"error": str(e)}) + "\n"
        elif fname == 'status.json':
            # Simplified status check placeholder
            data_str = json.dumps({"service": service_name, "status": "unknown"}, indent=2) + "\n"

        b_data = data_str.encode('utf-8')
        self.file_cache.set(key, b_data)
        return b_data

    def _get_kv_keys(self, prefix):
        # Prefix should not start with slash for Consul API
        api_prefix = prefix.lstrip('/')
        if api_prefix and not api_prefix.endswith('/'):
            api_prefix += '/'

        cache_key = f"keys:{api_prefix}"
        cached = self.kv_cache.get(cache_key)
        if cached:
            return cached

        try:
            # keys=true returns list of keys under prefix
            url = f"{self.base_url}/kv/{api_prefix}?keys=true&separator=/"
            resp = requests.get(url, timeout=2)
            if resp.status_code == 200:
                keys = resp.json()
                # Clean up keys to be relative to current dir
                clean_keys = []
                for k in keys:
                    rel = k[len(api_prefix):]
                    if rel: # skip the directory itself if present
                        # remove trailing slash for display
                        clean_keys.append(rel.rstrip('/'))
                self.kv_cache.set(cache_key, clean_keys)
                return clean_keys
        except Exception as e:
             logger.error(f"Consul KV list error: {e}")

        return []

    def _get_kv_value(self, path):
        # Path relative to /consul/kv
        api_path = path.lstrip('/')
        cache_key = f"val:{api_path}"
        cached = self.kv_cache.get(cache_key)
        if cached:
            return cached

        try:
            resp = requests.get(f"{self.base_url}/kv/{api_path}", timeout=2)
            if resp.status_code == 200:
                data = resp.json()
                if data and len(data) > 0 and 'Value' in data[0]:
                    val = data[0]['Value']
                    if val:
                        decoded = base64.b64decode(val)
                        self.kv_cache.set(cache_key, decoded)
                        return decoded
        except Exception as e:
             logger.error(f"Consul KV get error: {e}")

        empty = b""
        self.kv_cache.set(cache_key, empty)
        return empty

    def readdir(self, path):
        parts = [p for p in path.split('/') if p]

        if not parts:
            return ['services', 'kv']

        if parts[0] == 'services':
            if len(parts) == 1:
                return list(self._get_services_list().keys())
            elif len(parts) == 2:
                # /consul/services/<service_name>
                return ['status.json', 'nodes.json']

        if parts[0] == 'kv':
            # Path inside KV: /consul/kv/foo/bar -> prefix "foo/bar"
            # subpath is everything after 'kv'
            kv_path = "/".join(parts[1:])
            return self._get_kv_keys(kv_path)

        return []

    def getattr(self, path):
        parts = [p for p in path.split('/') if p]
        now = time.time()

        # /consul root
        if not parts:
            return dict(st_mode=(stat.S_IFDIR | 0o755), st_nlink=2, st_ctime=now, st_mtime=now, st_atime=now)

        if parts[0] == 'services':
            if len(parts) == 1: # /consul/services
                 return dict(st_mode=(stat.S_IFDIR | 0o755), st_nlink=2, st_ctime=now, st_mtime=now, st_atime=now)

            if len(parts) == 2: # /consul/services/<name>
                 return dict(st_mode=(stat.S_IFDIR | 0o755), st_nlink=2, st_ctime=now, st_mtime=now, st_atime=now)

            if len(parts) == 3: # /consul/services/<name>/<file>
                 fname = parts[2]
                 if fname in ['status.json', 'nodes.json']:
                     content = self._get_service_file(parts[1], fname)
                     return dict(st_mode=(stat.S_IFREG | 0o444), st_nlink=1, st_size=len(content), st_ctime=now, st_mtime=now, st_atime=now)

        if parts[0] == 'kv':
             # Need to distinguish file vs dir
             # Heuristic: try to list keys. If children exist -> DIR.
             # If no children, check if it has a value -> FILE.
             kv_path = "/".join(parts[1:])
             if not kv_path: # /consul/kv root
                 return dict(st_mode=(stat.S_IFDIR | 0o755), st_nlink=2, st_ctime=now, st_mtime=now, st_atime=now)

             # Check if it has children (is a folder)
             children = self._get_kv_keys(kv_path)
             if children:
                  return dict(st_mode=(stat.S_IFDIR | 0o755), st_nlink=2, st_ctime=now, st_mtime=now, st_atime=now)

             # If no children, treat as file (or empty dir, but we assume file first for access)
             # Fetch value to get size
             content = self._get_kv_value(kv_path)
             if content or content == b"":
                 # Valid key (even if empty)
                 return dict(st_mode=(stat.S_IFREG | 0o444), st_nlink=1, st_size=len(content), st_ctime=now, st_mtime=now, st_atime=now)

        raise FuseOSError(errno.ENOENT)

    def read(self, path, size, offset):
        parts = [p for p in path.split('/') if p]

        if parts[0] == 'services' and len(parts) == 3:
            service = parts[1]
            fname = parts[2]
            content = self._get_service_file(service, fname)
            return content[offset:offset+size]

        if parts[0] == 'kv':
            kv_path = "/".join(parts[1:])
            content = self._get_kv_value(kv_path)
            return content[offset:offset+size]

        raise FuseOSError(errno.ENOENT)

class MemoryBackend(Backend):
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.cache = DataCache(ttl=5)

    def _get_recent_events(self):
        cached = self.cache.get('recent.json')
        if cached:
            return cached

        try:
            resp = requests.get(f"{self.base_url}/events?limit=20", timeout=2)
            if resp.status_code == 200:
                data_str = json.dumps(resp.json(), indent=2) + "\n"
            else:
                data_str = "[]\n"
        except Exception as e:
            data_str = json.dumps({"error": str(e)}) + "\n"

        b_data = data_str.encode('utf-8')
        self.cache.set('recent.json', b_data)
        return b_data

    def readdir(self, path):
        parts = [p for p in path.split('/') if p]
        if not parts:
            return ['events']
        if parts[0] == 'events':
            return ['recent.json']
        return []

    def getattr(self, path):
        parts = [p for p in path.split('/') if p]
        now = time.time()

        if not parts:
             return dict(st_mode=(stat.S_IFDIR | 0o755), st_nlink=2)

        if parts[0] == 'events':
            if len(parts) == 1:
                return dict(st_mode=(stat.S_IFDIR | 0o755), st_nlink=2)
            if len(parts) == 2 and parts[1] == 'recent.json':
                content = self._get_recent_events()
                return dict(st_mode=(stat.S_IFREG | 0o444), st_nlink=1, st_size=len(content), st_ctime=now, st_mtime=now, st_atime=now)

        raise FuseOSError(errno.ENOENT)

    def read(self, path, size, offset):
        parts = [p for p in path.split('/') if p]
        if len(parts) == 2 and parts[0] == 'events' and parts[1] == 'recent.json':
            content = self._get_recent_events()
            return content[offset:offset+size]

        raise FuseOSError(errno.ENOENT)


class UnifiedFS(LoggingMixIn, Operations):
    def __init__(self, root_storage):
        self.root_storage = root_storage
        self.consul = ConsulBackend()
        self.memory = MemoryBackend()
        self.mutex = Lock()

    def getattr(self, path, fh=None):
        if path == '/':
            now = time.time()
            return dict(st_mode=(stat.S_IFDIR | 0o755), st_nlink=2, st_ctime=now, st_mtime=now, st_atime=now)

        parts = [p for p in path.split('/') if p]
        first = parts[0]
        subpath = '/' + '/'.join(parts[1:])

        if first == 'consul':
            return self.consul.getattr(subpath)
        elif first == 'memory':
            return self.memory.getattr(subpath)
        elif first == 'fs':
            # Passthrough
            full_path = os.path.join(self.root_storage, *parts[1:])
            try:
                st = os.lstat(full_path)
                return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
            except OSError:
                raise FuseOSError(errno.ENOENT)

        raise FuseOSError(errno.ENOENT)

    def readdir(self, path, fh):
        dirents = ['.', '..']
        if path == '/':
            dirents.extend(['consul', 'memory', 'fs'])
            return dirents

        parts = [p for p in path.split('/') if p]
        first = parts[0]
        subpath = '/' + '/'.join(parts[1:])

        if first == 'consul':
            dirents.extend(self.consul.readdir(subpath))
        elif first == 'memory':
            dirents.extend(self.memory.readdir(subpath))
        elif first == 'fs':
             full_path = os.path.join(self.root_storage, *parts[1:])
             if os.path.isdir(full_path):
                 dirents.extend(os.listdir(full_path))

        return dirents

    def read(self, path, size, offset, fh):
        parts = [p for p in path.split('/') if p]
        first = parts[0]
        subpath = '/' + '/'.join(parts[1:])

        if first == 'consul':
            return self.consul.read(subpath, size, offset)
        elif first == 'memory':
            return self.memory.read(subpath, size, offset)
        elif first == 'fs':
            full_path = os.path.join(self.root_storage, *parts[1:])
            with open(full_path, 'rb') as f:
                f.seek(offset)
                return f.read(size)

        raise FuseOSError(errno.ENOENT)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: %s <mountpoint> <root_storage>' % sys.argv[0])
        sys.exit(1)

    mountpoint = sys.argv[1]
    root_storage = sys.argv[2]

    if not os.path.exists(root_storage):
        print(f"Root storage {root_storage} does not exist.")
        sys.exit(1)

    # Enable default_permissions to enforce kernel-level permission checks for the underlying FS
    fuse = FUSE(UnifiedFS(root_storage), mountpoint, foreground=True, allow_other=True, default_permissions=True)

import os
import subprocess
import time
import xml.etree.ElementTree as ET
import requests
import platform
import tarfile
import zipfile
import stat

class SyncthingNode:
    def __init__(self, name, gui_port, listen_port, base_dir="."):
        self.name = name
        self.gui_port = gui_port
        self.listen_port = listen_port
        self.home_dir = os.path.abspath(os.path.join(base_dir, f"node_{name}"))
        self.config_file = os.path.join(self.home_dir, "config.xml")
        self.api_url = f"http://127.0.0.1:{self.gui_port}"
        self.api_key = None
        self.device_id = None
        self.process = None

        is_windows = platform.system() == "Windows"
        bin_name = "syncthing.exe" if is_windows else "syncthing_bin"
        self.syncthing_bin = os.path.abspath(os.path.join(os.path.dirname(__file__), bin_name))

        os.makedirs(self.home_dir, exist_ok=True)
        self._ensure_binary_exists()

    def _ensure_binary_exists(self):
        # We need to make sure we don't treat a broken ASCII file as a real binary
        if os.path.exists(self.syncthing_bin) and os.path.getsize(self.syncthing_bin) > 5000000:
            return

        print(f"[{self.name}] Downloading Syncthing binary for {platform.system()} {platform.machine()}...")
        version = "v1.27.6"
        os_name = platform.system().lower()
        arch = platform.machine().lower()

        if os_name == "darwin":
            os_name = "macos"

        if arch in ["x86_64", "amd64"]:
            arch = "amd64"
        elif arch in ["arm64", "aarch64"]:
            arch = "arm64"

        ext = "zip" if os_name == "windows" else "tar.gz"
        filename = f"syncthing-{os_name}-{arch}-{version}.{ext}"
        url = f"https://github.com/syncthing/syncthing/releases/download/{version}/{filename}"

        download_path = os.path.join(os.path.dirname(__file__), filename)

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(download_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        if ext == "zip":
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    if member.endswith('syncthing.exe'):
                        with open(self.syncthing_bin, 'wb') as outfile:
                            outfile.write(zip_ref.read(member))
                        break
        else:
            with tarfile.open(download_path, 'r:gz') as tar_ref:
                for member in tar_ref.getmembers():
                    # The actual binary in the tar is usually named exactly `syncthing` and has a large size
                    if member.isfile() and member.name.endswith('/syncthing') and member.size > 1000000:
                        f = tar_ref.extractfile(member)
                        if f:
                            with open(self.syncthing_bin, 'wb') as outfile:
                                outfile.write(f.read())
                        break

        st = os.stat(self.syncthing_bin)
        os.chmod(self.syncthing_bin, st.st_mode | stat.S_IEXEC)
        os.remove(download_path)
        print(f"[{self.name}] Binary downloaded and extracted successfully.")

    def generate_config(self):
        print(f"[{self.name}] Generating configuration...")
        subprocess.run([self.syncthing_bin, "generate", "--home", self.home_dir], capture_output=True)
        self._modify_config_ports()
        self.api_key = self._get_api_key()
        res = subprocess.run([self.syncthing_bin, "--home", self.home_dir, "cli", "show", "system"], capture_output=True, env={"STGUIAPIKEY": self.api_key, "STNOUPGRADE": "1"})
        self.device_id = self._get_device_id()

    def _modify_config_ports(self):
        tree = ET.parse(self.config_file)
        root = tree.getroot()
        gui = root.find("gui")
        address = gui.find("address")
        address.text = f"127.0.0.1:{self.gui_port}"
        gui.set("enabled", "true")
        gui.set("tls", "false")
        options = root.find("options")
        listen = options.find("listenAddress")
        listen.text = f"tcp://127.0.0.1:{self.listen_port}"
        options.find("natEnabled").text = "false"
        options.find("globalAnnounceEnabled").text = "false"
        options.find("localAnnounceEnabled").text = "false"
        tree.write(self.config_file)

    def _get_api_key(self):
        tree = ET.parse(self.config_file)
        return tree.getroot().find("gui").find("apikey").text

    def _get_device_id(self):
        tree = ET.parse(self.config_file)
        for device in tree.getroot().findall("device"):
             return device.attrib["id"]
        return None

    def start(self):
        print(f"[{self.name}] Starting Syncthing...")
        self.process = subprocess.Popen([self.syncthing_bin, "--home", self.home_dir, "--no-browser", "--gui-apikey", self.api_key], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(15):
            try:
                res = requests.get(f"{self.api_url}/rest/system/ping", headers={"X-API-Key": self.api_key})
                if res.status_code == 200:
                    status = requests.get(f"{self.api_url}/rest/system/status", headers={"X-API-Key": self.api_key}).json()
                    self.device_id = status["myID"]
                    print(f"[{self.name}] Online! Device ID: {self.device_id}")
                    return
            except requests.ConnectionError:
                pass
            time.sleep(1)
        raise Exception(f"[{self.name}] Failed to start.")

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            print(f"[{self.name}] Stopped.")

    def get_config(self):
        res = requests.get(f"{self.api_url}/rest/config", headers={"X-API-Key": self.api_key})
        return res.json()

    def set_config(self, config):
        res = requests.put(f"{self.api_url}/rest/config", headers={"X-API-Key": self.api_key}, json=config)
        return res.status_code == 200

    def add_device(self, device_id, address):
        config = self.get_config()
        for dev in config["devices"]:
            if dev["deviceID"] == device_id:
                return
        config["devices"].append({
            "deviceID": device_id,
            "name": "Peer",
            "addresses": [f"tcp://{address}"],
            "compression": "metadata",
            "certName": "",
            "introducer": False,
            "skipIntroductionRemovals": False,
            "introducedBy": "",
            "paused": False,
            "allowedNetworks": [],
            "autoAcceptFolders": True,
            "maxSendKbps": 0,
            "maxRecvKbps": 0,
            "ignoredFolders": [],
            "maxRequestKiB": 0,
            "untrusted": False,
            "remoteGUIPort": 0
        })
        self.set_config(config)
        print(f"[{self.name}] Added peer device {device_id}")

    def share_folder(self, folder_id, path, peer_device_id, type="sendreceive"):
        config = self.get_config()
        os.makedirs(path, exist_ok=True)
        folder = {
            "id": folder_id,
            "label": "Models",
            "filesystemType": "basic",
            "path": path,
            "type": type,
            "devices": [{"deviceID": self.device_id}, {"deviceID": peer_device_id}],
            "rescanIntervalS": 5,
            "fsync": True,
            "copiers": 0,
            "pullerMaxPendingKiB": 0,
            "hashers": 0,
            "order": "random",
            "ignorePerms": False,
            "shortID": "",
            "autoNormalize": True,
            "pullerPauseS": 0,
            "maxConflicts": -1,
            "disableSparseFiles": False,
            "disableTempIndexes": False,
            "paused": False,
            "weakHashThresholdPct": 25,
            "markerName": ".stfolder",
            "copyOwnershipFromParent": False,
            "modTimeWindowS": 0,
            "maxConcurrentWrites": 2,
            "disableFsync": False,
            "blockPullOrder": "standard",
            "copyRangeMethod": "standard",
            "caseSensitiveFS": False,
            "syncOwnership": False,
            "sendOwnership": False,
            "syncXattrs": False,
            "sendXattrs": False,
            "xattrFilter": {
                "maxSingleEntrySize": 1024,
                "maxTotalSize": 4096
            }
        }
        for i, f in enumerate(config["folders"]):
            if f["id"] == folder_id:
                config["folders"][i] = folder
                self.set_config(config)
                return
        config["folders"].append(folder)
        self.set_config(config)
        print(f"[{self.name}] Shared folder '{folder_id}' at {path}")

    def get_completion(self, device_id, folder_id):
        res = requests.get(f"{self.api_url}/rest/db/completion", headers={"X-API-Key": self.api_key}, params={"device": device_id, "folder": folder_id})
        if res.status_code == 200:
            return res.json()["completion"]
        return 0

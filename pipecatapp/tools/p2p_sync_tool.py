import os
import time
import platform
import tarfile
import zipfile
import stat
import subprocess
import requests
import xml.etree.ElementTree as ET
import logging
from typing import Dict, Any, Optional

class P2PSyncTool:
    """A tool to manage P2P file synchronization (like .gguf models) using Syncthing."""

    def __init__(self, base_dir: Optional[str] = None, name: str = "agent_node", gui_port: int = 8384, listen_port: int = 22000):
        self.name = "p2p_sync"
        self.description = "A tool to manage P2P file synchronization (like .gguf models) using Syncthing."
        self.input_schema = {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["start", "stop", "add_peer", "share_folder", "status"],
                    "description": "The P2P sync action to perform."
                },
                "peer_device_id": {
                    "type": "string",
                    "description": "The device ID of the peer Syncthing node."
                },
                "address": {
                    "type": "string",
                    "description": "IP/host and port of the peer node (required for 'add_peer')."
                },
                "folder_id": {
                    "type": "string",
                    "description": "The ID of the synchronized folder."
                },
                "path": {
                    "type": "string",
                    "description": "The local path for the folder (required for 'share_folder')."
                },
                "folder_type": {
                    "type": "string",
                    "enum": ["sendreceive", "sendonly", "receiveonly"],
                    "default": "sendreceive",
                    "description": "Type of synchronization for the folder."
                }
            },
            "required": ["action"]
        }

        self.name_tool = "p2p_sync_tool"

        if base_dir is None:
            # Use a default temp/storage dir for the agent if none provided
            self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.sync_data"))
        else:
            self.base_dir = base_dir

        self.name = name
        self.gui_port = gui_port
        self.listen_port = listen_port
        self.home_dir = os.path.abspath(os.path.join(self.base_dir, f"node_{name}"))
        self.config_file = os.path.join(self.home_dir, "config.xml")
        self.api_url = f"http://127.0.0.1:{self.gui_port}"
        self.api_key = None
        self.device_id = None
        self.process = None

        is_windows = platform.system() == "Windows"
        bin_name = "syncthing.exe" if is_windows else "syncthing_bin"
        self.syncthing_bin = os.path.abspath(os.path.join(os.path.dirname(__file__), bin_name))

        os.makedirs(self.home_dir, exist_ok=True)

    def _ensure_binary_exists(self):
        if os.path.exists(self.syncthing_bin) and os.path.getsize(self.syncthing_bin) > 5000000:
            return

        logging.info(f"[{self.name}] Downloading Syncthing binary for {platform.system()} {platform.machine()}...")
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
                    if member.isfile() and member.name.endswith('/syncthing') and member.size > 1000000:
                        f = tar_ref.extractfile(member)
                        if f:
                            with open(self.syncthing_bin, 'wb') as outfile:
                                outfile.write(f.read())
                        break

        st = os.stat(self.syncthing_bin)
        os.chmod(self.syncthing_bin, st.st_mode | stat.S_IEXEC)
        os.remove(download_path)
        logging.info(f"[{self.name}] Binary downloaded and extracted successfully.")

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

    def initialize_and_start(self) -> str:
        """Downloads binary if missing, generates config, and starts the daemon."""
        try:
            self._ensure_binary_exists()

            # Generate config if it doesn't exist
            if not os.path.exists(self.config_file):
                subprocess.run([self.syncthing_bin, "generate", "--home", self.home_dir], capture_output=True)
                self._modify_config_ports()

            self.api_key = self._get_api_key()
            self.device_id = self._get_device_id()

            self.process = subprocess.Popen(
                [self.syncthing_bin, "--home", self.home_dir, "--no-browser", "--gui-apikey", self.api_key],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            for _ in range(15):
                try:
                    res = requests.get(f"{self.api_url}/rest/system/ping", headers={"X-API-Key": self.api_key})
                    if res.status_code == 200:
                        status = requests.get(f"{self.api_url}/rest/system/status", headers={"X-API-Key": self.api_key}).json()
                        self.device_id = status["myID"]
                        return f"Syncthing started successfully. Device ID: {self.device_id}"
                except requests.ConnectionError:
                    pass
                time.sleep(1)

            return f"Error: Failed to start Syncthing on port {self.gui_port}."
        except Exception as e:
            logging.error(f"Failed to start Syncthing: {e}")
            return f"Error initializing Syncthing: {e}"

    def stop(self) -> str:
        """Stops the Syncthing daemon."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
            return "Syncthing stopped."
        return "Syncthing is not running."

    def get_config(self):
        res = requests.get(f"{self.api_url}/rest/config", headers={"X-API-Key": self.api_key})
        return res.json()

    def set_config(self, config):
        res = requests.put(f"{self.api_url}/rest/config", headers={"X-API-Key": self.api_key}, json=config)
        return res.status_code == 200

    def add_peer(self, peer_device_id: str, address: str) -> str:
        """Adds a peer node to synchronize with."""
        if not self.process:
            return "Error: Syncthing daemon is not running."

        try:
            config = self.get_config()
            for dev in config["devices"]:
                if dev["deviceID"] == peer_device_id:
                    return f"Peer {peer_device_id} already exists."

            config["devices"].append({
                "deviceID": peer_device_id,
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
            return f"Added peer device {peer_device_id} at {address}."
        except Exception as e:
            return f"Error adding peer: {e}"

    def share_folder(self, folder_id: str, path: str, peer_device_id: str, folder_type: str = "sendreceive") -> str:
        """Shares a folder with a specific peer device."""
        if not self.process:
            return "Error: Syncthing daemon is not running."

        try:
            config = self.get_config()
            os.makedirs(path, exist_ok=True)
            folder = {
                "id": folder_id,
                "label": "Models",
                "filesystemType": "basic",
                "path": path,
                "type": folder_type,
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
                    return f"Updated shared folder '{folder_id}' at {path}."

            config["folders"].append(folder)
            self.set_config(config)
            return f"Shared folder '{folder_id}' at {path}."
        except Exception as e:
            return f"Error sharing folder: {e}"

    def check_sync_status(self, peer_device_id: str, folder_id: str) -> str:
        """Returns the completion percentage of a synced folder with a peer."""
        if not self.process:
            return "Error: Syncthing daemon is not running."

        try:
            res = requests.get(
                f"{self.api_url}/rest/db/completion",
                headers={"X-API-Key": self.api_key},
                params={"device": peer_device_id, "folder": folder_id}
            )
            if res.status_code == 200:
                completion = res.json()["completion"]
                return f"Sync completion for '{folder_id}' with peer {peer_device_id}: {completion:.2f}%"
            return f"Error: Could not retrieve status (Status Code: {res.status_code})"
        except Exception as e:
            return f"Error checking sync status: {e}"

    def run(self, action: str, **kwargs) -> str:
        """Runs the specified Syncthing action."""
        if action == "start":
            return self.initialize_and_start()
        elif action == "stop":
            return self.stop()
        elif action == "add_peer":
            peer_device_id = kwargs.get("peer_device_id", "")
            address = kwargs.get("address", "")
            return self.add_peer(peer_device_id, address)
        elif action == "share_folder":
            folder_id = kwargs.get("folder_id", "")
            path = kwargs.get("path", "")
            peer_device_id = kwargs.get("peer_device_id", "")
            folder_type = kwargs.get("folder_type", "sendreceive")
            return self.share_folder(folder_id, path, peer_device_id, folder_type)
        elif action == "status":
            peer_device_id = kwargs.get("peer_device_id", "")
            folder_id = kwargs.get("folder_id", "")
            return self.check_sync_status(peer_device_id, folder_id)
        else:
            return f"Error: Unknown action '{action}'"

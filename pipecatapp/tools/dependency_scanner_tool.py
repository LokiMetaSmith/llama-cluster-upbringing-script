import httpx
import logging
from typing import Optional, Dict, Any

class DependencyScannerTool:
    """A tool for scanning Python packages for known security vulnerabilities.

    This tool queries the OSV (Open Source Vulnerabilities) database and PyPI
    to identify potential security risks in dependencies.

    Attributes:
        description (str): A brief description of the tool's purpose.
        name (str): The name of the tool.
    """
    def __init__(self):
        """Initializes the DependencyScannerTool."""
        self.description = "Scans Python packages for known security vulnerabilities using OSV.dev."
        self.name = "dependency_scanner"

    def _get_latest_version(self, package_name: str) -> Optional[str]:
        """Fetches the latest version of a package from PyPI."""
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"https://pypi.org/pypi/{package_name}/json")
                if response.status_code == 200:
                    data = response.json()
                    return data.get("info", {}).get("version")
                else:
                    logging.warning(f"Could not find package '{package_name}' on PyPI. Status: {response.status_code}")
                    return None
        except Exception as e:
            logging.error(f"Error fetching version for '{package_name}': {e}")
            return None

    def scan_package(self, package_name: str, version: Optional[str] = None) -> str:
        """Scans a specific package version for vulnerabilities.

        If no version is provided, it attempts to resolve the latest version from PyPI.

        Args:
            package_name (str): The name of the package (e.g., 'requests').
            version (str, optional): The specific version to check. Defaults to latest.

        Returns:
            str: A report of the findings.
        """
        if not version:
            version = self._get_latest_version(package_name)
            if not version:
                return f"Error: Could not determine version for package '{package_name}'. It may not exist on PyPI."

        logging.info(f"Scanning {package_name}=={version} for vulnerabilities...")

        payload = {
            "package": {
                "name": package_name,
                "ecosystem": "PyPI"
            },
            "version": version
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post("https://api.osv.dev/v1/query", json=payload)

                if response.status_code != 200:
                    return f"Error querying OSV API: {response.status_code} {response.text}"

                data = response.json()
                vulns = data.get("vulns", [])

                if not vulns:
                    return f"Safe: No known vulnerabilities found for {package_name}=={version}."

                report = f"⚠️ UNSAFE: Found {len(vulns)} vulnerabilities for {package_name}=={version}:\n"
                for vuln in vulns:
                    vuln_id = vuln.get("id", "Unknown ID")
                    summary = vuln.get("summary", "No summary available")
                    details = vuln.get("details", "")[:100] + "..." if vuln.get("details") else ""
                    report += f"- [{vuln_id}] {summary}: {details}\n"

                return report

        except Exception as e:
            return f"Error during vulnerability scan: {e}"

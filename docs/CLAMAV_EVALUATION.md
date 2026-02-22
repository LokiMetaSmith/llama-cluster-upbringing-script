# ClamAV Evaluation Report

## Executive Summary
This evaluation confirms that **ClamAV is a viable and valuable tool** for preventing malware, including "rogue agent" code, within the Pipecat environment. By leveraging custom signatures, we successfully demonstrated the detection of specific malicious patterns (e.g., destructive commands, reverse shells) that a rogue AI agent might generate.

## 1. Installation & Integration
We implemented a dedicated Ansible role (`ansible/roles/clamav`) to automate the deployment of ClamAV.
- **Components Installed:** `clamav` (scanner), `clamav-daemon` (service), `clamav-freshclam` (updater).
- **Configuration:** The role automatically configures the daemon and deploys custom signature databases.
- **Ease of Use:** The installation is seamless and integrates directly into the existing Ansible playbook structure.

## 2. Capabilities & "Rogue Agent" Detection
While ClamAV is traditionally used for email and file scanning against known malware, our evaluation focused on its ability to detect **custom malicious patterns** typical of a compromised or hallucinating AI agent.

### Custom Signatures
We developed a custom signature database (`rogue_agent.ldb`) using ClamAV's logical signature format to detect:
1.  **Destructive Commands:** Python scripts executing `rm -rf /`.
2.  **Reverse Shells:** Python scripts importing `socket` + `subprocess` + `os.dup2`.

### Test Results
We ran a controlled test suite (`scripts/evaluate_clamav.py`) against:
- A standard EICAR test file (Control: Known Malware)
- A generated "Rogue" script with `rm -rf /` (Control: Destructive Behavior)
- A generated "Rogue" script with a reverse shell (Control: Remote Access Trojan)
- A safe "Hello World" script (Control: False Positive)

**Results:**
- **Detection Rate:** 100% (All threats detected).
- **False Positives:** 0% (Safe file ignored).
- **Performance:** Scan time for the test batch was ~9 seconds (mostly database loading time).

## 3. Recommendation
**We recommend adopting ClamAV** as part of the defense-in-depth strategy for the Pipecat agent environment.

**Value Proposition:**
- **Low-hanging Fruit:** Immediately catches standard malware downloaded from the internet.
- **Customizable Defense:** Allows us to write specific rules for "bad code" patterns that LLMs might generate, acting as a guardrail.
- **Open Source & Standard:** Well-supported, easy to automate.

### Next Steps
1.  **Integrate into CI/CD:** Run `clamscan` on agent code repositories.
2.  **Runtime Protection:** Integrate `clamdscan` (daemon client) into the `CodeRunnerTool` to scan generated code *before* execution.
3.  **Expand Rules:** Add more patterns to `rogue_agent.ldb` (e.g., cryptocurrency miners, suspicious network calls).

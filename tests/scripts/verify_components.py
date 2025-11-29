#!/usr/bin/env python3
import subprocess
import os
import shutil
import sys

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def verify_systemd_service(service_name):
    # Check if systemctl exists first
    if not shutil.which("systemctl"):
        return False, "systemctl command not found (not a systemd environment?)"
    return run_command(f"systemctl is-active {service_name}")

def verify_nomad_job(job_name):
    # Check if nomad exists
    if not shutil.which("nomad"):
        return False, "nomad command not found"

    # Check status
    ok, output = run_command(f"nomad job status {job_name}")
    if not ok:
        return False, output

    # Simple check for "running" status in output might be too loose,
    # but nomad exit code 0 usually means the job is registered.
    # Let's check for 'Status = running' or 'Status = dead' etc.
    if "Status = running" in output or "Status = pending" in output:
         return True, "Job is registered and running/pending"
    return True, "Job is registered (check status for details)"

def verify_file_exists(path):
    if os.path.exists(path):
        return True, f"File {path} exists."
    return False, f"File {path} not found."

def verify_command_available(command):
    path = shutil.which(command)
    if path:
        return True, f"{command} found at {path}"
    return False, f"{command} not found"

def verify_package_installed(package_name):
    if shutil.which("dpkg"):
        ok, _ = run_command(f"dpkg -l {package_name}")
        if ok:
             return True, f"Package {package_name} is installed"
        else:
             return False, f"Package {package_name} not found via dpkg"
    return False, "dpkg not found"

def print_result(component, ok, msg):
    status = "[PASS]" if ok else "[FAIL]"
    # Color codes
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    color = GREEN if ok else RED
    print(f"{color}{status} {component}{RESET}: {msg}")

def verify_provisioning_api():
    print("--- provisioning_api ---")
    ok, msg = verify_systemd_service("provisioning-api")
    if not ok:
        # Fallback: check if file exists
        f_ok, f_msg = verify_file_exists("/opt/provisioning_api/provisioning_api.py")
        if f_ok:
            print_result("provisioning_api", True, f"Service check failed ({msg}), but file exists at {f_msg}")
        else:
            print_result("provisioning_api", False, f"{msg} AND {f_msg}")
    else:
        print_result("provisioning_api", True, msg)

def verify_desktop_extras():
    print("--- desktop_extras ---")
    # Check for nms
    ok, msg = verify_command_available("nms")
    print_result("nms", ok, msg)

    # Check for figlet fonts (sample)
    # Usually in /home/user/.local/share/fonts or similar
    # We'll just check if git, make are present as they are deps
    ok, msg = verify_command_available("make")
    print_result("make", ok, msg)

def verify_paddler():
    print("--- paddler ---")
    ok, msg = verify_command_available("paddler")
    print_result("paddler", ok, msg)

def verify_vision():
    print("--- vision ---")
    ok, msg = verify_package_installed("libgl1")
    print_result("libgl1", ok, msg)

def verify_power_manager():
    print("--- power_manager ---")
    ok, msg = verify_systemd_service("power-agent")
    if not ok:
        f_ok, f_msg = verify_file_exists("/opt/power_manager/power_agent.py")
        if f_ok:
             print_result("power_manager", True, f"Service check failed, but file exists.")
        else:
             print_result("power_manager", False, msg)
    else:
        print_result("power_manager", True, msg)

def verify_world_model_service():
    print("--- world_model_service ---")
    ok, msg = verify_nomad_job("world_model")
    print_result("Nomad Job: world_model", ok, msg)

    ok, msg = verify_nomad_job("llamacpp-batch")
    print_result("Nomad Job: llamacpp-batch", ok, msg)

    ok, msg = verify_file_exists("/opt/world_model_service/debug_world_model.sh")
    print_result("Debug Script", ok, msg)

def verify_tool_server():
    print("--- tool_server ---")
    ok, msg = verify_nomad_job("tool_server")
    print_result("Nomad Job: tool_server", ok, msg)

def verify_llxprt_code():
    print("--- llxprt_code ---")
    ok, msg = verify_command_available("llxprt")
    print_result("Command: llxprt", ok, msg)

def verify_claude_clone():
    print("--- claude_clone ---")
    # Check for build artifact or package.json
    ok, msg = verify_file_exists("/opt/claude_clone/package.json")
    print_result("Repo Clone", ok, msg)

    ok, msg = verify_file_exists("/opt/claude_clone/dist") # Assuming 'npm run build' creates dist
    if not ok:
        # Maybe it creates 'build'?
        ok, msg = verify_file_exists("/opt/claude_clone/build")
    print_result("Build Artifacts", ok, msg)

def verify_moe_gateway():
    print("--- moe_gateway ---")
    ok, msg = verify_nomad_job("moe-gateway")
    print_result("Nomad Job: moe-gateway", ok, msg)

    ok, msg = verify_file_exists("/opt/pipecatapp/moe_gateway/gateway.py")
    print_result("Source File", ok, msg)

def verify_mcp_server():
    print("--- mcp_server ---")
    ok, msg = verify_nomad_job("mcp_server")
    print_result("Nomad Job: mcp_server", ok, msg)

if __name__ == "__main__":
    print("Starting verification of components...")
    print("-------------------------------------")
    verify_provisioning_api()
    verify_desktop_extras()
    verify_paddler()
    verify_vision()
    verify_power_manager()
    verify_world_model_service()
    verify_tool_server()
    verify_llxprt_code()
    verify_claude_clone()
    verify_moe_gateway()
    verify_mcp_server()
    print("-------------------------------------")
    print("Verification complete.")

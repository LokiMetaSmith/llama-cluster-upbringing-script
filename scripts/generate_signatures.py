import binascii

def to_hex(s):
    return binascii.hexlify(s.encode()).decode()

def create_ldb_sig(name, target_type, logic, subsigs):
    hex_subsigs = [to_hex(s) for s in subsigs]
    return f"{name};Target:{target_type};{logic};{';'.join(hex_subsigs)}"

# Signature 1: Destructive Command (rm -rf /)
# Matches "rm -rf /" literals in any file
sig1 = create_ldb_sig(
    "RogueAgent.DestructiveCommand",
    0, # Any file
    "0", # Just match subsig 0
    ["rm -rf /"]
)

# Signature 2: Python Reverse Shell components
# Matches presence of 'socket', 'subprocess', and 'os.dup2' in the same file
sig2 = create_ldb_sig(
    "RogueAgent.PythonReverseShell",
    0,
    "0&1&2", # All three must be present
    ["import socket", "import subprocess", "os.dup2"]
)

print(sig1)
print(sig2)

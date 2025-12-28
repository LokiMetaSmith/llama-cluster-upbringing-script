import sys
import os

# Add files dir to path
sys.path.append("/app/ansible/roles/pipecatapp/files")

print("DEBUG: Starting import test", flush=True)

try:
    print("DEBUG: Importing app...", flush=True)
    import app
    print("DEBUG: Successfully imported app.", flush=True)
except ImportError as e:
    print(f"DEBUG: ImportError: {e}", flush=True)
    sys.exit(1)
except Exception as e:
    print(f"DEBUG: Exception during import: {e}", flush=True)
    sys.exit(1)

print("DEBUG: Import test complete.", flush=True)

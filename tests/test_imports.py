import sys
import os

# Add files dir to path
sys.path.append("/app/ansible/roles/pipecatapp/files")

# Fallback for local testing
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(repo_root, "pipecatapp"))

def test_import_app():
    print("DEBUG: Starting import test", flush=True)
    try:
        print("DEBUG: Importing app...", flush=True)
        import app
        print("DEBUG: Successfully imported app.", flush=True)
    except ImportError as e:
        print(f"DEBUG: ImportError: {e}", flush=True)
        raise e
    except Exception as e:
        print(f"DEBUG: Exception during import: {e}", flush=True)
        raise e
    print("DEBUG: Import test complete.", flush=True)

if __name__ == "__main__":
    try:
        test_import_app()
    except Exception:
        sys.exit(1)

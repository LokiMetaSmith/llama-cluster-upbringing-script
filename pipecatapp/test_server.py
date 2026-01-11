import os
import logging
from api_keys import initialize_api_keys
from web_server import app

# This is a special entry point for testing purposes.
# It initializes the API keys from the environment before the app starts.
# In the real application, this initialization is handled by app.py.

logging.basicConfig(level=logging.INFO)

hashed_api_keys_str = os.getenv("PIECAT_API_KEYS", "")
if hashed_api_keys_str:
    hashed_keys = [key.strip() for key in hashed_api_keys_str.split(',')]
    initialize_api_keys(hashed_keys)
    logging.info(f"Test server initialized with {len(hashed_keys)} API key(s).")
else:
    logging.warning("PIECAT_API_KEYS environment variable not set for test server.")

# Initialize global state attributes for testing
app.state.is_ready = False
app.state.twin_service_instance = None

# The 'app' object is imported from web_server and will be used by uvicorn.

import contextlib
import logging
import os
import sys

@contextlib.contextmanager
def suppress_stderr():
    """A context manager to temporarily redirect stderr to /dev/null."""
    stderr = sys.stderr
    devnull = open(os.devnull, 'w')
    sys.stderr = devnull
    try:
        yield
    finally:
        sys.stderr = stderr  # Restore stderr
        devnull.close()

def find_workable_audio_input_device():
    """
    Silently scans for a workable PyAudio input device.

    Returns:
        An integer (device_index) if a workable device is found.
        None if no workable device is found.
    """
    logging.info("Starting silent audio device scan...")
    pa = None
    try:
        import pyaudio
        # 1. Suppress C-level spam during init
        with suppress_stderr():
            pa = pyaudio.PyAudio()

        # 2. Scan devices for a workable input
        for i in range(pa.get_device_count()):
            device_info = pa.get_device_info_by_index(i)
            # This is a basic check. You can make this more robust
            # (e.g., check for sample rate, "USB", "Analog", etc.)
            if device_info.get('maxInputChannels') > 0:
                logging.info(f"Found workable audio device: [Index {i}] {device_info.get('name')}")
                return i  # Return the first workable device index

        logging.warning("No workable audio input device found after full scan.")
        return None

    except (ImportError, Exception) as e:
        # This catches errors like "No Default Input Device" on truly headless systems
        logging.warning(f"Audio subsystem scan failed (this is OK for headless): {e}")
        return None

    finally:
        # 3. Always terminate PyAudio to release resources
        if pa:
            pa.terminate()

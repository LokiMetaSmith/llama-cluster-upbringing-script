import os

def load_sudo_env():
    """
    When scripts are executed via sudo, environment variables like NOMAD_ADDR
    or CONSUL_HTTP_TOKEN are stripped by default. This function attempts to
    recover them from the sudo process's environment using /proc without subprocesses.
    """
    if not os.environ.get('SUDO_USER'):
        return

    sudo_pid = None
    curr_pid = os.getpid()
    while True:
        try:
            with open(f"/proc/{curr_pid}/stat", 'r') as f:
                stat_data = f.read().split()
                # stat format: pid (comm) state ppid ...
                stat_str = " ".join(stat_data)
                import re
                match = re.search(r'\((.*?)\)\s+\w+\s+(\d+)', stat_str)
                if not match:
                    break
                comm = match.group(1)
                ppid = int(match.group(2))

                if comm == "sudo":
                    sudo_pid = curr_pid
                    break
                curr_pid = ppid
                if curr_pid <= 1:
                    break
        except Exception:
            break

    if not sudo_pid:
        return

    try:
        with open(f"/proc/{sudo_pid}/environ", 'rb') as f:
            env_data = f.read().split(b'\0')
            for item in env_data:
                if b'=' in item:
                    key, value = item.split(b'=', 1)
                    key = key.decode('utf-8', errors='ignore')
                    value = value.decode('utf-8', errors='ignore')
                    if key.startswith('NOMAD_') or key.startswith('CONSUL_'):
                        if key not in os.environ:
                            os.environ[key] = value
    except Exception:
        pass

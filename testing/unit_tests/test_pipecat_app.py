import sys
import requests

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_pipecat_app.py <ip_address>")
        sys.exit(1)

    ip_address = sys.argv[1]
    url = f"http://{ip_address}:8000"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"Health check passed for {url}")
            sys.exit(0)
        else:
            print(f"Health check failed for {url}. Status code: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Health check failed for {url}. Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
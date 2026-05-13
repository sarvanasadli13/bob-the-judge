"""
One-click launcher for Bob the Judge.
Run: python launch.py
Starts legacy bank (8001) + modern bank (8002) + dashboard (8501), then opens browser.
"""

import subprocess
import sys
import time
import webbrowser
import urllib.request
import os
import shutil

def _python():
    """Return the Python executable — works both as script and PyInstaller exe."""
    if getattr(sys, "frozen", False):
        for name in ("python", "python3", "py"):
            found = shutil.which(name)
            if found:
                return found
        raise RuntimeError("Python not found in PATH. Install Python 3.11+ and try again.")
    return sys.executable

SERVICES = [
    {"name": "Legacy Bank",  "cmd": [_python(), "-m", "uvicorn", "services.legacy_bank:app",  "--port", "8001", "--log-level", "error"], "health": "http://localhost:8001/health"},
    {"name": "Modern Bank",  "cmd": [_python(), "-m", "uvicorn", "services.modern_bank:app",  "--port", "8002", "--log-level", "error"], "health": "http://localhost:8002/health"},
]
DASHBOARD_CMD = [_python(), "-m", "streamlit", "run", "dashboard.py",
                 "--server.port", "8501", "--server.headless", "true",
                 "--browser.gatherUsageStats", "false"]
DASHBOARD_URL = "http://localhost:8501"


def _kill_port(port: int):
    try:
        result = subprocess.run(
            ["netstat", "-ano"], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if f":{port}" in line and "LISTENING" in line:
                pid = line.strip().split()[-1]
                subprocess.run(["taskkill", "/F", "/PID", pid],
                               capture_output=True)
    except Exception:
        pass


def _wait_healthy(url: str, name: str, timeout: int = 15) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=2)
            print(f"  [OK] {name} ready")
            return True
        except Exception:
            time.sleep(0.5)
    print(f"  [FAIL] {name} did not start in time")
    return False


def main():
    if getattr(sys, "frozen", False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("\n=== BOB THE JUDGE  -  IBM Hackathon ===\n")

    # Kill anything on our ports
    print("Clearing ports...")
    for port in [8001, 8002, 8501]:
        _kill_port(port)
    time.sleep(0.5)

    # Start bank services
    procs = []
    print("Starting services...")
    for svc in SERVICES:
        p = subprocess.Popen(svc["cmd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        procs.append(p)

    # Health check
    all_ok = all(_wait_healthy(svc["health"], svc["name"]) for svc in SERVICES)
    if not all_ok:
        print("\nService startup failed. Check your environment.")
        sys.exit(1)

    # Start dashboard
    print("Starting dashboard...")
    dash = subprocess.Popen(DASHBOARD_CMD, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    procs.append(dash)

    # Wait for Streamlit
    if _wait_healthy(DASHBOARD_URL, "Dashboard", timeout=20):
        print(f"\n  >> Opening {DASHBOARD_URL}\n")
        time.sleep(1)
        webbrowser.open(DASHBOARD_URL)
    else:
        print(f"\n  Dashboard slow to start — open {DASHBOARD_URL} manually\n")

    print("Bob the Judge is running. Press Ctrl+C to stop all services.")
    print("MCP server: run  python mcp_server.py  in a separate terminal,")
    print("then add bob-mcp-config.json to Bob IDE settings.\n")

    try:
        while True:
            time.sleep(1)
            # Restart any service that died unexpectedly
            for i, (svc, p) in enumerate(zip(SERVICES, procs[:-1])):
                if p.poll() is not None:
                    print(f"  [!] {svc['name']} crashed - restarting...")
                    new_p = subprocess.Popen(svc["cmd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    procs[i] = new_p
    except KeyboardInterrupt:
        print("\nShutting down...")
        for p in procs:
            try:
                p.terminate()
            except Exception:
                pass
        print("Done.\n")


if __name__ == "__main__":
    main()

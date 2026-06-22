"""
Launch Friday: starts the Python backend, waits for it to be ready,
then starts the Electron desktop app.
"""
import subprocess
import sys
import time
import httpx
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def wait_for_backend(url: str, retries: int = 20, delay: float = 0.5) -> bool:
    for _ in range(retries):
        try:
            r = httpx.get(url, timeout=2)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(delay)
    return False


def main() -> None:
    print("[FRIDAY] Starting backend server...")
    backend = subprocess.Popen(
        [sys.executable, str(ROOT / "scripts" / "run.py")],
        cwd=ROOT,
    )

    health_url = "http://127.0.0.1:8000/api/v1/health"
    if not wait_for_backend(health_url):
        print("[FRIDAY] Backend did not start in time. Check your .env file.")
        backend.terminate()
        sys.exit(1)

    print("[FRIDAY] Backend online. Launching desktop app...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    desktop = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=ROOT / "desktop",
    )

    try:
        backend.wait()
    except KeyboardInterrupt:
        print("\n[FRIDAY] Shutting down...")
    finally:
        backend.terminate()
        desktop.terminate()


if __name__ == "__main__":
    main()

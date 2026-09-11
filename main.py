"""Main Application Entry Point: Native Desktop & Web Server for LYRA Digital Twin."""

import sys
import os
import time
import threading
import urllib.request
import webbrowser
import uvicorn

from backend.config import HOST, PORT, APP_NAME

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_uvicorn_server():
    """Runs Uvicorn server hosting FastAPI backend and static frontend."""
    config = uvicorn.Config(
        "backend.app:app",
        host=HOST,
        port=PORT,
        log_level="info",
        reload=False
    )
    server = uvicorn.Server(config)
    server.run()


def wait_for_server(url: str, timeout: int = 15) -> bool:
    """Waits for local server to be responsive."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.3)
    return False


def main():
    print("=" * 65)
    print(f"  Starting {APP_NAME}...")
    print(f"  Local API & UI: http://{HOST}:{PORT}")
    print("=" * 65)

    # Start FastAPI server in daemon thread
    server_thread = threading.Thread(target=run_uvicorn_server, daemon=True)
    server_thread.start()

    health_url = f"http://{HOST}:{PORT}/api/health"
    print("Waiting for server to initialize...")
    if not wait_for_server(health_url):
        print("Error: Server failed to start within timeout.")
        sys.exit(1)

    print("Server ready!")

    # Check CLI arguments
    server_only = "--server-only" in sys.argv or os.environ.get("SERVER_ONLY") == "1"

    if server_only:
        print(f"Running in server-only mode. Access via browser at http://{HOST}:{PORT}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down server.")
            sys.exit(0)

    # Launch native desktop window using pywebview
    try:
        import webview
        print("Launching native desktop application window...")
        window = webview.create_window(
            title="LYRA - Business Digital Twin",
            url=f"http://{HOST}:{PORT}",
            width=1000,
            height=750,
            resizable=True,
            min_size=(750, 550)
        )
        webview.start()
        print("Desktop window closed. Exiting.")
    except Exception as e:
        print(f"Native GUI window failed ({e}). Falling back to system default web browser.")
        webbrowser.open(f"http://{HOST}:{PORT}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down.")
            sys.exit(0)


if __name__ == "__main__":
    main()

import os
import subprocess
import threading
import time
import webbrowser
import sys
import signal
import shutil

print("Starting deploy.py...")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
VENV_DIR = os.path.join(BACKEND_DIR, "venv")

print("BASE_DIR:", BASE_DIR)
print("BACKEND_DIR:", BACKEND_DIR, "exists:", os.path.exists(BACKEND_DIR))
print("FRONTEND_DIR:", FRONTEND_DIR, "exists:", os.path.exists(FRONTEND_DIR))

def run_frontend():
    """Run the frontend server using Python's http.server"""
    try:
        print("Starting frontend server...")
        if not os.path.exists(FRONTEND_DIR):
            print(f"\n[ERROR] Frontend directory not found at {FRONTEND_DIR}\nPlease make sure the 'frontend' folder exists in your project root.")
            return None
        os.chdir(FRONTEND_DIR)
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8080"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        print("Frontend server running at http://localhost:8080")
        for line in frontend_process.stdout:
            print(f"[Frontend] {line.strip()}")
        os.chdir(BASE_DIR)
        return frontend_process
    except Exception as e:
        print(f"\n[ERROR] Error starting frontend server: {e}\n")
        return None

def run_backend():
    """Run the backend FastAPI server"""
    try:
        print("Starting backend server...")
        if not os.path.exists(BACKEND_DIR):
            print(f"\n[ERROR] Backend directory not found at {BACKEND_DIR}\nPlease make sure the 'backend' folder exists in your project root.")
            return None
        os.chdir(BACKEND_DIR)
        if not os.path.exists(VENV_DIR):
            print("Creating Python virtual environment for backend...")
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        else:
            print("Virtual environment already exists.")
        if os.name == "nt":
            venv_python = os.path.join(VENV_DIR, "Scripts", "python.exe")
            venv_pip = os.path.join(VENV_DIR, "Scripts", "pip.exe")
        else:
            venv_python = os.path.join(VENV_DIR, "bin", "python")
            venv_pip = os.path.join(VENV_DIR, "bin", "pip")
        print("Installing backend dependencies (this may take a moment)...")
        try:
            subprocess.check_call([venv_pip, "install", "--upgrade", "pip"])
            subprocess.check_call([venv_pip, "install", "-r", "requirements.txt"])
        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR] Failed to install backend dependencies.\n{e}\nCheck your requirements.txt and internet connection.")
            return None
        backend_process = subprocess.Popen(
            [venv_python, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        print("Backend server running at http://localhost:8000")
        for line in backend_process.stdout:
            if "Application startup complete" in line:
                print("[Backend] Server started successfully!")
            print(f"[Backend] {line.strip()}")
        os.chdir(BASE_DIR)
        return backend_process
    except Exception as e:
        print(f"\n[ERROR] Error starting backend server: {e}\n")
        return None

def main():
    print("\n===== SpamDetector Application =====\n")
    servers_started = True
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    print("Waiting for backend server to initialize...")
    time.sleep(3)
    try:
        import requests
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("Backend health check passed!")
        else:
            print("\n[WARNING] Backend health check returned non-200 status code.\nCheck the backend logs above for details.")
            servers_started = False
    except Exception as e:
        print(f"\n[WARNING] Backend server may not be running correctly.\nReason: {e}\nCheck the backend logs above for details.")
        servers_started = False
    frontend_thread = threading.Thread(target=run_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()
    time.sleep(1)
    if servers_started:
        print("\nOpening application in web browser...")
        webbrowser.open("http://localhost:8080")
    else:
        print("\n[WARNING] Servers may not have started correctly. Check the logs above for more information.")
    def signal_handler(sig, frame):
        print("\nShutting down servers...")
        print("Application stopped.")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    print("\nPress Ctrl+C to stop all servers")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        print("Application stopped.")

if __name__ == "__main__":
    main() 
import os
import subprocess
import threading
import time
import webbrowser
import sys
import signal

# Get absolute paths to directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

def run_frontend():
    """Run the frontend server using Python's http.server"""
    try:
        print("Starting frontend server...")
        if not os.path.exists(FRONTEND_DIR):
            print(f"Error: Frontend directory not found at {FRONTEND_DIR}")
            return None
            
        # Change to the frontend directory
        os.chdir(FRONTEND_DIR)
        
        # Use Python's built-in HTTP server
        frontend_process = subprocess.Popen(
            ["python", "-m", "http.server", "8080"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        print("Frontend server running at http://localhost:8080")
        
        # Monitor the frontend output
        for line in frontend_process.stdout:
            print(f"[Frontend] {line.strip()}")
            
        # Change back to the root directory
        os.chdir(BASE_DIR)
        
        return frontend_process
    except Exception as e:
        print(f"Error starting frontend server: {e}")
        return None

def run_backend():
    """Run the backend FastAPI server"""
    try:
        print("Starting backend server...")
        if not os.path.exists(BACKEND_DIR):
            print(f"Error: Backend directory not found at {BACKEND_DIR}")
            return None
            
        # Change to the backend directory
        os.chdir(BACKEND_DIR)
        
        # Install dependencies if needed
        print("Installing dependencies...")
        subprocess.call(["pip", "install", "-r", "requirements.txt"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Run the FastAPI server
        backend_process = subprocess.Popen(
            ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        print("Backend server running at http://localhost:8000")
        
        # Monitor the backend output
        for line in backend_process.stdout:
            if "Application startup complete" in line:
                print("[Backend] Server started successfully!")
            print(f"[Backend] {line.strip()}")
        
        # Change back to the root directory
        os.chdir(BASE_DIR)
        
        return backend_process
    except Exception as e:
        print(f"Error starting backend server: {e}")
        return None

def main():
    """Main function to run both servers"""
    print("\n===== SpamDetector Application =====\n")
    
    # Create a flag to track if servers started successfully
    servers_started = True
    
    # Start the backend server in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Give the backend server time to start
    print("Waiting for backend server to initialize...")
    time.sleep(3)
    
    # Check if backend is running
    try:
        import requests
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("Backend health check passed!")
        else:
            print("Warning: Backend health check returned non-200 status code")
            servers_started = False
    except:
        print("Warning: Backend server may not be running correctly")
        servers_started = False
    
    # Start the frontend server in a separate thread
    frontend_thread = threading.Thread(target=run_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    # Give the frontend server time to start
    time.sleep(1)
    
    if servers_started:
        # Open the application in the default web browser
        print("\nOpening application in web browser...")
        webbrowser.open("http://localhost:8080")
    else:
        print("\nServers may not have started correctly. Check the logs above.")
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        print("\nShutting down servers...")
        print("Application stopped.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    print("\nPress Ctrl+C to stop all servers")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        print("Application stopped.")

if __name__ == "__main__":
    main() 
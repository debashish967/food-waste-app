import subprocess
import sys

def run_command(command):
    """Run a command and return the output"""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = ['streamlit', 'pandas', 'plotly', 'mysql-connector-python', 'folium', 'streamlit-folium', 'geopy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        for package in missing_packages:
            stdout, stderr, returncode = run_command([sys.executable, "-m", "pip", "install", package])
            if returncode != 0:
                print(f"Error installing {package}: {stderr}")
                return False
    return True

def main():
    print("Preparing for deployment...")
    
    # Check dependencies
    if not check_dependencies():
        print("Failed to install dependencies")
        return
    
    # Run the app
    print("Starting the application...")
    run_command([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    main()
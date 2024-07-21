import sys
import os
import subprocess

def upload_files(directory_path, target_directory):
    
    files = os.listdir(target_directory)
    exception_occurred = False

    for file in files:
        print("Uploading", file)
        file_path = os.path.join(target_directory, file)
        if os.path.isfile(file_path):
            command = f"ampy --port {directory_path} -b 115200 put {file_path}"
            try:
                subprocess.run(command, shell=True)
            except Exception as e:
                print(e)
                exception_occurred = True
                print("Error: Press rst key to reset your device.")
                break
        #else:
            #print("Skipping directory:", file_path)
    if not exception_occurred:
        print("Done")
            
def is_pycontroller(directory_path):
    command = f"ampy --port {directory_path} -b 115200 get main.py | grep ble_simple_central"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        if "ble_simple_central" in result.stdout:
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        return False

def is_pydrone(directory_path):
    command = f"ampy --port {directory_path} -b 115200 get main.py | grep ble_simple_peripheral"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        if "ble_simple_peripheral" in result.stdout:
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        return False

# Update the path of pyDrone/pyController directory
directory_path = '/dev/cu.usbmodem1234561'

if os.path.exists(directory_path):
    # Update the full path of pyDrone/pyController directory
    target_directory = '/Users/cwit/Desktop/drone-hacking/drone-hacking-main/pyDrone' 
    
    if "pyDrone" in target_directory:
        #print("pyDrone")
        if is_pydrone(directory_path):
            upload_files(directory_path, target_directory)
        else:
            print("This is not pyDrone.")
    elif "pyController" in target_directory:
        print("pyController")
        if is_pycontroller(directory_path):
            upload_files(directory_path, target_directory)
        else:
            print("This is not pyController.")
    else:
        print("The specified directory is not the expected type.")
else:
    print("Directory does not exist:", directory_path)

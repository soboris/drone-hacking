import sys
import os
import subprocess

# Update the path of pyDrone/pyController directory
directory_paths = ['/dev/cu.usbmodem1234561', '/dev/cu.usbmodem2']

# Update the full path of pyDrone directory
targetDir_pyDrone = '/Users/cwit/Desktop/drone-hacking/drone-hacking-main/pyDrone'

# Update the full path of pyController directory
targetDir_pyController = '/Users/cwit/Desktop/drone-hacking/drone-hacking-main/pyController'

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
    if not exception_occurred:
        print("Done")
            
def is_pycontroller(osVer, directory_path):
    if osVer == "Windows":
        command = f"ampy --port {directory_path} -b 115200 ls | findstr -i ble_simple_central"
    elif osVer == "Linux":
        command = f"ampy --port {directory_path} -b 115200 ls | grep ble_simple_central"
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, timeout=10, universal_newlines=True)
        if "ble_simple_central" in result.stdout:
            return True

    except subprocess.CalledProcessError as exc:
        err_msg = "Status : FAIL" + str(exc.returncode) + str(exc.output)
        raise Exception(err_msg)
        
def is_pydrone(osVer, directory_path):
    if osVer == "Windows":
        command = f"ampy --port {directory_path} -b 115200 ls | findstr -i ble_simple_peripheral"
    elif osVer == "Linux":
        command = f"ampy --port {directory_path} -b 115200 ls | grep ble_simple_peripheral"
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, timeout=10, universal_newlines=True)
        if "ble_simple_peripheral" in result.stdout:
            return True

    except subprocess.CalledProcessError as exc:
        err_msg = "Status : FAIL" + str(exc.returncode) + str(exc.output)
        raise Exception(err_msg)

command = "dir"
try:
    chkos = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, timeout=3, universal_newlines=True)
except subprocess.CalledProcessError as exc:
    osVer = "Linux"
else:
    print("Output: \n{}\n".format(chkos))
    osVer = "Windows"

for path in directory_paths:
    if os.path.exists(path):
        try:
            if is_pydrone(osVer, path):
                print("pyDrone")
                
                if "pyDrone" in targetDir_pyDrone:
                    upload_files(path, targetDir_pyDrone)
                else:
                    print("This is not pyDrone directory.")

            elif is_pycontroller(osVer, path):
                print("pyController")

                if "pyController" in targetDir_pyController:
                    upload_files(path, targetDir_pyController)
                else:
                    print("This is not pyController directory.")
            else:
                print("The specified directory is not the expected type.")
        
        except Exception as e:
            print(e)
    else:
        print("Directory does not exist:", path)

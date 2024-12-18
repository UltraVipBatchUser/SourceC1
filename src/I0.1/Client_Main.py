import sys
import time
import os
import datetime
import asyncio
import shutil
import requests
import psutil
import subprocess
import ctypes
import re
def set_window_size(width, height):
    """Set the console window size."""
    if os.name == 'nt':
        os.system(f"mode con: cols={width} lines={height}")
    else:
        sys.stdout.write(f'\033[8;{height};{width}t')
        sys.stdout.flush()



        
def rgb_gradient(ascii_art, start_color, end_color):
    """Generate an RGB gradient for ASCII art."""
    lines = ascii_art.splitlines()
    total_chars = sum(len(line) for line in lines)
    r_step = (end_color[0] - start_color[0]) / total_chars
    g_step = (end_color[1] - start_color[1]) / total_chars
    b_step = (end_color[2] - start_color[2]) / total_chars

    gradient_art = ""
    current_r, current_g, current_b = start_color
    for line in lines:
        for char in line:
            if char.strip():  # Avoid coloring spaces
                gradient_art += f"\033[38;2;{int(current_r)};{int(current_g)};{int(current_b)}m{char}"
                current_r += r_step
                current_g += g_step
                current_b += b_step
            else:
                gradient_art += char
        gradient_art += "\033[0m\n"  

    return gradient_art
def clear_console():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else: 
        os.system('clear')

ascii_art = '''
                              ███╗░░░███╗░█████╗░░░░░░░░██████╗░██████╗░
                              ████╗░████║██╔══██╗░░░░░░██╔════╝██╔════╝░
                              ██╔████╔██║██║░░╚═╝█████╗╚█████╗░██║░░██╗░
                              ██║╚██╔╝██║██║░░██╗╚════╝░╚═══██╗██║░░╚██╗
                              ██║░╚═╝░██║╚█████╔╝░░░░░░██████╔╝╚██████╔╝
                              ╚═╝░░░░░╚═╝░╚════╝░░░░░░░╚═════╝░░╚═════╝░ 
'''

set_window_size(112, 31)
start_color = (255, 0, 255)  # Magenta
end_color = (118, 0, 128)    # Darker Purple

gradient_art = rgb_gradient(ascii_art, start_color, end_color)
sys.stdout.write(gradient_art)

info = '''
To use the client type here a version Latest version. >> [1.21.4]
Oldest >> [1.7] 
'''

start_color1 = (169, 169, 169)
end_color1 = (105, 105, 105)  
start_color2 = (169, 169, 169)      
end_color2 = (255, 0, 255)    
gradient_version_1_7 = rgb_gradient("1.7", start_color1, end_color1)
gradient_version_1_21 = rgb_gradient("1.21.4", start_color2, end_color2)

info_with_gradient = info.replace("[1.7]", gradient_version_1_7).replace("[1.21.4]", gradient_version_1_21)

sys.stdout.write(info_with_gradient)

def check_version_in_file(version):
    try:
        with open("GoodPatches.txt", "r") as file:
            # Read all lines in the file and remove newlines
            valid_versions = file.read().splitlines()

            # Check if the entered version is in the list
            if version in valid_versions:
                return True
            else:
                return False
    except FileNotFoundError:
        print("GoodPatches.txt file not found.")
        return False

choice = input(">> ")
def mainold():
    print('old')

def is_java_installed():
    try:
        # First, check if 'java -version' works to detect Java installation
        result = subprocess.run(['java', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True

        # If 'java -version' fails, check in the Windows registry
        try:
            # Open the registry key for installed programs
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
            for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                sub_key = winreg.EnumKey(reg_key, i)
                try:
                    sub_key_handle = winreg.OpenKey(reg_key, sub_key)
                    display_name, _ = winreg.QueryValueEx(sub_key_handle, "DisplayName")
                    if "Java" in display_name:
                        return True
                except OSError:
                    continue
            return False
        except FileNotFoundError:
            return False
    except FileNotFoundError:
        return False

# Example usage:
if is_java_installed():
    print("Java is installed.")
else:
    print("Java is not installed.")

# Function to download Java installer
def download_java_installer():
    url = "https://javadl.oracle.com/webapps/download/AutoDL?BundleId=251408_0d8f12bc927a4e2c9f8568ca567db4ee"
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        installer_path = os.path.join(os.path.expanduser("~"), "Desktop", "jdk_installer.exe")
        with open(installer_path, 'wb') as f:
            f.write(response.content)
        print(f"Java installer downloaded to {installer_path}")
        run_java_installer(installer_path)

        choice2 = input(">> ")

    else:
        print("Failed to download Java installer.")
        choice3 = input(">> ")

        return None

# Function to run the Java installer

def run_java_installer(installer_path):
    """Uninstall existing Java installations and run the Java installer visibly."""
    print("Checking for existing Java installations...")

    try:
        # Retrieve Java installations using WMIC (Windows only)
        uninstall_list = subprocess.check_output(
            'wmic product where "Name like \'%Java%\'" get Name,IdentifyingNumber',
            shell=True,
            universal_newlines=True
        )
        print("Found the following Java installations:\n", uninstall_list)

        # Use regex to extract GUIDs (IdentifyingNumber) from the output
        installations = re.findall(r"(\{[\w\-]+\})\s+(.+)", uninstall_list)
        if installations:
            for guid, name in installations:
                print(f"Continuing Java: {name} ({guid})")
                try:
                    main_newer2()
                except subprocess.CalledProcessError as e:
                    print(f"Error during uninstallation of {name}: {e}")
        else:
            print("No Java installations found.")
    except subprocess.CalledProcessError as e:
        print("Error checking for Java installations:", e)
    except Exception as e:
        print("Unexpected error:", e)

    print("Running Java installer...")

    # Command to run the installer visibly without silent arguments
    command = f'"{installer_path}"'

    try:
        # Use subprocess to execute the installer command
        subprocess.run(command, shell=True, check=True)
        print("Java installation complete.")
        mainnewer()
    except subprocess.CalledProcessError as e:
        print(f"Error running Java installer: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


        
###
        

# Function to check if java.exe is running
def is_java_running():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'java.exe':
            return True
    return False

# Function to create start.bat with RAM allocation
def create_start_bat(ram_allocation):
    start_bat_path = os.path.join(os.path.expanduser("~"), "Desktop", "server", "start.bat")
    ram_allocation_int = int(ram_allocation)
    allocation_command = f"java -Xmx{ram_allocation_int}M -Xms{ram_allocation_int}M -jar server.jar nogui"

    with open(start_bat_path, "w") as f:
        f.write(allocation_command)

    print(f"Created start.bat with allocated RAM: {ram_allocation}MB")

# Function to launch start.bat

# Main function to set up the server
def mainnewer():
    clear_console()

    # Check if Java is installed
    if not is_java_installed():
        print("Java is not installed. Downloading and installing Java...")
        installer_path = download_java_installer()
        ERR = input(f"E:: ")
        if installer_path:
            run_java_installer(installer_path)
        else:
            print("Error: Could not download the Java installer.")
            choice2 = input(">> ")

            return

    # Proceed with the rest of the server setup
    total_ram = get_system_ram()
    log_action(f"System RAM: {total_ram:.2f} GB")

    ram_choice = input(f"Enter the amount of RAM (in GB) to allocate for the server (You have {total_ram:.2f} GB available): ")

    try:
        # Convert the input to an integer
        ram_choice_int = int(ram_choice)

        # Check if the input is valid (must be less than or equal to system RAM in GB)
        if ram_choice_int > total_ram:
            log_action(f"Invalid RAM allocation: {ram_choice} GB exceeds available RAM.")
            print("Error: You cannot allocate more RAM than your system has.")
            return

        # Convert GB to MB (1 GB = 1024 MB)
        ram_choice_mb = ram_choice_int * 1024

        # Create the server folder before creating start.bat
        server_folder = create_server_folder()

        # If valid, create the start.bat file with the user's choice (in MB)
        create_start_bat(ram_choice_mb)

        # Proceed with the rest of the server setup
        download_spigot_file(server_folder)

        # Log successful server setup
        log_action("Server setup complete.")
        print("Server setup complete, you can now start it with the start.bat file.")

        # Launch the start.bat file
        start_bat_path = os.path.join(os.path.expanduser("~"), "Desktop", "server", "start.bat")
        subprocess.Popen(start_bat_path, shell=True)
        print(f"Started server with {start_bat_path}")
            # Wait for 1 second and check if Java is running
        time.sleep(4)

        # Check if java.exe is running


    except ValueError:
        log_action(f"Invalid input: '{ram_choice}' is not a valid number.")
        print("Please enter a valid number for RAM allocation.")

def main_newer2():
    clear_console()

    # Check if Java is installed
 

    # Proceed with the rest of the server setup
    total_ram = get_system_ram()
    log_action(f"System RAM: {total_ram:.2f} GB")

    ram_choice = input(f"Enter the amount of RAM (in GB) to allocate for the server (You have {total_ram:.2f} GB available): ")

    try:
        # Convert the input to an integer
        ram_choice_int = int(ram_choice)

        # Check if the input is valid (must be less than or equal to system RAM in GB)
        if ram_choice_int > total_ram:
            log_action(f"Invalid RAM allocation: {ram_choice} GB exceeds available RAM.")
            print("Error: You cannot allocate more RAM than your system has.")
            return

        # Convert GB to MB (1 GB = 1024 MB)
        ram_choice_mb = ram_choice_int * 1024

        # Create the server folder before creating start.bat
        server_folder = create_server_folder()

        # If valid, create the start.bat file with the user's choice (in MB)
        create_start_bat(ram_choice_mb)

        # Proceed with the rest of the server setup
        download_spigot_file(server_folder)

        # Log successful server setup
        log_action("Server setup complete.")
        print("Server setup complete, you can now start it with the start.bat file.")

        # Launch the start.bat file
        start_bat_path = os.path.join(os.path.expanduser("~"), "Desktop", "server", "start.bat")
        subprocess.Popen(start_bat_path, shell=True)
        print(f"Started server with {start_bat_path}")
            # Wait for 1 second and check if Java is running
        time.sleep(4)

        # Check if java.exe is running


    except ValueError:
        log_action(f"Invalid input: '{ram_choice}' is not a valid number.")
        print("Please enter a valid number for RAM allocation.")

# Utility functions for clearing console and logging
def clear_console():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else: 
        os.system('clear')

def log_action(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {current_time} {message}")

def get_system_ram():
    import psutil
    ram = psutil.virtual_memory()
    total_ram = ram.total / (1024 ** 3)  # Convert from bytes to GB
    return total_ram

def create_server_folder():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    server_folder = os.path.join(desktop_path, "server")

    if not os.path.exists(server_folder):
        os.makedirs(server_folder)
        log_action("Created 'server' folder on Desktop.")
    else:
        log_action("'server' folder already exists on Desktop.")
    
    return server_folder

def download_spigot_file(server_folder):
    url = "https://api.papermc.io/v2/projects/paper/versions/1.8.8/builds/445/downloads/paper-1.8.8-445.jar"
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        
        # Define the path for the new file
        file_path = os.path.join(server_folder, "server.jar")
        
        # Write the content of the downloaded file to the new file path
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        
        log_action("Spigot file downloaded and renamed to 'server.jar' inside the 'server' folder.")
    except requests.exceptions.RequestException as e:
        log_action(f"Failed to download Spigot file: {e}")


if check_version_in_file(choice):
    print(f"Passed: {choice}")
    if choice == "1.7":
        mainold() 
    elif choice == "1.8.8":
        mainnewer()  
else:
    print("Version not found / Accepted")




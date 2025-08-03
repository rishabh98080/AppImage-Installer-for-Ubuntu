#!/usr/bin/env python3
import os
import sys
import shutil
import glob

def main():
    """
    Installs a chosen AppImage from the current directory to a dedicated folder
    in the user's home directory and creates a desktop entry.
    MUST BE RUN WITH SUDO.
    """
    # 1. Check for sudo permissions and get the original user's info
    # -------------------------------------------------------------------
    if os.geteuid() != 0:
        print("❌ Error: This script must be run with sudo.")
        print("   Usage: sudo python3 install_appimage.py")
        sys.exit(1)

    # Get the original user who ran sudo, not 'root'
    sudo_user = os.environ.get('SUDO_USER')
    if sudo_user is None:
        print("❌ Error: Could not determine the original user. Are you running with sudo?")
        sys.exit(1)
        
    sudo_gid = int(os.environ.get('SUDO_GID'))
    home_dir = os.path.expanduser(f'~{sudo_user}')

    # 2. Find and select the AppImage from the current directory
    # -------------------------------------------------------------------
    current_dir = os.getcwd()
    print(f"🔍 Searching for AppImages in: {current_dir}")
    
    # Use glob to find files ending with .AppImage (case-insensitive)
    appimages = [f for f in os.listdir('.') if f.lower().endswith('.appimage')]

    if not appimages:
        print("❌ Error: No AppImage files found in the current directory.")
        sys.exit(1)

    print("\nFound the following AppImages:")
    for i, app in enumerate(appimages):
        print(f"  [{i+1}] {app}")

    try:
        choice = int(input("\nEnter the number of the AppImage to install: ")) - 1
        if not 0 <= choice < len(appimages):
            raise ValueError
        appimage_path_in = os.path.join(current_dir, appimages[choice])
    except (ValueError, IndexError):
        print("❌ Error: Invalid selection.")
        sys.exit(1)
    
    print(f"\n✅ You selected: {os.path.basename(appimage_path_in)}")

    # 3. Get user input for names and icon
    # -------------------------------------------------------------------
    permanent_name = input("Enter a short, permanent name for the app (e.g., 'obsidian'): ").strip().replace(' ', '-')
    if not permanent_name:
        print("❌ Error: The application name cannot be empty.")
        sys.exit(1)
        
    icon_path_in = input("Enter the full path to the icon file (e.g., /path/to/icon.png): ").strip()
    if not os.path.exists(icon_path_in):
        print(f"❌ Error: Icon not found at '{icon_path_in}'")
        sys.exit(1)

    # 4. Set up directories and copy files
    # -------------------------------------------------------------------
    install_dir = os.path.join(home_dir, '.local', 'bin', permanent_name)
    print(f"🛠️  Creating permanent directory at: {install_dir}")
    os.makedirs(install_dir, exist_ok=True)
    # Important: Change ownership of the created directory to the original user
    shutil.chown(install_dir, user=sudo_user, group=sudo_gid)

    # Copy, rename, and set permissions for the AppImage
    new_appimage_path = os.path.join(install_dir, permanent_name)
    print(f"➡️  Copying AppImage to {new_appimage_path}...")
    shutil.copy(appimage_path_in, new_appimage_path)
    os.chmod(new_appimage_path, 0o755)
    shutil.chown(new_appimage_path, user=sudo_user, group=sudo_gid)

    # Copy and rename the icon
    icon_extension = os.path.splitext(icon_path_in)[1]
    new_icon_path = os.path.join(install_dir, f"{permanent_name}{icon_extension}")
    print(f"➡️  Copying icon to {new_icon_path}...")
    shutil.copy(icon_path_in, new_icon_path)
    shutil.chown(new_icon_path, user=sudo_user, group=sudo_gid)

    # 5. Create the .desktop file
    # -------------------------------------------------------------------
    display_name = input(f"Enter the display name for the app menu [default: {permanent_name.capitalize()}]: ") or permanent_name.capitalize()
    comment = input("Enter a short description for the app: ")

    desktop_file_content = f"""[Desktop Entry]
Name={display_name}
Comment={comment}
Exec="{new_appimage_path}"
Icon={new_icon_path}
Terminal=false
Type=Application
Categories=Utility;
"""
    desktop_entry_dir = os.path.join(home_dir, '.local', 'share', 'applications')
    os.makedirs(desktop_entry_dir, exist_ok=True)
    shutil.chown(desktop_entry_dir, user=sudo_user, group=sudo_gid) # Ensure parent dir is owned correctly
    
    desktop_filepath = os.path.join(desktop_entry_dir, f"{permanent_name}.desktop")
    
    print(f"📄 Creating desktop file at {desktop_filepath}...")
    with open(desktop_filepath, "w") as f:
        f.write(desktop_file_content)
    
    # Change ownership of the final .desktop file
    shutil.chown(desktop_filepath, user=sudo_user, group=sudo_gid)
    
    print("\n✅ Success! Application installed.")
    print("You might need to log out and back in for it to appear in your application menu.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)
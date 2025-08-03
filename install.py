#!/usr/bin/env python3
import os
import sys
import shutil
import tempfile
import subprocess

def get_wm_class(appimage_path):
    """
    Attempts to automatically extract the StartupWMClass from an AppImage
    by mounting it and reading its internal .desktop file.
    """
    print("🔎 Trying to auto-detect 'StartupWMClass' for a perfect taskbar icon...")
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            # Use the AppImage's extract flag to dump its contents
            extract_cmd = [appimage_path, "--appimage-extract"]
            # Run silently without printing stdout/stderr unless there's an error
            subprocess.run(extract_cmd, cwd=tmpdir, check=True, capture_output=True)
            
            squashfs_root = os.path.join(tmpdir, "squashfs-root")
            
            # Find the first .desktop file inside the extracted contents
            for root, _, files in os.walk(squashfs_root):
                for file in files:
                    if file.endswith(".desktop"):
                        desktop_file_path = os.path.join(root, file)
                        with open(desktop_file_path, 'r') as f:
                            for line in f:
                                if line.strip().startswith("StartupWMClass="):
                                    wm_class = line.strip().split("=", 1)[1]
                                    print(f"✔️  Success! Found StartupWMClass: {wm_class}")
                                    return wm_class
            
            print("⚠️  Could not find a StartupWMClass entry automatically.")
            return None
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Auto-detection failed (app may not support extraction).")
            return None

def main():
    """
    Installs a chosen AppImage from the current directory to a dedicated folder
    in the user's home directory and creates a desktop entry.
    """
    # 1. Check permissions (NO SUDO!)
    # -------------------------------------------------------------------
    if os.geteuid() == 0:
        print("❌ Error: Do not run this script with sudo. It installs to your home directory.")
        sys.exit(1)

    home_dir = os.path.expanduser('~')

    # 2. Find and select the AppImage
    # -------------------------------------------------------------------
    current_dir = os.getcwd()
    print(f"🔍 Searching for AppImages in: {current_dir}")
    
    appimages = [f for f in os.listdir('.') if f.lower().endswith('.appimage')]

    if not appimages:
        print("❌ No AppImage files found in the current directory.")
        sys.exit(1)

    print("\nFound the following AppImages:")
    for i, app in enumerate(appimages):
        print(f"  [{i+1}] {app}")

    try:
        choice = int(input("\nEnter the number of the AppImage to install: ")) - 1
        appimage_path_in = os.path.join(current_dir, appimages[choice])
    except (ValueError, IndexError):
        print("❌ Error: Invalid selection.")
        sys.exit(1)
    
    print(f"\n✅ You selected: {os.path.basename(appimage_path_in)}")

    # 3. Get user input for names and icon
    # -------------------------------------------------------------------
    permanent_name = input("Enter a short, one-word name for the app (e.g., 'obsidian'): ").strip().replace(' ', '-')
    if not permanent_name:
        print("❌ Error: The application name cannot be empty.")
        sys.exit(1)
        
    icon_path_in = input("Enter the full path to the icon file (e.g., /path/to/icon.png): ").strip()
    if not os.path.exists(icon_path_in):
        print(f"❌ Error: Icon not found at '{icon_path_in}'")
        sys.exit(1)
        
    # 4. Handle StartupWMClass (The fix for taskbar icons)
    # -------------------------------------------------------------------
    wm_class = get_wm_class(appimage_path_in)
    if not wm_class:
        print("\nTo ensure the correct icon shows in the taskbar, you can enter the 'StartupWMClass'.")
        print("You can find this by running the app and using the 'xprop WM_CLASS' command.")
        wm_class = input("Enter StartupWMClass (or press Enter to skip): ").strip()

    # 5. Set up directories and copy files
    # -------------------------------------------------------------------
    install_dir = os.path.join(home_dir, '.local', 'bin', permanent_name)
    print(f"\n🛠️  Creating permanent directory at: {install_dir}")
    os.makedirs(install_dir, exist_ok=True)

    new_appimage_path = os.path.join(install_dir, permanent_name)
    print(f"➡️  Copying AppImage and making it executable...")
    shutil.copy(appimage_path_in, new_appimage_path)
    os.chmod(new_appimage_path, 0o755)

    icon_extension = os.path.splitext(icon_path_in)[1]
    new_icon_path = os.path.join(install_dir, f"{permanent_name}{icon_extension}")
    print(f"➡️  Copying icon...")
    shutil.copy(icon_path_in, new_icon_path)

    # 6. Create the .desktop file
    # -------------------------------------------------------------------
    display_name = input(f"Enter the display name for the app menu [default: {permanent_name.capitalize()}]: ") or permanent_name.capitalize()
    comment = input("Enter a short description for the app (e.g., 'A video editor'): ")

    # This is the updated template with StartupNotify=true
    desktop_file_content = f"""[Desktop Entry]
Name={display_name}
Comment={comment}
Exec="{new_appimage_path}" --no-sandbox
Icon={new_icon_path}
Terminal=false
Type=Application
Categories=Utility;
StartupNotify=true
"""
    # Add the WMClass only if it exists
    if wm_class:
        desktop_file_content += f"StartupWMClass={wm_class}\n"

    desktop_entry_dir = os.path.join(home_dir, '.local', 'share', 'applications')
    os.makedirs(desktop_entry_dir, exist_ok=True)
    
    desktop_filepath = os.path.join(desktop_entry_dir, f"{permanent_name}.desktop")
    
    print(f"📄 Creating desktop file at {desktop_filepath}...")
    with open(desktop_filepath, "w") as f:
        f.write(desktop_file_content)
    
    print("\n🎉 Success! Application installed.")
    print("   You might need to log out and back in for it to appear in your application menu.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)
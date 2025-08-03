<br/>
<div align="center">
<h1 align="center">AppImage Installer</h1>
<p align="center">
A simple, interactive script to properly install and integrate AppImages into your Linux desktop.
<br />
<br />
<a href="https://github.com/rishabh98080/AppImage-Installer-for-Ubuntu/issues">Report Bug</a>
·
<a href="https://github.com/rishabh98080/AppImage-Installer-for-Ubuntu/issues">Request Feature</a>
</p>
</div>

About The Project
Hey there! So, you love AppImages, right? They're awesome because they let you run apps on almost any Linux distro without a messy installation. But let's be real, getting them to show up in your application menu and keeping them organized is a manual chore.

This project fixes that. It's a simple installer that takes an AppImage, gives it a permanent home, and creates a desktop shortcut for it. No more stashing AppImages in your Downloads folder!

(A quick GIF showing the script running would be perfect here!)

Features
✅ Auto-Detection: Finds all .AppImage files in the current folder.

✅ Interactive & Friendly: A simple command-line menu guides you through the process.

✅ Proper Desktop Integration: Creates a .desktop file so your app appears in your Activities/Start Menu.

✅ Clean & Organized: Installs each app into its own neat folder in ~/.local/bin/.

✅ Handles Permissions Correctly: Safely uses sudo for installation while ensuring all files are owned by you, not root.

Getting Started
Ready to get it running? It's super easy. Just follow these steps.

1. Prerequisites
Make sure you have Python 3 installed. Most modern Linux distros have it by default.

2. Installation
First, you'll need to get the files onto your system.

Clone the repository:

Bash

git clone https://github.com/rishabh98080/AppImage-Installer-for-Ubuntu.git
cd AppImage-Installer-for-Ubuntu
Create the runPython.sh script:
This is a helper script to make running the installer easier. Create a file named runPython.sh and paste this code into it:

Bash

#!/bin/bash
# This script ensures the Python installer is executable and runs it with sudo.

# The name of the main Python installer script
INSTALL_SCRIPT="install.py"

echo "Setting up the installer..."

# Make the Python script executable
chmod +x "$INSTALL_SCRIPT"

# Check if the script is being run with sudo, which is required
if [ "$EUID" -ne 0 ]; then
  echo "❌ Error: This installer needs to be run with root privileges."
  echo "Please run it like this: sudo ./runPython.sh"
  exit 1
fi

# Execute the Python script with sudo
echo "🚀 Launching the AppImage Installer..."
sudo python3 "$INSTALL_SCRIPT"
Make the helper script executable:
Run this command in your terminal to give runPython.sh permission to run.

Bash

chmod +x runPython.sh
3. How to Use It
Now for the fun part!

Move your files:
Place the .AppImage file you want to install and its icon (e.g., a .png or .svg file) into the same folder as the scripts.

Run the installer:
Execute the helper script with sudo.

Bash

sudo ./runPython.sh
Follow the on-screen prompts:
The script will ask you to:

Choose the AppImage from a list it finds in the folder.

Enter a permanent name for the app (e.g., obsidian, bitwarden). This will be used for the folder and file names.

Provide the full path to the icon file.

Enter a display name (what you'll see in the app menu) and a short description.

And you're done! The app should now be available in your system's application menu. You might need to log out and back in for the menu to refresh.

How It Works Under the Hood
For those who are curious, here’s what the script is doing:

Gets Sudo User Info: When you run the script with sudo, it cleverly figures out who you, the original user, are (e.g., ubuntu, not root). This is crucial for setting the right file ownership.

Creates a Home for the App: It makes a new, dedicated folder for your application at ~/.local/bin/your-app-name/.

Copies and Prepares Files:

The AppImage is copied into the new folder and renamed to your-app-name.

The icon is also copied into this folder.

The AppImage is made executable (chmod 755).

Builds the Shortcut: It generates a .desktop file and places it in ~/.local/share/applications/. This is the standard location for user-specific application shortcuts. This file tells your desktop environment the app's name, description, where to find its executable, and which icon to use.

Sets Ownership: Finally, it ensures that all the newly created files and folders are owned by you, so you won't have any permission issues later.

Contributing
Got ideas to make this better? Feel free to fork the repo and create a pull request, or open an issue with the "enhancement" tag.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

License
Distributed under the MIT License. See LICENSE file for more information.

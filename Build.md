<div align="center">
<h1 align="center">AppImage Manager GUI</h1>
<p align="center">
A modern, graphical application to properly install, manage, and integrate AppImages into your Linux desktop.
<br />
<br />
<a href="#">Report Bug</a>
·
<a href="#">Request Feature</a>
</p>
</div>

About The Project
Hey there! So, you love AppImages, right? They're fantastic because they let you run applications on almost any Linux distribution without a complicated installation process. But let's be real, managing them—getting them to show up in your application menu, keeping them organized, and uninstalling them cleanly—is often a manual chore.

This project fixes that. It's a modern, graphical application that takes the guesswork out of AppImage management. It gives your AppImages a permanent, organized home and seamlessly integrates them into your desktop environment. No more hunting for AppImages in your Downloads folder!

(A screenshot of the application's interface would be perfect here!)

For Users: How to Get Started (No Installation Needed!)
This section is for you if you just want to download and use the application.

1. Download the Executable
Download the AppImageManager executable file from the project's Releases page on GitHub.

2. Run the Application
To launch the manager, just run it from your terminal or by double-clicking it in your file manager.

./AppImageManager

Important Note on Naming: For the best experience, keep the filename as AppImageManager. If you rename it to something generic like install, your file manager might get confused and try to open it as a text file instead of running it as an application.

Troubleshooting Tip: If you get a "Permission denied" error, it means the file isn't marked as executable. You can fix this by running chmod +x AppImageManager in your terminal. You only need to do this once.

Features in Detail
✅ Modern & Intuitive GUI

A clean, professional, dark-themed interface that is easy to navigate right from the start.

✅ Simple Tabbed Interface

The application is split into two main tabs: Install and Uninstall. This separation keeps the workspace uncluttered and makes the process for each task clear and straightforward.

✅ Flexible File & Folder Discovery

Automatic Scan on Launch: The application automatically scans the folder it's in when you first open it, immediately showing any available AppImages.

Browse for File: Don't want to move your files? No problem. You can add a single AppImage from anywhere on your system.

Browse for Folder: Have a dedicated folder for your AppImages? You can scan an entire directory at once to populate your list.

✅ Proper Desktop Integration

Creates a standard .desktop file in ~/.local/share/applications/. This is what allows your AppImage to appear in your system's application launcher (like the Activities menu in GNOME or the Start Menu in KDE) just like a natively installed app.

✅ Smart WMClass Detection

Includes an "Auto-Detect" feature to find the StartupWMClass. This is a crucial piece of information that helps your desktop environment match the running application window to its icon in the taskbar or dock. Without it, you might see a generic icon instead of the correct one.

✅ Clean & Tidy Uninstaller

The Uninstall tab scans for all applications installed by this tool. When you choose to uninstall an app, it completely removes all associated files, including the application directory and its .desktop shortcut, leaving your system clean.

✅ Organized & Safe by Design

Installs each application into its own neatly named folder inside ~/.local/bin/. This keeps your AppImages organized and out of the way. The entire process operates within your user's home directory, which means no sudo or root permissions are required, making it safer to use.

For Developers: Building from Source
This section is for you if you want to run the application from the Python source code or build your own executable.

1. Prerequisites
Python 3 and pip

Python's venv module (usually included with Python)

2. Setup and Run
Clone the repository:

git clone <your-repo-url>
cd <your-repo-folder>

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install the required libraries:
The GUI is built with ttkbootstrap.

pip install ttkbootstrap

Run the script:

python3 app_manager.py

3. Building Your Own Executable
You can bundle the application into a single, standalone executable using PyInstaller.

Install PyInstaller in your virtual environment:

pip install pyinstaller

Run the build command:
Navigate to the project's root directory in your terminal and run:

pyinstaller --onefile --windowed app_manager.py

--onefile: Bundles everything into a single executable file.

--windowed: Prevents a terminal window from appearing when the GUI is run.

Find your executable: Your new standalone application will be located in the dist/ folder!

Contributing
Got ideas to make this better? Feel free to fork the repo and create a pull request, or open an issue with the "enhancement" tag.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

License
Distributed under the MIT License. See the LICENSE file for more information.

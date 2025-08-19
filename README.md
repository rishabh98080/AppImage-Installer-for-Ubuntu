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

How to Use It
Getting started is incredibly simple. All you need is the executable file.

1. Download the Executable
Download the AppImageManager executable file from the project's releases page.

2. Run the Application
To launch the manager, just run it from your terminal or by double-clicking it in your file manager.

./AppImageManager

Troubleshooting Tip: If you get a "Permission denied" error, it means the file isn't marked as executable. You can fix this by running chmod +x AppImageManager in your terminal. You only need to do this once.

The Workflow
To Install an App:
Find Your AppImage: When you launch the app, it will automatically list any AppImages in the same folder. You can also use the Browse for File or Browse for Folder buttons to find AppImages located elsewhere on your system.

Select the AppImage: Click on the AppImage you want to install from the list.

Fill in the Details:

Short Name: A simple, one-word name (e.g., obsidian). This is a critical field, as it will be used for the folder and executable name.

Display Name: The full name that will appear in your app menu (e.g., Obsidian).

Icon Path: Click Browse... to select a .png or .svg icon file for your app.

StartupWMClass: Click Auto-Detect. The tool will try to extract this automatically. This is highly recommended for ensuring your app has the correct icon when running.

Install: Click the big green INSTALL APPLICATION button. The log window will show you the progress, and a pop-up will confirm when it's done!

To Uninstall an App:
Switch Tabs: Go to the Uninstall AppImage tab.

Scan for Apps: Click Scan for Installed Apps. The list will populate with all the apps you've previously installed with this tool.

Select the App: Click on the application you wish to remove.

Uninstall: Click Uninstall Selected App and confirm your choice in the pop-up dialog.

And you're done! The app should now be available in (or removed from) your system's application menu. You might need to log out and back in for the menu to refresh.

Contributing
Got ideas to make this better? Feel free to fork the repo and create a pull request, or open an issue with the "enhancement" tag.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

License
Distributed under the MIT License. See the LICENSE file for more information.

<div align="center">
<h1 align="center">AppImage Manager GUI</h1>
<p align="center">
A modern, graphical application to properly install, manage, and integrate AppImages into your Linux desktop.
<br />
<br />
<a href="#"><strong>Report Bug</strong></a>
·
<a href="#"><strong>Request Feature</strong></a>
</p>
<p align="center">
<img alt="License" src="https://img.shields.io/badge/License-MIT-blue.svg">
<img alt="Python" src="https://img.shields.io/badge/Python-3.x-blueviolet.svg">
</p>
</div>

<hr>

🎯 About The Project
Hey there! So, you love AppImages, right? They're fantastic because they let you run applications on almost any Linux distribution without a complicated installation process. But let's be real, managing them—getting them to show up in your application menu, keeping them organized, and uninstalling them cleanly—is often a manual chore.

This project fixes that. It's a modern, graphical application that takes the guesswork out of AppImage management. It gives your AppImages a permanent, organized home and seamlessly integrates them into your desktop environment. No more hunting for AppImages in your Downloads folder!

(A screenshot of the application's interface would be perfect here!)

<hr>

✨ Features in Detail
<table>
<tr>
<td width="50%" valign="top">

<ul style="list-style: none; padding-left: 0;">
<li style="margin-bottom: 15px;">
<strong style="font-size: 1.1em;">✅ Modern & Intuitive GUI</strong><br>
A clean, professional, dark-themed interface that is easy to navigate right from the start.
</li>
<li style="margin-bottom: 15px;">
<strong style="font-size: 1.1em;">✅ Simple Tabbed Interface</strong><br>
Split into <strong>Install</strong> and <strong>Uninstall</strong> tabs to keep the workspace uncluttered.
</li>
<li style="margin-bottom: 15px;">
<strong style="font-size: 1.1em;">✅ Flexible File Discovery</strong><br>
<ul>
<li><strong>Automatic Scan:</strong> Scans the current folder on launch.</li>
<li><strong>Browse for File:</strong> Add a single AppImage from anywhere.</li>
<li><strong>Browse for Folder:</strong> Scan an entire directory at once.</li>
</ul>
</li>
</ul>

</td>
<td width="50%" valign="top">

<ul style="list-style: none; padding-left: 0;">
<li style="margin-bottom: 15px;">
<strong style="font-size: 1.1em;">✅ Proper Desktop Integration</strong><br>
Creates a standard <code>.desktop</code> file so your app appears in your system's application launcher.
</li>
<li style="margin-bottom: 15px;">
<strong style="font-size: 1.1em;">✅ Smart WMClass Detection</strong><br>
Includes an "Auto-Detect" feature to find the <code>StartupWMClass</code> for correct taskbar icons.
</li>
<li style="margin-bottom: 15px;">
<strong style="font-size: 1.1em;">✅ Clean & Tidy Uninstaller</strong><br>
Completely removes all associated files, including the app directory and its <code>.desktop</code> shortcut.
</li>
<li style="margin-bottom: 15px;">
<strong style="font-size: 1.1em;">✅ Organized & Safe by Design</strong><br>
Installs apps into <code>~/.local/bin/</code> and operates entirely within your home directory — <strong>no <code>sudo</code> required!</strong>
</li>
</ul>

</td>
</tr>
</table>

<hr>

🚀 How to Use It
Getting started is incredibly simple. All you need is the executable file.

1. Download the Executable
Download the AppImageManager executable file from the project's releases page.

2. Run the Application
To launch the manager, just run it from your terminal or by double-clicking it in your file manager.
<br>

<pre style="background-color: #2d2d2d; padding: 10px; border-radius: 5px; border: 1px solid #444;"><code>./AppImageManager</code></pre>

Troubleshooting Tip: If you get a "Permission denied" error, it means the file isn't marked as executable. You can fix this by running chmod +x AppImageManager in your terminal. You only need to do this once.

<hr>

🛠️ The Workflow
To Install an App:
Find Your AppImage: When you launch the app, it will automatically list any AppImages in the same folder. You can also use the Browse for File or Browse for Folder buttons to find AppImages located elsewhere on your system.

Important Note: For an AppImage to be discoverable by the scanner, its filename must end with .AppImage. If you have an application that you know is an AppImage but it isn't showing up, simply rename the file to include the extension.

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

And you're done! The app should now be instantly available in (or removed from) your system's application menu. On some desktop environments, you might need to log out and back in for the menu to refresh.

<hr>

📜 A Note on the Source Code
This release provides a standalone executable for ease of use. While this is the primary version being released, the project can always be improved in the future. The full Python source code is available in the project's repository for those who wish to view it, modify it, or contribute.

<hr>

🙌 Contributing
Got ideas to make this better? Feel free to fork the repo and create a pull request, or open an issue with the "enhancement" tag.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

<hr>

📄 License
Distributed under the MIT License. See the LICENSE file for more information.

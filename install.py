#!/usr/bin/env python3
import os
import sys
import shutil
import tempfile
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext, font, messagebox, Listbox, END, SINGLE
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def get_wm_class(appimage_path):
    """
    Attempts to automatically extract the StartupWMClass from an AppImage
    by mounting it and reading its internal .desktop file.
    Returns the wm_class string or None if not found.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            extract_cmd = [appimage_path, "--appimage-extract"]
            subprocess.run(extract_cmd, cwd=tmpdir, check=True, capture_output=True, timeout=30)
            squashfs_root = os.path.join(tmpdir, "squashfs-root")
            
            for root, _, files in os.walk(squashfs_root):
                for file in files:
                    if file.endswith(".desktop"):
                        desktop_file_path = os.path.join(root, file)
                        with open(desktop_file_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                if line.strip().startswith("StartupWMClass="):
                                    wm_class = line.strip().split("=", 1)[1]
                                    return wm_class
            return None
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None

class AppImageInstaller(ttk.Window):
    """
    A GUI application to install and uninstall AppImages using ttkbootstrap.
    """
    def __init__(self):
        super().__init__(themename="darkly")

        # --- Initial Checks ---
        if os.geteuid() == 0:
            self.withdraw()
            messagebox.showerror("Permission Error", "Do not run this script with sudo. It installs to your home directory.")
            self.destroy()
            sys.exit(1)

        # --- Window Configuration ---
        self.title("AppImage Manager")
        self.geometry("800x800")
        self.minsize(800, 800) # Set the minimum size to the default size
        self.home_dir = os.path.expanduser('~')
        self.install_base_dir = os.path.join(self.home_dir, '.local', 'bin')
        self.desktop_entry_dir = os.path.join(self.home_dir, '.local', 'share', 'applications')
        self.log_font = font.Font(family="Consolas", size=10)
        
        # --- Tabbed Interface ---
        self.notebook = ttk.Notebook(self, bootstyle="dark")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.install_tab = ttk.Frame(self.notebook)
        self.uninstall_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.install_tab, text='Install AppImage')
        self.notebook.add(self.uninstall_tab, text='Uninstall AppImage')

        self.create_install_widgets()
        self.create_uninstall_widgets()

    def _bind_hover_events(self, widget):
        """Binds enter and leave events to change cursor to a hand pointer."""
        widget.bind("<Enter>", lambda e: widget.config(cursor="hand2"))
        widget.bind("<Leave>", lambda e: widget.config(cursor=""))

    # --- INSTALL TAB WIDGETS AND LOGIC ---
    def create_install_widgets(self):
        # This list will store the full paths, parallel to the listbox
        self.appimage_paths = []

        # --- Configure resizing for the install tab ---
        self.install_tab.columnconfigure(0, weight=1)
        self.install_tab.rowconfigure(2, weight=1) # Log frame should expand most

        # --- Main Layout Frames ---
        top_frame = ttk.Frame(self.install_tab)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        middle_frame = ttk.Frame(self.install_tab)
        middle_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        log_frame = ttk.Frame(self.install_tab)
        log_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # --- Top Frame: AppImage Selection ---
        ttk.Label(top_frame, text="1. Select AppImage to Install:").pack(anchor='w')
        self.appimage_listbox = Listbox(top_frame, bg="#1e1e1e", fg="#dcdcdc", selectbackground="#0078d7", height=5, exportselection=False, relief=tk.FLAT)
        self.appimage_listbox.pack(fill=tk.X, expand=True, pady=5)
        self._bind_hover_events(self.appimage_listbox)
        
        # --- New Button Frame for Scanning/Browsing ---
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        button_frame.columnconfigure((0, 1, 2), weight=1)

        scan_dir_btn = ttk.Button(button_frame, text="Scan Current Dir", command=self.scan_current_dir, bootstyle="info-outline")
        scan_dir_btn.grid(row=0, column=0, sticky='ew', padx=(0, 5))
        self._bind_hover_events(scan_dir_btn)

        browse_file_btn = ttk.Button(button_frame, text="Browse for File", command=self.browse_for_file, bootstyle="info-outline")
        browse_file_btn.grid(row=0, column=1, sticky='ew', padx=5)
        self._bind_hover_events(browse_file_btn)

        browse_folder_btn = ttk.Button(button_frame, text="Browse for Folder", command=self.browse_for_folder, bootstyle="info-outline")
        browse_folder_btn.grid(row=0, column=2, sticky='ew', padx=(5, 0))
        self._bind_hover_events(browse_folder_btn)

        # --- Middle Frame: User Inputs ---
        ttk.Label(middle_frame, text="2. Enter Application Details:").grid(row=0, column=0, columnspan=3, sticky='w', pady=(10,5))
        
        self.entries = {}
        self.fields = {
            "Short Name": "A short, one-word name (e.g., 'obsidian')",
            "Display Name": "Name for the app menu (e.g., 'Obsidian')",
            "Icon Path": "Full path to the icon file (.png, .svg)",
            "Description": "A short description for the app",
            "StartupWMClass": "(Optional) For correct taskbar icon"
        }
        
        for i, (label, hint) in enumerate(self.fields.items()):
            ttk.Label(middle_frame, text=f"{label}:").grid(row=i+1, column=0, sticky='w', padx=5, pady=5)
            entry = ttk.Entry(middle_frame, width=50)
            entry.grid(row=i+1, column=1, sticky='ew', pady=5)
            entry.insert(0, hint)
            entry.config(foreground='grey')
            entry.bind("<FocusIn>", self.clear_placeholder)
            entry.bind("<FocusOut>", lambda e, l=label, h=hint: self.add_placeholder(e, l, h))
            self.entries[label] = entry

        browse_icon_btn = ttk.Button(middle_frame, text="Browse...", command=self.browse_for_icon, bootstyle="info")
        browse_icon_btn.grid(row=3, column=2, padx=5)
        self._bind_hover_events(browse_icon_btn)
        
        autodetect_btn = ttk.Button(middle_frame, text="Auto-Detect", command=self.autodetect_wm_class, bootstyle="info")
        autodetect_btn.grid(row=5, column=2, padx=5)
        self._bind_hover_events(autodetect_btn)
        
        middle_frame.grid_columnconfigure(1, weight=1)

        # --- Log Frame: Output & Install Button ---
        log_frame.rowconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)

        ttk.Label(log_frame, text="3. Install Progress:").grid(row=0, column=0, sticky='w')
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, bg="#1e1e1e", fg="#dcdcdc", font=self.log_font, relief=tk.FLAT, height=10)
        self.log_area.grid(row=1, column=0, sticky='nsew', pady=5)
        self.log_area.config(state=tk.DISABLED)
        
        install_btn = ttk.Button(log_frame, text="INSTALL APPLICATION", command=self.install_application, bootstyle="success")
        install_btn.grid(row=2, column=0, sticky='ew', ipady=5, pady=(5,0))
        self._bind_hover_events(install_btn)
        
        self.scan_current_dir() # Initial scan on startup

    def clear_placeholder(self, event):
        for label, widget in self.entries.items():
            if widget == event.widget and widget.get() == self.fields[label]:
                widget.delete(0, END)
                widget.config(foreground=self.style.colors.fg)
                break

    def add_placeholder(self, event, label, placeholder):
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(foreground='grey')

    def log(self, message, level="info"):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(END, f"{message}\n")
        self.log_area.config(state=tk.DISABLED)
        self.log_area.see(END)
        self.update_idletasks()

    def scan_current_dir(self):
        """Wrapper to scan the current directory."""
        self.scan_for_appimages()

    def scan_for_appimages(self, directory='.'):
        """Scans a given directory for AppImages and populates the listbox."""
        self.appimage_listbox.delete(0, END)
        self.appimage_paths.clear()
        abs_dir = os.path.abspath(directory)
        self.log(f"🔍 Searching for AppImages in: {abs_dir}")
        try:
            found_appimages = [os.path.join(abs_dir, f) for f in os.listdir(abs_dir) if f.lower().endswith('.appimage')]
            if not found_appimages:
                self.log("❌ No AppImage files found in the selected directory.", "error")
                return
            for app_path in found_appimages:
                self.appimage_paths.append(app_path)
                self.appimage_listbox.insert(END, os.path.basename(app_path))
            self.log(f"✔️ Found {len(found_appimages)} AppImage(s).")
        except Exception as e:
            self.log(f"❌ Error scanning directory: {e}", "error")

    def browse_for_file(self):
        """Opens a file dialog to select a single AppImage file."""
        filepath = filedialog.askopenfilename(
            title="Select an AppImage File",
            filetypes=[("AppImage files", "*.appimage"), ("All files", "*.*")]
        )
        if filepath:
            if filepath not in self.appimage_paths:
                self.appimage_paths.append(filepath)
                self.appimage_listbox.insert(END, os.path.basename(filepath))
                self.log(f"➕ Added: {os.path.basename(filepath)}")
            else:
                self.log(f"⚠️ Already in list: {os.path.basename(filepath)}")

    def browse_for_folder(self):
        """Opens a directory dialog to scan a folder for AppImages."""
        folder_path = filedialog.askdirectory(title="Select a Folder to Scan")
        if folder_path:
            self.scan_for_appimages(directory=folder_path)

    def browse_for_icon(self):
        filepath = filedialog.askopenfilename(title="Select an Icon File", filetypes=[("Image Files", "*.png *.svg *.ico"), ("All Files", "*.*")])
        if filepath:
            self.entries["Icon Path"].delete(0, END)
            self.entries["Icon Path"].insert(0, filepath)
            self.entries["Icon Path"].config(foreground=self.style.colors.fg)

    def autodetect_wm_class(self):
        selection = self.appimage_listbox.curselection()
        if not selection:
            self.log("⚠️ Please select an AppImage from the list first.", "error")
            return
        
        selection_index = selection[0]
        appimage_path = self.appimage_paths[selection_index]
        appimage_name = self.appimage_listbox.get(selection_index)
        
        self.log(f"🔎 Trying to auto-detect 'StartupWMClass' for {appimage_name}...")
        wm_class = get_wm_class(appimage_path)
        
        if wm_class:
            self.log(f"✔️ Success! Found StartupWMClass: {wm_class}", "success")
            self.entries["StartupWMClass"].delete(0, END)
            self.entries["StartupWMClass"].insert(0, wm_class)
            self.entries["StartupWMClass"].config(foreground=self.style.colors.fg)
        else:
            self.log("⚠️ Auto-detection failed. You may need to enter it manually.", "error")

    def install_application(self):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete('1.0', END)
        self.log_area.config(state=tk.DISABLED)

        selection = self.appimage_listbox.curselection()
        if not selection:
            self.log("❌ Error: Please select an AppImage to install.", "error")
            return
        
        selection_index = selection[0]
        appimage_path_in = self.appimage_paths[selection_index]

        if not os.path.exists(appimage_path_in):
            self.log(f"❌ Error: Source file not found at '{appimage_path_in}'", "error")
            return
        
        permanent_name = self.entries["Short Name"].get().strip().replace(' ', '-')
        if not permanent_name or " " in permanent_name or permanent_name == self.fields["Short Name"]:
            self.log("❌ Error: The 'Short Name' is invalid or empty.", "error")
            return
        
        icon_path_in = self.entries["Icon Path"].get().strip()
        if not os.path.exists(icon_path_in):
            self.log(f"❌ Error: Icon not found at '{icon_path_in}'", "error")
            return

        install_dir = os.path.join(self.install_base_dir, permanent_name)
        self.log(f"🛠️  Creating permanent directory at: {install_dir}")
        os.makedirs(install_dir, exist_ok=True)

        new_appimage_path = os.path.join(install_dir, permanent_name)
        self.log(f"➡️  Copying AppImage and making it executable...")
        shutil.copy(appimage_path_in, new_appimage_path)
        os.chmod(new_appimage_path, 0o755)

        icon_extension = os.path.splitext(icon_path_in)[1]
        new_icon_path = os.path.join(install_dir, f"{permanent_name}{icon_extension}")
        self.log(f"➡️  Copying icon...")
        shutil.copy(icon_path_in, new_icon_path)

        display_name = self.entries["Display Name"].get()
        if not display_name or display_name == self.fields["Display Name"]:
            display_name = permanent_name.capitalize()
            
        comment = self.entries["Description"].get()
        if comment == self.fields["Description"]: comment = ""
            
        wm_class = self.entries["StartupWMClass"].get()
        if wm_class == self.fields["StartupWMClass"]: wm_class = ""

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
        if wm_class:
            desktop_file_content += f"StartupWMClass={wm_class}\n"

        os.makedirs(self.desktop_entry_dir, exist_ok=True)
        desktop_filepath = os.path.join(self.desktop_entry_dir, f"{permanent_name}.desktop")
        
        self.log(f"📄 Creating desktop file at {desktop_filepath}...")
        with open(desktop_filepath, "w") as f:
            f.write(desktop_file_content)
        
        self.log("\n🎉 Success! Application installed.", "success")
        messagebox.showinfo("Installation Complete", f"'{display_name}' has been installed successfully!")

    # --- UNINSTALL TAB WIDGETS AND LOGIC ---
    def create_uninstall_widgets(self):
        self.installed_apps = {} 

        frame = ttk.Frame(self.uninstall_tab)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Installed Applications:").pack(anchor='w')
        self.uninstall_listbox = Listbox(frame, bg="#1e1e1e", fg="#dcdcdc", selectbackground="#0078d7", height=15, exportselection=False, relief=tk.FLAT)
        self.uninstall_listbox.pack(fill='both', expand=True, pady=5)
        self._bind_hover_events(self.uninstall_listbox)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=5)

        scan_installed_btn = ttk.Button(button_frame, text="Scan for Installed Apps", command=self.scan_for_installed_apps, bootstyle="info-outline")
        scan_installed_btn.pack(side='left', expand=True, fill='x')
        self._bind_hover_events(scan_installed_btn)

        uninstall_btn = ttk.Button(button_frame, text="Uninstall Selected App", command=self.uninstall_application, bootstyle="danger")
        uninstall_btn.pack(side='left', expand=True, fill='x', padx=(10, 0))
        self._bind_hover_events(uninstall_btn)
        
        self.scan_for_installed_apps()

    def scan_for_installed_apps(self):
        self.uninstall_listbox.delete(0, END)
        self.installed_apps.clear()
        
        os.makedirs(self.desktop_entry_dir, exist_ok=True)
        
        for filename in os.listdir(self.desktop_entry_dir):
            if filename.endswith(".desktop"):
                filepath = os.path.join(self.desktop_entry_dir, filename)
                display_name = ""
                exec_path = ""
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip().startswith("Name="):
                                display_name = line.strip().split("=", 1)[1]
                            if line.strip().startswith("Exec="):
                                exec_path = line.strip().split("=", 1)[1].strip('"')
                    
                    if self.install_base_dir in exec_path:
                        permanent_name = os.path.splitext(filename)[0]
                        self.installed_apps[display_name] = permanent_name
                        self.uninstall_listbox.insert(END, display_name)
                except Exception:
                    continue

    def uninstall_application(self):
        selection = self.uninstall_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an application to uninstall.")
            return

        display_name = self.uninstall_listbox.get(selection[0])
        permanent_name = self.installed_apps.get(display_name)

        if not permanent_name:
            messagebox.showerror("Error", "Could not find the application data for uninstallation.")
            return

        if not messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to permanently uninstall '{display_name}'?"):
            return

        try:
            install_dir = os.path.join(self.install_base_dir, permanent_name)
            if os.path.isdir(install_dir):
                shutil.rmtree(install_dir)
            
            desktop_filepath = os.path.join(self.desktop_entry_dir, f"{permanent_name}.desktop")
            if os.path.exists(desktop_filepath):
                os.remove(desktop_filepath)

            messagebox.showinfo("Success", f"'{display_name}' has been uninstalled successfully.")
            self.scan_for_installed_apps() 

        except Exception as e:
            messagebox.showerror("Uninstallation Error", f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        # Before running, make sure you have ttkbootstrap installed:
        # pip install ttkbootstrap
        app = AppImageInstaller()
        app.mainloop()
    except ImportError:
        messagebox.showerror("Missing Library", "Please install 'ttkbootstrap' to run this application.\n\nRun: pip install ttkbootstrap")
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
        sys.exit(1)

#!/usr/bin/env python3
import os
import sys
import shutil
import tempfile
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext, font, messagebox, Listbox, END, SINGLE
from tkinter import ttk # Import for Notebook (tabs)

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

class AppImageInstaller(tk.Tk):
    """
    A GUI application to install and uninstall AppImages.
    """
    def __init__(self):
        super().__init__()

        # --- Initial Checks ---
        if os.geteuid() == 0:
            self.withdraw()
            messagebox.showerror("Permission Error", "Do not run this script with sudo. It installs to your home directory.")
            self.destroy()
            sys.exit(1)

        # --- Window Configuration ---
        self.title("AppImage Manager")
        self.geometry("800x750")
        self.home_dir = os.path.expanduser('~')
        self.install_base_dir = os.path.join(self.home_dir, '.local', 'bin')
        self.desktop_entry_dir = os.path.join(self.home_dir, '.local', 'share', 'applications')

        # --- Style Configuration ---
        self.style_config = {
            "bg": "#2e2e2e", "fg": "#dcdcdc", "entry_bg": "#1e1e1e",
            "button_bg": "#4a4a4a", "active_bg": "#5a5a5a",
            "list_bg": "#1e1e1e", "list_select_bg": "#0078d7",
            "success": "#4CAF50", "error": "#F44336"
        }
        self.configure(bg=self.style_config["bg"])
        self.log_font = font.Font(family="Consolas", size=10)
        
        # --- Tabbed Interface ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        self.install_tab = tk.Frame(self.notebook, bg=self.style_config["bg"])
        self.uninstall_tab = tk.Frame(self.notebook, bg=self.style_config["bg"])

        self.notebook.add(self.install_tab, text='Install AppImage')
        self.notebook.add(self.uninstall_tab, text='Uninstall AppImage')

        self.create_install_widgets()
        self.create_uninstall_widgets()

    def button_styles(self, pady=5):
        return {"bg": self.style_config["button_bg"], "fg": self.style_config["fg"], "activebackground": self.style_config["active_bg"], "activeforeground": self.style_config["fg"], "relief": tk.FLAT, "padx": 10, "pady": pady}

    # --- INSTALL TAB WIDGETS AND LOGIC ---
    def create_install_widgets(self):
        # --- Main Layout Frames ---
        top_frame = tk.Frame(self.install_tab, bg=self.style_config["bg"])
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        middle_frame = tk.Frame(self.install_tab, bg=self.style_config["bg"])
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        log_frame = tk.Frame(self.install_tab, bg=self.style_config["bg"])
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Top Frame: AppImage Selection ---
        tk.Label(top_frame, text="1. Select AppImage to Install:", bg=self.style_config["bg"], fg=self.style_config["fg"]).pack(anchor='w')
        self.appimage_listbox = Listbox(top_frame, bg=self.style_config["list_bg"], fg=self.style_config["fg"], selectbackground=self.style_config["list_select_bg"], height=5, exportselection=False, relief=tk.FLAT)
        self.appimage_listbox.pack(fill=tk.X, expand=True, pady=5)
        tk.Button(top_frame, text="Scan Current Directory for AppImages", command=self.scan_for_appimages, **self.button_styles()).pack(fill=tk.X)

        # --- Middle Frame: User Inputs ---
        tk.Label(middle_frame, text="2. Enter Application Details:", bg=self.style_config["bg"], fg=self.style_config["fg"]).grid(row=0, column=0, columnspan=3, sticky='w', pady=(10,5))
        
        self.entries = {}
        self.fields = {
            "Short Name": "A short, one-word name (e.g., 'obsidian')",
            "Display Name": "Name for the app menu (e.g., 'Obsidian')",
            "Icon Path": "Full path to the icon file (.png, .svg)",
            "Description": "A short description for the app",
            "StartupWMClass": "(Optional) For correct taskbar icon"
        }
        
        for i, (label, hint) in enumerate(self.fields.items()):
            tk.Label(middle_frame, text=f"{label}:", bg=self.style_config["bg"], fg=self.style_config["fg"]).grid(row=i+1, column=0, sticky='w', padx=5, pady=5)
            entry = tk.Entry(middle_frame, bg=self.style_config["entry_bg"], fg=self.style_config["fg"], insertbackground=self.style_config["fg"], relief=tk.FLAT, width=50)
            entry.grid(row=i+1, column=1, sticky='ew', pady=5)
            entry.insert(0, hint)
            entry.config(fg='grey')
            entry.bind("<FocusIn>", self.clear_placeholder)
            entry.bind("<FocusOut>", lambda e, l=label, h=hint: self.add_placeholder(e, l, h))
            self.entries[label] = entry

        tk.Button(middle_frame, text="Browse...", command=self.browse_for_icon, **self.button_styles()).grid(row=3, column=2, padx=5)
        tk.Button(middle_frame, text="Auto-Detect", command=self.autodetect_wm_class, **self.button_styles()).grid(row=5, column=2, padx=5)
        middle_frame.grid_columnconfigure(1, weight=1)

        # --- Log Frame: Output & Install Button ---
        tk.Label(log_frame, text="3. Install Progress:", bg=self.style_config["bg"], fg=self.style_config["fg"]).pack(anchor='w')
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, bg=self.style_config["entry_bg"], fg=self.style_config["fg"], font=self.log_font, relief=tk.FLAT, height=10)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_area.config(state=tk.DISABLED)
        tk.Button(log_frame, text="INSTALL APPLICATION", command=self.install_application, **self.button_styles(pady=10)).pack(fill=tk.X)
        
        self.scan_for_appimages()

    def clear_placeholder(self, event):
        for label, widget in self.entries.items():
            if widget == event.widget and widget.get() == self.fields[label]:
                widget.delete(0, END)
                widget.config(fg=self.style_config["fg"])
                break

    def add_placeholder(self, event, label, placeholder):
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(fg='grey')

    def log(self, message, level="info"):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(END, f"{message}\n")
        self.log_area.config(state=tk.DISABLED)
        self.log_area.see(END)
        self.update_idletasks()

    def scan_for_appimages(self):
        self.appimage_listbox.delete(0, END)
        self.log("🔍 Searching for AppImages in current directory...")
        appimages = [f for f in os.listdir('.') if f.lower().endswith('.appimage')]
        if not appimages:
            self.log("❌ No AppImage files found.", "error")
            return
        for app in appimages:
            self.appimage_listbox.insert(END, app)
        self.log(f"✔️ Found {len(appimages)} AppImage(s).")

    def browse_for_icon(self):
        filepath = filedialog.askopenfilename(title="Select an Icon File", filetypes=[("Image Files", "*.png *.svg *.ico"), ("All Files", "*.*")])
        if filepath:
            self.entries["Icon Path"].delete(0, END)
            self.entries["Icon Path"].insert(0, filepath)
            self.entries["Icon Path"].config(fg=self.style_config["fg"])

    def autodetect_wm_class(self):
        selection = self.appimage_listbox.curselection()
        if not selection:
            self.log("⚠️ Please select an AppImage from the list first.", "error")
            return
        appimage_name = self.appimage_listbox.get(selection[0])
        appimage_path = os.path.join(os.getcwd(), appimage_name)
        
        self.log(f"🔎 Trying to auto-detect 'StartupWMClass' for {appimage_name}...")
        wm_class = get_wm_class(appimage_path)
        
        if wm_class:
            self.log(f"✔️ Success! Found StartupWMClass: {wm_class}", "success")
            self.entries["StartupWMClass"].delete(0, END)
            self.entries["StartupWMClass"].insert(0, wm_class)
            self.entries["StartupWMClass"].config(fg=self.style_config["fg"])
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
        appimage_path_in = os.path.join(os.getcwd(), self.appimage_listbox.get(selection[0]))
        
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
        self.installed_apps = {} # To map display names to permanent names

        frame = tk.Frame(self.uninstall_tab, bg=self.style_config["bg"], padx=10, pady=10)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text="Installed Applications:", bg=self.style_config["bg"], fg=self.style_config["fg"]).pack(anchor='w')
        self.uninstall_listbox = Listbox(frame, bg=self.style_config["list_bg"], fg=self.style_config["fg"], selectbackground=self.style_config["list_select_bg"], height=15, exportselection=False, relief=tk.FLAT)
        self.uninstall_listbox.pack(fill='both', expand=True, pady=5)

        button_frame = tk.Frame(frame, bg=self.style_config["bg"])
        button_frame.pack(fill='x', pady=5)

        tk.Button(button_frame, text="Scan for Installed Apps", command=self.scan_for_installed_apps, **self.button_styles()).pack(side='left', expand=True, fill='x')
        tk.Button(button_frame, text="Uninstall Selected App", command=self.uninstall_application, **self.button_styles()).pack(side='left', expand=True, fill='x', padx=(10, 0))
        
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
                    
                    # Heuristic: check if it was installed by this tool
                    if self.install_base_dir in exec_path:
                        permanent_name = os.path.splitext(filename)[0]
                        self.installed_apps[display_name] = permanent_name
                        self.uninstall_listbox.insert(END, display_name)
                except Exception:
                    continue # Ignore malformed desktop files

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
            # Delete the installation directory
            install_dir = os.path.join(self.install_base_dir, permanent_name)
            if os.path.isdir(install_dir):
                shutil.rmtree(install_dir)
            
            # Delete the .desktop file
            desktop_filepath = os.path.join(self.desktop_entry_dir, f"{permanent_name}.desktop")
            if os.path.exists(desktop_filepath):
                os.remove(desktop_filepath)

            messagebox.showinfo("Success", f"'{display_name}' has been uninstalled successfully.")
            self.scan_for_installed_apps() # Refresh the list

        except Exception as e:
            messagebox.showerror("Uninstallation Error", f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        app = AppImageInstaller()
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
        sys.exit(1)

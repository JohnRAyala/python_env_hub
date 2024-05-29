import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Listbox, SINGLE, OptionMenu, StringVar, PhotoImage
import subprocess
import os
import sys
import threading
import json

class EnvironmentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Environment Hub")
        self.root.configure(bg="#2c3e50")
        self.icon_path = "new_shadows_icon_vjd_icon.ico"
        self.root.iconbitmap(self.icon_path)  # Set the icon for the window and taskbar

        self.button_widgets = {}
        self.custom_buttons = []
        self.custom_software = []
        self.create_widgets()
        self.load_custom_software()

    def create_widgets(self):
        self.button_bg = "#004080"
        self.button_fg = "#FFFFFF"
        self.unavailable_button_bg = "#7f8c8d"
        self.custom_button_bg = "#27ae60"
        button_font = ("Helvetica", 14, "bold")

        title_label = tk.Label(self.root, text="Python Environment Hub", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

        # Environment Manager Section
        env_label = tk.Label(self.root, text="Environment Manager", font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="#ecf0f1")
        env_label.grid(row=1, column=0, pady=(10, 10))

        env_buttons = [
            ("Create Environment", self.show_create_environment_dialog),
            ("Activate Environment", self.show_activate_dialog),
            ("Delete Environment", self.show_delete_environment_dialog)
        ]

        for i, (text, command) in enumerate(env_buttons):
            button = tk.Button(self.root, text=text, command=command, bg=self.button_bg, fg=self.button_fg, font=button_font, width=25, height=2)
            button.grid(row=i+2, column=0, padx=20, pady=10)
            self.button_widgets[text] = button

        # Tools Section
        tools_label = tk.Label(self.root, text="Tools", font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="#ecf0f1")
        tools_label.grid(row=1, column=1, pady=(10, 10))

        tools_buttons = [
            ("Open Jupyter Notebook", self.open_jupyter),
            ("Open Spyder", self.open_spyder),
            ("Help", self.show_help)
        ]

        for i, (text, command) in enumerate(tools_buttons):
            button = tk.Button(self.root, text=text, command=command, bg=self.button_bg, fg=self.button_fg, font=button_font, width=25, height=2)
            button.grid(row=i+2, column=1, padx=20, pady=10)
            self.button_widgets[text] = button

        # Custom Software Section
        custom_label = tk.Label(self.root, text="Custom Software", font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="#ecf0f1")
        custom_label.grid(row=1, column=2, pady=(10, 10))

        add_custom_button = tk.Button(self.root, text="Add Custom Software", command=self.show_custom_software_dialog, bg=self.custom_button_bg, fg=self.button_fg, font=button_font, width=25, height=2)
        add_custom_button.grid(row=2, column=2, padx=20, pady=10)
        self.button_widgets["Add Custom Software"] = add_custom_button

    def run_command(self, command):
        try:
            subprocess.run(command, check=True, shell=True)
            messagebox.showinfo("Success", "Command executed successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Command failed: {e}")

    def find_python_versions(self):
        python_versions = []
        for path in os.getenv('PATH').split(os.pathsep):
            if os.path.isdir(path):
                for file in os.listdir(path):
                    if file.startswith("python") and (file.endswith(".exe") or not os.path.splitext(file)[1]):
                        full_path = os.path.join(path, file)
                        try:
                            version_output = subprocess.check_output([full_path, "--version"], stderr=subprocess.STDOUT)
                            version = version_output.decode().strip().split()[-1]
                            python_versions.append((file, version))
                        except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
                            continue
        return list(set(python_versions))  # Remove duplicates and return

    def show_create_environment_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Create Environment")
        dialog.geometry("400x300")
        dialog.configure(bg="#2c3e50")
        dialog.attributes("-topmost", True)

        tk.Label(dialog, text="Enter environment name:", bg="#2c3e50", fg="#ecf0f1", font=("Helvetica", 12)).pack(pady=5)
        env_name_entry = tk.Entry(dialog, font=("Helvetica", 12))
        env_name_entry.pack(pady=5)

        tk.Label(dialog, text="Select Python version:", bg="#2c3e50", fg="#ecf0f1", font=("Helvetica", 12)).pack(pady=5)
        python_versions = self.find_python_versions()
        if not python_versions:
            messagebox.showerror("Error", "No Python versions found.")
            dialog.destroy()
            return

        python_version_var = StringVar(dialog)
        python_version_var.set(f"{python_versions[0][0]} ({python_versions[0][1]})")
        python_version_menu = OptionMenu(dialog, python_version_var, *[f"{pv[0]} ({pv[1]})" for pv in python_versions])
        python_version_menu.configure(font=("Helvetica", 12))
        python_version_menu.pack(pady=5)

        def on_create():
            env_name = env_name_entry.get()
            selected_version = python_version_var.get().split()[0]  # Extract the executable name
            if env_name:
                self.create_environment(env_name, selected_version)
            dialog.destroy()

        tk.Button(dialog, text="Create", command=on_create, bg=self.button_bg, fg=self.button_fg, font=("Helvetica", 12)).pack(pady=10)

    def create_environment(self, env_name, python_version):
        env_path = os.path.join(os.getcwd(), env_name)
        command = f"{python_version} -m venv {env_path}"
        try:
            subprocess.run(command, check=True, shell=True)
            messagebox.showinfo("Success", f"Environment '{env_name}' created successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Command failed: {e}. Ensure that the specified Python version is installed.")

    def show_activate_dialog(self):
        envs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d) and (os.path.exists(os.path.join(d, 'bin', 'activate')) or os.path.exists(os.path.join(d, 'Scripts', 'activate.bat')))]
        if not envs:
            messagebox.showinfo("Environments", "No environments found.")
            return

        dialog = Toplevel(self.root)
        dialog.title("Select Environment to Activate")
        dialog.geometry("300x250")
        dialog.configure(bg="#2c3e50")
        dialog.attributes("-topmost", True)

        listbox = Listbox(dialog, selectmode=SINGLE, font=("Helvetica", 12), bg="#34495e", fg="#ecf0f1", selectbackground="#1abc9c")
        listbox.pack(fill=tk.BOTH, expand=True)

        for env in envs:
            listbox.insert(tk.END, env)

        def on_select():
            selected_env = listbox.get(listbox.curselection())
            dialog.destroy()
            self.activate_environment(selected_env)

        listbox.bind("<Double-1>", lambda event: on_select())
        tk.Button(dialog, text="Activate", command=on_select, bg=self.button_bg, fg=self.button_fg, font=("Helvetica", 12)).pack(pady=10)

    def activate_environment(self, env_name):
        env_path = os.path.join(os.getcwd(), env_name)
        if os.path.exists(env_path):
            activate_script = os.path.join(env_path, 'bin', 'activate') if os.name != 'nt' else os.path.join(env_path, 'Scripts', 'activate.bat')
            if os.path.exists(activate_script):
                if os.name == 'nt':
                    cmd_command = f'start cmd /k "{activate_script}"'
                else:
                    cmd_command = f'x-terminal-emulator -e "bash -c \\"source {activate_script}; exec bash\\""'
                threading.Thread(target=self.run_command, args=(cmd_command,)).start()
            else:
                messagebox.showerror("Error", "Activate script not found.")
        else:
            messagebox.showerror("Error", "Environment does not exist.")

    def show_delete_environment_dialog(self):
        self.delete_dialog = Toplevel(self.root)
        self.delete_dialog.title("Delete Environment")
        self.delete_dialog.geometry("300x300")
        self.delete_dialog.configure(bg="#2c3e50")
        self.delete_dialog.attributes("-topmost", True)

        tk.Label(self.delete_dialog, text="Environments:", bg="#2c3e50", fg="#ecf0f1", font=("Helvetica", 12)).pack(pady=5)

        self.env_listbox = Listbox(self.delete_dialog, font=("Helvetica", 12), bg="#34495e", fg="#ecf0f1", selectbackground="#1abc9c")
        self.env_listbox.pack(fill=tk.BOTH, expand=True)

        envs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d) and (os.path.exists(os.path.join(d, 'bin', 'activate')) or os.path.exists(os.path.join(d, 'Scripts', 'activate.bat')))]
        for env in envs:
            self.env_listbox.insert(tk.END, env)

        tk.Label(self.delete_dialog, text="Type 'DELETE' to confirm:", bg="#2c3e50", fg="#ecf0f1", font=("Helvetica", 12)).pack(pady=5)
        self.confirm_entry = tk.Entry(self.delete_dialog, font=("Helvetica", 12))
        self.confirm_entry.pack(pady=5)

        tk.Button(self.delete_dialog, text="Delete", command=self.on_delete_confirm, bg=self.button_bg, fg=self.button_fg, font=("Helvetica", 12)).pack(pady=10)

    def on_delete_confirm(self):
        if self.confirm_entry.get().upper() == "DELETE":
            selected_env = self.env_listbox.get(tk.ACTIVE)
            self.delete_environment(selected_env)
            self.env_listbox.delete(tk.ACTIVE)
            self.confirm_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Type 'DELETE' to confirm.")

    def delete_environment(self, env_name):
        env_path = os.path.join(os.getcwd(), env_name)
        if os.path.exists(env_path):
            if os.name == 'nt':
                self.run_command(f"rmdir /s /q {env_path}")
            else:
                self.run_command(f"rm -rf {env_path}")
            messagebox.showinfo("Success", f"Environment '{env_name}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Environment does not exist.")

    def open_jupyter(self):
        threading.Thread(target=self.run_command, args=("jupyter notebook",)).start()

    def open_spyder(self):
        threading.Thread(target=self.run_command, args=("spyder",)).start()

    def show_custom_software_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Add Custom Software")
        dialog.geometry("400x200")
        dialog.configure(bg="#2c3e50")
        dialog.attributes("-topmost", True)

        tk.Label(dialog, text="Enter software name:", bg="#2c3e50", fg="#ecf0f1", font=("Helvetica", 12)).pack(pady=5)
        software_name_entry = tk.Entry(dialog, font=("Helvetica", 12))
        software_name_entry.pack(pady=5)

        def on_add(event=None):
            software_name = software_name_entry.get()
            if software_name:
                self.add_custom_software(software_name)
                dialog.destroy()

        software_name_entry.bind("<Return>", on_add)
        tk.Button(dialog, text="Add", command=on_add, bg=self.button_bg, fg=self.button_fg, font=("Helvetica", 12)).pack(pady=10)

    def add_custom_software(self, software_name):
        if software_name not in self.custom_software:
            self.custom_software.append(software_name)
            self.save_custom_software()
            self.create_custom_software_button(software_name)

    def create_custom_software_button(self, software_name):
        frame = tk.Frame(self.root, bg="#2c3e50")
        button = tk.Button(frame, text=f"Open {software_name}", command=lambda: self.open_custom_software(software_name), bg=self.custom_button_bg, fg=self.button_fg, font=("Helvetica", 14, "bold"), width=22, height=2)
        button.pack(side=tk.LEFT)

        remove_button = tk.Button(frame, text="X", command=lambda: self.remove_custom_software(software_name, frame), bg="#e74c3c", fg=self.button_fg, font=("Helvetica", 14, "bold"), width=3, height=2)
        remove_button.pack(side=tk.RIGHT)

        self.custom_buttons.append(frame)
        self.place_buttons()

    def remove_custom_software(self, software_name, frame):
        if software_name in self.custom_software:
            self.custom_software.remove(software_name)
            self.save_custom_software()
            self.custom_buttons.remove(frame)
            frame.destroy()
            self.place_buttons()

    def open_custom_software(self, software_name):
        threading.Thread(target=self.run_command, args=(software_name,)).start()

    def load_custom_software(self):
        try:
            with open("custom_software.json", "r") as file:
                self.custom_software = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.custom_software = []

        for software in self.custom_software:
            self.create_custom_software_button(software)

    def save_custom_software(self):
        with open("custom_software.json", "w") as file:
            json.dump(self.custom_software, file)

    def show_help(self):
        help_message = """
Python Environment Hub Help:

To open a Jupyter Notebook in your active environment, type the following command:
    jupyter notebook

To download Jupyter and install, go to the following link:
    https://jupyter.org/install

To download Spyder, go to the following link:
    https://www.spyder-ide.org/

To download Notepad++, go to the following link:
    https://notepad-plus-plus.org/downloads/

To download PyCharm Community Edition, go to the following link:
    https://www.jetbrains.com/pycharm/download/

To activate an environment manually, type the following command + environment name:
    source /path_to_env/bin/activate (Linux/Mac)
    .\path_to_env\Scripts\activate (Windows)

To create an environment manually, type the following command:
    python -m venv env_name

To install Python libraries, use pip. To know more, refer to the following link:
    https://pip.pypa.io/en/stable/installation/
        """
        messagebox.showinfo("Help", help_message)

    def place_buttons(self):
        row_start = 3
        col = 2  # Start in the Custom Software column

        for idx, frame in enumerate(self.custom_buttons):
            row = (idx % 3) + row_start  # Reset row after every 3 buttons
            if row == row_start and idx != 0:
                col += 1  # Move to the next column after every 3 buttons
            frame.grid(row=row, column=col, padx=20, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnvironmentManagerApp(root)
    root.mainloop()

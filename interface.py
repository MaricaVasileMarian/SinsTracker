import tkinter as tk
from tkinter import ttk
import datetime
from functions.timer import Timer
from functions.excel_manager import ExcelManager
from functions.update_checker import check_for_updates
from functions.donations import open_donation_link
from functions.project_selector import ProjectSelector

class SinsTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sins Tracker")
        self.master.geometry('600x400')  # Set the window size
        self.master.configure(bg="#333333")
        
        # Set the icon
        self.master.iconbitmap('icon.ico')  # Path to your .ico file
        
        self.timer = Timer(self.update_timer_label)
        self.excel_manager = ExcelManager()
        
        self.setup_ui()

    def setup_ui(self):
        self.master.columnconfigure(0, weight=1)  # Makes the column growable
        self.master.rowconfigure(4, weight=1)  # Makes the row growable

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 10), background='#333333', foreground='black', width=20)
        style.configure('TEntry', font=('Helvetica', 10), width=50)
        style.configure('TLabel', background="#333333", foreground="white", font=('Helvetica', 10))
        style.configure('TCombobox', font=('Helvetica', 10), width=27)

        ttk.Label(self.master, text="Activity Name:", style='TLabel').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.activity_name = ttk.Entry(self.master, width=50)  # Directly set the width here
        self.activity_name.grid(row=0, column=1, padx=10, pady=5, sticky='ew')  # Expanded along the grid cell
        
        ttk.Label(self.master, text="Category:", style='TLabel').grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.category = ttk.Combobox(self.master, values=["Project", "Research"], style='TCombobox')
        self.category.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
        self.category.set("Project")  # Default value
        
        # Buttons
        self.start_button = ttk.Button(self.master, text="Start", command=self.start_timer, style='TButton')
        self.start_button.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
        
        self.pause_button = ttk.Button(self.master, text="Pause", command=self.pause_timer, state=tk.DISABLED, style='TButton')
        self.pause_button.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        
        self.stop_button = ttk.Button(self.master, text="Stop", command=self.stop_timer, state=tk.DISABLED, style='TButton')
        self.stop_button.grid(row=2, column=2, padx=10, pady=5, sticky='ew')
        
        ttk.Button(self.master, text="Check for Updates", command=lambda: check_for_updates(self), style='TButton').grid(row=3, column=0, padx=10, pady=5, sticky='ew')
        ttk.Button(self.master, text="Donate a Coffee", command=open_donation_link, style='TButton').grid(row=3, column=1, padx=10, pady=5, sticky='ew')
        ttk.Button(self.master, text="Choose Project", command=self.open_project_selector, style='TButton').grid(row=3, column=2, padx=10, pady=5, sticky='ew')

        self.timer_label = ttk.Label(self.master, text="00:00:00", font=("Helvetica", 48), foreground="red")
        self.timer_label.grid(row=4, column=0, columnspan=3, padx=10, pady=20, sticky='n')

    def update_timer_label(self, time_str):
        self.timer_label.config(text=time_str)

    def start_timer(self):
        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timer.start()
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)

    def pause_timer(self):
        self.timer.pause_continue()
        if self.timer._running:
            self.stop_button.config(state=tk.NORMAL)
            self.pause_button.config(text="Pause")
        else:
            self.stop_button.config(state=tk.DISABLED)
            self.pause_button.config(text="Continue")

    def stop_timer(self):
        elapsed_time = self.timer.stop()
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text="Pause")
        self.stop_button.config(state=tk.DISABLED)
        duration_str = self.timer._format_time(elapsed_time)
        self.excel_manager.log_activity(
            self.activity_name.get(),
            self.category.get(),
            self.start_time,
            end_time,
            elapsed_time
        )
        print(f"Activity duration: {duration_str}")  # Place where Excel logging would occur

    def open_project_selector(self):
        ProjectSelector(self, "Select Project", self.excel_manager)

    def update_ui_after_download(self):
        tk.messagebox.showinfo("Update", "The application has been updated successfully!")
        # Other UI changes after download if necessary
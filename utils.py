import os
from datetime import datetime
from tkinter import filedialog, messagebox


class Utils:
    """
    Helper functions for HashGuard Pro
    """

    # -----------------------------------
    # Select Multiple Files
    # -----------------------------------
    @staticmethod
    def select_files():

        files = filedialog.askopenfilenames(
            title="Select File(s)",
            filetypes=[
                ("All Files", "*.*"),
                ("PDF Files", "*.pdf"),
                ("Text Files", "*.txt"),
                ("Word Files", "*.docx"),
                ("Images", "*.png *.jpg *.jpeg"),
                ("Executables", "*.exe")
            ]
        )

        return list(files)

    # -----------------------------------
    # Current Date
    # -----------------------------------
    @staticmethod
    def current_date():

        return datetime.now().strftime("%d-%m-%Y")

    # -----------------------------------
    # Current Time
    # -----------------------------------
    @staticmethod
    def current_time():

        return datetime.now().strftime("%I:%M:%S %p")

    # -----------------------------------
    # Show Success Message
    # -----------------------------------
    @staticmethod
    def success(title, message):

        messagebox.showinfo(title, message)

    # -----------------------------------
    # Show Error Message
    # -----------------------------------
    @staticmethod
    def error(title, message):

        messagebox.showerror(title, message)

    # -----------------------------------
    # Show Warning
    # -----------------------------------
    @staticmethod
    def warning(title, message):

        messagebox.showwarning(title, message)

    # -----------------------------------
    # Ask Yes / No
    # -----------------------------------
    @staticmethod
    def confirm(title, message):

        return messagebox.askyesno(title, message)

    # -----------------------------------
    # Clear Listbox
    # -----------------------------------
    @staticmethod
    def clear_listbox(listbox):

        listbox.delete(0, "end")

    # -----------------------------------
    # Clear Text Widget
    # -----------------------------------
    @staticmethod
    def clear_textbox(textbox):

        textbox.delete("1.0", "end")

    # -----------------------------------
    # Create Reports Folder
    # -----------------------------------
    @staticmethod
    def create_reports_folder():

        if not os.path.exists("reports"):
            os.makedirs("reports")

    # -----------------------------------
    # Open Reports Folder
    # -----------------------------------
    @staticmethod
    def open_reports_folder():

        Utils.create_reports_folder()

        os.startfile("reports")

    # -----------------------------------
    # Format Hash
    # -----------------------------------
    @staticmethod
    def short_hash(hash_value):

        if len(hash_value) <= 20:
            return hash_value

        return hash_value[:10] + "..." + hash_value[-10:]

    # -----------------------------------
    # Get File Extension
    # -----------------------------------
    @staticmethod
    def file_extension(file_path):

        return os.path.splitext(file_path)[1]

    # -----------------------------------
    # Convert Bytes
    # -----------------------------------
    @staticmethod
    def format_bytes(size):

        power = 1024
        n = 0
        units = ["Bytes", "KB", "MB", "GB", "TB"]

        while size >= power and n < len(units) - 1:
            size /= power
            n += 1

        return f"{size:.2f} {units[n]}"

    # -----------------------------------
    # About Project
    # -----------------------------------
    @staticmethod
    def about():

        messagebox.showinfo(

            "About HashGuard Pro",

            """
HashGuard Pro v1.0

A Professional File Integrity Monitoring Tool

Features

• SHA-256
• MD5
• SQLite Database
• Multiple File Support
• Integrity Verification
• Report Export

Developed By

Abubaker Raheem
            """

        )
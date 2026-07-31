import hashlib
import os
from datetime import datetime


class FileHasher:
    """
    Handles file hashing and file information.
    """

    @staticmethod
    def calculate_hash(file_path, algorithm="SHA-256"):
        """
        Generate SHA-256 or MD5 hash of a file.
        """

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if algorithm.upper() == "SHA-256":
            hasher = hashlib.sha256()
        elif algorithm.upper() == "MD5":
            hasher = hashlib.md5()
        else:
            raise ValueError("Unsupported algorithm. Use SHA-256 or MD5.")

        try:
            with open(file_path, "rb") as file:
                while True:
                    chunk = file.read(4096)

                    if not chunk:
                        break

                    hasher.update(chunk)

            return hasher.hexdigest()

        except Exception as e:
            raise Exception(f"Error while hashing file:\n{e}")

    # ------------------------------------
    # Get File Size
    # ------------------------------------

    @staticmethod
    def get_file_size(file_path):

        if not os.path.exists(file_path):
            return "Unknown"

        size = os.path.getsize(file_path)

        if size < 1024:
            return f"{size} Bytes"

        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"

        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.2f} MB"

        else:
            return f"{size / (1024 * 1024 * 1024):.2f} GB"

    # ------------------------------------
    # Last Modified Date
    # ------------------------------------

    @staticmethod
    def get_last_modified(file_path):

        if not os.path.exists(file_path):
            return "Unknown"

        timestamp = os.path.getmtime(file_path)

        return datetime.fromtimestamp(timestamp).strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

    # ------------------------------------
    # File Exists
    # ------------------------------------

    @staticmethod
    def file_exists(file_path):

        return os.path.exists(file_path)

    # ------------------------------------
    # File Name
    # ------------------------------------

    @staticmethod
    def get_file_name(file_path):

        return os.path.basename(file_path)

    # ------------------------------------
    # Full File Information
    # ------------------------------------

    @staticmethod
    def get_file_info(file_path):

        return {
            "name": FileHasher.get_file_name(file_path),
            "path": file_path,
            "size": FileHasher.get_file_size(file_path),
            "last_modified": FileHasher.get_last_modified(file_path)
        }
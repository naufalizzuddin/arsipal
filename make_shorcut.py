import os, re

current_directory = os.getcwd()
nama = os.getlogin()

with open(f"C:\\Users\\{nama}\\Desktop\\Jalankan Arsipal.bat", "w") as bat:
    bat.write(
    """
    @echo off
    py {}/manage.py runserver
    pause
    """.format(current_directory))
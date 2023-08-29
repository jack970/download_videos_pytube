@echo
env\Scripts\activate && pyinstaller -F main.py --noconfirm --onedir --windowed --name "YouTube Downloader" --add-data "assets;assets" --icon assets\logo.ico --collect-all customtkinter -w
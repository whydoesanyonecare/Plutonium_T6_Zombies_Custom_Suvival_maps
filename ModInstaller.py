import os, stat
import sys
import subprocess
import shutil
import psutil
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QProgressBar, QSizePolicy, QFileDialog, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
import webbrowser
import qdarktheme
from pathlib import Path

LOCALAPPDATA = os.getenv('LOCALAPPDATA')
INSTALL_FOLDER = f"{LOCALAPPDATA}/Plutonium/storage/t6/scripts/zm"
SAFE = f"{INSTALL_FOLDER}/safe"
MOD_DOWNLOAD_FOLDER = "./"
MOD_FOLDER = "./scripts"

def popup_message(title, message, icon=QMessageBox.Warning):
    popup = QMessageBox()
    popup.setWindowTitle(title)
    popup.setText(message)
    popup.setIcon(icon)
    popup.exec_()

class mod_installer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('T6 Custom Survival Map - Mod Installer')
        self.setWindowIcon(QIcon('bo2.ico'))
        self.setGeometry(100, 100, 400, 100)

        layout = QVBoxLayout()

        buttons_layout = QHBoxLayout()

        self.install_button = QPushButton("Install")
        self.install_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.install_button.clicked.connect(self.install_mod)
        buttons_layout.addWidget(self.install_button, 75)

        self.uninstall_button = QPushButton("Uninstall")
        self.uninstall_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.uninstall_button.clicked.connect(self.uninstall_mod)
        buttons_layout.addWidget(self.uninstall_button, 75)

        layout.addLayout(buttons_layout)

        buttons_layout_row2 = QHBoxLayout()

        self.discord_button = QPushButton("Discord")
        self.discord_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.discord_button.clicked.connect(self.open_discord_invite)
        buttons_layout_row2.addWidget(self.discord_button, 75)

        self.mods_button = QPushButton("More Mods")
        self.mods_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mods_button.clicked.connect(self.open_mods)
        buttons_layout_row2.addWidget(self.mods_button, 75)

        self.forum_button = QPushButton("Forum Post")
        self.forum_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.forum_button.clicked.connect(self.open_forum_post)
        buttons_layout_row2.addWidget(self.forum_button, 75)

        layout.addLayout(buttons_layout_row2)

        buttons_layout_row3 = QHBoxLayout()

        self.launch_button = QPushButton("Launch Plutonium Without Updating".upper())
        self.launch_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.launch_button.clicked.connect(self.open_plutonium)
        buttons_layout_row3.addWidget(self.launch_button, 75)

        layout.addLayout(buttons_layout_row3)
        self.setLayout(layout)

    def install_mod(self):
        if not os.path.exists( INSTALL_FOLDER ):
            os.makedirs( INSTALL_FOLDER )

        files = os.listdir( INSTALL_FOLDER )
        if len( files ) > 0:
            if not os.path.exists( SAFE ):
                os.makedirs( SAFE )

            for item in files:
                try:
                    shutil.move(os.path.join( INSTALL_FOLDER, item ), SAFE)
                except Exception as error:
                    print(error)

        current_folder = os.getcwd()
        files = os.listdir( current_folder )
        lua_file = f"{LOCALAPPDATA}/Plutonium/storage/t6/ui_mp/t6/menus/privategamelobby_project.lua"
        if os.path.exists(lua_file):
            try:
                os.remove(f"{LOCALAPPDATA}/Plutonium/storage/t6/ui_mp/t6/menus/privategamelobby_project.lua")
            except Exception as error:
                print(f"Error: Lua file does not exists in plutonium folder {error}")
        try:
            shutil.copyfile(f"{current_folder}/privategamelobby_project.lua", f"{LOCALAPPDATA}/Plutonium/storage/t6/ui_mp/t6/menus/privategamelobby_project.lua")
        except Exception as error:
            print(f"Error copying lua to install folder: {error}")    
        
        try:
            shutil.copytree( MOD_FOLDER, INSTALL_FOLDER, dirs_exist_ok=True)
        except Exception as error:
            print(f"Error: There was problem copying script folders to install location {error}")

        popup_message("Install Complete!", f"Mod was installed successfully! \n\nSTART PLUTONIUM WITH 'LAUNCH PLUTONIUM WITHOUT UPDATING' BUTTON. \n\nYour old mods was moved to safe folder to get them back use the Uninstall button.", icon=QMessageBox.Information)

    def uninstall_mod(self):

        if os.path.exists( INSTALL_FOLDER ):
            try:
                if os.path.exists( f"{INSTALL_FOLDER}/zm_prison" ):
                    shutil.rmtree( f"{INSTALL_FOLDER}/zm_prison" )
    
                if os.path.exists( f"{INSTALL_FOLDER}/zm_transit" ):
                    shutil.rmtree( f"{INSTALL_FOLDER}/zm_transit" )

                if os.path.exists( f"{LOCALAPPDATA}/Plutonium/storage/t6/ui_mp/t6/menus/privategamelobby_project.lua" ):
                    os.remove(f"{LOCALAPPDATA}/Plutonium/storage/t6/ui_mp/t6/menus/privategamelobby_project.lua")

            except Exception as error:
                print(f"Error: There was problem deleting script folders from install location {error}")

            if os.path.exists( SAFE ):
                directory = os.listdir( SAFE )
                if len(directory) > 0:
                    for item in directory:
                        try:
                            shutil.move(os.path.join( SAFE, item ), INSTALL_FOLDER)
                        except Exception as error:
                            print(f"Error: There was problem moving old mods back {error}")

                files = os.listdir( SAFE )
                if len(files) == 0:
                    try:
                        shutil.rmtree( SAFE )
                    except Exception as error:
                        print(f"Error: There was problem deleting SAFE folder {error}")

        popup_message("Uninstall Complete!", f"Mod was uninstalled successfully!", icon=QMessageBox.Information)

    def open_discord_invite(self):
        link = "https://discord.com/invite/mtAsvArAJD"
        webbrowser.open(link)
    
    def open_forum_post(self):
        link = "https://forum.plutonium.pw/topic/17208/release-zombies-custom-survival-maps-option-for-custom-games"
        webbrowser.open(link)
    
    def open_mods(self):
        link = "https://forum.plutonium.pw/user/dontknowletspl/topics"
        webbrowser.open(link)
    
    def open_plutonium(self):
        subprocess.Popen(f"{LOCALAPPDATA}/Plutonium/bin/plutonium-launcher-win32.exe")
        subprocess.run(['taskkill', '/F', '/IM', 'ModInstaller.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = mod_installer()
    window.show()

    sys.exit(app.exec_())

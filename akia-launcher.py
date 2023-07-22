import sys
import os
import json
import requests
import functools
import zipfile
import shutil
from PyQt5.QtGui import QIcon  # Importez QIcon depuis PyQt5.QtGui
from qtpy.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget
from qtpy.QtGui import QFont
from win32com.client import Dispatch

def ressource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        list_addon = []
        list_addon.append(["WhatIDoToday","https://github.com/akia-web/WhatIDoToday/archive/refs/heads/main.zip"])
        list_addon.append(["SummonedMount","https://github.com/akia-web/SummonedMount/archive/refs/heads/main.zip"])
        
        self.setWindowTitle("Akia's addons")
        self.resize(1000, 700)  # Définir la taille de la fenêtre

        self.center_window()  # Appeler la fonction pour centrer la fenêtre

        self.folder_line_edit = QLineEdit(self)
        self.folder_line_edit.setReadOnly(True)
        self.folder_line_edit.setFixedWidth(500)  # Définir une largeur fixe de 500 pixels
        self.folder_line_edit.setStyleSheet("QLineEdit { color: gray; background-color: #F0F0F0; }")

        self.button = QPushButton("Sélectionner un dossier", self)
        self.buttonUpdate = QPushButton("Mise à jour logiciel", self)
        self.buttonUpdate.clicked.connect(self.button_update)
        self.button.clicked.connect(self.select_folder)
        

        # Créer un layout horizontal pour le champ d'entrée et le bouton
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.folder_line_edit)
        layout_horizontal.addWidget(self.button)

        # Créer un widget pour le layout horizontal
        widget_horizontal = QWidget(self)
        widget_horizontal.setLayout(layout_horizontal)

        # Créer un label pour afficher "Vos addons"
        label_text = QLabel("Vos addons", self)
        label_text.setFont(QFont("Arial", 20))
        # Créer un layout vertical pour organiser les éléments
        layout_vertical = QVBoxLayout()
        layout_vertical.addWidget(self.buttonUpdate)
        layout_vertical.addWidget(widget_horizontal)  # Ajouter le layout horizontal
        layout_vertical.addWidget(label_text)         # Ajouter le label "Vos addons"

        for item in list_addon:
            addon = QLabel(item[0], self)
            button = QPushButton("Cliquez ici", self)
            button.clicked.connect(functools.partial(self.button_clicked,item))
            layout_vertical.addWidget(addon)
            layout_vertical.addWidget(button)
        # Ajouter des espacements pour aligner le layout horizontal en haut
        layout_vertical.addStretch(1)

        # Créer un widget conteneur pour le layout vertical
        widget = QWidget(self)
        widget.setLayout(layout_vertical)

        # Définir le widget conteneur en tant que widget central de la fenêtre
        self.setCentralWidget(widget)

        self.load_config()  # Charger le chemin du dossier à partir du fichier de configuration

    def center_window(self):
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier")
        if folder_path:
            self.folder_line_edit.setText(folder_path)
            self.save_config()  # Enregistrer le chemin du dossier dans le fichier de configuration

    def load_config(self):
        config_file = "config.json"
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                config_data = json.load(file)
                folder_path = config_data.get("folder_path", "")
                self.folder_line_edit.setText(folder_path)

    def save_config(self):
        config_data = {"folder_path": self.folder_line_edit.text()}
        config_file = "config.json"
        with open(config_file, "w") as file:
            json.dump(config_data, file)
    
    def button_clicked(self, item):
        print("Le bouton a été cliqué !")
        print(item[1])
        folder_path = self.folder_line_edit.text()
        print(folder_path)
        if folder_path:
            try:
            # Supprimer le dossier "WhatIDoToday-main" s'il existe
                addon_folder_path = os.path.join(folder_path, item[0])
                if os.path.exists(addon_folder_path):
                    shutil.rmtree(addon_folder_path)

                response = requests.get(item[1])
                if response.status_code == 200:
                    with open("temp.zip", "wb") as file:
                        file.write(response.content)

                    with zipfile.ZipFile("temp.zip", "r") as zip_ref:
                        zip_ref.extractall(folder_path)

                    os.remove("temp.zip")

                    extracted_folder_path = os.path.join(folder_path, item[0]+"-main")
                    new_folder_path = os.path.join(folder_path, item[0])
                    os.rename(extracted_folder_path, new_folder_path)


                    print("Dossier téléchargé avec succès !")
                else:
                    print("Erreur lors du téléchargement du dossier.")
            except Exception as e:
                print(f"Une erreur est survenue : {e}")
        else:
            print("Veuillez sélectionner un dossier avant de télécharger.")
    
    def button_update(self):
        print(os.path.abspath("icone.ico"))
        print(os.path.dirname(os.path.abspath(sys.argv[0])))


    def button_update2(self):
        url = "https://example.com/nouvelle_version.zip"  # Remplacez par l'URL de téléchargement de la nouvelle version
        folder_path = os.path.abspath(sys.argv[0])

        if folder_path:
            try:
                # Supprimer le dossier temporaire s'il existe
                temp_folder_path = os.path.join(folder_path, "temp")
                if os.path.exists(temp_folder_path):
                    shutil.rmtree(temp_folder_path)

                # Télécharger la nouvelle version depuis l'URL
                response = requests.get(url)
                if response.status_code == 200:
                    with open("nouvelle_version.zip", "wb") as file:
                        file.write(response.content)

                    # Extraire les fichiers de la nouvelle version dans un dossier temporaire
                    with zipfile.ZipFile("nouvelle_version.zip", "r") as zip_ref:
                        zip_ref.extractall(temp_folder_path)

                    os.remove("nouvelle_version.zip")

                    # Copier les fichiers de la nouvelle version dans le dossier de l'application
                    for root, dirs, files in os.walk(temp_folder_path):
                        for file in files:
                            source_file = os.path.join(root, file)
                            destination_file = os.path.join(folder_path, file)
                            shutil.copy(source_file, destination_file)

                    # Supprimer le dossier temporaire
                    shutil.rmtree(temp_folder_path)

                    print("Mise à jour réussie ! Veuillez redémarrer l'application.")
                else:
                    print("Erreur lors du téléchargement de la nouvelle version.")
            except Exception as e:
                print(f"Une erreur est survenue : {e}")
        else:
            print("Veuillez sélectionner un dossier avant de mettre à jour.")


def create_shortcut_on_desktop(name, target, icon=None):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    path = os.path.join(desktop, f"{name}.lnk")
    shell = Dispatch('WScript.Shell')

    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target

    if icon:
        
        shortcut.IconLocation = ressource_path(icon)

    shortcut.save()


if __name__ == "__main__":
    app_path = sys.executable
    icon_path = "icone.ico"
    create_shortcut_on_desktop("Akia Launcher", app_path, icon_path)
    app = QApplication(sys.argv)
    QApplication.setStyle("Fusion")  # Spécifier un style de fenêtre explicite
    window = MainWindow()
    window_icon = QIcon(ressource_path(icon_path))
    window.setWindowIcon(window_icon)
    window.show()
    sys.exit(app.exec_())
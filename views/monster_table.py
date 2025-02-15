from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class MonsterTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.image_dir = "images/monsters/"
        self.monsters = []
        self.setup_table()

    def setup_table(self):
        headers = ["Image", "Nom", "Étoiles", "HP", "ATK", "DEF", "VIT",
                  "Taux Critique", "Dégâts Critiques", "Élément"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Configuration du tableau
        header = self.horizontalHeader()
        for i in range(self.columnCount()):
            if i == 0:  # Pour la colonne image
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                self.setColumnWidth(0, 150)  # Largeur fixe pour la colonne image
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        self.verticalHeader().setDefaultSectionSize(50)
        self.setShowGrid(True)
        self.setAlternatingRowColors(True)

    def update_monsters(self, monsters):
        self.monsters = monsters
        self.setRowCount(len(monsters))
        for row, monster in enumerate(monsters):
            # Gestion de l'image avec image_filename
            if hasattr(monster, 'image_filename') and monster.image_filename:
                image_path = os.path.join(self.image_dir, monster.image_filename)
                if os.path.exists(image_path):
                    label = QLabel()
                    pixmap = QPixmap(image_path)
                    scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
                    label.setPixmap(scaled_pixmap)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setCellWidget(row, 0, label)
                else:
                    # Afficher le chemin si l'image n'est pas trouvée
                    item = QTableWidgetItem(f"Not found: {image_path}")
                    item.setToolTip(image_path)  # Ajoute une infobulle avec le chemin complet
                    self.setItem(row, 0, item)
            else:
                self.set_default_image(row)

            # Ajouter les données du monstre
            monster_data = monster.to_table_row()
            for col, value in enumerate(monster_data, start=1):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(row, col, item)

    def set_default_image(self, row):
        """Définit l'image par défaut pour une ligne donnée"""
        default_image = os.path.join(self.image_dir, "default.png")
        if os.path.exists(default_image):
            label = QLabel()
            pixmap = QPixmap(default_image)
            scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setCellWidget(row, 0, label)
        else:
            # Afficher le chemin de l'image par défaut si elle n'existe pas
            path = os.path.abspath(default_image)
            item = QTableWidgetItem(f"Default not found: {path}")
            item.setToolTip(path)
            self.setItem(row, 0, item)

    def get_monster(self, row):
        if 0 <= row < len(self.monsters):
            return self.monsters[row]
        return None

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Maintenir la largeur fixe de la colonne image lors du redimensionnement
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 50)
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class RuneTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.rune_images_dir = "images/runes/"  # Chemin pour les images des runes
        self.runes = []
        self.setup_table()

    def setup_table(self):
        headers = ["Set", "Niveau", "Slot", "Qualité", "Stat Principale", 
                  "Stat Préfixe", "Sous-statistiques"]
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        # Configuration du tableau
        header = self.horizontalHeader()
        for i in range(self.columnCount()):
            if i == 0:  # Colonne Set
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                self.setColumnWidth(0, 150)
            elif i == 6:  # Colonne sous-stats
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            else:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.verticalHeader().setDefaultSectionSize(80)
        self.setShowGrid(True)
        self.setAlternatingRowColors(True)

    def update_runes(self, runes):
        self.runes = runes
        self.setRowCount(len(runes))
        
        for row, rune in enumerate(runes):
            # Image du set de runes
            if hasattr(rune, 'set_id'):
                image_path = os.path.join(self.rune_images_dir, f"set_{rune.set_id}.png")
                if os.path.exists(image_path):
                    label = QLabel()
                    pixmap = QPixmap(image_path)
                    scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
                    label.setPixmap(scaled_pixmap)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setCellWidget(row, 0, label)
                else:
                    item = QTableWidgetItem(f"Set {rune.set_id}")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.setItem(row, 0, item)

            # Ajouter les données de la rune
            rune_data = rune.to_table_row()
            for col, value in enumerate(rune_data[1:], start=1):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(row, col, item)

    def get_rune(self, row):
        if 0 <= row < len(self.runes):
            return self.runes[row]
        return None
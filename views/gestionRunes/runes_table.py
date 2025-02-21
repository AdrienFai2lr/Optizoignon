from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QWidget, QHBoxLayout
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
                self.setColumnWidth(0, 100)
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
            if hasattr(rune, 'set_id'):
                set_name = rune.get_set_name()
                image_path = os.path.join(self.rune_images_dir, f"{set_name}.png")
                
                # Créer un widget conteneur pour les images
                container = QWidget()
                layout = QHBoxLayout(container)
                layout.setSpacing(2)
                layout.setContentsMargins(0, 0, 0, 0)
                
                # Ajouter l'image de la rune
                if os.path.exists(image_path):
                    rune_label = QLabel()
                    pixmap = QPixmap(image_path)
                    scaled_pixmap = pixmap.scaled(40,40, Qt.AspectRatioMode.KeepAspectRatio)
                    rune_label.setPixmap(scaled_pixmap)
                    rune_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(rune_label)
                    
                    # Ajouter le symbole ancient si nécessaire
                    if rune.is_ancient:
                        ancient_path = os.path.join(self.rune_images_dir, "ancient.png")
                        if os.path.exists(ancient_path):
                            ancient_label = QLabel()
                            ancient_pixmap = QPixmap(ancient_path)
                            scaled_ancient = ancient_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio)
                            ancient_label.setPixmap(scaled_ancient)
                            ancient_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            layout.addWidget(ancient_label)
                    
                    self.setCellWidget(row, 0, container)
                else:
                    item = QTableWidgetItem(set_name.capitalize())
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
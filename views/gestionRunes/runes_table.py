from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, 
                            QScrollArea, QSizePolicy, QPushButton, QHBoxLayout)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSlot
import os

class RuneCard(QFrame):
    def __init__(self, rune, rune_images_dir):
        super().__init__()
        self.rune = rune
        self.rune_images_dir = rune_images_dir
        self.is_expanded = False
        self.setup_ui()
        
    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(200, 200)
        self.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 15px;
                border: 2px solid #3d3d3d;
            }
            QLabel {
                color: #ffffff;
                font-size: 15px;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888888;
                font-size: 10px;
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 0)  # Réduit la marge en bas
        self.main_layout.setSpacing(1)  # Réduit l'espacement entre les éléments
        
        self.create_basic_content()
        
        # Modification du bouton d'expansion
        self.expand_button = QPushButton("⌄")
        self.expand_button.setFixedSize(15, 20)  # Hauteur réduite
        self.expand_button.clicked.connect(self.toggle_details)
        self.expand_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888888;
                font-size: 20px;
               
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)
        self.main_layout.addWidget(self.expand_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Container pour les détails
        self.details_widget = QWidget()
        self.details_layout = QVBoxLayout(self.details_widget)
        self.details_layout.setContentsMargins(0, 0, 0, 10)  # Ajoute une petite marge en bas
        self.details_layout.setSpacing(2)
        self.create_details_content()
        self.details_widget.hide()
        self.main_layout.addWidget(self.details_widget)
        
    def create_basic_content(self):
        # Header avec image et info principale
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)  # Petit espacement entre les images
        
        # Conteneur pour les images (set et ancient)
        images_container = QWidget()
        images_layout = QHBoxLayout(images_container)
        images_layout.setContentsMargins(0, 0, 0, 0)
        images_layout.setSpacing(2)
        
        if hasattr(self.rune, 'set_id'):
            set_name = self.rune.get_set_name()
            image_path = os.path.join(self.rune_images_dir, f"{set_name}.png")
            if os.path.exists(image_path):
                img_container = QLabel()
                layout = QHBoxLayout(img_container)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(2)

                # Image du set
                rune_label = QLabel()
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio)
                rune_label.setPixmap(scaled_pixmap)
                layout.addWidget(rune_label)

                # Image ancient si nécessaire
                if self.rune.is_ancient:
                    ancient_path = os.path.join(self.rune_images_dir, "ancient.png")
                    if os.path.exists(ancient_path):
                        ancient_label = QLabel()
                        ancient_pixmap = QPixmap(ancient_path)
                        scaled_ancient = ancient_pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio)
                        ancient_label.setPixmap(scaled_ancient)
                        layout.addWidget(ancient_label)

            header_layout.addWidget(img_container)

        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(0)
        
        slot_level = QLabel(f"{self.rune.slot_no} | +{self.rune.level}")
        slot_level.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addWidget(slot_level)
        
        quality = QLabel(f"{self.rune.quality}")
        quality.setStyleSheet("color: #888888;")
        info_layout.addWidget(quality)
        
        header_layout.addWidget(info_container)
        self.main_layout.addWidget(header)

        # Stat principale
        main_stat = QLabel(self.rune.get_main_stat_display())
        main_stat.setStyleSheet("font-size: 13px; font-weight: bold; color: #4a9eff;")
        main_stat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(main_stat)

    def create_details_content(self):
        if self.rune.substats:
            for substat in self.rune.substats:
                stat_text = f"{substat.stat_type}: {substat.stat_value}"
                if hasattr(substat, 'upgrade_count') and substat.upgrade_count > 0:
                    stat_text += f" +{substat.upgrade_count}"
                
                substat_label = QLabel(stat_text)
                substat_label.setStyleSheet("color: #cccccc;")
                if hasattr(substat, 'initial_value'):
                    substat_label.setToolTip(f"Initial: {substat.initial_value}")
                self.details_layout.addWidget(substat_label)

        if self.rune.prefix_eff_type:
            prefix_label = QLabel(self.rune.get_prefix_stat_display())
            prefix_label.setStyleSheet("color: #888888; font-style: italic;")
            self.details_layout.addWidget(prefix_label)

    @pyqtSlot()
    def toggle_details(self):
        self.is_expanded = not self.is_expanded
        self.expand_button.setText("⌃" if self.is_expanded else "⌄")
        self.details_widget.setVisible(self.is_expanded)
        if self.is_expanded:
            self.setMinimumHeight(200)
        else:
            self.setMinimumHeight(200)

class RuneGrid(QScrollArea):
    def __init__(self):
        super().__init__()
        self.rune_images_dir = "images/runes/"
        self.setup_grid()
        self.setStyleSheet("""
            QScrollArea {
                background-color: #1e1e1e;
                border: none;
            }
            QWidget {
                background-color: #1e1e1e;
            }
        """)
        
    def setup_grid(self):
        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.grid_layout.setSpacing(12)
        self.grid_layout.setContentsMargins(12, 12, 12, 12)
        self.setWidget(self.container)
        self.setWidgetResizable(True)
        
    def update_runes(self, runes):
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        cols = 5  # Une colonne de plus pour un meilleur affichage
        for i, rune in enumerate(runes):
            row = i // cols
            col = i % cols
            card = RuneCard(rune, self.rune_images_dir)
            self.grid_layout.addWidget(card, row, col)
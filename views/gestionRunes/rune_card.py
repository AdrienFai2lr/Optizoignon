from PyQt6.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, 
                             QSizePolicy, QPushButton, QHBoxLayout)
from PyQt6.QtGui import QPixmap
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
        self.main_layout.setContentsMargins(4, 4, 4, 0)
        self.main_layout.setSpacing(1)
        
        self.create_basic_content()
        
        # Bouton d'expansion
        self.expand_button = QPushButton("⌄")
        self.expand_button.setFixedSize(15, 20)
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
        self.details_layout.setContentsMargins(0, 0, 0, 10)
        self.details_layout.setSpacing(2)
        self.create_details_content()
        self.details_widget.hide()
        self.main_layout.addWidget(self.details_widget)
        
    def create_basic_content(self):
        # Header avec image et info principale
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)
        
        # Conteneur pour les images
        img_container = QLabel()
        layout = QHBoxLayout(img_container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Image du set
        if hasattr(self.rune, 'set_id'):
            set_name = self.rune.get_set_name()
            image_path = os.path.join(self.rune_images_dir, f"{set_name}.png")
            if os.path.exists(image_path):
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
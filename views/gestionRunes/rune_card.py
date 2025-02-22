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
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration initiale de l'interface utilisateur"""
        # Configuration du cadre
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(300, 375)
        
        # Style général de la carte
        self.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border-radius: 15px;
                border: 5px solid #3d3d3d;
                padding: 10px;
            }
            QLabel {
                color: #ffffff;
                font-size: 10px;
            }
            QLabel.substat {
                color: #cccccc;
                font-size: 10px;
                padding-left: 5px;
            }
            QLabel.prefix {
                color: #888888;
                font-style: italic;
            }
            QLabel.main-stat {
                font-size: 15px;
                font-weight: bold;
                color: #4a9eff;
            }
            QLabel.rune-quality {
                font-weight: bold;
            }
        """)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(8)
        
        # Création des sections
        self.create_header()
        self.create_stats_section()
        
    def create_header(self):
        """Création de l'en-tête de la carte (image du set et infos de base)"""
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        
        # Image du set et indicateur ancien
        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(0)
        
        # Image du set de runes
        set_name = self.rune.get_set_name()
        image_path = os.path.join(self.rune_images_dir, f"{set_name}.png")
        if os.path.exists(image_path):
            rune_image = QLabel()
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(40, 40, 
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            rune_image.setPixmap(scaled_pixmap)
            image_layout.addWidget(rune_image)

            # Indicateur de rune ancienne
            if self.rune.is_ancient:
                ancient_path = os.path.join(self.rune_images_dir, "ancient.png")
                if os.path.exists(ancient_path):
                    ancient_label = QLabel()
                    ancient_pixmap = QPixmap(ancient_path)
                    scaled_ancient = ancient_pixmap.scaled(20, 20,
                                                         Qt.AspectRatioMode.KeepAspectRatio,
                                                         Qt.TransformationMode.SmoothTransformation)
                    ancient_label.setPixmap(scaled_ancient)
                    image_layout.addWidget(ancient_label)

        header_layout.addWidget(image_container)
        
        # Informations de base (slot, niveau, qualité)
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(0)
        
        # Slot et niveau
        slot_level = QLabel(f"Slot {self.rune.slot_no} | +{self.rune.level}")
        slot_level.setStyleSheet("font-weight: bold; font-size: 14px;")
        info_layout.addWidget(slot_level)
        
        # Qualité
        quality = QLabel(self.rune.quality.capitalize())
        quality.setProperty("class", "rune-quality")
        quality.setStyleSheet(self.get_quality_style(self.rune.quality))
        info_layout.addWidget(quality)
        
        header_layout.addWidget(info_container)
        self.main_layout.addWidget(header)
        
    def create_stats_section(self):
        """Création de la section des statistiques"""
        stats_container = QWidget()
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setContentsMargins(4, 4, 4, 4)
        stats_layout.setSpacing(0)
        
        # Stat principale
        main_stat = QLabel(self.rune.get_main_stat_display())
        main_stat.setProperty("class", "main-stat")
        main_stat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(main_stat)
        
        # Préfixe si présent
        if self.rune.prefix_eff_type:
            prefix_label = QLabel(self.rune.get_prefix_stat_display())
            prefix_label.setProperty("class", "prefix")
            stats_layout.addWidget(prefix_label)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #3d3d3d;")
        stats_layout.addWidget(separator)
        
        # Sous-stats
        if self.rune.substats:
            for substat in self.rune.substats:
                substat_text = f"{substat.stat_type}: {substat.stat_value}"
                if substat.upgrade_count > 0:
                    substat_text += f" +{substat.upgrade_count}"
                
                substat_label = QLabel(substat_text)
                substat_label.setProperty("class", "substat")
                if substat.tooltip:
                    substat_label.setToolTip(substat.tooltip)
                stats_layout.addWidget(substat_label)
        
        self.main_layout.addWidget(stats_container)

    def get_quality_style(self, quality):
        """Retourne le style CSS en fonction de la qualité de la rune"""
        colors = {
            'normal': '#FFFFFF',
            'magic': '#04d2eb',
            'rare': '#f0b266',
            'heroic': '#9a1eff',
            'legendary': '#f4af3d'
        }
        color = colors.get(quality.lower(), '#FFFFFF')
        return f"color: {color}; font-weight: bold;"
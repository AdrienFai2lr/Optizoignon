from PyQt6.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, 
                             QSizePolicy, QPushButton, QHBoxLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class RuneCard(QFrame):
    def __init__(self, rune, rune_images_dir):
        super().__init__()
        self.rune = rune
        self.rune_images_dir = rune_images_dir
        
        # Charger les styles
        try:
            with open('styles/styles.qss', 'r') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Erreur lors du chargement des styles: {e}")
            
        self.setup_ui()
        
    def setup_ui(self):
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(320, 400)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(12)
        
        self.create_header()
        self.create_stats_section()
        
    def create_header(self):
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(15)
        
        # Image container
        image_container = QFrame()
        image_container.setObjectName("imageContainer")
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(8, 8, 8, 8)
        image_layout.setSpacing(5)
        
        # Image du set
        set_name = self.rune.get_set_name().lower()
        image_path = os.path.join(self.rune_images_dir, f"{set_name}.png")
        if os.path.exists(image_path):
            rune_image = QLabel()
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(50, 50,
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            rune_image.setPixmap(scaled_pixmap)
            image_layout.addWidget(rune_image, alignment=Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(image_container)
        
        # Informations de base
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)
        
        # Slot, niveau et indicateur ancien
        slot_text = f"Slot {self.rune.slot_no} | +{self.rune.level}"
        if self.rune.is_ancient:
            slot_text += " | Ancient"
        slot_level = QLabel(slot_text)
        slot_level.setProperty("class", "slot-level")
        info_layout.addWidget(slot_level)
        
        # Qualité de la rune
        quality = QLabel(self.rune.quality.capitalize())
        quality.setProperty("class", f"quality-{self.rune.quality.lower()}")
        info_layout.addWidget(quality)
        
        header_layout.addWidget(info_container)
        self.main_layout.addWidget(header)
        
    def create_stats_section(self):
        stats_container = QFrame()
        stats_container.setProperty("class", "stats-container")
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setContentsMargins(10, 15, 10, 10)
        stats_layout.setSpacing(8)
        
        # Stat principale
        main_stat = QLabel(self.rune.get_main_stat_display())
        main_stat.setProperty("class", "main-stat")
        main_stat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(main_stat)
        
        # Préfixe avec grind
        if self.rune.prefix_stat_type:
            prefix_text = self.rune.get_prefix_stat_display()
            prefix_label = QLabel(prefix_text)
            prefix_label.setProperty("class", "prefix")
            if self.rune.prefix_is_gemmed:
                prefix_label.setProperty("class", "prefix gemmed")
            stats_layout.addWidget(prefix_label)
        
        # Sous-stats avec grind et gemmes
        if self.rune.substats:
            for substat in self.rune.substats:
                substat_widget = QWidget()
                substat_layout = QHBoxLayout(substat_widget)
                substat_layout.setContentsMargins(0, 0, 0, 0)
                
                # Création du texte de la sous-stat
                substat_text = f"{substat['type']}: {substat['value']}"
                if substat['grind_value'] > 0:
                    substat_text += f" (+{substat['grind_value']})"
                
                substat_label = QLabel(substat_text)
                substat_label.setProperty("class", "substat")
                
                if substat['is_gemmed']:
                    substat_label.setProperty("class", "substat gemmed")
                    tooltip = f"Gemmé (ancienne stat: {substat['original_type']})"
                    substat_label.setToolTip(tooltip)
                
                substat_layout.addWidget(substat_label)
                stats_layout.addWidget(substat_widget)
        
        self.main_layout.addWidget(stats_container)
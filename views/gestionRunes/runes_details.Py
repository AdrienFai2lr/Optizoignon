from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGridLayout, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

class RuneDetailView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.rune = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Barre supérieure avec bouton retour
        top_bar = QHBoxLayout()
        back_button = QPushButton("Retour à la liste")
        back_button.clicked.connect(self.return_to_list)
        top_bar.addWidget(back_button)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # Conteneur principal
        main_container = QFrame()
        main_container.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        main_layout = QGridLayout(main_container)

        # Image du set de runes
        self.rune_image = QLabel()
        self.rune_image.setFixedSize(100, 100)
        self.rune_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.rune_image, 0, 0, 2, 1)

        # Informations de base
        self.info_basic = QLabel()
        self.info_basic.setFont(QFont('Arial', 12))
        main_layout.addWidget(self.info_basic, 0, 1)

        # Statistique principale
        self.main_stat = QLabel()
        self.main_stat.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        main_layout.addWidget(self.main_stat, 1, 1)

        # Stat préfixe (si présente)
        self.prefix_stat = QLabel()
        main_layout.addWidget(self.prefix_stat, 2, 1)

        # Sous-statistiques
        substats_frame = QFrame()
        substats_frame.setFrameStyle(QFrame.Shape.Box)
        substats_layout = QVBoxLayout(substats_frame)
        self.substat_labels = []
        for _ in range(4):  # Maximum 4 sous-stats
            label = QLabel()
            self.substat_labels.append(label)
            substats_layout.addWidget(label)
        main_layout.addWidget(substats_frame, 3, 0, 1, 2)

        # Efficacité et score
        self.efficiency_label = QLabel()
        main_layout.addWidget(self.efficiency_label, 4, 0, 1, 2)

        layout.addWidget(main_container)
        layout.addStretch()

    def update_rune(self, rune):
        if not rune:
            return

        self.rune = rune

        # Mise à jour de l'image du set
        image_path = f"images/runes/set_{rune.set_id}.png"
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(90, 90, Qt.AspectRatioMode.KeepAspectRatio)
            self.rune_image.setPixmap(scaled_pixmap)
        else:
            self.rune_image.setText(f"Set {rune.set_id}")

        # Informations de base
        quality_color = self.get_quality_color(rune.quality)
        self.info_basic.setText(
            f'<span style="color: {quality_color};">{rune.quality}</span> Rune {rune.set_id} '
            f'Slot {rune.slot_no} +{rune.level}'
        )

        # Stat principale
        self.main_stat.setText(rune.get_main_stat_display())

        # Stat préfixe
        prefix_text = rune.get_prefix_stat_display()
        self.prefix_stat.setText(prefix_text if prefix_text else "")
        self.prefix_stat.setVisible(bool(prefix_text))

        # Sous-stats
        for i, label in enumerate(self.substat_labels):
            if i < len(rune.substats):
                substat = rune.substats[i]
                label.setText(f"{substat.stat_type}: +{substat.stat_value}")
                label.setVisible(True)
            else:
                label.setVisible(False)

        # Calcul et affichage de l'efficacité (à implémenter)
        efficiency = self.calculate_efficiency(rune)
        self.efficiency_label.setText(f"Efficacité: {efficiency:.1f}%")

    def calculate_efficiency(self, rune):
        # À implémenter : calcul de l'efficacité de la rune
        # Cela dépendra de vos règles métier spécifiques
        return 0.0

    def get_quality_color(self, quality):
        colors = {
            'normal': '#FFFFFF',
            'magic': '#00FF00',
            'rare': '#0000FF',
            'heroic': '#800080',
            'legendary': '#FFA500'
        }
        return colors.get(quality.lower(), '#FFFFFF')

    def return_to_list(self):
        if self.parent:
            self.parent.show_runes_list()
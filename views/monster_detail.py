import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QGridLayout, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QCursor

class RuneLabel(QLabel):
    def __init__(self, rune_number):
        super().__init__()
        self.base_pixmap = None
        self.overlay_pixmap = None
        self.rune_number = rune_number
        
        # Chargement de l'image de base de la rune
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        rune_path = os.path.join(project_root, "images", "runes", f"rune{rune_number}.png")
        
        if os.path.exists(rune_path):
            self.base_pixmap = QPixmap(rune_path)
            self.base_pixmap = self.base_pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, 
                                                      Qt.TransformationMode.SmoothTransformation)
            
        self.setFixedSize(60, 60)
        
        # Rendre le label cliquable
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setToolTip(f"Cliquez pour voir les détails de la rune {rune_number}")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.show_rune_details()

    def show_rune_details(self):
        # Pour plus tard - Afficher les détails de la rune
        print(f"Détails de la rune {self.rune_number}")
        # Ici vous pourrez implémenter l'affichage des détails

    def paintEvent(self, event):
        if self.base_pixmap:
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.base_pixmap)
            if self.overlay_pixmap:
                painter.drawPixmap(self.rect(), self.overlay_pixmap)
            painter.end()

class MonsterDetailView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)  # Réduire l'espacement entre les éléments

        # Bouton retour
        back_button = QPushButton("Retour à la liste")
        back_button.clicked.connect(self.return_to_list)
        main_layout.addWidget(back_button)

        # En-tête avec nom du monstre
        self.monster_name = QLabel()
        self.monster_name.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(self.monster_name)

        # Conteneur horizontal principal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)  # Espacement entre les sections

        # Section gauche (Stats + Skills)
        left_section = QVBoxLayout()
        left_section.setSpacing(10)
        
        # Stats
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.Shape.Box)
        stats_layout = QGridLayout(stats_frame)
        stats = [
            ("PV", "hp"), ("ATK", "attack"), ("DEF", "defense"),
            ("VIT", "speed"), ("Taux Critique", "crit_rate"),
            ("Dégâts Critiques", "crit_damage"), ("Résistance", "resistance"),
            ("Précision", "accuracy")
        ]
        for i, (label, attr) in enumerate(stats):
            stats_layout.addWidget(QLabel(label), i // 2, (i % 2) * 2)
            stats_layout.addWidget(QLabel(), i // 2, (i % 2) * 2 + 1)
        left_section.addWidget(stats_frame)

        # Skills
        skills_frame = QFrame()
        skills_frame.setFrameStyle(QFrame.Shape.Box)
        skills_layout = QVBoxLayout(skills_frame)
        skills_layout.addWidget(QLabel("Compétences"))
        for i in range(3):
            skill_label = QLabel(f"Compétence {i+1}")
            skills_layout.addWidget(skill_label)
        left_section.addWidget(skills_frame)

        # Section droite (Runes + Artéfacts)
        right_section = QVBoxLayout()
        right_section.setSpacing(10)
        
        # Runes en étoile
        runes_frame = QFrame()
        runes_layout = QGridLayout(runes_frame)
        runes_layout.setSpacing(0)  # Réduire l'espacement entre les runes au minimum
        
        # Positions des runes en étoile ajustées pour former une étoile plus compacte
        rune_positions = [
            (0, 2),    # Rune 1 (haut)
            (1, 4),    # Rune 2 (droite haut)
            (3, 4),    # Rune 3 (droite bas)
            (4, 2),    # Rune 4 (bas)
            (3, 0),    # Rune 5 (gauche bas)
            (1, 0)     # Rune 6 (gauche haut)
        ]

        # Création des labels pour les runes
        self.rune_labels = []
        for i, pos in enumerate(rune_positions):
            rune_label = RuneLabel(i + 1)
            self.rune_labels.append(rune_label)
            runes_layout.addWidget(rune_label, pos[0], pos[1])

        # Ajuster les marges du layout des runes
        runes_layout.setContentsMargins(-10, -10, -10, -10)

        # Optionnel : Ajouter des spacers invisibles plus petits
        for i in range(5):  # 5 lignes
            for j in range(5):  # 5 colonnes
                if not runes_layout.itemAtPosition(i, j):
                    spacer = QLabel()
                    spacer.setFixedSize(80, 80)  # Spacers encore plus petits
                    runes_layout.addWidget(spacer, i, j)

        right_section.addWidget(runes_frame)
        right_section.addStretch()

        # Artéfacts
        artifacts_frame = QFrame()
        artifacts_frame.setFrameStyle(QFrame.Shape.Box)
        artifacts_layout = QVBoxLayout(artifacts_frame)
        artifacts_layout.addWidget(QLabel("Artéfact de Type"))
        artifacts_layout.addWidget(QLabel("Artéfact d'Élément"))
        right_section.addWidget(artifacts_frame)

        # Ajout des sections au layout principal
        content_layout.addLayout(left_section, 1)
        content_layout.addLayout(right_section, 1)
        main_layout.addLayout(content_layout)

    def update_monster(self, monster):
        """Met à jour l'affichage avec les données du monstre"""
        self.monster_name.setText(f"{monster.name} {monster.stars_display}")

    def return_to_list(self):
        """Retourne à la liste des monstres"""
        self.main_window.show_monster_list()
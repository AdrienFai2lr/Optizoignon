from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QTabWidget, QGridLayout, QPushButton)
from PyQt6.QtCore import Qt

class MonsterDetailView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Référence à la fenêtre principale
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Bouton retour
        back_button = QPushButton("Retour à la liste")
        back_button.clicked.connect(self.return_to_list)
        layout.addWidget(back_button)

        # En-tête avec infos de base
        header_layout = QHBoxLayout()
        self.monster_name = QLabel()
        self.monster_name.setStyleSheet("font-size: 12px; font-weight: bold;")
        header_layout.addWidget(self.monster_name)
        layout.addLayout(header_layout)

        # Onglets pour différentes sections
        tabs = QTabWidget()
        tabs.addTab(self.create_stats_tab(), "Statistiques")
        tabs.addTab(self.create_runes_tab(), "Runes")
        tabs.addTab(self.create_artifacts_tab(), "Artéfacts")
        tabs.addTab(self.create_skills_tab(), "Compétences")
        #tabs.addTab(self.create_Opti_tab(), "Optimisation")
        layout.addWidget(tabs)

    def create_stats_tab(self):
        tab = QWidget()
        layout = QGridLayout()

        # Stats de base
        stats = [
            ("PV", "hp"), ("ATK", "attack"), ("DEF", "defense"),
            ("VIT", "speed"), ("Taux Critique", "crit_rate"),
            ("Dégâts Critiques", "crit_damage"), ("Résistance", "resistance"),
            ("Précision", "accuracy")
        ]

        for i, (label, attr) in enumerate(stats):
            layout.addWidget(QLabel(label), i // 2, (i % 2) * 2)
            layout.addWidget(QLabel(), i // 2, (i % 2) * 2 + 1)

        tab.setLayout(layout)
        return tab

    def create_runes_tab(self):
        tab = QWidget()
        layout = QGridLayout()

        # Emplacements de runes (1 à 6)
        for i in range(6):
            rune_widget = QLabel(f"Rune {i+1}")
            layout.addWidget(rune_widget, i // 2, i % 2)

        tab.setLayout(layout)
        return tab

    def create_artifacts_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Artéfacts (Type et Élément)
        layout.addWidget(QLabel("Artéfact de Type"))
        layout.addWidget(QLabel("Artéfact d'Élément"))

        tab.setLayout(layout)
        return tab

    def create_skills_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Compétences
        for i in range(3):
            skill_widget = QLabel(f"Compétence {i+1}")
            layout.addWidget(skill_widget)

        tab.setLayout(layout)
        return tab

    def update_monster(self, monster):
        """Met à jour l'affichage avec les données du monstre"""
        self.monster_name.setText(f"{monster.name} {monster.stars_display}")
        # Mettre à jour les autres informations...

    def return_to_list(self):
        """Retourne à la liste des monstres"""
        self.main_window.show_monster_list()
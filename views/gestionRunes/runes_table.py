# runes_table.py
from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, 
                            QScrollArea, QSizePolicy, QPushButton, QHBoxLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from .rune_card import RuneCard

class RuneGrid(QScrollArea):
    page_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.rune_images_dir = "images/runes/"
        self.current_page = 1
        self.total_pages = 1
        self.load_stylesheet()
        self.setup_ui()
        
    def load_stylesheet(self):
        """Charge le fichier de style QSS"""
        try:
            with open('styles/styles.qss', 'r') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Erreur lors du chargement du style: {e}")
    
    def setup_ui(self):
        """Configuration initiale de l'interface utilisateur"""
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Container pour la grille de runes
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        
        self.setup_pagination()
        
        self.main_layout.addWidget(self.grid_container)
        self.main_layout.addWidget(self.pagination_widget)
        
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        
    def setup_pagination(self):
        """Configuration des contrôles de pagination"""
        self.pagination_widget = QWidget()
        self.pagination_layout = QHBoxLayout(self.pagination_widget)
        
        self.prev_button = QPushButton("←")
        self.prev_button.setFixedSize(40, 40)
        self.prev_button.clicked.connect(self.goto_previous_page)  # Changé ici
        
        self.page_label = QLabel("Page 1")
        self.page_label.setFixedWidth(100)
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.next_button = QPushButton("→")
        self.next_button.setFixedSize(40, 40)
        self.next_button.clicked.connect(self.goto_next_page)  # Changé ici
        
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.next_button)
        self.pagination_layout.addStretch()
        
        self.pagination_widget.setLayout(self.pagination_layout)

    def update_runes(self, runes, current_page=1, total_pages=1):
        """Mise à jour de l'affichage des runes"""
        self.current_page = current_page
        self.total_pages = total_pages
        
        # Mise à jour du label de pagination
        self.page_label.setText(f"Page {current_page}/{total_pages}")
        
        # Activation/désactivation des boutons de pagination
        self.prev_button.setEnabled(current_page > 1)
        self.next_button.setEnabled(current_page < total_pages)
        
        # Nettoyage de la grille existante
        for i in reversed(range(self.grid_layout.count())): 
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Ajout des nouvelles runes
        cols = 5
        for i, rune in enumerate(runes):
            row = i // cols
            col = i % cols
            card = RuneCard(rune, self.rune_images_dir)
            self.grid_layout.addWidget(card, row, col)

    def goto_previous_page(self):  # Nouvelle méthode
        """Gestion du clic sur le bouton précédent"""
        if self.current_page > 1:
            self.current_page -= 1
            self.page_changed.emit(self.current_page)
            
    def goto_next_page(self):  # Nouvelle méthode
        """Gestion du clic sur le bouton suivant"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.page_changed.emit(self.current_page)
            
    def get_rune(self, index):
        """Récupère une rune à partir de son index dans la grille"""
        if 0 <= index < self.grid_layout.count():
            item = self.grid_layout.itemAt(index)
            if item and item.widget():
                return item.widget().rune
        return None
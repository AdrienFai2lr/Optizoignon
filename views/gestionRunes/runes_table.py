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
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration initiale de l'interface utilisateur"""
        # Widget principal
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # Container pour la grille de runes
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(5)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)
        
        # Contrôles de pagination
        self.setup_pagination()
        
        # Assemblage final
        self.main_layout.addWidget(self.grid_container)
        self.main_layout.addWidget(self.pagination_widget)
        
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        
        self.apply_styles()
        
    def setup_pagination(self):
        """Configuration des contrôles de pagination"""
        self.pagination_widget = QWidget()
        self.pagination_layout = QHBoxLayout(self.pagination_widget)
        
        # Bouton précédent
        self.prev_button = QPushButton("< Précédent")
        self.prev_button.clicked.connect(self.previous_page)
        
        # Label de page
        self.page_label = QLabel("Page 1")
        
        # Bouton suivant
        self.next_button = QPushButton("Suivant >")
        self.next_button.clicked.connect(self.next_page)
        
        # Ajout des widgets au layout
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.next_button)
        self.pagination_layout.addStretch()
        
    def apply_styles(self):
        """Application des styles CSS"""
        self.setStyleSheet("""
            QScrollArea {
                background-color: #1e1e1e;
                border: none;
            }
            QWidget {
                background-color: #1e1e1e;
            }
            QPushButton {
                background-color: #333333;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:disabled {
                background-color: #222222;
                color: #666666;
            }
            QLabel {
                color: white;
            }
        """)
        
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
            
    def previous_page(self):
        """Gestion du clic sur le bouton précédent"""
        if self.current_page > 1:
            self.current_page -= 1
            self.page_changed.emit(self.current_page)
            
    def next_page(self):
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
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
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # Container pour la grille de runes
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(12)
        self.grid_layout.setContentsMargins(12, 12, 12, 12)
        
        # Contrôles de pagination
        self.pagination_widget = QWidget()
        self.pagination_layout = QHBoxLayout(self.pagination_widget)
        
        self.prev_button = QPushButton("< Précédent")
        self.prev_button.clicked.connect(self.previous_page)
        
        self.page_label = QLabel("Page 1")
        
        self.next_button = QPushButton("Suivant >")
        self.next_button.clicked.connect(self.next_page)
        
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.next_button)
        self.pagination_layout.addStretch()
        
        # Assemblage final
        self.main_layout.addWidget(self.grid_container)
        self.main_layout.addWidget(self.pagination_widget)
        
        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
        
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
        self.current_page = current_page
        self.total_pages = total_pages
        
        self.page_label.setText(f"Page {current_page}/{total_pages}")
        
        self.prev_button.setEnabled(current_page > 1)
        self.next_button.setEnabled(current_page < total_pages)
        
        # Nettoyage de la grille existante
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        # Ajout des nouvelles runes
        cols = 5
        for i, rune in enumerate(runes):
            row = i // cols
            col = i % cols
            card = RuneCard(rune, self.rune_images_dir)
            self.grid_layout.addWidget(card, row, col)
            
    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.page_changed.emit(self.current_page)
            
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.page_changed.emit(self.current_page)
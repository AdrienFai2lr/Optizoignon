from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QComboBox, QLabel,
                           QStackedWidget)
from .monster_detail import MonsterDetailView
from .monster_table import MonsterTable  # Import corrigé ici
from controllers.monster_controller import MonsterController, DatabaseError

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.monster_controller = MonsterController()
        self.setWindowTitle("OPTIZ-oignoin - Gestion de monstres")
        self.setMinimumSize(1200, 800)
        self.init_ui()
        self.load_monsters()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Gestionnaire de pages
        self.stacked_widget = QStackedWidget()
        
        # Page liste des monstres
        self.list_page = QWidget()
        self.setup_list_page()
        self.stacked_widget.addWidget(self.list_page)
        
        # Page détail d'un monstre
        self.detail_view = MonsterDetailView(self)  # Passer self comme référence à la MainWindow
        self.stacked_widget.addWidget(self.detail_view)
        
        self.main_layout.addWidget(self.stacked_widget)

    def setup_list_page(self):
        layout = QVBoxLayout(self.list_page)

        # Barre d'outils supérieure
        toolbar = QHBoxLayout()
        
        # Filtres
        filter_group = QHBoxLayout()
        
        # Filtre attribut
        self.filter_attribute = QComboBox()
        self.filter_attribute.addItems(["Tous", "Eau", "Feu", "Vent", "Lumière", "Ténèbres"])
        self.filter_attribute.currentTextChanged.connect(self.apply_filters)
        filter_group.addWidget(QLabel("Attribut:"))
        filter_group.addWidget(self.filter_attribute)
        
        # Filtre classe
        self.filter_class = QComboBox()
        self.filter_class.addItems(["Toutes", "4★", "5★"])
        self.filter_class.currentTextChanged.connect(self.apply_filters)
        filter_group.addWidget(QLabel("Classe:"))
        filter_group.addWidget(self.filter_class)
        
        toolbar.addLayout(filter_group)
        toolbar.addStretch()
        
        # Bouton thème
        self.theme_button = QPushButton("Thème Sombre")
        self.theme_button.clicked.connect(self.toggle_theme)
        toolbar.addWidget(self.theme_button)
        
        layout.addLayout(toolbar)
        
        # Table des monstres
        self.monster_table = MonsterTable()
        self.monster_table.cellDoubleClicked.connect(self.show_monster_detail)
        layout.addWidget(self.monster_table)
        
        # Barre d'état
        self.statusBar().showMessage("Chargement des données...")

    def load_monsters(self):
        try:
            monsters = self.monster_controller.get_monsters()
            self.monster_table.update_monsters(monsters)
            self.statusBar().showMessage(f"{len(monsters)} monstres chargés")
        except DatabaseError as err:
            self.statusBar().showMessage(str(err))

    def apply_filters(self):
        try:
            element_filter = self.filter_attribute.currentText()
            stars_filter = self.filter_class.currentText()
            
            monsters = self.monster_controller.get_monsters(
                element_filter=element_filter,
                stars_filter=stars_filter
            )
            
            self.monster_table.update_monsters(monsters)
            self.statusBar().showMessage(f"{len(monsters)} monstres affichés")
        except DatabaseError as err:
            self.statusBar().showMessage(str(err))

    def show_monster_detail(self, row, column):
        monster = self.monster_table.get_monster(row)
        self.detail_view.update_monster(monster)
        self.stacked_widget.setCurrentWidget(self.detail_view)

    def show_monster_list(self):
        self.stacked_widget.setCurrentWidget(self.list_page)

    def toggle_theme(self):
        if self.theme_button.text() == "Thème Sombre":
            self.theme_button.setText("Thème Clair")
        else:
            self.theme_button.setText("Thème Sombre")
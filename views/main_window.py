from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QComboBox, QLabel,
                           QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from .gestionMonstres.monster_detail import MonsterDetailView
from .gestionMonstres.monster_table import MonsterTable
from .gestionRunes.runes_table import RuneGrid
from controllers.runes_controller import RuneController
from controllers.monster_controller import MonsterController, DatabaseError
from .gestionJson.dropJson import DropZoneWidget
from PyQt6.QtWidgets import QGridLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.monster_controller = MonsterController()
        self.rune_controller = RuneController()
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
        
        # Page d'accueil
        self.home_page = QWidget()
        self.setup_home_page()
        self.stacked_widget.addWidget(self.home_page)
        
        # Page liste des monstres
        self.list_page = QWidget()
        self.setup_list_page()
        self.stacked_widget.addWidget(self.list_page)
        
        # Page détail d'un monstre
        self.detail_view = MonsterDetailView(self)
        self.stacked_widget.addWidget(self.detail_view)
        
        self.main_layout.addWidget(self.stacked_widget)

        # Page liste des runes
        self.runes_page = QWidget()
        self.setup_runes_page()
        self.stacked_widget.addWidget(self.runes_page)
        
        self.main_layout.addWidget(self.stacked_widget)
        
        # Définir la page d'accueil comme page par défaut
        self.stacked_widget.setCurrentWidget(self.home_page)

    def setup_runes_page(self):
        layout = QVBoxLayout(self.runes_page)

        # Barre d'outils supérieure
        toolbar = QHBoxLayout()
        
        # Bouton retour vers l'accueil
        back_button = QPushButton("Retour à l'accueil")
        back_button.clicked.connect(self.show_home_page)
        toolbar.addWidget(back_button)
        
        # Filtres
        filter_group = QHBoxLayout()
        
        # Filtre set de runes
        self.filter_rune_set = QComboBox()
        sets = ["Tous"] + list(self.rune_controller.rune_sets.values())
        self.filter_rune_set.addItems(sets)
        self.filter_rune_set.currentTextChanged.connect(self.apply_rune_filters)
        filter_group.addWidget(QLabel("Set:"))
        filter_group.addWidget(self.filter_rune_set)
        
        # Filtre slot
        self.filter_slot = QComboBox()
        self.filter_slot.addItems(["Tous"] + [str(i) for i in range(1, 7)])
        self.filter_slot.currentTextChanged.connect(self.apply_rune_filters)
        filter_group.addWidget(QLabel("Slot:"))
        filter_group.addWidget(self.filter_slot)
        
        toolbar.addLayout(filter_group)
        toolbar.addStretch()
        
        # Bouton thème
        theme_button = QPushButton("Thème Sombre")
        theme_button.clicked.connect(self.toggle_theme)
        toolbar.addWidget(theme_button)
        
        layout.addLayout(toolbar)
        
        # Table des runes
        self.rune_table = RuneGrid()
        self.rune_table.page_changed.connect(self.on_rune_page_changed)
        layout.addWidget(self.rune_table)
        
        # Barre d'état
        self.statusBar().showMessage("Chargement des runes...")

    def on_rune_page_changed(self, page):
        try:
            set_filter = self.filter_rune_set.currentText()
            slot_filter = self.filter_slot.currentText()
            
            runes, total_count = self.rune_controller.get_runes(
                set_filter=set_filter if set_filter != "Tous" else None,
                slot_filter=slot_filter if slot_filter != "Tous" else None,
                page=page
            )
            
            total_pages = (total_count + 49) // 50  # 50 runes par page
            self.rune_table.update_runes(runes, page, total_pages)
            self.statusBar().showMessage(f"Page {page}/{total_pages} ({len(runes)} runes)")
        except Exception as err:
            self.statusBar().showMessage(f"Erreur lors du chargement de la page : {str(err)}")

    def load_runes(self, page=1):
        try:
            set_filter = self.filter_rune_set.currentText()
            slot_filter = self.filter_slot.currentText()
            
            runes, total_count = self.rune_controller.get_runes(
                set_filter=set_filter if set_filter != "Tous" else None,
                slot_filter=slot_filter if slot_filter != "Tous" else None,
                page=page
            )
            
            total_pages = (total_count + 49) // 50  # 50 runes par page
            self.rune_table.update_runes(runes, page, total_pages)
            self.statusBar().showMessage(f"Page {page}/{total_pages} ({len(runes)} runes)")
        except Exception as err:
            self.statusBar().showMessage(f"Erreur lors du chargement des runes : {str(err)}")

    def apply_rune_filters(self):
        self.load_runes(page=1)  # Retour à la première page lors du filtrage

    def show_rune_detail(self, row, column):
        """Affiche les détails d'une rune"""
        rune = self.rune_table.get_rune(row)
        if rune:
            # Pour l'instant, on affiche juste un message dans la barre d'état
            self.statusBar().showMessage(f"Détails de la rune {rune.id} (à implémenter)")
            # Plus tard, vous pourrez créer une vue détaillée comme pour les monstres
            # self.rune_detail_view.update_rune(rune)
            # self.stacked_widget.setCurrentWidget(self.rune_detail_view)

    def handle_json_import(self, data):
        """Gère l'importation des données JSON"""
        try:
            if not isinstance(data, dict):
                raise ValueError("Le format des données n'est pas valide")
            
            required_fields = ['monsters', 'runes', 'artifacts']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Champ requis manquant: {field}")
            
            self.monster_controller.import_data(data)
            self.load_monsters()
            self.statusBar().showMessage("Données importées avec succès", 5000)
            
        except ValueError as e:
            self.statusBar().showMessage(f"Erreur de format: {str(e)}", 5000)
        except DatabaseError as e:
            self.statusBar().showMessage(f"Erreur de base de données: {str(e)}", 5000)
        except Exception as e:
            self.statusBar().showMessage(f"Erreur inattendue: {str(e)}", 5000)
            print(f"Erreur détaillée: {str(e)}")

    def setup_home_page(self):
        layout = QVBoxLayout(self.home_page)
        
        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("images/logo_optizoignon.png")
        scaled_logo = logo_pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Conteneur principal
        main_container = QWidget()
        grid_layout = QGridLayout(main_container)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # DropZone
        self.drop_zone = DropZoneWidget(self)
        self.drop_zone.setFixedSize(400, 200)
        self.drop_zone.json_imported.connect(self.handle_json_import)
        grid_layout.addWidget(self.drop_zone, 0, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Boutons
        buttons_container = QWidget()
        buttons_layout = QVBoxLayout(buttons_container)
        button_style = """
        QPushButton {
            font-size: 18px;
            padding: 10px 20px;
            min-width: 200px;
            color: white;
            background-color: #333333;
        }
        """
        buttons = [
            ("Liste des Monstres", self.show_monster_list),
            ("Gestion des runes", self.show_runes_list),
            ("Gestion des artéfacts", self.show_monster_list),
            ("Optimisation des teams", self.show_monster_list)
        ]
        
        for text, callback in buttons:
            button = QPushButton(text)
            button.clicked.connect(callback)
            button.setStyleSheet(button_style)
            buttons_layout.addWidget(button)
        
        grid_layout.addWidget(buttons_container, 1, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Assemblage final
        layout.addStretch(1)
        layout.addWidget(logo_label)
        layout.addWidget(main_container)
        layout.addStretch(2)

    def setup_list_page(self):
        layout = QVBoxLayout(self.list_page)

        # Barre d'outils supérieure
        toolbar = QHBoxLayout()
        
        # Bouton retour vers l'accueil
        back_button = QPushButton("Retour à l'accueil")
        back_button.clicked.connect(self.show_home_page)
        toolbar.addWidget(back_button)
        
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
        self.filter_class.addItems(["Toutes","1★","2★", "3★","4★", "5★"])
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
    
    def show_runes_list(self):
        """Affiche la page de liste des runes"""
        self.load_runes()  # Charge les runes au moment d'afficher la page
        self.stacked_widget.setCurrentWidget(self.runes_page)

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def toggle_theme(self):
        if self.theme_button.text() == "Thème Sombre":
            self.theme_button.setText("Thème Clair")
        else:
            self.theme_button.setText("Thème Sombre")
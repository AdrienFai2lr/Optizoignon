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
        self.cached_images = {}  # Cache d'images pour éviter les rechargements
        # Réduire les appels de style
        self.setup_ui()
        
    def setup_ui(self):
        # Réduire les marges et utiliser une mise en page plus légère
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(220, 280)
        self.setMaximumSize(250, 320)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        #debut de la gamification des runes comme des carte etc
        self.create_efficiency_section(self.main_layout)
        self.create_header()
        self.create_stats_section()
               
        # Désactiver l'interaction pour améliorer les performances
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        
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
        
        # Optimisation du chargement d'images
        set_name = self.rune.get_set_name().lower()
        image_path = os.path.join(self.rune_images_dir, f"{set_name}.png")
        if os.path.exists(image_path):
            rune_image = QLabel()
            # Utiliser le cache d'images si possible
            if set_name in self.cached_images:
                scaled_pixmap = self.cached_images[set_name]
            else:
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(50, 50,
                                            Qt.AspectRatioMode.KeepAspectRatio,
                                            Qt.TransformationMode.FastTransformation) # Utiliser FastTransformation
                self.cached_images[set_name] = scaled_pixmap
            rune_image.setPixmap(scaled_pixmap)
            image_layout.addWidget(rune_image, alignment=Qt.AlignmentFlag.AlignCenter)
        
        header_layout.addWidget(image_container)

        #on va ajoute ici l'effi de la rune + les autres ajout
        
        # Informations de base
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)
        
        # Slot, niveau et indicateur ancien
        slot_text = f"Slot {self.rune.slot_no} | +{self.rune.level}"
        slot_level = QLabel(slot_text)
        slot_level.setProperty("class", "slot-level")
        info_layout.addWidget(slot_level)
        
        #si la rune est anciennce on met l'image
        if self.rune.is_ancient:
            ancient_icon = QLabel()
            ancient_pixmap = QPixmap("images/runes/ancient.png")
            # Vérifiez que le pixmap a bien été chargé
            if ancient_pixmap.isNull():
                print("Erreur: Impossible de charger l'image 'images/runes/ancient.png'")
            else:
                # Utilisez Qt.KeepAspectRatio pour PyQt6
                scaled_pixmap = ancient_pixmap.scaled(15, 15, Qt.AspectRatioMode.KeepAspectRatio)
                ancient_icon.setPixmap(scaled_pixmap)
            info_layout.addWidget(ancient_icon)
        
        # Qualité de la rune
        quality = QLabel(self.rune.quality.capitalize())
        quality.setProperty("class", f"quality-{self.rune.quality.lower()}")
        info_layout.addWidget(quality)
        
        header_layout.addWidget(info_container)
        
        # Ajout de l'image du monstre si la rune est équipée
        if hasattr(self.rune, 'monster_info') and self.rune.monster_info:
            monster_container = QFrame()
            monster_container.setObjectName("monsterContainer")
            monster_layout = QVBoxLayout(monster_container)
            monster_layout.setContentsMargins(8, 8, 8, 8)
            monster_layout.setSpacing(5)
            
            # Créer le label pour l'image du monstre
            monster_image = QLabel()
            monster_image_path = os.path.join("images/monsters", f"{self.rune.monster_info['image_filename']}")
            
            # Vérifier si l'image existe
            if os.path.exists(monster_image_path):
                # Clé pour le cache d'images basée sur le chemin du fichier
                cache_key = f"monster_{self.rune.monster_info['com2us_id']}"
                
                # Utiliser le cache si disponible
                if hasattr(self, 'cached_monster_images') and cache_key in self.cached_monster_images:
                    scaled_monster_pixmap = self.cached_monster_images[cache_key]
                else:
                    monster_pixmap = QPixmap(monster_image_path)
                    scaled_monster_pixmap = monster_pixmap.scaled(40, 40,
                                                                Qt.AspectRatioMode.KeepAspectRatio,
                                                                Qt.TransformationMode.FastTransformation)
                    
                    # Initialiser le dictionnaire de cache si nécessaire
                    if not hasattr(self, 'cached_monster_images'):
                        self.cached_monster_images = {}
                        
                    self.cached_monster_images[cache_key] = scaled_monster_pixmap
                
                monster_image.setPixmap(scaled_monster_pixmap)
                monster_layout.addWidget(monster_image, alignment=Qt.AlignmentFlag.AlignCenter)
                
                header_layout.addWidget(monster_container)
        self.main_layout.addWidget(header)
        
    def create_stats_section(self):
        stats_container = QFrame()
        stats_container.setProperty("class", "stats-container")
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.setContentsMargins(10, 15, 10, 10)
        stats_layout.setSpacing(10)
        
        # Stat principale
        main_stat = QLabel(self.rune.get_main_stat_display())
        main_stat.setProperty("class", "main-stat")
        main_stat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(main_stat)
        
        # Préfixe si elle existe alors on l'affiche sinon on ne fait rien ici
        if self.rune.prefix_stat_type != "UNKNOWN":
            prefix_text = self.rune.get_prefix_stat_display()
            prefix_label = QLabel(prefix_text)
            prefix_label.setProperty("class", "prefix")
            stats_layout.addWidget(prefix_label)
        
        # Sous-stats avec grind et gemmes
        if self.rune.substats:
            for substat in self.rune.substats:
                substat_widget = QWidget()
                substat_layout = QHBoxLayout(substat_widget)
                substat_layout.setContentsMargins(0, 0, 0, 0)
                #print(self.rune.substats)
                # Ajouter l'icône si la stat est gemmée
                if substat['is_gemmed']:
                    gemmed_icon = QLabel()
                    gemmed_pixmap = QPixmap("images/runes/enchanted.png")
                    # Vérifier que le pixmap a bien été chargé
                    if gemmed_pixmap.isNull():
                        print("Erreur: Impossible de charger l'image 'images/runes/enchanted.png'")
                    else:
                        # Utilisez Qt.KeepAspectRatio pour PyQt6
                        scaled_pixmap = gemmed_pixmap.scaled(15, 15, Qt.AspectRatioMode.KeepAspectRatio)
                        gemmed_icon.setPixmap(scaled_pixmap)
                        substat_layout.addWidget(gemmed_icon)
                substat_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                
                # Création de la partie de base de la sous-stat
                stat_base_text = f"{substat['type']}: {substat['value']}"
                
                # Si la sous-stat a une valeur de grind, on crée un layout horizontal pour contenir les deux labels
                if substat['grind_value'] > 0:
                    # Créer le label pour la valeur de base
                    base_label = QLabel(stat_base_text)
                    if substat['is_gemmed']:
                        base_label.setProperty("class", "substat gemmed")
                        tooltip = f"Gemmé (ancienne stat: {substat['original_type']})"
                        base_label.setToolTip(tooltip)
                    else:
                        base_label.setProperty("class", "substat")
                    
                    substat_layout.addWidget(base_label)
                    
                    # Créer le label pour la valeur de grind
                    grind_label = QLabel(f" (+{substat['grind_value']})")
                    grind_label.setProperty("class", "substat grind")
                    substat_layout.addWidget(grind_label)
                else:
                    # Pas de grind, on utilise simplement un seul label
                    substat_label = QLabel(stat_base_text)
                    if substat['is_gemmed']:
                        substat_label.setProperty("class", "substat gemmed")
                        tooltip = f"Gemmé (ancienne stat: {substat['original_type']})"
                        substat_label.setToolTip(tooltip)
                    else:
                        substat_label.setProperty("class", "substat")
                    
                    substat_layout.addWidget(substat_label)
                    
                    # Ajouter une croix pour les stats non-grindables
                    if not self.is_grindable_stat(substat['type']):
                        cross_label = QLabel("✗")  # Symbole de
                        cross_label.setProperty("class", "substat grind")
                        cross_label.setToolTip("Cette statistique ne peut pas être grindée")
                        substat_layout.addWidget(cross_label)
                
                # Ajouter le widget de sous-stat au conteneur de stats
                stats_layout.addWidget(substat_widget)
        
        self.main_layout.addWidget(stats_container)
    
    def is_grindable_stat(self, stat_type):
        """Vérifie si un type de statistique peut être grindé"""
        # Liste des stats qui ne peuvent pas être grindées
        non_grindable = [
            "TC%", "DC%", "RESIS%", "PRECI%", 
            "Taux Critique", "Dégâts Critiques", "Résistance", "Précision"
        ]
        result = stat_type not in non_grindable
        return result  
    
    def create_efficiency_section(self, stats_layout):
        """Crée une section dédiée à l'efficacité"""
        eff_value = self.rune.get_eff() if hasattr(self, 'rune') else self.get_eff()

        if eff_value is not None and eff_value != "Null":
            eff_section = QFrame()
            eff_layout = QVBoxLayout(eff_section)
            eff_layout.setContentsMargins(10, 5, 10, 5)
            eff_layout.setSpacing(5)

            # Création du QLabel
            eff_label = QLabel(f"Eff: {eff_value}")
            eff_label.setProperty("class", "efficiency-stat")  # Classe par défaut

            # Appliquer un style selon l'efficacité
            if isinstance(eff_value, (int, float)):
                if eff_value < 50:
                    eff_label.setProperty("class", "eff-low")
                elif eff_value < 75:
                    eff_label.setProperty("class", "eff-medium")
                else:
                    eff_label.setProperty("class", "eff-high")

            eff_layout.addWidget(eff_label)
            stats_layout.addWidget(eff_section)

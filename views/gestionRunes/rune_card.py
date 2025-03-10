from PyQt6.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, QGridLayout,
                             QSizePolicy, QPushButton, QHBoxLayout, QToolTip)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt
import os

class RuneCard(QFrame):
    def __init__(self, rune, rune_images_dir):
        super().__init__()
        self.rune = rune
        self.rune_images_dir = rune_images_dir
        self.cached_images = {}  # Cache d'images pour éviter les rechargements
        self.showing_replacement_indicators = False  # Attribut pour suivre l'état
        self.worst_stat_indicator = None  # Pour stocker la référence à l'indicateur
        self.setup_ui()
        
    def setup_ui(self):
        # Configuration de base
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(280, 320)  
        self.setMaximumSize(320, 400)  
        
        # Layout principal pour tout le contenu
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        
        # Obtenir la valeur d'efficacité de la rune
        eff_value = self.rune.get_eff()
        if eff_value is not None and eff_value != "Null":
            eff_class = self._get_efficiency_class(eff_value)
            self.setProperty("eff-class", eff_class)
            
            # Créer un layout pour le badge d'efficacité
            eff_container = QFrame()
            eff_container.setObjectName("efficiencyContainer")
            eff_layout = QHBoxLayout(eff_container)
            eff_layout.setContentsMargins(0, 0, 0, 0)
            eff_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            
            # Créer le badge d'efficacité actuelle
            eff_badge = QLabel(f"{float(eff_value):.2f}")
            eff_badge.setObjectName("efficiencyBadge")
            eff_badge.setProperty("eff-class", eff_class)
            eff_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Ajouter le badge d'efficacité actuelle
            eff_layout.addWidget(eff_badge)
            
            # Ajouter le bouton œil uniquement si la rune est de niveau 12+
            if hasattr(self.rune, 'level') and isinstance(self.rune.level, (int, float)) and self.rune.level >= 12:
                # Ajouter le badge d'efficacité maximale avec function d'œil
                eff_value_max = self.rune.get_eff_max()
                eff_max_button = QPushButton(f"{float(eff_value_max):.2f}")
                eff_max_button.setObjectName("efficiencyMaxButton")
                
                # Configuration du bouton pour ressembler à un badge mais être cliquable
                eff_max_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                eff_max_button.setStyleSheet("font-size: 12px; padding: 2px 5px;")
                
                # Connecter le bouton au toggle
                eff_max_button.clicked.connect(self.toggle_stat_replacement_info)
                
                # Ajouter le bouton d'efficacité max au conteneur
                eff_layout.addWidget(eff_max_button)
            else:
                # Pour les runes de niveau <12, ajouter simplement le label standard
                eff_value_max = self.rune.get_eff_max()
                eff_max_badge = QLabel(f"{float(eff_value_max):.2f}")
                eff_max_badge.setObjectName("efficiencyMaxBadge")
                eff_layout.addWidget(eff_max_badge)
            
            # Ajouter le conteneur au layout principal
            self.main_layout.addWidget(eff_container)
            
            # Appliquer les styles
            self.style().unpolish(eff_badge)
            self.style().polish(eff_badge)
        
        # Appliquer les changements de style à la carte
        self.style().unpolish(self)
        self.style().polish(self)
        
        # Créer les sections de la carte
        self.create_header()
        self.create_stats_section()
        
        # Ne pas désactiver l'interaction pour permettre le clic sur le bouton efficacité max si niveau >=12
        if hasattr(self.rune, 'level') and isinstance(self.rune.level, (int, float)) and self.rune.level >= 12:
            # Ne pas désactiver l'interaction pour permettre le clic
            pass
        else:
            # Désactiver l'interaction pour les runes de niveau <12
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
    
    def toggle_stat_replacement_info(self):
        """Alterne l'affichage des informations de remplacement de stats théoriques"""
        if self.showing_replacement_indicators:
            self.hide_replacement_indicators()
            # Cacher le tooltip quand on désactive
            QToolTip.hideText()
        else:
            self.show_stat_replacement_info()
    
    def show_stat_replacement_info(self):
        """Affiche les informations de remplacement de stats théoriques"""
        # Créer le texte d'info à afficher
        info_text = "Remplacements théoriques:\n\n"
        
        # Obtenir les informations de remplacement et la pire stat
        replacement_type = ""
        worst_stat_idx = ""
        
        try:
            replacement_type = self.rune.get_remplacement_stats()
        except Exception as e:
            print(f"Erreur lors de l'accès à get_remplacement_stats: {e}")
        
        try:
            worst_stat_idx = self.rune.get_worst_stat_number()
            
            # Vérifier que l'index est dans la plage valide (1-4)
            if isinstance(worst_stat_idx, str):
                try:
                    worst_stat_num = int(worst_stat_idx)
                    if worst_stat_num < 1 or worst_stat_num > 4:
                        print(f"Index hors plage: {worst_stat_num}")
                        # Garder la valeur originale pour l'affichage
                    else:
                        # Convertir en entier si dans la plage correcte
                        worst_stat_idx = worst_stat_num
                except ValueError:
                    # Si ce n'est pas un nombre, garder la chaîne
                    pass
        except Exception as e:
            print(f"Erreur lors de l'accès à get_worst_stat_number: {e}")
        
        # Ajouter les informations au texte
        if replacement_type:
            info_text += f"Type de remplacement recommandé: {replacement_type}\n\n"
        
        if worst_stat_idx:
            # Si c'est un nombre entre 1 et 4, afficher normalement
            if isinstance(worst_stat_idx, int) and 1 <= worst_stat_idx <= 4:
                info_text += f"Stat à remplacer: #{worst_stat_idx}"
            # Sinon, afficher la valeur reçue
            else:
                info_text += f"Stat à remplacer: {worst_stat_idx}"
        
        # Afficher l'info en tooltip près du curseur
        QToolTip.showText(QCursor.pos(), info_text, self)
        
        # Mettre à jour l'état pour indiquer que les indicateurs sont affichés
        self.showing_replacement_indicators = True
        
        # Rafraîchir la section des stats pour afficher les indicateurs
        self.refresh_stats_section()
    
    def hide_replacement_indicators(self):
        """Cache les indicateurs de remplacement de stats"""
        # Mettre à jour l'état pour indiquer que les indicateurs sont masqués
        self.showing_replacement_indicators = False
        
        # Rafraîchir la section des stats pour masquer les indicateurs
        self.refresh_stats_section()
    
    def refresh_stats_section(self):
        """Actualise la section des stats pour refléter l'état actuel des indicateurs"""
        # Supprimer l'ancienne section
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i).widget()
            if item and item.property("class") == "stats-container":
                item.deleteLater()
        
        # Recréer la section avec l'état actuel
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
                                            Qt.TransformationMode.FastTransformation)
                self.cached_images[set_name] = scaled_pixmap
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
        slot_level = QLabel(slot_text)
        slot_level.setProperty("class", "slot-level")
        info_layout.addWidget(slot_level)
        
        # Si la rune est ancienne
        if self.rune.is_ancient:
            ancient_icon = QLabel()
            ancient_pixmap = QPixmap("images/runes/ancient.png")
            if not ancient_pixmap.isNull():
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
                    scaled_monster_pixmap = monster_pixmap.scaled(25, 25,
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
        stats_layout.setContentsMargins(8, 12, 8, 8)
        stats_layout.setSpacing(10)  # Augmenté l'espacement entre les éléments
        
        # Stat principale
        main_stat = QLabel(self.rune.get_main_stat_display())
        main_stat.setProperty("class", "main-stat")
        main_stat.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(main_stat)
        
        # Préfixe si elle existe
        if self.rune.prefix_stat_type and self.rune.prefix_stat_type != "UNKNOWN":
            prefix_text = self.rune.get_prefix_stat_display()
            prefix_label = QLabel(prefix_text)
            prefix_label.setProperty("class", "prefix")
            stats_layout.addWidget(prefix_label)
        
        # Section des sous-stats en utilisant un QGridLayout
        substats_widget = QWidget()
        substats_layout = QGridLayout(substats_widget)
        substats_layout.setContentsMargins(0, 0, 0, 0)
        substats_layout.setHorizontalSpacing(10)  # Espacement horizontal important
        substats_layout.setVerticalSpacing(8)     # Espacement vertical entre les lignes
        
        # Définir les entêtes de colonnes (invisibles mais utiles pour le layout)
        # Colonne 0: Icônes (gemme/pire stat)
        # Colonne 1: Type de stat
        # Colonne 2: Valeur de base
        # Colonne 3: Valeur de grind
        
        # Obtenir l'index de la pire stat (si disponible et si mode d'affichage activé)
        worst_stat_idx = None
        if self.showing_replacement_indicators:
            try:
                if hasattr(self.rune, 'level') and isinstance(self.rune.level, (int, float)) and self.rune.level >= 12:
                    worst_stat_idx = self.rune.get_worst_stat_number()
                    
                    if isinstance(worst_stat_idx, str):
                        try:
                            worst_stat_num = int(worst_stat_idx)
                            if 1 <= worst_stat_num <= 4:
                                worst_stat_idx = worst_stat_num
                            else:
                                worst_stat_idx = None
                        except ValueError:
                            worst_stat_idx = None
            except Exception as e:
                print(f"Erreur: {e}")
                worst_stat_idx = None
        
        # Sous-stats avec grind et gemmes
        if self.rune.substats:
            for i, substat in enumerate(self.rune.substats, 1):
                row = i - 1  # Index de ligne dans le grid
                col = 0      # Commence à la colonne 0
                
                # Vérifier si c'est la pire stat
                is_worst_stat = False
                if self.showing_replacement_indicators and worst_stat_idx is not None:
                    if worst_stat_idx == i:
                        is_worst_stat = True
                
                # 1. Colonne pour les icônes
                icon_widget = QWidget()
                icon_layout = QHBoxLayout(icon_widget)
                icon_layout.setContentsMargins(0, 0, 0, 0)
                icon_layout.setSpacing(2)
                
                # Icône d'avertissement pour la pire stat
                if is_worst_stat:
                    worst_icon = QLabel("➡️")
                    worst_icon.setProperty("class", "worst-stat-icon")
                    worst_icon.setToolTip("Statistique recommandée à remplacer")
                    icon_layout.addWidget(worst_icon)
                    self.worst_stat_indicator = worst_icon
                
                # Icône de gemme
                if substat.get('is_gemmed', False):
                    gemmed_icon = QLabel()
                    gemmed_pixmap = QPixmap("images/runes/enchanted.png")
                    if not gemmed_pixmap.isNull():
                        scaled_pixmap = gemmed_pixmap.scaled(15, 15, Qt.AspectRatioMode.KeepAspectRatio)
                        gemmed_icon.setPixmap(scaled_pixmap)
                        icon_layout.addWidget(gemmed_icon)
                
                substats_layout.addWidget(icon_widget, row, col)
                col += 1
                
                # 2. Colonne pour le type de stat
                stat_type = substat.get('type', '')
                type_label = QLabel(f"{stat_type}:")
                if substat.get('is_gemmed', False):
                    type_label.setProperty("class", "stat-type gemmed")
                    original_type = substat.get('original_type', 'Unknown')
                    type_label.setToolTip(f"Gemmé (ancienne stat: {original_type})")
                else:
                    type_label.setProperty("class", "stat-type")
                
                # Appliquer le style de la pire stat si nécessaire
                if is_worst_stat:
                    type_label.setProperty("is-worst", "true")
                
                substats_layout.addWidget(type_label, row, col)
                col += 1
                
                # 3. Colonne pour la valeur de base
                stat_value = substat.get('value', 0)
                value_label = QLabel(f"{stat_value}")
                value_label.setProperty("class", "stat-value")
                if is_worst_stat:
                    value_label.setProperty("is-worst", "true")
                substats_layout.addWidget(value_label, row, col)
                col += 1
                
                # 4. Colonne pour la valeur de grind ou l'indicateur non-grindable
                grind_value = substat.get('grind_value', 0)
                if grind_value > 0:
                    grind_label = QLabel(f"(+{grind_value})")
                    grind_label.setProperty("class", "grind-value")
                    substats_layout.addWidget(grind_label, row, col)
                elif not self.is_grindable_stat(stat_type):
                    cross_label = QLabel("✗")
                    cross_label.setProperty("class", "non-grindable")
                    cross_label.setToolTip("Cette statistique ne peut pas être grindée")
                    substats_layout.addWidget(cross_label, row, col)
        
        # Ajouter le widget de sous-stats au layout principal
        stats_layout.addWidget(substats_widget)
        
        # Ajouter un stretch pour pousser tout vers le haut
        stats_layout.addStretch(1)
        
        # Ajouter le conteneur de stats au layout principal
        self.main_layout.addWidget(stats_container)
    
    def is_grindable_stat(self, stat_type):
        """Vérifie si un type de statistique peut être grindé"""
        non_grindable = [
            "TC%", "DC%", "RESIS%", "PRECI%", 
            "Taux Critique", "Dégâts Critiques", "Résistance", "Précision"
        ]
        return stat_type not in non_grindable
    
    def _get_efficiency_class(self, eff_value):
        """Détermine la classe CSS en fonction de la classification de la rune"""
        # Récupérer la classification de la rune
        classification = self.rune.get_classification()
        
        # Traiter les cas spéciaux avec caractères accentués ou majuscules
        if classification == "GOAT":
            return "goat"
        elif classification == "Ultime":
            return "ultime"
        elif classification == "Magistral":
            return "magistral"
        elif classification == "Divine":
            return "divine"
        elif classification == "Précieuse":
            return "precieuse"
        elif classification == "Fiable":
            return "fiable"
        elif classification == "Basique":
            return "basique"
        
        # Si pas de classification reconnue, utiliser une valeur par défaut
        return "basique"
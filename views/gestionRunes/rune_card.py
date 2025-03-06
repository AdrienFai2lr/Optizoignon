from PyQt6.QtWidgets import (QWidget, QLabel, QFrame, QVBoxLayout, 
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
        self.setup_ui()
        
    def setup_ui(self):
        # Configuration de base
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(220, 280)
        self.setMaximumSize(250, 320)
        
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
            
            # Obtenir l'efficacité maximale
            eff_value_max = self.rune.get_eff_max()
            
            # Créer le badge d'efficacité actuelle
            eff_badge = QLabel(f"{float(eff_value):.2f}")
            eff_badge.setObjectName("efficiencyBadge")
            eff_badge.setProperty("eff-class", eff_class)
            eff_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Ajouter le badge d'efficacité actuelle
            eff_layout.addWidget(eff_badge)
                        
            # Ajouter le badge d'efficacité maximale
            eff_max_badge = QLabel(f"{float(eff_value_max):.2f}")
            eff_max_badge.setObjectName("efficiencyMaxBadge")
            eff_layout.addWidget(eff_max_badge)
            
            # Ajouter le bouton œil uniquement si la rune est de niveau 12+
            if hasattr(self.rune, 'level') and isinstance(self.rune.level, (int, float)) and self.rune.level >= 12:
                eye_button = QPushButton()
                eye_button.setObjectName("eyeButton")
                eye_button.setMaximumSize(20, 20)
                eye_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                
                # Charger l'icône d'œil (assurez-vous que le fichier existe)
                eye_icon_path = os.path.join("images/icons", "eye.png")
                if os.path.exists(eye_icon_path):
                    eye_pixmap = QPixmap(eye_icon_path)
                    eye_pixmap = eye_pixmap.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio)
                    eye_button.setIcon(QPixmap(eye_pixmap))
                else:
                    # Utiliser un texte comme alternative si l'image n'existe pas
                    eye_button.setText("👁️")
                    eye_button.setStyleSheet("font-size: 10px; padding: 0;")
                
                # Connecter le bouton à la fonction d'affichage des infos de remplacement
                eye_button.clicked.connect(self.show_stat_replacement_info)
                
                # Ajouter le bouton œil au conteneur
                eff_layout.addWidget(eye_button)
            
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
        
        # Ne pas désactiver l'interaction pour permettre le clic sur le bouton œil si niveau >=12
        if hasattr(self.rune, 'level') and isinstance(self.rune.level, (int, float)) and self.rune.level >= 12:
            # Ne pas désactiver l'interaction pour permettre le clic sur l'œil
            pass
        else:
            # Désactiver l'interaction pour les runes de niveau <12
            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
    
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
        stats_layout.setContentsMargins(10, 15, 10, 10)
        stats_layout.setSpacing(10)
        
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
        
        # Obtenir l'index de la pire stat (si disponible)
        worst_stat_idx = None
        try:
            if hasattr(self.rune, 'level') and isinstance(self.rune.level, (int, float)) and self.rune.level >= 12:
                worst_stat_idx = self.rune.get_worst_stat_number()
                
                # Vérifier si l'index est un nombre et le convertir
                if isinstance(worst_stat_idx, str):
                    try:
                        worst_stat_num = int(worst_stat_idx)
                        # Vérifier si l'index est dans la plage valide (1-4)
                        if 1 <= worst_stat_num <= 4:
                            worst_stat_idx = worst_stat_num
                        else:
                            print(f"Avertissement: Index de sous-stat hors plage: {worst_stat_num}")
                            worst_stat_idx = None  # Ignorer les indices hors plage
                    except ValueError:
                        # Pas un nombre valide
                        worst_stat_idx = None
        except Exception as e:
            print(f"Erreur lors de l'accès à get_worst_stat_number: {e}")
            worst_stat_idx = None
        
        # Sous-stats avec grind et gemmes
        if self.rune.substats:
            for i, substat in enumerate(self.rune.substats, 1):
                substat_widget = QWidget()
                
                # Vérifier si c'est la pire stat pour appliquer un style spécial
                is_worst_stat = False
                if worst_stat_idx is not None:
                    if worst_stat_idx == i:
                        is_worst_stat = True
                
                if is_worst_stat:
                    substat_widget.setProperty("class", "worst-stat-widget")
                    
                substat_layout = QHBoxLayout(substat_widget)
                substat_layout.setContentsMargins(0, 0, 0, 0)
                
                # Ajouter une icône de warning si c'est la pire stat
                if is_worst_stat:
                    worst_icon = QLabel("⚠️")  # Emoji d'avertissement
                    worst_icon.setProperty("class", "worst-stat-icon")
                    worst_icon.setToolTip("Statistique recommandée à remplacer")
                    substat_layout.addWidget(worst_icon)
                
                # Ajouter l'icône si la stat est gemmée
                if substat.get('is_gemmed', False):
                    gemmed_icon = QLabel()
                    gemmed_pixmap = QPixmap("images/runes/enchanted.png")
                    if not gemmed_pixmap.isNull():
                        scaled_pixmap = gemmed_pixmap.scaled(15, 15, Qt.AspectRatioMode.KeepAspectRatio)
                        gemmed_icon.setPixmap(scaled_pixmap)
                        substat_layout.addWidget(gemmed_icon)
                
                substat_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                
                # Création de la partie de base de la sous-stat
                stat_type = substat.get('type', '')
                stat_value = substat.get('value', 0)
                stat_base_text = f"{stat_type}: {stat_value}"
                
                # Gestion des grinds
                grind_value = substat.get('grind_value', 0)
                is_gemmed = substat.get('is_gemmed', False)
                
                # Si la sous-stat a une valeur de grind
                if grind_value > 0:
                    # Label pour la valeur de base
                    base_label = QLabel(stat_base_text)
                    base_label.setProperty("class", "substat gemmed" if is_gemmed else "substat")
                    if is_gemmed:
                        original_type = substat.get('original_type', 'Unknown')
                        base_label.setToolTip(f"Gemmé (ancienne stat: {original_type})")
                    
                    substat_layout.addWidget(base_label)
                    
                    # Label pour la valeur de grind
                    grind_label = QLabel(f" (+{grind_value})")
                    grind_label.setProperty("class", "substat grind")
                    substat_layout.addWidget(grind_label)
                else:
                    # Pas de grind, un seul label
                    substat_label = QLabel(stat_base_text)
                    substat_label.setProperty("class", "substat gemmed" if is_gemmed else "substat")
                    if is_gemmed:
                        original_type = substat.get('original_type', 'Unknown')
                        substat_label.setToolTip(f"Gemmé (ancienne stat: {original_type})")
                    
                    substat_layout.addWidget(substat_label)
                    
                    # Ajouter une croix pour les stats non-grindables
                    if not self.is_grindable_stat(stat_type):
                        cross_label = QLabel("✗")
                        cross_label.setProperty("class", "substat grind")
                        cross_label.setToolTip("Cette statistique ne peut pas être grindée")
                        substat_layout.addWidget(cross_label)
                
                # Ajouter le widget de sous-stat au conteneur de stats
                stats_layout.addWidget(substat_widget)
        
        self.main_layout.addWidget(stats_container)
    
    def is_grindable_stat(self, stat_type):
        """Vérifie si un type de statistique peut être grindé"""
        non_grindable = [
            "TC%", "DC%", "RESIS%", "PRECI%", 
            "Taux Critique", "Dégâts Critiques", "Résistance", "Précision"
        ]
        return stat_type not in non_grindable
    
    def _get_efficiency_class(self, eff_value):
        """Détermine la classe CSS en fonction de la valeur d'efficacité"""
        if isinstance(eff_value, (int, float)):
            if eff_value < 50:
                return "low"
            elif eff_value < 75:
                return "medium"
            elif eff_value < 90:
                return "high"
            else:
                return "legendary"
        return "low"  # Valeur par défaut
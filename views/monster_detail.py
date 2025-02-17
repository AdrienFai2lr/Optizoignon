import os
from dataclasses import dataclass
from typing import List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QCursor, QFont
from controllers.skills_controler import SkillsController, DatabaseError

@dataclass
class SkillData:
    """Data class for skill information"""
    description: str
    passive: bool
    hits: int = 1
    aoe: bool = False
    cooldown: Optional[int] = None
    icon_filename: Optional[str] = None
    level_progress_description: Optional[str] = None
    

    def paintEvent(self, event):
        """Custom paint event to handle base and overlay pixmaps"""
        if self.base_pixmap:
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), self.base_pixmap)
            if self.overlay_pixmap:
                painter.drawPixmap(self.rect(), self.overlay_pixmap)
            painter.end()

class SkillFrame(QLabel):
    def __init__(self, skill):
        super().__init__()
        self.setFixedSize(40, 40)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Configurer le tooltip avec la description du skill
        self.setToolTip(skill.description)
        
        # Charger l'icône
        if skill.icon_filename:
            icon_path = os.path.join("images", "skills", skill.icon_filename)
            if os.path.exists(icon_path):
                pixmap = QPixmap(icon_path)
                scaled_pixmap = pixmap.scaled(
                    40, 40, 
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.setPixmap(scaled_pixmap)
            else:
                self.setText("?")
                self.setStyleSheet("""
                    QLabel {
                        background-color: #f0f0f0;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                    }
                """)
        else:
            self.setText("?")
            self.setStyleSheet("""
                QLabel {
                    background-color: #f0f0f0;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }
            """)
    
    def _setup_ui(self):
        """Initialize and setup the UI components"""
        self.setFrameStyle(QFrame.Shape.Box)
        layout = QVBoxLayout(self)
        
        self._setup_header(layout)
        self._setup_description(layout)
        self._setup_info(layout)
        self._setup_progression(layout)
    
    def _setup_header(self, layout: QVBoxLayout):
        """Setup the skill header with icon and cooldown"""
        header = QHBoxLayout()
        
        icon_label = self._create_skill_icon()
        header.addWidget(icon_label)
        
        if self.skill_data.cooldown:
            cooldown_label = QLabel(f"(Turn: {self.skill_data.cooldown})")
            header.addWidget(cooldown_label)
            
        header.addStretch()
        layout.addLayout(header)
    
    def _create_skill_icon(self) -> QLabel:
        """Create and configure the skill icon label"""
        icon_label = QLabel()
        icon_label.setFixedSize(40, 40)
        
        if self.skill_data.icon_filename:
            # Ajout de logs pour déboguer
            current_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"Current directory: {current_dir}")
           

            project_root = os.path.dirname(current_dir)
            print(f"Project root: {project_root}")
            print(f"Trying to load skill icon from: {os.path.abspath(icon_path)}")
            if os.path.exists(icon_path):
                print(f"✅ Found skill icon at: {icon_path}")
            else:
                print(f"❌ Skill icon not found at: {icon_path}")

            icon_path = os.path.join(project_root, "images", "skills", self.skill_data.icon_filename)
            print(f"Trying to load skill icon from: {icon_path}")
            
            # Affiche le chemin complet recherché pour l'image
            print(f"Recherche de l'image de compétence: {os.path.abspath(icon_path)}")
            
            if os.path.exists(icon_path):
                print(f"Found skill icon at: {icon_path}")
                pixmap = QPixmap(icon_path)
                scaled_pixmap = pixmap.scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                icon_label.setPixmap(scaled_pixmap)
                icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                print(f"❌ Skill icon not found at: {icon_path}")
                # Ajout d'un label placeholder pour indiquer l'absence d'image
                icon_label.setText("?")
                icon_label.setStyleSheet("QLabel { background-color: #f0f0f0; border: 1px solid #ddd; }")
                icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        return icon_label
    
    def _setup_description(self, layout: QVBoxLayout):
        """Setup the skill description"""
        desc_label = QLabel(self.skill_data.description)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
    
    def _setup_info(self, layout: QVBoxLayout):
        """Setup additional skill information"""
        info_layout = QHBoxLayout()
        
        type_label = QLabel("Passive" if self.skill_data.passive else "Active")
        info_layout.addWidget(type_label)
        
        if not self.skill_data.passive and self.skill_data.hits > 1:
            hits_label = QLabel(f"Hits: {self.skill_data.hits}")
            info_layout.addWidget(hits_label)
        
        if self.skill_data.aoe:
            aoe_label = QLabel("AOE")
            info_layout.addWidget(aoe_label)
            
        info_layout.addStretch()
        layout.addLayout(info_layout)
    
    def _setup_progression(self, layout: QVBoxLayout):
        """Setup skill progression information"""
        if self.skill_data.level_progress_description:
            upgrades_label = QLabel("Upgrades:")
            upgrades_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            layout.addWidget(upgrades_label)
            
            for upgrade in self.skill_data.level_progress_description.split('\n'):
                if upgrade.strip():
                    upgrade_label = QLabel(f"• {upgrade.strip()}")
                    layout.addWidget(upgrade_label)

class MonsterDetailView(QWidget):
    """Main widget for displaying detailed monster information"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.stat_labels = {}
        self.skills_controller = SkillsController()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        self._setup_back_button(main_layout)
        self._setup_header(main_layout)
        self._setup_scroll_area(main_layout)
    
    def _setup_back_button(self, layout: QVBoxLayout):
        """Setup the back button"""
        back_button = QPushButton("Back to List")
        back_button.clicked.connect(self.return_to_list)
        layout.addWidget(back_button)
    
    def _setup_header(self, layout: QVBoxLayout):
        """Setup the monster header section"""
        header_layout = QHBoxLayout()
        
        self.monster_image = QLabel()
        self.monster_image.setFixedSize(80, 80)
        header_layout.addWidget(self.monster_image)
        
        info_layout = QVBoxLayout()
        self.monster_name = QLabel()
        self.monster_name.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(self.monster_name)
        
        self.monster_type = QLabel()
        info_layout.addWidget(self.monster_type)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        layout.addLayout(header_layout)
    
    def _setup_scroll_area(self, layout: QVBoxLayout):
        """Setup the scrollable content area"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        self._setup_left_section(content_layout)
        
        
        scroll_layout.addLayout(content_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
    
    def _setup_left_section(self, layout: QHBoxLayout):
        """Setup the left section with stats and skills"""
        left_section = QVBoxLayout()
        left_section.setSpacing(10)
        
        self._setup_stats_frame(left_section)
        self._setup_skills_section(left_section)
        
        layout.addLayout(left_section, 1)
    
    def _setup_stats_frame(self, layout: QVBoxLayout):
        """Setup the stats display frame"""
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.Shape.Box)
        stats_layout = QGridLayout(stats_frame)
        
        stats = [
            ("HP", "hp"), ("ATK", "attack"), ("DEF", "defense"),
            ("SPD", "speed"), ("Crit Rate", "crit_rate"),
            ("Crit Damage", "crit_damage"), ("Resistance", "resistance"),
            ("Accuracy", "accuracy")
        ]
        
        for i, (label, attr) in enumerate(stats):
            stat_label = QLabel(label)
            stats_layout.addWidget(stat_label, i, 0)
            
            value_label = QLabel()
            value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.stat_labels[attr] = value_label
            stats_layout.addWidget(value_label, i, 1)
        
        layout.addWidget(stats_frame)
    
    def _setup_skills_section(self, layout: QVBoxLayout):
        """Setup the skills section"""
        self.skills_layout = QVBoxLayout()
        self.skills_layout.addWidget(QLabel("Skills"))
        layout.addLayout(self.skills_layout)
    

    

    def update_monster(self, monster):
        """Update the display with monster data
        
        Args:
            monster: Monster object containing all necessary data
        """
        self._update_monster_image(monster)
        self._update_monster_info(monster)
        self._update_monster_stats(monster)
        self._update_monster_skills(monster)
        
    
    def _update_monster_image(self, monster):
        """Update the monster's image"""
        if monster.image_filename:
            image_path = os.path.join("images/monsters", monster.image_filename)
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                scaled_pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
                self.monster_image.setPixmap(scaled_pixmap)
    
    def _update_monster_info(self, monster):
        """Update the monster's basic information"""
        self.monster_name.setText(f"{monster.name} {monster.stars_display}")
        self.monster_type.setText(f"{monster.element.capitalize()}")
    
    def _update_monster_stats(self, monster):
        """Update the monster's statistics"""
        stats_mapping = {
            'hp': monster.hp,
            'attack': monster.attack,
            'defense': monster.defense,
            'speed': monster.speed,
            'crit_rate': monster.crit_rate,
            'crit_damage': monster.crit_damage,
            'resistance': monster.resistance,
            'accuracy': monster.accuracy
        }
        
        for stat, value in stats_mapping.items():
            if stat in self.stat_labels:
                self.stat_labels[stat].setText(str(value))
    
    def _update_monster_skills(self, monster):
        skills = self.skills_controller.get_skills_by_monster_id(monster.id)
        monster.skills = skills  # Met à jour l'objet monster avec ses skills

        # Nettoyer les widgets existants
        for i in reversed(range(self.skills_layout.count())):
            widget = self.skills_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add skills section title
        # Ajouter le titre
        title = QLabel("Skills")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.skills_layout.addWidget(title)
       
        print(f"🔍 Checking skills for monster {monster.name}")
        print(f"🔍 Checking skills for monster {monster.id}")
        print(f"📊 Skills attribute exists: {hasattr(monster, 'skills')}")
        print(f"📊 Number of skills: {len(monster.skills) if hasattr(monster, 'skills') else 0}")
       # Afficher les skills
        for skill in skills:
            skill_frame = SkillFrame(skill)
            self.skills_layout.addWidget(skill_frame)
            print(skill_frame)

    def return_to_list(self):
        """Return to the monster list view"""
        self.main_window.show_monster_list()

    def clear_data(self):
        """Clear all displayed data"""
        self.monster_image.clear()
        self.monster_name.clear()
        self.monster_type.clear()
        
        # Clear stats
        for label in self.stat_labels.values():
            label.clear()
            
        # Clear skills
        for i in reversed(range(self.skills_layout.count())):
            widget = self.skills_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
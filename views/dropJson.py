from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
import json
import os

class DropZoneWidget(QWidget):
    # Signal émis lorsqu'un fichier JSON valide est importé
    json_imported = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 200)
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            DropZoneWidget {
                border: 2px dashed #999;
                border-radius: 5px;
                background-color: #f0f0f0;
            }
            DropZoneWidget:hover {
                border-color: #555;
                background-color: #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(self)
        
        self.label = QLabel("Déposez votre fichier JSON ici\nou cliquez pour sélectionner")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.button = QPushButton("Sélectionner un fichier")
        self.button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)  # marges
        layout.setSpacing(5)  # espace entre widgets
        

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file_path in files:
            if file_path.endswith('.json'):
                self.process_json_file(file_path)
                break

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier JSON",
            "",
            "Fichiers JSON (*.json)"
        )
        if file_path:
            self.process_json_file(file_path)

    def process_json_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.json_imported.emit(data)
                self.label.setText(f"Fichier importé avec succès:\n{os.path.basename(file_path)}")
        except json.JSONDecodeError:
            self.label.setText("Erreur: Le fichier n'est pas un JSON valide")
        except Exception as e:
            self.label.setText(f"Erreur lors de l'importation:\n{str(e)}")
    

    def reset_state(self):
        """Réinitialise l'état de la zone de dépôt"""
        self.label.setText("Déposez votre fichier JSON ici\nou cliquez pour sélectionner")
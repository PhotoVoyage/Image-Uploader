import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout, QSizePolicy, QLineEdit, QMessageBox, QScrollArea, QGridLayout, QAction, QMenu
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Uploader")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Menú principal
        self.create_menu()

        self.search_layout = QHBoxLayout()  
        self.layout.addLayout(self.search_layout)

        self.search_entry = QLineEdit()  
        self.search_entry.setPlaceholderText("Buscar por ID de imagen")
        self.search_layout.addWidget(self.search_entry)
        self.search_entry.textChanged.connect(self.search_image)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        self.image_layout = QGridLayout(self.scroll_content)
        self.image_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.upload_button = QPushButton("Subir imagen")
        self.upload_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.upload_button)

        self.image_widgets = []  
        self.image_paths = {}  

        # Cargar imágenes almacenadas en el archivo JSON
        self.load_images_from_json()

    def create_menu(self):
        menubar = self.menuBar()
        
        home_menu = menubar.addMenu('Home')
        home_action = QAction('Home', self)
        home_menu.addAction(home_action)
        
        admin_menu = menubar.addMenu('Admin')
        admin_action = QAction('Admin', self)
        admin_menu.addAction(admin_action)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self, "Seleccionar imagen", "", "Archivos de imagen (*.png *.jpg *.jpeg *.gif)", options=options)
        for file_name in file_names:
            self.add_image(file_name)

    def add_image(self, file_name):
        if file_name not in self.image_paths.values():
            pixmap = QPixmap(file_name)
            label = QLabel()
            label.setPixmap(pixmap.scaledToWidth(200))
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.image_widgets.append(label)
            self.image_paths[str(len(self.image_paths) + 1)] = file_name  # Generar un ID único para la imagen

            # Añadir imagen al layout
            row, col = divmod(len(self.image_widgets) - 1, 9)  # Hasta 9 imágenes por fila
            self.image_layout.addWidget(label, row, col)

            # Ajustar el tamaño del scroll area
            self.adjust_scroll_area_size()
        else:
            QMessageBox.warning(self, "Imagen repetida", "La imagen ya ha sido cargada.")

    def adjust_scroll_area_size(self):
        # Calcular el ancho total de las imágenes
        total_width = sum(label.width() for label in self.image_widgets)
        total_width += self.image_layout.horizontalSpacing() * (self.image_layout.columnCount() - 1)

        # Calcular el ancho de la ventana
        viewport_width = self.scroll_area.viewport().width()

        # Ajustar el tamaño del scroll area
        if total_width > viewport_width:
            self.scroll_content.setMinimumWidth(total_width)
        else:
            self.scroll_content.setMinimumWidth(viewport_width)

    def save_images_to_json(self):
        with open('images.json', 'w') as f:
            json.dump(self.image_paths, f)

    def load_images_from_json(self):
        try:
            with open('images.json', 'r') as f:
                loaded_paths = json.load(f)
                for file_name in loaded_paths.values():
                    self.add_image(file_name)
                self.image_paths.update(loaded_paths)
        except FileNotFoundError:
            pass

    def search_image(self):
        search_text = self.search_entry.text()
        if search_text:
            if search_text in self.image_paths:
                QMessageBox.information(self, "Imagen encontrada", f"Imagen encontrada con ID: {search_text}")
            else:
                QMessageBox.warning(self, "Imagen no encontrada", f"No se encontró ninguna imagen con el ID: {search_text}")

    def closeEvent(self, event):
        self.save_images_to_json()
        event.accept()

    def showFullScreen(self):
        self.showMaximized()  # Mostrar la ventana en pantalla completa

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageUploader()
    window.showFullScreen()  # Mostrar la ventana
    sys.exit(app.exec_())

import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout, QSizePolicy, QMessageBox, QScrollArea, QGridLayout, QAction, QMenu
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class AdminWindow(QMainWindow):
    def __init__(self, image_paths):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_paths = image_paths

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        self.image_layout = QGridLayout(self.scroll_content)
        self.image_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.load_images()

    def load_images(self):
        for index, (image_id, image_path) in enumerate(self.image_paths.items()):
            pixmap = QPixmap(image_path)
            label = QLabel()
            label.setPixmap(pixmap.scaledToWidth(200))
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            delete_button = QPushButton("Borrar")
            delete_button.clicked.connect(lambda _, img_id=image_id: self.delete_image(img_id))

            self.image_layout.addWidget(label, index, 0)
            self.image_layout.addWidget(delete_button, index, 1)

    def delete_image(self, image_id):
        reply = QMessageBox.question(self, 'Eliminar imagen', f"¿Estás seguro que quieres eliminar la imagen {image_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            del self.image_paths[image_id]
            self.save_images_to_json()
            self.clear_layout()
            self.load_images()

    def clear_layout(self):
        for i in reversed(range(self.image_layout.count())):
            widget = self.image_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def save_images_to_json(self):
        with open('images.json', 'w') as f:
            json.dump(self.image_paths, f)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    admin_window = AdminWindow()
    admin_window.show()
    sys.exit(app.exec_())

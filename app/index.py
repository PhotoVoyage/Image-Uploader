import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout, QSizePolicy, QLineEdit, QMessageBox, QScrollArea, QGridLayout, QAction, QMenu
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from admin import AdminWindow  # Import the admin window

class ImageUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Uploader")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Main menu
        self.create_menu()

        self.search_layout = QHBoxLayout()  
        self.layout.addLayout(self.search_layout)

        self.search_entry = QLineEdit()  
        self.search_entry.setPlaceholderText("Search by Image ID")
        self.search_layout.addWidget(self.search_entry)
        self.search_entry.textChanged.connect(self.search_image)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

        self.image_layout = QGridLayout(self.scroll_content)
        self.image_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.upload_button)

        self.image_widgets = []  
        self.image_paths = {}  

        # Load images stored in the JSON file
        self.load_images_from_json()

    def create_menu(self):
        menubar = self.menuBar()
        
        admin_menu = menubar.addMenu('Admin')
        admin_action = QAction('Admin', self)
        admin_action.triggered.connect(self.open_admin_panel)  # Connect the action to the method
        admin_menu.addAction(admin_action)

    def open_admin_panel(self):
        admin_window = AdminWindow(self.image_paths)  # Pass image paths to the admin
        admin_window.exec_()  # Execute the admin window

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.gif)", options=options)
        for file_name in file_names:
            self.add_image(file_name)

    def add_image(self, file_name):
        if file_name not in self.image_paths.values():
            pixmap = QPixmap(file_name)
            label = QLabel()
            label.setPixmap(pixmap.scaledToWidth(200))
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.image_widgets.append(label)
            self.image_paths[str(len(self.image_paths) + 1)] = file_name  # Generate a unique ID for the image

            # Add image to layout
            row, col = divmod(len(self.image_widgets) - 1, 9)  # Up to 9 images per row
            self.image_layout.addWidget(label, row, col)

            # Adjust scroll area size
            self.adjust_scroll_area_size()
        else:
            QMessageBox.warning(self, "Duplicate Image", "The image has already been uploaded.")

    def adjust_scroll_area_size(self):
        # Calculate total width of images
        total_width = sum(label.width() for label in self.image_widgets)
        total_width += self.image_layout.horizontalSpacing() * (self.image_layout.columnCount() - 1)

        # Calculate viewport width
        viewport_width = self.scroll_area.viewport().width()

        # Adjust scroll area size
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
                QMessageBox.information(self, "Image Found", f"Image found with ID: {search_text}")
            else:
                QMessageBox.warning(self, "Image Not Found", f"No image found with ID: {search_text}")

    def closeEvent(self, event):
        self.save_images_to_json()
        event.accept()

    def showFullScreen(self):
        self.showMaximized()  # Show window in fullscreen mode

    def open_admin_panel(self):
        admin_window = AdminWindow(self.image_paths)  # Create an instance of AdminWindow
        admin_window.show()  # Show the admin window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageUploader()
    window.showFullScreen()  # Show the window
    sys.exit(app.exec_())

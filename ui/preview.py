from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class Preview(QWidget):
    def __init__(self):
        super().__init__()
        
        # This prevents the widget from influencing the layout with its size hint
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        layout = QVBoxLayout(self)
        self.image_label = QLabel("Select an image to preview")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label)

    def set_preview_image(self, image_path):
        if not image_path:
            self.image_label.clear()
            self.image_label.setText("Select an image to preview")
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.clear()
            self.image_label.setText("Cannot preview this image.")
        else:
            self.image_label.setPixmap(pixmap)
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageLabel(QLabel):
    """A custom QLabel that scales its pixmap while preserving aspect ratio."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        self._update_scaled_pixmap()

    def resizeEvent(self, event):
        self._update_scaled_pixmap()
        super().resizeEvent(event)

    def _update_scaled_pixmap(self):
        if self._pixmap.isNull():
            # Let the base class handle clearing or showing text
            super().setPixmap(self._pixmap)
            return

        scaled_pixmap = self._pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        super().setPixmap(scaled_pixmap)

class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        layout = QVBoxLayout(self)
        self.image_label = ImageLabel("Select an image to preview")
        layout.addWidget(self.image_label)

    def set_preview_image(self, image_path):
        if not image_path:
            self.image_label.setText("Select an image to preview")
            self.image_label.setPixmap(QPixmap()) # Clear pixmap
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.setText("Cannot preview this image.")
            self.image_label.setPixmap(QPixmap()) # Clear pixmap
        else:
            self.image_label.setText("") # Clear text
            self.image_label.setPixmap(pixmap)
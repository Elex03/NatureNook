# pyqt_window.py
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pygame as pg
from Slider import Slider  # Asegúrate de que el archivo Slider.py esté en el mismo directorio o en el path correcto

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title
        self.setWindowTitle("Audio Settings")

        # Set window opacity
        self.setWindowOpacity(0.5)

        # Set the geometry of the window
        self.setGeometry(150, 100, 800, 600)

        # Initialize Pygame
        pg.init()
        self.screen = pg.Surface((800, 600), pg.SRCALPHA)
        self.slider = Slider(150, 250, 500, 20, 0, 100, 50)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pygame)
        self.timer.start(16)  # Approximately 60 FPS

        # Create a QLabel to display the Pygame surface
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)

        # Create a switch
        self.switch = QPushButton("OFF", self)
        self.switch.setCheckable(True)
        self.switch.setGeometry(360, 300, 100, 30)
        self.switch.clicked.connect(self.toggle_switch)

        # Show all the widgets
        self.show()

    def toggle_switch(self):
        if self.switch.isChecked():
            self.switch.setText("ON")
        else:
            self.switch.setText("OFF")

    def update_pygame(self):
        # Fill the screen with transparent color
        self.screen.fill((0, 0, 0, 0))

        # Draw the slider
        self.slider.draw(self.screen)

        # Convert the Pygame surface to a QImage
        width, height = self.screen.get_size()
        image = pg.image.tostring(self.screen, 'RGBA')
        qimage = QImage(image, width, height, QImage.Format_RGBA8888)

        # Set the QImage on the QLabel
        self.label.setPixmap(QPixmap.fromImage(qimage))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_P:
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_p))
        super().keyPressEvent(event)

def run_pyqt_app():
    app = QApplication(sys.argv)
    window = TransparentWindow()
    sys.exit(app.exec())

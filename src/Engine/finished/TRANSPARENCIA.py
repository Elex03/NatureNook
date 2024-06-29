import pygame
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title
        self.setWindowTitle("Python")

        self.setWindowOpacity(0.5)

        # setting the geometry of window
        self.setGeometry(150, 100, 400, 200)

        #show all the widgets
        self.show()

def run_pyqt_app():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Window")

# Background color
background_color = (0, 0, 0)  # black

# Create a new thread to run the PyQt5 application
from threading import Thread
pyqt_thread = Thread(target=run_pyqt_app)
pyqt_thread.start()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    pygame.display.flip()

pygame.quit()

import sys
import os
from PySide6 import QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from py_toggle import PyToggle

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        #Resize MainWindow
        self.resize(400, 300)

        #Title of the window
        self.setWindowTitle("AwesomePyBot")

        #Create container and layout
        self.container = QFrame()
        self.container.setObjectName("container")
        self.container.setStyleSheet("#container { background-color: #222 }")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        #Adding the label
        self.label = QLabel("Off")
        self.label.setStyleSheet("color: #FFF; font-size: 50px; padding-top: 100px")
        self.layout.addWidget(self.label, Qt.AlignCenter, Qt.AlignCenter)

        #Add widget
        self.toggle = PyToggle()
        self.layout.addWidget(self.toggle, Qt.AlignCenter, Qt.AlignCenter)

        #Set central widget
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        #Show window
        self.show()

        #Change the text when the button is pressed
        self.toggle.stateChanged.connect(self.change_text)

    def change_text(self, value):
        if value:
            self.label.setText("On")
        else:
            self.label.setText("Off")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
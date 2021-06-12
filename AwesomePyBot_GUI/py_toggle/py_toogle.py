from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class PyToggle(QCheckBox):
    def __init__(
        self,
        width = 100,
        bg_color = "#777",
        circle_color = "#DDD",
        active_color = "#6441A5",
        animation_curve = QEasingCurve.OutBounce
    ):
        QCheckBox.__init__(self)

        #Set default parameters
        self.setFixedSize(width, 50)
        self.setCursor(Qt.PointingHandCursor)

        #Colors
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        #Create animation
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500) #Time in milisseconds

        #Connect state changed
        self.stateChanged.connect(self.start_transition)

    @Property(float) #Get
    def circle_position(self):
        return self._circle_position

    @circle_position.setter #Set
    def circle_position(self, pos):
        self._circle_position = pos
        self.update

    def start_transition(self, value):
        self.animation.stop() #Stop animation if running
        if value:
            self.animation.setEndValue(self.width() - 47)
        else:
            self.animation.setEndValue(3)
        
        #Start animation
        self.animation.start()

        print(f"Status: {self.isChecked()}")

    #Set new hit area
    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    #Draw new items
    def paintEvent(self, event):
        #Set painter
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        #Set as no pen
        p.setPen(Qt.NoPen)

        #Draw rectangle
        rect = QRect(0, 0, self.width(), self.height())

        #Move circle
        #Off
        if not self.isChecked():
            #Draw BG
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            #Draw circle
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 44, 44)
        #On
        else:
            #Draw BG
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            #Draw circle
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 44, 44)

        p.end()
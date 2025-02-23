import pygame
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPainterPath, QPen
from PyQt5.QtCore import QRectF

# load sfx
pygame.mixer.init()
hatch_sound =  pygame.mixer.Sound("sfx/hatching.wav")
attention_sound = pygame.mixer.Sound("sfx/attention.wav")
game_start = pygame.mixer.Sound("sfx/game-start.wav")
death_sound = pygame.mixer.Sound("sfx/death.wav")

EGGS = {
    "Bulbasar": "img/bulbasaur-egg.png",
    "Jigglypuff": "img/jigglypuff-egg.png",
    "Charizard": "img/charizard-egg.png",
    "Squirtle": "img/squirtle-egg.png",
    "Ghastly": "img/ghastly-egg.png",
    "Oddish": "img/oddish-egg.png"
}

TAMAGOCHIS = {
    "Bulbasaur": "img/bulbasaur.png",
    "Jigglypuff": "img/jigglypuff.png",
    "Charizard": "img/charizard.png",
    "Squirtle": "img/squirtle-egg.png",
    "Ghastly": "img/ghastly.png",
    "Oddish": "img/oddish.png"
}

MENU_ITEMS = [
    {"name": "Status", "image": "img/heart.png"},
    {"name": "Medicine", "image": "img/medicine.png"},
    {"name": "Feed", "image": "img/feed.png"},
    {"name": "Play", "image": "img/play.png"}
]

## TAMAGOTCHI STATS
weight = 1
happiness = 10
health = 10
sleep = 10

class Tamagotchi(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(281, 318) ## WINDOW SIZE

        self.bg_image = QPixmap("img/bg.png")
        if self.bg_image.isNull():
            print("Errorr")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        ellipse_path = QPainterPath()
        ellipse_path.addEllipse(QRectF(0,0,281,318))
        
        ## mask clipping for shell wallpaper
        if not self.bg_image.isNull():
            painter.setClipPath(QPainterPath())
            bg_image = self.bg_image.scaled(281,318)
            painter.drawPixmap(0,0, bg_image)
        
        pen = QPen(QColor(63,99,171))
        pen.setWidth(8)
        painter.setPen(pen)
        painter.setClipping(False)
        painter.drawEllipse(QRectF(0,0,281,318))

        screen_w = 162
        screen_h = 151
        center_x = (self.width() - screen_w)//2
        center_y = (self.height() - screen_h)//2
        screen = QRectF(center_x, center_y, screen_w, screen_h)
        painter.setBrush(QColor(200,200,200))
        painter.drawRect(screen)


#run
app = QApplication(sys.argv)
window = Tamagotchi()
window.show()
sys.exit(app.exec())
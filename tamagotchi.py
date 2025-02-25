import pygame
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPainterPath, QPen
from PyQt5.QtCore import *

# load sfx
pygame.mixer.init()
hatch_sound =  pygame.mixer.Sound("sfx/hatching.wav")
attention_sound = pygame.mixer.Sound("sfx/attention.wav")
game_start = pygame.mixer.Sound("sfx/game-start.wav")
death_sound = pygame.mixer.Sound("sfx/death.wav")

EGGS = {
    "Bulbasaur": "img/bulbasaur-egg.png",
    "Jigglypuff": "img/jigglypuff-egg.png",
    "Charizard": "img/charizard-egg.png",
    "Squirtle": "img/squirtle-egg.png",
    "Ghastly": "img/ghastly-egg.png",
    "Oddish": "img/oddish-egg.png"
}

TAMAGOTCHIS = {
    "Bulbasaur": "img/bulbasaur.png",
    "Jigglypuff": "img/jigglypuff.png",
    "Charizard": "img/charizard.png",
    "Squirtle": "img/squirtleegg.png",
    "Ghastly": "img/ghastly.png",
    "Oddish": "img/oddish.png"
}

MENU_ITEMS = [
    {"name": "Status", "image": "img/heart.png", "width": 78.5, "height": 64},
    {"name": "Medicine", "image": "img/medicine.png", "width": 78, "height": 75},
    {"name": "Feed", "image": "img/feed.png", "width": 79.5, "height": 73.5},
    {"name": "Play", "image": "img/play.png", "width": 73.5, "height": 73.5}
]

## TAMAGOTCHI STATS
weight = 1
happiness = 10
health = 10
sleep = 10

class Tamagotchi(QWidget):
    def __init__(self):
        super().__init__()
        global MENU_ACTIONS
        MENU_ACTIONS = {
        "Status": self.status,
        "Medicine": self.medicine,
        "Feed": self.feed,
        "Play": self.play
        }

        self.setFixedSize(270, 318) ## WINDOW SIZE
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #INITIALIZATION
        self.egg_x_position = (self.width() - 65) // 2
        self.egg_y_position = (self.height()-75) // 2
        self.current_egg_index = 0
        self.is_hatched = False
        self.current_menu_index = 0
        self.menu_active = False
        

        #LOAD HERE
        self.bg_image = QPixmap("img/bg.png")
        if self.bg_image.isNull():
            print("Errorr")

                #EGGS
        self.egg_images = {name: QPixmap(path) for name, path in EGGS.items()}
        for egg_name, pixmap in self.egg_images.items():
            if pixmap.isNull():
                print("error: no egg image")
        self.current_egg_image = self.egg_images[list(EGGS.keys())[self.current_egg_index]]
                #menu
        self.menu_items = {item["name"]: QPixmap(item["image"]) for item in MENU_ITEMS}
        for item_name, pixmap in self.menu_items.items():    
            if pixmap.isNull():
                print("error: no menu image")

        game_start.play()
        self.create_buttons()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        ellipse_path = QPainterPath()
        ellipse_path.addEllipse(QRectF(0,0,270,318))

        ## mask clipping for shell wallpaper
        if not self.bg_image.isNull():
            painter.setClipPath(ellipse_path)
            bg_image = self.bg_image.scaled(281,318)
            painter.drawPixmap(0,0, bg_image)
    
        pen = QPen(QColor(63,99,171))
        ellipse_outline_width = 10
        pen.setWidth(ellipse_outline_width)
        painter.setPen(pen)
        painter.setClipping(False)
        painter.drawEllipse(ellipse_outline_width // 2, ellipse_outline_width // 2,
            self.width() - ellipse_outline_width, self.height() - ellipse_outline_width)


        screen_w = 162
        screen_h = 151
        center_x = (self.width() - screen_w)//2
        center_y = (self.height() - screen_h)//2
        screen = QRectF(center_x, center_y, screen_w, screen_h)
        painter.setBrush(QColor(200,200,200))
        painter.setPen(pen)
        painter.drawRect(screen)

            # EGGS -------------------------------------------------
        if not self.is_hatched:
            scaled_egg = self.current_egg_image.scaled(65,76, Qt.KeepAspectRatio)
            painter.drawPixmap(self.egg_x_position, self.egg_y_position, scaled_egg)
        else:
            scaled_tamagotchi = self.current_egg_image.scaled(85,85, Qt.KeepAspectRatio)
            tamagotchi_x_position = (self.width() - 85) // 2
            tamagotchi_y_position = (self.height() - 85) // 2 - 15
            painter.drawPixmap(tamagotchi_x_position, tamagotchi_y_position, scaled_tamagotchi)

        if self.current_egg_image is not None:
            if not self.is_hatched:
                scaled_egg = self.current_egg_image.scaled(65,76, Qt.KeepAspectRatio)

        if self.menu_active:
            self.menu_layout(painter, center_x, center_y)

    # action 1
    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()
        
    #action 2
    def mouseMoveEvent(self, event):
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()

    def create_buttons(self):
                #A
        self.buttonA = QPushButton("A", self)
        self.buttonA.setFixedSize(30,30)
        self.buttonA.setStyleSheet("border-radius: 15px; background-color: lightgray; border: 3px solid rgb(63,99,171);")
        self.buttonA.move(73,260)
        self.buttonA.clicked.connect(self.move_egg_left)
                #B
        self.buttonB = QPushButton("B", self)
        self.buttonB.setFixedSize(30,30)
        self.buttonB.setStyleSheet("border-radius: 15px; background-color: lightgray; border: 3px solid rgb(63,99,171);")
        self.buttonB.move(120,260)
        self.buttonB.clicked.connect(self.hatch_egg)
        self.buttonB.clicked.connect(self.menu_options)
                #C
        self.buttonC = QPushButton("C", self)
        self.buttonC.setFixedSize(30,30)
        self.buttonC.setStyleSheet("border-radius: 15px; background-color: lightgray; border: 3px solid rgb(63,99,171);")
        self.buttonC.move(168,260)
        self.buttonC.clicked.connect(self.move_egg_right)


    def move_egg_left(self):
        if not self.is_hatched:
            if self.current_egg_index > 0:
                self.current_egg_index -= 1
                self.current_egg_image = self.egg_images[list(EGGS.keys())[self.current_egg_index]]
                self.update()
        elif self.menu_active:
            self.current_menu_index = (self.current_menu_index - 1) % 4
            self.update()
    def move_egg_right(self):
        if not self.is_hatched:
            if self.current_egg_index < len(EGGS) - 1:
                self.current_egg_index += 1
                self.current_egg_image = self.egg_images[list(EGGS.keys())[self.current_egg_index]]
                self.update()
        elif self.menu_active:
            self.current_menu_index = (self.current_menu_index + 1) % 4
            self.update()
    def hatch_egg(self):
        if not self.is_hatched:
            selected_egg = list(EGGS.keys())[self.current_egg_index]
            self.current_egg_image = QPixmap(TAMAGOTCHIS[selected_egg])
            hatch_sound.play()
            self.update()

            self.buttonA.setDisabled(True)
            self.buttonC.setDisabled(True)

            self.is_hatched = True

            QTimer.singleShot(500, self.activate_menu)

    def activate_menu(self):
        self.menu_active = True
        self.buttonA.setDisabled(False)
        self.buttonC.setDisabled(False)
        self.update()


    def menu_layout(self, painter, center_x, center_y):
        item_w = 30
        item_h = 30
        start_x = center_x + 12
        start_y = center_y + 110

        for i, item_name in enumerate(self.menu_items):
            item_x = start_x + i * (item_w + 5)
            scaled_menu_item = self.menu_items[item_name].scaled(item_w, item_h)
            painter.drawPixmap(item_x, start_y, scaled_menu_item)

            if i == self.current_menu_index: 
                pen = QPen(QColor(63,99,171), 4)
                painter.setPen(pen)
                painter.drawRect(QRectF(item_x, start_y, item_w, item_h))

    def menu_options(self):
        if self.is_hatched and self.menu_active:
            selected_menu = list(MENU_ACTIONS.keys())[self.current_menu_index]
            action = MENU_ACTIONS.get(selected_menu)

            self.clear_screen(keep_image=True)

            if selected_menu == "Status":
                self.status()
            elif selected_menu == "Medicine":
                self.medicine()
            elif selected_menu == "Feed":
                self.Feed()
            elif selected_menu == "Play":
                self.Play()
            else:
                print("Invalid")

    def clear_screen(self, keep_image=False):
        if not keep_image:
            self.current_egg_image = None
        self.menu_active = False
        self.update()

    def select(self, event):
        if event.key() == Qt.Key_B and self.is_status_screen:
            self.is_status_screen = False
            self.menu_active
            self.update()
    def status(self):
        self.clear_screen()
        self.menu_active = False

        self.status = f"Weight: {weight}\nHappiness: {happiness}/10\nHealth: {health}/10\nSleep: {sleep}/10"
        self.is_status_screen = True
        self.update()

    def medicine(self):
        self.clear_screen()

    def feed(self):
        self.clear_screen()

    def play(self):
        self.clear_screen()

#run
app = QApplication(sys.argv)
window = Tamagotchi()
window.show()
sys.exit(app.exec())
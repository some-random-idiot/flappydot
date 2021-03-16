import tkinter as tk
from gamelib import Sprite, GameApp, Text
from random import randint

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5
STARTING_VELOCITY = -30
PILLAR_SPEED = -10


class Dot(Sprite):
    def init_element(self):
        self.vy = STARTING_VELOCITY
        self.is_started = False

    def update(self):
        if self.is_started:
            self.y += self.vy
            self.vy += GRAVITY

    def start(self):
        self.is_started = True


class PillarPair(Sprite):
    def update(self):
        if self.is_out_of_screen():
            self.x = CANVAS_WIDTH
        self.x += PILLAR_SPEED

    def is_out_of_screen(self):
        return self.x == -100

    def reset_position(self):
        self.x = CANVAS_WIDTH + 100

    def random_height(self):
        self.y = randint(100, CANVAS_HEIGHT - 100)


class FlappyGame(GameApp):
    def create_sprites(self):
        self.dot = Dot(self, 'images/dot.png', CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
        self.elements.append(self.dot)
        self.pillar_pair = PillarPair(self, 'images/pillar-pair.png', CANVAS_WIDTH, CANVAS_HEIGHT // 2)
        self.elements.append(self.pillar_pair)

    def init_game(self):
        self.create_sprites()
        self.pillar_pair.random_height()

    def pre_update(self):
        pass

    def post_update(self):
        if self.pillar_pair.is_out_of_screen():
            self.pillar_pair.reset_position()
            self.pillar_pair.random_height()

    def on_key_pressed(self, event):
        self.dot.start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Monkey Banana Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()

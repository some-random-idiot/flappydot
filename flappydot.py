import tkinter as tk
from gamelib import Sprite, GameApp, Text
from random import randint

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

UPDATE_DELAY = 33
GRAVITY = 2.5
STARTING_VELOCITY = -30
PILLAR_SPEED = -10
JUMP_VELOCITY = -20


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

    def jump(self):
        self.vy = JUMP_VELOCITY


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
        self.is_defeated = False
        self.score_text = Text(self, 0, CANVAS_WIDTH / 2, 40)
        self.defeated_text = Text(self, "", CANVAS_WIDTH / 2, CANVAS_WIDTH / 2)

    def init_game(self):
        self.create_sprites()
        self.pillar_pair.random_height()

    def pre_update(self):
        pass

    def post_update(self):
        if self.pillar_pair.is_out_of_screen() and not self.is_defeated:
            self.pillar_pair.reset_position()
            self.pillar_pair.random_height()
        if not self.is_defeated:
            self.check_collide()

    def on_key_pressed(self, event):
        if not self.is_defeated:
            self.dot.start()
            self.dot.jump()

    def check_collide(self):
        if (self.dot.y > app.pillar_pair.y + 199 / 2 - 20 or self.dot.y < app.pillar_pair.y - 199 / 2 + 20) and app.pillar_pair.x - 60 <= self.dot.x <= app.pillar_pair.x + 60:
            self.is_defeated = True
            self.defeated_text.set_text("Game over!, Junkyard Boyz!!!")
            self.pillar_pair.x, self.pillar_pair.y = 10**10, 10**10
        elif self.dot.x == self.pillar_pair.x + 40:
            self.score_text.set_text(self.score_text.text + 1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Flappy Dot Game")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = FlappyGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()

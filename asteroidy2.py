import math
import pyglet
from pyglet import gl
from pyglet.window import key

WIDTH = 1200
HEIGHT = 800

# Todo 1: Vytvorte konštanty pre zrýchlenie rakety a rýchlosť otáčania a pokúste sa nájsť optimálne hodnoty
ACCELERATION = 400
ROTATION_SPEED = 300

objects = []
batch = pyglet.graphics.Batch()
pressed_keyboards = set()

def set_anchor_of_image_to_center(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2


class Spaceship:

    def __init__(self, sprite):
        self.x_speed = 0
        self.y_speed = 0
        self.rotation = 1.57

        self.sprite = pyglet.sprite.Sprite(sprite, batch=batch)
        self.sprite.x = WIDTH // 2
        self.sprite.y = HEIGHT // 2

    def checkBoundaries(self):
        # Todo 6: Skontrolujte či sa ne-nachádzate s loďou mimo okna ak áno loď by sa mala objaviť na druhej strane
        if self.sprite.y > HEIGHT:
            self.sprite.y = 0
        if self.sprite.y < 0:
            self.sprite.y = HEIGHT
        if self.sprite.x > WIDTH:
            self.sprite.x = 0
        if self.sprite.x < 0:
            self.sprite.x = WIDTH


    def tick(self, dt):
        # Todo 5: Dokončite metódu tick ktorá sa stará o ovládanie lodi
        if key.W in pressed_keyboards:
            self.x_speed = self.x_speed + dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed = self.y_speed + dt * ACCELERATION * math.sin(self.rotation)

        "Spomalenie/spätný chod po kliknutí klávesy S"
        # Todo
        if key.S in pressed_keyboards:
            self.x_speed = self.x_speed - dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed = self.y_speed - dt * ACCELERATION * math.sin(self.rotation)

        "Otočenie doľava - A"
        # Todo
        if key.A in pressed_keyboards:
            self.rotation += dt

        "Otočenie doprava - D"
        # Todo
        if key.D in pressed_keyboards:
            self.rotation -= dt

        "Ručná brzda - SHIFT"
        # Todo
        if key.LSHIFT in pressed_keyboards:
            self.x_speed = 0
            self.y_speed = 0

        "Posunutie vesmírnej lode na novú pozíciu"
        self.sprite.x += dt * self.x_speed
        self.sprite.y += dt * self.y_speed
        print(f'X: {self.sprite.x} Y: {self.sprite.y}')
        self.sprite.rotation = 90 - math.degrees(self.rotation)

        "Kontrola či sme prešli kraj"
        self.checkBoundaries()

class Game:

    def __init__(self):
        self.window = None
        self.game_objects = []

    def load_resources(self):
        self.playerShip_image = pyglet.image.load('Assetss/PNG/playerShip1_blue.png')
        set_anchor_of_image_to_center(self.playerShip_image)
        self.background_image = pyglet.image.load('Assetss/Backgrounds/black.png')

    def init_objects(self):
        # Todo 5: Vytvorte objekt pre loď a pridajte ho do game_objects
        self.game_objects.append(Spaceship(sprite=self.playerShip_image))
        self.background = pyglet.sprite.Sprite(self.background_image)
        self.background.scale_x = 6
        self.background.scale_y = 4

    def draw_game(self):
        self.window.clear()
        self.background.draw()

        for x_offset in (-self.window.width, 0, self.window.width):
            for y_offset in (-self.window.height, 0, self.window.height):

                gl.glPushMatrix()

                gl.glTranslatef(x_offset, y_offset, 0)

                batch.draw()

                gl.glPopMatrix()

    def key_press(self, symbol, modifikatory):
        # Todo 2: Vytvorte Event Handler pre zmáčknuté klávesy
        # Todo Tie ktoré hráč zmačkol sa uložia do množiny pressed_keyboards
        print(f'Pressed key id {symbol}')
        pressed_keyboards.add(symbol)
        pass

    def key_release(self, symbol, modifikatory):
        # Todo 3: Vytvorte Event Handler pre klávesy ktoré už ďalej nie sú zmaćknuté
        # Todo Tieto klávesy odoberte z pressed_keyboards mnoźiny
        pressed_keyboards.discard(symbol)
        pass

    def start(self):
        self.window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

        self.window.push_handlers(
            on_draw=self.draw_game,
            on_key_press=self.key_press,
            on_key_release=self.key_release
        )

        self.load_resources()

        self.init_objects()

        for object in self.game_objects:
            pyglet.clock.schedule_interval(object.tick, 1. / 60)
        pyglet.app.run()

Game().start()
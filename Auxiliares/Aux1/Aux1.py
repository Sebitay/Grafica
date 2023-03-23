from pyglet.window import Window
from pyglet.app import run

WIDTH, HEIGHT = 1000 , 700
WINDOW_TITLE = 'AUX 1'
FULL_SCREEN = False

win = Window(WIDTH, HEIGHT, WINDOW_TITLE)

win.set_fullscreen(True)

run()
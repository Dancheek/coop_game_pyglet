import pyglet
from pyglet.gl import *


class Camera:
	def __init__(self, window, sprite):
		self.window = window
		self.sprite = sprite
		self.scale = 1

	def draw(self):
		self.zoom()
		glTranslatef(-self.sprite.x + self.window.width/2,
			-self.sprite.y + self.window.height/2, 0)

	def zoom(self):
		glTranslated(self.window.width/2, self.window.height/2, 0)
		glScaled(self.scale, self.scale, 1)
		glTranslated(-self.window.width/2, -self.window.height/2, 0)

	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		self.scale += scroll_y * 0.2
		if (self.scale == 0.45):
			self.scale = 0.4
		self.scale = round(self.scale, 2)
		if (self.scale < 0.4):
			self.scale = 0.25
		elif (self.scale >= 4.0):
			self.scale = 4.0

	def update(self, dtime):
		pass


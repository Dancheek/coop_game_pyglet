from uuid import uuid4
import math

import pyglet
from pyglet.window import key
import vecrec

import api


class Entity:
	def __init__(self, x=0, y=0, batch=None, group=None, uuid=None, meta={}):
		self.uuid = str(uuid4()) if (uuid == None) else uuid

		if (not hasattr(self, 'image')):
			self.image = self.entity_id
		if (not hasattr(self, 'width')):
			self.width = 1
		if (not hasattr(self, 'height')):
			self.height = 1

		self.collider = vecrec.Rect(
			x - self.width / 2,
			y - self.height / 2,
			self.width,
			self.height)

		self.sprite = pyglet.sprite.Sprite(api.images[self.image],
			x=self.x * api.TILE_WIDTH,
			y=self.y * api.TILE_WIDTH,
			batch=batch,
			group=group)

		self.vx = 0
		self.vy = 0
		self.dx = 0
		self.dy = 0

	@property
	def x(self):
		return self.collider.center_x

	@x.setter
	def x(self, value):
		self.collider.center_x = value

	@property
	def y(self):
		return self.collider.center_y

	@y.setter
	def y(self, value):
		self.collider.center_y = value

	def _update(self, dtime):
		self.update(dtime)
		self.sprite.update(
			x=round(self.x * api.TILE_WIDTH),
			y=round(self.y * api.TILE_WIDTH))

	def move_to(self, target_x, target_y):
		if (not api.game_world.check_collide(self.x, target_y, self.width)):
			self.y = target_y
		else:
			delta_y = target_y - self.y
			if (target_y > self.y):
				self.collider.top = math.floor(self.collider.top + delta_y)
			else:
				self.collider.bottom = math.ceil(self.collider.bottom + delta_y)
		if (not api.game_world.check_collide(target_x, self.y, self.width)):
			self.x = target_x
		else:
			delta_x = target_x - self.x
			if (target_x > self.x):
				self.collider.right = math.floor(self.collider.right + delta_x)
			else:
				self.collider.left = math.ceil(self.collider.left + delta_x)

	def on_init(self):
		pass

	def update(self, dtime):
		pass


class MainPlayer(Entity):
	entity_id = 'default:player'
	speed = 2
	width = 0.75
	height = 0.75
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.key_handler = key.KeyStateHandler()

	def update(self, dtime):
		self.dx = 0
		self.dy = 0
		if (self.key_handler[key.W]):
			self.dy += 1
		if (self.key_handler[key.S]):
			self.dy += -1
		if (self.key_handler[key.A]):
			self.dx += -1
		if (self.key_handler[key.D]):
			self.dx += 1
		if (self.dx != 0 and self.dy != 0):
			self.dx *= 0.7071
			self.dy *= 0.7071
		self.move_to(
			self.x + self.speed * self.dx * dtime,
			self.y + self.speed * self.dy * dtime)


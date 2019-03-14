import pyglet
from vecrec import Rect
from vecrec import Vector

import tile
from entity import Entity
from tile import Tile


TILE_WIDTH = 32
IMAGE_SIZE = (TILE_WIDTH, TILE_WIDTH)


images = {}
tile_classes = {}
enitity_classes = {}

game_world = None


current_mod_name = None
_bin = pyglet.image.atlas.TextureBin()
_tmp_dir = ''


def log(text):
	print(f'[{pyglet.clock.time.strftime("%T")}] {text}')


def on_server():
	return False


def mod_name(name):
	global current_mod_name
	current_mod_name = name


def register_image(name, filename, path=None, size=IMAGE_SIZE):
	image = pyglet.image.load((_tmp_dir+'/assets' if path == None else path) + '/' + filename)
	image = _bin.add(image)
	image.width, image.height = size
	image.anchor_x = image.width/2
	image.anchor_y = image.height/2
	images[name] = image


def register_tile(name, data):
	data.tile_id = name
	tile_classes[name] = data


def register_entity(name, data):
	enitity_classes[name] = data


import pyglet
from pyglet.gl import *
from pyglet.window import key
import numpy

import api
import loader
import world
import camera
import entity

api.log('(game) Start init')
pyglet.clock.tick()

window = pyglet.window.Window(width=800, height=800, vsync=0, caption='Tile game', resizable=True)
main_batch = pyglet.graphics.Batch()
hud_batch = pyglet.graphics.Batch()
api.main_batch = main_batch


mods = loader.load_mods_zip()


objects_group = pyglet.graphics.OrderedGroup(0)
api.objects_group = objects_group
tex_group = pyglet.graphics.TextureGroup(api.images['default:wall'])


# opengl stuff
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glClearColor(0.145, 0.145, 0.145, 1)

player = entity.MainPlayer(x=2, y=2, batch=main_batch, group=objects_group)
window.push_handlers(player.key_handler)

labels = {'fps': pyglet.text.Label('fps',
	x=window.width-10,
	y=window.height-10,
	anchor_x='right',
	anchor_y='top',
	font_name='consolas',
	font_size=15,
	batch=hud_batch),
		'scale': pyglet.text.Label('scale',
	x=window.width-10,
	y=window.height-30,
	anchor_x='right',
	anchor_y='top',
	font_name='consolas',
	font_size=15,
	batch=hud_batch),
		'x': pyglet.text.Label('x',
	x=window.width-10,
	y=window.height-50,
	anchor_x='right',
	anchor_y='top',
	font_name='consolas',
	font_size=15,
	batch=hud_batch),
		'y': pyglet.text.Label('y',
	x=window.width-10,
	y=window.height-70,
	anchor_x='right',
	anchor_y='top',
	font_name='consolas',
	font_size=15,
	batch=hud_batch)}

# follows the player's sprite
camera = camera.Camera(window, player.sprite)
window.push_handlers(camera)

#loaded_world = world.load('default_world')
loaded_world = world.load('gigamir')
#loaded_world = world.World(width=512, height=512)

api.game_world = loaded_world

loaded_world.objects[player.uuid] = player
loaded_world.spawn(2, 2, 'test:zombie')

def gen_vertex(x=0, y1=0):
	vertex_data = []
	texture_data = []
	for i in range(loaded_world.height):
		y2 = y1 + api.TILE_WIDTH
		x1 = x
		for j in range(loaded_world.width):
			x2 = x1 + api.TILE_WIDTH
			vertex_data.extend([x1, y1, x2, y1, x2, y2, x1, y2])
			texture_data.extend(api.images[loaded_world.get_tile(j, i).image].tex_coords)
			x1 = x2
		y1 = y2
	return vertex_data, texture_data

vertex_data, texture_data = gen_vertex()
v = main_batch.add(
	loaded_world.width * loaded_world.height * 4,
	GL_QUADS,
	tex_group,
	('v2f', vertex_data),
	('t3f', texture_data))


@window.event
def on_draw():
	window.clear()

	glPushMatrix()
	camera.draw()
	main_batch.draw()
	glPopMatrix()

	hud_batch.draw()


@window.event
def on_resize(width, height):
	for i, name in enumerate(labels):
		labels[name].x = window.width - 10
		labels[name].y = window.height - 10 - 20*i


def on_key_press(symbol, mods):
	pass
window.on_key_press = on_key_press


def update(dtime):
	for obj_uuid in loaded_world.objects:
		loaded_world.objects[obj_uuid]._update(dtime)
	camera.update(dtime)
	player._update(dtime)
	labels['fps'].text = f'FPS: {pyglet.clock.get_fps():.0f}'
	labels['scale'].text = f'scale: {camera.scale:.2f}'
	labels['x'].text = f'x: {player.x:.3f}'
	labels['y'].text = f'y: {player.y:.3f}'


if (__name__ == '__main__'):
	pyglet.clock.schedule_interval(update, 1/60)
	api.log(f'(game) Init done')
	api.log(f'(game) Total time: {pyglet.clock.tick():.3f}s')
	pyglet.app.run()
	api.log('(game) Exiting...')

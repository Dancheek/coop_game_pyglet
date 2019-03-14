import time
import numpy
import math

import tile
import api
import loader
import entity

#TODO: rework, maybe use DB like sqlite

class World:
	def __init__(self, world_dict={}, width=32, height=32, fill_tile='default:floor'):
		if (world_dict == {}):
			world_dict['spawn_point'] = (1, 1)
			world_dict['players'] = {}
			world_dict['objects'] = {}
			world_dict['tile_map'] = []

			api.log('generating world...')
			for i in range(width):
				world_dict['tile_map'].append([])
				for j in range(height):
					world_dict['tile_map'][i].append({'id': fill_tile, 'meta': {}})

		self.spawn_point = world_dict['spawn_point']
		self.players = world_dict['players']
		self.objects_from_dict(world_dict['objects'])
		self.tile_map_from_dict(world_dict['tile_map'])

	# -------- tiles ---------

	def tile_map_from_dict(self, tile_map):
		api.log('(world) memory allocating...')
		self.tile_map = numpy.empty(numpy.shape(tile_map), dtype=tile.Tile)
		self.height, self.width = self.tile_map.shape

		api.log('(world) tiles initialisation...')
		start_time = time.time()
		for y in range(self.height):
			for x in range(self.width):
				self.set_tile(x, y, tile_map[y][x]['id'], meta=tile_map[y][x]['meta'])
		api.log('(world) done')
		end_time = time.time()
		api.log(f'(world) Total time: {end_time-start_time:.3f}s')
		api.log(f'(world) Average speed: {(self.width*self.height)/(end_time-start_time)/1000:.3f} tiles/ms')

	def tile_map_to_dict(self):
		return [[tile.to_dict() for tile in row] for row in self.tile_map]

	def get_tile(self, x, y):
		int_x = math.floor(x)
		int_y = math.floor(y)
		if (self.is_outside(int_x, int_y)):
			api.log(f'(world) called get_tile({x}, {y}) method')
			return None
		return self.tile_map[y][x]

	def set_tile(self, x, y, tile_id, meta=None):
		self.tile_map[y][x] = api.tile_classes[tile_id](meta=meta)
		self.tile_map[y][x].on_init(x, y)
		if (api.on_server()):
			api.server.update_tile(x, y)

	# ------- objects --------

	def is_outside(self, x, y):
		if (x < 0):					return True
		if (x >= self.width):		return True
		if (y < 0):					return True
		if (y >= self.height):		return True
		return False

	def check_collide(self, x, y, width):
		x_min = math.floor(x - width / 2)
		x_max = math.floor(x + width / 2)
		y_min = math.floor(y - width / 2)
		y_max = math.floor(y + width / 2)

		# если игрок стоит вплотную к стене, мы не должны считать, что он стоит в стене
		if (x_max == x + width / 2): x_max -= 1
		if (y_max == y + width / 2): y_max -= 1

		for i in range(y_min, y_max + 1):
			for j in range(x_min, x_max + 1):
				if (self.is_outside(j, i) or self.get_tile(j, i).is_wall):
					return True
		return False

	def objects_from_dict(self, objects):
		self.objects = {}
		for obj in objects:
			self.spawn(
				objects[obj]['x'],
				objects[obj]['y'],
				objects[obj]['id'],
				meta=objects[obj]['meta'],
				uuid=obj)

	def objects_to_dict(self):
		return {self.objects[obj].uuid: self.objects[obj].to_dict() for obj in self.objects}

	def get_object(self, uuid):
		return self.objects[uuid]

	def get_object_by_pos(self, x, y):
		for uuid in self.objects:
			obj = self.get_object(uuid)
			if (obj.x == x and obj.y == y):
				return obj
		return None

	def spawn(self, x, y, entity_id, meta=None, uuid=None):
		new_entity = api.enitity_classes[entity_id](x, y,
			meta=meta,
			uuid=uuid,
			batch=api.main_batch,
			group=api.objects_group)

		new_entity.on_init()

		self.objects[new_entity.uuid] = new_entity
		if (api.on_server()):
			api.server.send_objects()
		return new_entity.uuid

	def objects_update(self):
		for uuid in self.objects:
			if (self.get_object(uuid).update != None):
				self.get_object(uuid).update(self.get_object(uuid), api.delta_time)

	def add_player(self, player):
		self.players[player.nickname] = player.to_dict()
		self.objects[player.uuid] = player
		player.x = self.spawn_point[0]
		player.y = self.spawn_point[1]

	# --------- world ---------

	def to_dict(self):
		return {'spawn_point': self.spawn_point,
				'players': self.players,
				'tile_map': self.tile_map_to_dict(),
				'objects': self.objects_to_dict()}

	def save_as(self, name):
		world_dict = self.to_dict()

		for uuid in world_dict['objects']:
			obj = self.get_object(uuid)
			if (obj.id == 'default:player'):
				world_dict['players'][obj.nickname] = obj.to_dict()

		world_dict['objects'] = {uuid: world_dict['objects'][uuid] for uuid in world_dict['objects'] if world_dict['objects'][uuid]['id'] != 'default:player'}
		loader.save_world(world_dict, name)


def load(world_name):
	return World(loader.load_world(world_name))

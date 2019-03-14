import api


class Tile:
	def __init__(self, meta=None):
		if (not hasattr(self, 'image')):
			self.image = self.tile_id

		if (meta != None):
			self.meta = meta
		else:
			self.meta = {}

	def on_init(self, x, y):
		pass

	def on_interact(self, x, y, player):
		pass

		#self.on_step = data.get('on_step')

		#self.on_try_to_step = data.get('on_try_to_step')

	def from_dict(self, d):
		for i in d['meta']:
			if (i == 'storage'):
				self.meta['storage'].from_dict(d['meta']['storage'])
			else:
				self.meta[i] = d['meta'][i]
		for attr in d:
			if (attr != 'meta'):
				setattr(self, attr, d[attr])

	def to_dict(self):
		d =  {
			'id'	: self.tile_id,
			'meta'	: self.meta.copy()
		}
		if (d['meta'].get('storage') != None):
			d['meta']['storage'] = d['meta']['storage'].to_dict()
		return d


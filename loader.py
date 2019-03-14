from importlib.util import spec_from_file_location, module_from_spec
from os import listdir
from os.path import splitext, exists, isdir, basename
from tempfile import TemporaryDirectory
import zipfile
import pickle
import api


def load_mods(path='mods'):
	mods = []

	if (exists(path) and isdir(path)):
		files = listdir(path)
		for filename in files:
			if (splitext(filename)[1] in ('.py', '.pyc')):
				spec = spec_from_file_location('mod_' + filename.split('.')[0], path + '/' + filename)
				mod = module_from_spec(spec)
				spec.loader.exec_module(mod)
				mods.append(mod)
	return mods


def load_mod(filename):
	spec = spec_from_file_location(filename.split('.')[0], filename)
	mod = module_from_spec(spec)
	spec.loader.exec_module(mod)
	api.log(f'(loader/mod) {api.current_mod_name!r}')
	return mod


def load_mods_zip(path='mods'):
	api.log(f'(loader) Loading mods from {path!r} directory...')
	mods = []
	if (exists(path) and isdir(path)):
		files = listdir(path)
		for filename in files:
			if (zipfile.is_zipfile(path + '/' + filename)):
				mod = load_mod_zip(path + '/' + filename)
				mods.append(mod)
	return mods


def load_mod_zip(path):
	api.log(f'(loader) Mod from {path!r}')
	with TemporaryDirectory() as tmp_dir:
		with zipfile.ZipFile(path) as zip_ref:
			api._tmp_dir = tmp_dir
			zip_ref.extractall(tmp_dir)
			try:
				return load_mod(tmp_dir + '/main.py')
			except Exception as exception:
				api.log(f"(loader)[ERROR] While loading mod in {path!r}, occured an exception:")
				api.log(f'(loader)[ERROR] {exception}')
				raise exception


def load_world(name):
	api.log(f'(loader) loading world {name!r}...')
	with open('worlds/' + name, 'rb') as file:
		return pickle.load(file)


def save_world(world, name):
	with open('worlds/' + name, 'wb') as file:
		pickle.dump(world, file)

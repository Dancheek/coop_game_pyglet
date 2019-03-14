#!/usr/bin/env python
from shutil import make_archive
from os import listdir, chdir
from os.path import isdir

chdir('mods')
for dirname in listdir():
	print(dirname, end = ': ')
	if (isdir(dirname)):
		print('making archive... ', end = '')
		make_archive(dirname, 'zip', dirname)
		print('done.')
	else:
		print('skipping')

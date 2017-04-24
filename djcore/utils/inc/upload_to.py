import os
from random import choice
from string import ascii_letters
from hashlib import md5
from datetime import datetime

def generate_rand_str(length=32):
	return ''.join([choice(ascii_letters) for i in range(length)])


def upload_to(*path):
	'''
		example: 'date _ time', 'name - hash16 rand2 . ext'
	'''
	def wrapper(instance, filename):
		f_name, f_ext = filename.split('.')
		now = datetime.now()
		result = []
		for component in path:
			folder = []
			for subcomponent in component.split():
				if subcomponent == 'date':
					folder.append(now.strftime('%Y-%m-%d'))
				elif subcomponent == 'time':
					folder.append(now.strftime('%H-%M'))
				elif subcomponent.startswith('%'):
					folder.append(now.strftime(subcomponent))
				
				elif subcomponent == 'name':
					folder.append(f_name)
				elif subcomponent == 'ext':
					folder.append(f_ext)
				
				elif subcomponent.startswith('rand'):
					k = int(subcomponent[4:])
					folder.append(generate_rand_str(k))
				
				elif subcomponent.startswith('hash'):
					k = subcomponent[4:]
					k = int(k) if k.isdigit() else 64
					md5_handler = md5()
					md5_handler.update(filename.encode())
					folder.append(md5_handler.hexdigest()[:k])
				
				else:
					folder.append(subcomponent)
			result.append(''.join(folder))
		return os.path.join(*result)
	return wrapper


if __name__ == '__main__':
	f = upload_to('date', 'time ( %p )', 'name hash16 - rand2 . ext')
	print(f('', 'lol.png'))

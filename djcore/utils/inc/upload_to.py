import os
from random import choice
from string import ascii_letters
from hashlib import md5

from django.utils import timezone as datetime
try:
    datetime.now()
except:
    from datetime import datetime


class upload_to:
    '''
        example: 'date _ time', 'name - hash16 rand2 . ext'
    '''
    
    def __init__(self, *path):
        self.path = tuple([tuple(component.split()) for component in path])
    
    @staticmethod
    def generate_rand_str(length=32):
        return ''.join([choice(ascii_letters) for i in range(length)])
    
    @staticmethod
    def get_hash(filename, length=64):
        md5_handler = md5()
        md5_handler.update(filename.encode())
        return md5_handler.hexdigest()[:length]
    
    def get_path_component(self, subcomponent, now, filename):
        if subcomponent == 'date':
            return now.strftime('%Y-%m-%d')
        if subcomponent == 'time':
            return now.strftime('%H-%M')
        if subcomponent.startswith('%'):
            return now.strftime(subcomponent)
        
        f_name, f_ext = filename.split('.')
        if subcomponent == 'name':
            return f_name
        if subcomponent == 'ext':
            return f_ext
        
        if subcomponent.startswith('rand'):
            k = int(subcomponent[4:])
            return self.generate_rand_str(k)
        
        if subcomponent.startswith('hash'):
            k = subcomponent[4:]
            k = int(k) if k.isdigit() else 64
            f_hash = self.get_hash(filename, k)
            return f_hash
        
        return subcomponent
    
    def __call__(self, instance, filename):
        now = datetime.now()
        result = []
        for component in self.path:
            folder = []
            for subcomponent in component:
                folder.append(self.get_path_component(subcomponent, now, filename))
            result.append(''.join(folder))
        return os.path.join(*result)


if __name__ == '__main__':
    f = upload_to('date', 'time ( %p )', 'name hash16 - rand2 . ext')
    print(f('', 'lol.png'))

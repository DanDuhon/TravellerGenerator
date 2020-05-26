import pickle
import random
import json


class System:
    def __init__(self):
        self.property_list = ['starcount', 'stars']
        self.starcount = random.randint(1,3)
        self.stars = []
        for x in range(self.starcount):
            self.stars.append(Star())

    def save(self, filename):
        save_dict = {key:getattr(self, key) for key in self.property_list}
        with open(filename, 'w') as f:
            json.dump(save_dict, f, sort_keys=True, default=lambda x: x.save())

    def load(self, filename):
        print("sc1", getattr(self, 'starcount'))
        for key in self.property_list:
            delattr(self, key)
        print("sc2", getattr(self, 'starcount', None))
        with open(filename, 'r') as f:
            loaded = json.load(f)
        for key in self.property_list:
            setattr(self, key, loaded[key])
        print("sc3", getattr(self, 'starcount'))

class Star:
    def __init__(self, loaded=None):
        self.property_list = ['lumin', 'planets']
        if loaded:
            for key in self.property_list:
                setattr(self, key, loaded[key])
            return
        self.lumin = 15
        self.planets = []
        for x in range(5):
            self.planets.append(Planet(star=self))

    def report_lumin(self):
        print(lumin)

    def save(self):
        save_dict = {key:getattr(self, key) for key in self.property_list}
        save_dict['save_type'] = 'star'
        return save_dict

class Planet:
    def __init__(self, star=None, loaded=None):
        self.property_list = ['size']
        if loaded:
            for key in self.property_list:
                setattr(self, key, loaded[key])
        self.size = random.randint(1,5)
        self.star = star

    def save(self):
        save_dict = {key:getattr(self, key) for key in self.property_list}
        save_dict['save_type'] = 'planet'
        return save_dict

system = System()
system.save('file1.trav')
system = System()
system.save('file2.trav')
system.load('file1.trav')
system.save('file3.trav')
pickle.dump(system, open('pfile1.trav', "wb"), protocol=0)

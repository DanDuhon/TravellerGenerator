import random
import json


class System:
    def __init__(self):
        self.starcount = random.randint(1,3)
        self.stars = []
        for x in range(self.starcount):
            self.stars.append(Star())
        self.property_list = ['starcount', 'stars']

    def save(self, filename):
        save_dict = {key:self[key] for key in self.property_list}
        with open(filename, 'w') as f:
            json.dump(save_dict, f, sort_keys=True, default=lambda x: x.save())

    def load(self, filename):
        print("sc1", self.get('starcount'))
        for key in self.property_list:
            del self[key]
        print("sc2", self.get('starcount'))
        with open(filename, 'r') as f:
            loaded = json.load(f)
        self.starcount = loaded['starcount']
        self.stars = [Star(load=star) for star in loaded['stars']]
        print("sc3", self.get('starcount'))

class Star:
    def __init__(self, loaded=None):
        if loaded:
            self.lumin = loaded['lumin']
            self.planets = [Planet(star=self, loaded=planet) for planet in
                    loaded['planets'])
            return
        self.lumin = 15
        self.planets = []
        for x in range(5):
            self.planets.append(Planet(star=self))

    def report_lumin(self):
        print(lumin)

    def save(self):
        save_dict = {}
        save_dict['lumin'] = self.lumin
        save_dict['planets'] = self.planets
        return save_dict

class Planet:
    def __init__(self, star=None, loaded=None):
        if loaded:
            self.size = loaded['size']
            self.star = star
            return
        self.size = random.randint(1,5)
        self.star = star

    def save(self):
        save_dict = {}
        save_dict['size'] = self.size
        return save_dict

system = System()
system.save('file1.trav')
system = System()
system.save('file2.trav')
system.load('file1.trav')
system.save('file3.trav')

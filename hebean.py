from globalstuff import category, className, type, roll_xdy, coin_flip
from dwarfplanet import DwarfPlanet


class Hebean(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Hebean
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Geotidal
        self.type = (type.Hebean if coin_flip else type.Idunnian)


    def set_atmosphere(self):
        roll = roll_xdy(1, 6) + self.size - 6
        self.atmosphere = max(0, (10 if roll >= 2 else roll))
        

    def set_hydrosphere(self):
        self.hydrosphere = max(roll_xdy(2, 6) + self.size - 11)


    def set_biosphere(self):
        self.biosphere = 0

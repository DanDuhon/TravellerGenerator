from globalstuff import category, className, roll_xdy, coin_flip
from helianplanet import HelianPlanet


class Helian(HelianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Helian
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = (className.GeoHelian if coin_flip else className.Nebulous)


    def set_atmosphere(self):
        self.atmosphere = 13
        

    def set_hydrosphere(self):
        roll = roll_xdy(1, 6)
        if roll <= 2:
            self.hydrosphere = 0
        elif roll <= 4:
            self.hydrosphere = roll_xdy(1, 6) - 1
        else:
            self.hydrosphere = 15


    def set_biosphere(self):
        self.biosphere = 0

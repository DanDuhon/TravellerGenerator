from globalstuff import category, className, type, roll_xdy, coin_flip
from terrestrialplanet import TerrestrialPlanet


class Telluric(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Telluric
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Telluric
        self.type = (type.Phosphorian if coin_flip else type.Cytherean)


    def set_atmosphere(self):
        self.atmosphere = 12
        

    def set_hydrosphere(self):
        self.hydrosphere = (0 if roll_xdy(1, 6) <= 4 else 15)


    def set_biosphere(self):
        self.biosphere = 0

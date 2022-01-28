from globalstuff import category, className, coin_flip, type
from terrestrialplanet import TerrestrialPlanet


class JaniLithic(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.JaniLithic
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Epistellar
        self.type = type.JaniLithic


    def set_atmosphere(self):
        if coin_flip:
            self.atmosphere = 1
        else:
            self.atmosphere = 10
        

    def set_hydrosphere(self):
        self.hydrosphere = 0


    def set_biosphere(self):
        self.biosphere = 0

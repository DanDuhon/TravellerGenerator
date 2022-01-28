from globalstuff import category, className
from jovianplanet import JovianPlanet


class Chthonian(JovianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Chthonian
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Chthonian


    def set_atmosphere(self):
        self.atmosphere = 1
        

    def set_hydrosphere(self):
        self.hydrosphere = 0


    def set_biosphere(self):
        self.biosphere = 0

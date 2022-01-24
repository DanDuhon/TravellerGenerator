from dwarfplanet import DwarfPlanet


class Vesperian(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = "Geopassive"
        self.type = "Stygian"


    def set_atmosphere(self):
        self.atmosphere = 0
        

    def set_hydrosphere(self):
        self.hydrosphere = 0


    def set_biosphere(self):
        self.biosphere = 0

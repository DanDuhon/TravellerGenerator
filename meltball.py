from globalstuff import LookupTable, category, className, type, roll_xdy
from dwarfplanet import DwarfPlanet


chemistryTable = LookupTable(
    (3, LookupTable(
        (2, (None, None, className.Geothermic, type.Phaethonic)),
        (4, (None, None, className.Geothermic, type.Apollonian)),
        (100, (None, None, className.Geothermic, type.Sethian)))),
    (100, LookupTable(
        (3, (None, None, className.Geotidal, type.Hephaestian)),
        (100, (None, None, className.Geotidal, type.Lokian)))))


class Meltball(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Meltball
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        r = chemistryTable[roll_xdy(1, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        self.atmosphere = 1
        

    def set_hydrosphere(self):
        self.hydrosphere = 15


    def set_biosphere(self):
        self.biosphere = 0

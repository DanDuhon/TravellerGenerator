from globalstuff import LookupTable, roll_xdy, category, className, type, luminosityClass, orbitType
from dwarfplanet import DwarfPlanet


chemistryTable = LookupTable(
    (2, (None, None, className.Geopassive, type.Ferrinian)),
    (4, (None, None, className.Geopassive, type.Lithic)),
    (100, (None, None, className.Geopassive, type.Carbonian)))


class Rockball(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Rockball
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
        self.atmosphere = 0
        

    def set_hydrosphere(self):
        roll = roll_xdy(2, 6)
        if self.star.luminosityClass == luminosityClass.L:
            roll += 1
        if self.orbitType == orbitType.Epistellar:
            roll -= 2
        elif self.orbitType == orbitType.OuterZone:
            roll += 2

        self.hydrosphere = max(0, roll_xdy(2, 6) + self.size - 11)


    def set_biosphere(self):
        self.biosphere = 0

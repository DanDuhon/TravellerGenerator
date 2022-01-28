from globalstuff import LookupTable, roll_xdy, coin_flip, category, className, type, luminosityClass, orbitType, chemistry
from dwarfplanet import DwarfPlanet


chemistryTable = LookupTable(
    (4, (chemistry.Water, 0, className.Geopassive, type.Gelidian)),
    (6, (chemistry.Ammonia, 1, className.Geothermic, type.Erisian)),
    (100, (chemistry.Methane, 3, className.Geotidal, type.Plutonian)))


class Snowball(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Snowball
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        roll = roll_xdy(1, 6)
        if self.star.luminosityClass == luminosityClass.L:
            roll += 2
        if self.orbitType == orbitType.OuterZone:
            roll += 2
            
        r = chemistryTable[roll]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        self.atmosphere = (0 if roll_xdy(1, 6) <= 4 else 1)
        

    def set_hydrosphere(self):
        if coin_flip:
            self.hydrosphere = roll_xdy(2, 6) - 2
            self.subsurfaceOceans = True
        else:
            self.hydrosphere = 10


    def set_biosphere(self):
        if not self.subsurfaceOceans:
            self.biosphere = 0
            return

        if self.systemHex.age >= 6 + self.ageModifier:
            self.biosphere = max(0, roll_xdy(1, 6) + self.size - 2)
        elif self.systemHex.age >= roll_xdy(1, 6):
            self.biosphere = max(0, roll_xdy(1, 6) - 3)

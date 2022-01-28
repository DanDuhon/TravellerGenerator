from globalstuff import LookupTable, roll_xdy, category, className, type, luminosityClass, orbitType, chemistry
from dwarfplanet import DwarfPlanet


chemistryTable = LookupTable(
    (4, (chemistry.Water, 0, className.Geotidal, type.Promethean)),
    (6, (chemistry.Ammonia, 1, className.Geotidal, type.Burian)),
    (100, (chemistry.Methane, 3, className.Geotidal, type.Atlan)))


class Promethean(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Promethean
        self.set_chemistry_age_modifier_class_type()
        self.set_hydrosphere()
        self.set_biosphere()
        self.set_atmosphere()


    def set_chemistry_age_modifier_class_type(self):
        roll = roll_xdy(1, 6)
        if self.star.luminosityClass == luminosityClass.L:
            roll += 2
        if self.orbitType == orbitType.Epistellar:
            roll -= 2
        elif self.orbitType == orbitType.OuterZone:
            roll += 2

        r = chemistryTable[roll]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        if self.biosphere >= 3 and self.chemistry == chemistry.Water:
            self.atmosphere(max(2, min(9, roll_xdy(2, 6) + self.size - 7)))
        else:
            self.atmosphere = 10
        

    def set_hydrosphere(self):
        self.hydrosphere = roll_xdy(2, 6) - 2


    def set_biosphere(self):
        if self.systemHex.age >= 4 + self.ageModifier:
            self.biosphere = roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0)
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

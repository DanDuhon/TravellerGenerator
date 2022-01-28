from globalstuff import LookupTable, roll_xdy, luminosityClass, orbitType, chemistry, className, type, category
from terrestrialplanet import TerrestrialPlanet


chemistryTable = LookupTable(
    (6, (chemistry.Water, 0, className.Arid, type.Darwinian)),
    (8, (chemistry.Ammonia, 1, className.Arid, type.Saganian)),
    (100, (chemistry.Methane, 3, className.Arid, type.Asimovian)))


class Arid(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Arid
        self.set_chemistry_age_modifier_class_type()
        self.set_hydrosphere()
        self.set_biosphere()
        self.set_atmosphere()


    def set_chemistry_age_modifier_class_type(self):
        roll = roll_xdy(1, 6)
        if self.star.luminosityClass == luminosityClass.L:
            roll += 5
        elif self.star.luminosityClass == luminosityClass.K_V:
            roll += 2
        elif self.star.luminosityClass == luminosityClass.M_V:
            roll += 4

        if self.orbitType == orbitType.OuterZone:
            roll += 2

        r = chemistryTable[roll]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        if self.biosphere >= 3 and self.chemistry == chemistry.Water:
            self.atmosphere = max(0, min(9, roll_xdy(2, 6) - 7 + self.size))
        else:
            self.atmosphere = 10
        

    def set_hydrosphere(self):
        self.hydrosphere = roll_xdy(1, 3)


    def set_biosphere(self):
        if self.systemHex.age >= 4 + self.ageModifier:
            self.biosphere = roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0)
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

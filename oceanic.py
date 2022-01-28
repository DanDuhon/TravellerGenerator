from globalstuff import LookupTable, category, className, type, roll_xdy, luminosityClass, orbitType, chemistry
from terrestrialplanet import TerrestrialPlanet


chemistryTable = LookupTable(
    (6, LookupTable(
        (3, (chemistry.Water, 0, className.Oceanic, type.Pelagic)),
        (100, (chemistry.Water, 0, className.Tectonic, type.BathyGaian)))),
    (8, LookupTable(
        (3, (chemistry.Ammonia, 1, className.Oceanic, type.Nunnic)),
        (100, (chemistry.Ammonia, 1, className.Tectonic, type.BathyAmunian)))),
    (100, LookupTable(
        (3, (chemistry.Methane, 3, className.Oceanic, type.Teathic)),
        (100, (chemistry.Methane, 3, className.Tectonic, type.BathyTartarian)))))


class Oceanic(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Oceanic
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def lookup_chemistry(self, roll, roll2):
        r = chemistryTable[roll][roll2]
        return r[0], r[1], r[2], r[3]


    def set_chemistry_age_modifier_class_type(self):
        roll = roll_xdy(1, 6)
        if self.star.luminosityClass == luminosityClass.K_V:
            roll += 2
        elif self.star.luminosityClass == luminosityClass.M_V:
            roll += 4
        elif self.star.luminosityClass == luminosityClass.L:
            roll += 5

        if self.orbitType == orbitType.OuterZone:
            roll += 2

        r = chemistryTable[roll][roll_xdy(1, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        if self.chemistry == chemistry.Water:
            roll = roll_xdy(2, 6)
            if self.star.luminosityClass == luminosityClass.K_V:
                roll -= 1
            elif self.star.luminosityClass == luminosityClass.M_V:
                roll -= 2
            elif self.star.luminosityClass == luminosityClass.L:
                roll -= 3
            elif self.star.luminosityClass in [luminosityClass.F_IV, luminosityClass.G_IV, luminosityClass.K_IV]:
                roll -= 1

            self.atmosphere = max(0, min(12, roll))
        else:
            roll = roll_xdy(1, 6)

            if roll <= 1:
                self.atmosphere = 1
            elif roll <= 4:
                self.atmosphere = 10
            else:
                self.atmosphere = 12
        

    def set_hydrosphere(self):
        self.hydrosphere = 11


    def set_biosphere(self):
        if self.systemHex.age >= 4 + self.ageModifier:
            max(0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0))
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

from globalstuff import LookupTable, roll_xdy, category, className, type, luminosityClass, orbitType, chemistry
from terrestrialplanet import TerrestrialPlanet


chemistryTable = LookupTable(
    (8, LookupTable(
        (8, (chemistry.Water, 0, className.Tectonic, type.Gaian)),
        (11, (chemistry.Sulfur, 0, className.Tectonic, type.ThioGaian)),
        (100, (chemistry.Chlorine, 0, className.Tectonic, type.ChloriticGaian)))),
    (11, LookupTable((100, (chemistry.Ammonia, 1, className.Tectonic, type.Amunian)))),
    (100, LookupTable((100, (chemistry.Methane, 3, className.Tectonic, type.Tartarian)))))


class Tectonic(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Tectonic
        self.set_chemistry_age_modifier_class_type()
        self.set_hydrosphere()
        self.set_biosphere()
        self.set_atmosphere()


    def set_chemistry_age_modifier_class_type(self):
        roll = roll_xdy(1, 6)
        if self.star.luminosityClass == luminosityClass.K_V:
            roll += 2
        elif self.star.luminosityClass == luminosityClass.M_V:
            roll += 4
        elif self.star.lumiosityClass == luminosityClass.L:
            roll += 5
        if self.orbitType == orbitType.OuterZone:
            roll += 2

        r = chemistryTable[roll][roll_xdy(2, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        if self.biosphere >= 3:
            if self.chemistry == chemistry.Water:
                self.atmosphere = max(2, min(9, roll_xdy(2, 6) + self.size - 7))
            elif self.chemistry in [chemistry.Sulfur, chemistry.Chlorine]:
                self.atmosphere = 11
        else:
            self.atmosphere = 10
        

    def set_hydrosphere(self):
        self.hydrosphere = roll_xdy(2, 6) - 2


    def set_biosphere(self):
        if self.systemHex.age >= 4 + self.ageModifier:
            self.biosphere = max(0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0))
        else:
            self.biosphere = 0

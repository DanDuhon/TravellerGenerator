from globalstuff import LookupTable, category, className, type, roll_xdy, luminosityClass, orbitType, chemistry
from terrestrialplanet import TerrestrialPlanet


chemistryTable = LookupTable(
    (6, LookupTable(
        (3, ("Water", 0, "Oceanic", "Pelagic")),
        (100, ("Water", 0, "Tectonic", "Bathy-Gaian")))),
    (8, LookupTable(
        (3, ("Ammonia", 1, "Oceanic", "Nunnic")),
        (100, ("Ammonia", 1, "Tectonic", "Bathy-Amunian")))),
    (100, LookupTable(
        (3, ("Methane", 3, "Oceanic", "Teathic")),
        (100, ("Methane", 3, "Tectonic", "Bathy-Tartarian")))))


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

        self.chemistry, self.ageModifier, self.className, self.type = self.lookup_chemistry(roll, roll_xdy(1, 6))


    def set_atmosphere(self):
        self.atmosphere = 0
        

    def set_hydrosphere(self):
        self.hydrosphere = 0


    def set_biosphere(self):
        self.biosphere = 0

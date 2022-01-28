from globalstuff import LookupTable, category, className, chemistry, luminosityClass, roll_xdy
from helianplanet import HelianPlanet


chemistryTable = LookupTable(
    (6, LookupTable(
        (8, (chemistry.Water, 0, className.Panthalassic, None)),
        (11, (chemistry.Sulfur, 0, className.Panthalassic, None)),
        (100, (chemistry.Chlorine, 0, className.Panthalassic, None)))),
    (8, LookupTable((100, (chemistry.Methane, 1, className.Panthalassic, None)))),
    (100, LookupTable((100, (chemistry.Methane, 3, className.Panthalassic, None)))))


class Panthalassic(HelianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Panthalassic
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        roll = roll_xdy(1, 6)
        if self.star.luminosityClass == luminosityClass.K_V:
            roll += 2
        elif self.star.luminosityClass == luminosityClass.M_V:
            roll += 4
        elif self.star.luminosityClass == luminosityClass.L:
            roll += 5

        r = chemistryTable[roll][roll_xdy(2, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        self.atmosphere = min(13, roll_xdy(1, 6) + 8)
        

    def set_hydrosphere(self):
        self.hydrosphere = 11


    def set_biosphere(self):
        if self.systemHex.age >= 4 + self.ageModifier:
            self.biosphere = roll_xdy(2, 6)
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

from globalstuff import LookupTable, roll_xdy, category, className, type, chemistry
from terrestrialplanet import TerrestrialPlanet


chemistryTable = LookupTable(
    (11, (chemistry.Water, None, className.Epistellar, type.Vesperian)),
    (100, (chemistry.Chlorine, None, className.Epistellar, type.Vesperian)))


class Vesperian(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Vesperian
        self.set_chemistry_age_modifier_class_type()
        self.set_hydrosphere()
        self.set_biosphere()
        self.set_atmosphere()


    def set_chemistry_age_modifier_class_type(self):
        r = chemistryTable[roll_xdy(2, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        if self.biosphere >= 3:
            if self.chemistry == chemistry.Water:
                self.atmosphere = max(2, min(9, roll_xdy(2, 6) + self.size - 7))
            else:
                self.atmosphere = 11
        else:
            self.atmosphere = 10
        

    def set_hydrosphere(self):
        self.hydrosphere = roll_xdy(2, 6) - 2


    def set_biosphere(self):
        if self.systemHex.age >= 4:
            self.biosphere = roll_xdy(2, 6)
        elif self.systemHex.age >= roll_xdy(1, 3):
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

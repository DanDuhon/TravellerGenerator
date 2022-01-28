from globalstuff import LookupTable, roll_xdy, category, className, type, luminosityClass, orbitType, chemistry
from dwarfplanet import DwarfPlanet


chemistryTable = LookupTable(
    (4, (chemistry.Water, 0, className.Geocyclic, type.Arean)),
    (6, (chemistry.Ammonia, 1, className.Geocyclic, type.Utgardian)),
    (100, (chemistry.Methane, 3, className.Geocyclic, type.Titanian)))


class Arean(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Arean
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
        if roll_xdy(1, 6) - (2 if self.star.luminosityClass == luminosityClass.D else 0):
            self.atmosphere = 1
        else:
            self.atmosphere = 10
        

    def set_hydrosphere(self):
        self.hydrosphere = max(0, roll_xdy(2, 3) + self.size - 7 - (4 if self.atmosphere == 1 else 0))


    def set_biosphere(self):
        if self.systemHex.age >= 4 + self.ageModifier and self.atmosphere == 10:
            self.biosphere = max(0, roll_xdy(1, 6) + self.size - 2)
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = max(0, roll_xdy(1, 6) - 4) if self.atmosphere == 1 else roll_xdy(1, 3)
        else:
            self.biosphere = 0

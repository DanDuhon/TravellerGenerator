from globalstuff import LookupTable, category, className, type, roll_xdy, luminosityClass, orbitType, chemistry
from jovianplanet import JovianPlanet


chemistryTable = LookupTable(
    (3, (chemistry.Water, None, className.DwarfJovian, type.Brammian)),
    (100, (chemistry.Ammonia, None, className.DwarfJovian, type.Khonsonian)))


class Jovian(JovianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Jovian
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()
        self.set_chemistry_age_modifier_class_type()
        

    def set_chemistry_age_modifier_class_type(self):
        if self.biosphere > 0:
            roll = roll_xdy(1, 6)
            if self.star.luminosityClass == luminosityClass.L:
                roll += 1
            if self.orbitType == orbitType.Epistellar:
                roll -= 2
            elif self.orbitType == orbitType.OuterZone:
                roll += 2

            r = chemistryTable[roll]
            
            self.chemistry = r[0]
            self.ageModifier = r[1]
            self.className = r[2]
            self.type = r[3]
        else:
            self.className = className.Jovian


    def set_atmosphere(self):
        self.atmosphere = 16
        

    def set_hydrosphere(self):
        self.hydrosphere = 16


    def set_biosphere(self):
        if roll_xdy(1, 6) <= 5:
            self.biosphere = 0
        else:
            if self.systemHex.age >= 7:
                self.biosphere = roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0)
            elif self.systemHex.age >= roll_xdy(1, 6):
                self.biosphere = roll_xdy(1, 3)
            else:
                self.biosphere = 0

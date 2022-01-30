from globalstuff import roll_xdy, coin_flip, group, luminosityClass
from globalstuff import category, className, type, chemistry, orbitType
from globalstuff import LookupTable, starport, terrain


chemistryArean = LookupTable(
    (4, (chemistry.Water, 0, className.Geocyclic, type.Arean)),
    (6, (chemistry.Ammonia, 1, className.Geocyclic, type.Utgardian)),
    (100, (chemistry.Methane, 3, className.Geocyclic, type.Titanian)))

chemistryArid = LookupTable(
    (6, (chemistry.Water, 0, className.Arid, type.Darwinian)),
    (8, (chemistry.Ammonia, 1, className.Arid, type.Saganian)),
    (100, (chemistry.Methane, 3, className.Arid, type.Asimovian)))

chemistryJovian = LookupTable(
    (3, (chemistry.Water, None, className.DwarfJovian, type.Brammian)),
    (100, (chemistry.Ammonia, None, className.DwarfJovian, type.Khonsonian)))

chemistryMeltball = LookupTable(
    (3, LookupTable(
        (2, (None, None, className.Geothermic, type.Phaethonic)),
        (4, (None, None, className.Geothermic, type.Apollonian)),
        (100, (None, None, className.Geothermic, type.Sethian)))),
    (100, LookupTable(
        (3, (None, None, className.Geotidal, type.Hephaestian)),
        (100, (None, None, className.Geotidal, type.Lokian)))))

chemistryOceanic = LookupTable(
    (6, LookupTable(
        (3, (chemistry.Water, 0, className.Oceanic, type.Pelagic)),
        (100, (chemistry.Water, 0, className.Tectonic, type.BathyGaian)))),
    (8, LookupTable(
        (3, (chemistry.Ammonia, 1, className.Oceanic, type.Nunnic)),
        (100, (chemistry.Ammonia, 1, className.Tectonic, type.BathyAmunian)))),
    (100, LookupTable(
        (3, (chemistry.Methane, 3, className.Oceanic, type.Teathic)),
        (100, (chemistry.Methane, 3, className.Tectonic, type.BathyTartarian)))))

chemistryPanthalassic = LookupTable(
    (6, LookupTable(
        (8, (chemistry.Water, 0, className.Panthalassic, None)),
        (11, (chemistry.Sulfur, 0, className.Panthalassic, None)),
        (100, (chemistry.Chlorine, 0, className.Panthalassic, None)))),
    (8, LookupTable((100, (chemistry.Methane, 1, className.Panthalassic, None)))),
    (100, LookupTable((100, (chemistry.Methane, 3, className.Panthalassic, None)))))

chemistryPromethean = LookupTable(
    (4, (chemistry.Water, 0, className.Geotidal, type.Promethean)),
    (6, (chemistry.Ammonia, 1, className.Geotidal, type.Burian)),
    (100, (chemistry.Methane, 3, className.Geotidal, type.Atlan)))

chemistryRockball = LookupTable(
    (2, (None, None, className.Geopassive, type.Ferrinian)),
    (4, (None, None, className.Geopassive, type.Lithic)),
    (100, (None, None, className.Geopassive, type.Carbonian)))

chemistrySnowball = LookupTable(
    (4, (chemistry.Water, 0, className.Geopassive, type.Gelidian)),
    (6, (chemistry.Ammonia, 1, className.Geothermic, type.Erisian)),
    (100, (chemistry.Methane, 3, className.Geotidal, type.Plutonian)))

chemistryTectonic = LookupTable(
    (8, LookupTable(
        (8, (chemistry.Water, 0, className.Tectonic, type.Gaian)),
        (11, (chemistry.Sulfur, 0, className.Tectonic, type.ThioGaian)),
        (100, (chemistry.Chlorine, 0, className.Tectonic, type.ChloriticGaian)))),
    (11, LookupTable((100, (chemistry.Ammonia, 1, className.Tectonic, type.Amunian)))),
    (100, LookupTable((100, (chemistry.Methane, 3, className.Tectonic, type.Tartarian)))))

chemistryVesperian = LookupTable(
    (11, (chemistry.Water, None, className.Epistellar, type.Vesperian)),
    (100, (chemistry.Chlorine, None, className.Epistellar, type.Vesperian)))


acceptableAtmospheres = {
    0: [],
    1: [],
    2: [2, 4],
    3: [3, 5],
    4: [2, 4, 7],
    5: [3, 5, 6],
    6: [5, 6, 8],
    7: [4, 7, 9],
    8: [6, 8],
    9: [7, 9],
    10: [10],
    11: [11],
    12: [12],
    13: [13],
    14: [14]
}


idealAtmospheres = {
    0: [],
    1: [],
    2: [2, 4],
    3: [3, 5],
    4: [4, 7],
    5: [5, 6],
    6: [6, 8],
    7: [7, 9],
    8: [8],
    9: [9],
    10: [10],
    11: [11],
    12: [12],
    13: [13],
    14: [14]
}


starportTable = LookupTable((2, starport.X),
                            (4, starport.E),
                            (6, starport.D),
                            (8, starport.C),
                            (10, starport.B),
                            (100, starport.A))


def create_orbital_body(star,
        order,
        orbitType):
    roll = roll_xdy(1, 6)
    roll -= (1 if star.spectralType == luminosityClass.L else 0)

    if roll <= 1:
        AsteroidBelt(
            star,
            star,
            order,
            orbitType)
    else:
        create_planet(
            star,
            order,
            orbitType,
            roll)


def create_planet(star, order, orbitType, roll):
    if roll <= 2:
        create_dwarf_planet(star, star, order, orbitType)
    elif roll <= 3:
        create_terrestrial_planet(star, star, order, orbitType)
    elif roll <= 4:
        create_helian_planet(star, star, order, orbitType)
    else:
        create_jovian_planet(star, star, order, orbitType)


def create_dwarf_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        Stygian(star, parentObject, order, orbitType)
        return
        
    roll = roll_xdy(1, 6)
    roll2 = roll_xdy(1, 6)

    # If this planet is part of an asteroid belt
    if (star != parentObject
        and (parentObject.group == group.AsteroidBelt
            # If this planet is a companion to another dwarf planet
            # but that dwarf planet is part of an asteroid belt
            or (parentObject.group == group.DwarfPlanet
                and parentObject.parentObject.group == group.AsteroidBelt))):
        roll -= 2

    if orbitType == orbitType.Epistellar:
        create_epistellar_dwarf_planet(star, parentObject, order, orbitType, roll, roll2)
        return
        
    # If this planet is orbiting a helian planet
    if (star != parentObject
        and (parentObject.group == group.HelianPlanet
            # If this planet is a companion to another dwarf planet
            # but that dwarf planet is orbiting a helian planet
            or (parentObject.group == group.DwarfPlanet
                and parentObject.parentObject.group == group.HelianPlanet))):
        roll += 1
    # If this planet is orbiting a jovian planet
    elif (star != parentObject
        and (parentObject.group == group.JovianPlanet
            # If this planet is a companion to another dwarf planet
            # but that dwarf planet is orbiting a jovian planet
            or (parentObject.group == group.DwarfPlanet
                and parentObject.parentObject.group == group.JovianPlanet))):
        roll += 2

    if orbitType == orbitType.InnerZone:
        create_inner_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2)
    elif orbitType == orbitType.OuterZone:
        create_outer_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2)


def create_terrestrial_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        Acheronian(star, parentObject, order, orbitType)
        return
        
    if orbitType == orbitType.Epistellar:
        create_epistellar_terrestrial_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == orbitType.InnerZone:
        create_inner_zone_terrestrial_planet(star, parentObject, order, orbitType, roll_xdy(2, 6))
    elif orbitType == orbitType.OuterZone:
        create_outer_zone_terrestrial_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))


def create_helian_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        Asphodelian(star, parentObject, order, orbitType)
        return
        
    if orbitType == orbitType.Epistellar:
        create_epistellar_helian_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == orbitType.InnerZone:
        create_inner_zone_helian_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == orbitType.OuterZone:
        create_outer_zone_helian_planet(star, parentObject, order, orbitType)


def create_jovian_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        Chthonian(star, parentObject, order, orbitType)
        return
        
    if orbitType == orbitType.Epistellar:
        create_epistellar_jovian_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == orbitType.InnerZone:
        create_inner_zone_jovian_planet(star, parentObject, order, orbitType)
    elif orbitType == orbitType.OuterZone:
        create_outer_zone_jovian_planet(star, parentObject, order, orbitType)


def create_epistellar_dwarf_planet(star, parentObject, order, orbitType, roll, roll2):
    if roll <= 3:
        Rockball(star, parentObject, order, orbitType)
    elif roll <= 5:
        Meltball(star, parentObject, order, orbitType)
    elif roll2 <= 4:
        Hebean(star, parentObject, order, orbitType)
    else:
        Promethean(star, parentObject, order, orbitType)


def create_inner_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2):
    if roll <= 4:
        Rockball(star, parentObject, order, orbitType)
    elif roll <= 6:
        Arean(star, parentObject, order, orbitType)
    elif roll <= 7:
        Meltball(star, parentObject, order, orbitType)
    elif roll2 <= 4:
        Hebean(star, parentObject, order, orbitType)
    else:
        Promethean(star, parentObject, order, orbitType)


def create_outer_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2):
    if roll <= 0:
        Rockball(star, parentObject, order, orbitType)
    elif roll <= 4:
        Snowball(star, parentObject, order, orbitType)
    elif roll <= 6:
        Rockball(star, parentObject, order, orbitType)
    elif roll <= 7:
        Meltball(star, parentObject, order, orbitType)
    elif roll2 <= 3:
        Hebean(star, parentObject, order, orbitType)
    elif roll2 <= 5:
        Arean(star, parentObject, order, orbitType)
    else:
        Promethean(star, parentObject, order, orbitType)


def create_epistellar_terrestrial_planet(star, parentObject, order, orbitType, roll):
    if roll <= 4:
        JaniLithic(star, parentObject, order, orbitType)
    elif roll <= 5:
        Vesperian(star, parentObject, order, orbitType)
    else:
        Telluric(star, parentObject, order, orbitType)


def create_inner_zone_terrestrial_planet(star, parentObject, order, orbitType, roll):
    if roll <= 4:
        Telluric(star, parentObject, order, orbitType)
    elif roll <= 6:
        Arid(star, parentObject, order, orbitType)
    elif roll <= 7:
        Tectonic(star, parentObject, order, orbitType)
    elif roll <= 9:
        Oceanic(star, parentObject, order, orbitType)
    elif roll <= 10:
        Tectonic(star, parentObject, order, orbitType)
    else:
        Telluric(star, parentObject, order, orbitType)


def create_outer_zone_terrestrial_planet(star, parentObject, order, orbitType, roll):
    if parentObject != star and parentObject.group == group.JovianPlanet:
        roll += 2

    if roll <= 4:
        Arid(star, parentObject, order, orbitType)
    elif roll <= 6:
        Tectonic(star, parentObject, order, orbitType)
    else:
        Oceanic(star, parentObject, order, orbitType)


def create_epistellar_helian_planet(star, parentObject, order, orbitType, roll):
    if roll <= 5:
        Helian(star, parentObject, order, orbitType)
    else:
        Panthalassic(star, parentObject, order, orbitType)


def create_inner_zone_helian_planet(star, parentObject, order, orbitType, roll):
    if roll <= 4:
        Helian(star, parentObject, order, orbitType)
    else:
        Panthalassic(star, parentObject, order, orbitType)


def create_outer_zone_helian_planet(star, parentObject, order, orbitType):
    Helian(star, parentObject, order, orbitType)


def create_epistellar_jovian_planet(star, parentObject, order, orbitType, roll):
    if roll <= 5:
        Jovian(star, parentObject, order, orbitType)
    else:
        Chthonian(star, parentObject, order, orbitType)


def create_inner_zone_jovian_planet(star, parentObject, order, orbitType):
    Jovian(star, parentObject, order, orbitType)


def create_outer_zone_jovian_planet(star, parentObject, order, orbitType):
    Jovian(star, parentObject, order, orbitType)

def create_terra(star):
    newPlanet = Tectonic(
        star,
        star,
        star.epistellarOrbits + star.innerZoneOrbits + 1,
        orbitType.InnerZone)

    newPlanet.group = group.TerrestrialPlanet
    newPlanet.properName = "Terra"
    newPlanet.category = category.Tectonic
    newPlanet.size = 8
    newPlanet.chemistry = chemistry.Water
    newPlanet.ageModifier = 0
    newPlanet.className = className.Tectonic
    newPlanet.type = type.Gaian
    newPlanet.atmosphere = 6
    newPlanet.hydrosphere = 7
    newPlanet.subsurfaceOceans = False
    newPlanet.biosphere = 12
    newPlanet.terrain = [
        terrain.BeachShore,
        terrain.Clear,
        terrain.DeepOcean,
        terrain.Desert,
        terrain.Forest,
        terrain.Hills,
        terrain.Jungle,
        terrain.Mountains,
        terrain.OpenOcean,
        terrain.Plains,
        terrain.Rainforest,
        terrain.Riverbank,
        terrain.RoughBroken,
        terrain.ShallowOcean,
        terrain.SwampMarsh,
        terrain.Woods]
    newPlanet.animals = ["The animals of Earth."]
    newPlanet.satellites = []

        
def create_luna(star):
    newPlanet = Rockball(
        star,
        star.planets[-1],
        star.planets[-1].order,
        orbitType.InnerZone)

    newPlanet.group = group.DwarfPlanet
    newPlanet.properName = "Luna"
    newPlanet.category = category.Rockball
    newPlanet.size = 2
    newPlanet.className = className.Geopassive
    newPlanet.type = type.Lithic
    newPlanet.atmosphere = 0
    newPlanet.hydrosphere = 0
    newPlanet.biosphere = 0
    newPlanet.terrain = [terrain.Clear, terrain.Hills, terrain.Mountains, terrain.RoughBroken]


class OrbitalBody():
    """
    Defines an object that orbits a Star or other OrbitalBody.

    Required Parameters:
        star: Star class instance
            The star that this Orbital Body orbits (even if it already
            orbits another Orbital Body).
        parentObject: Class instance
            The object that this Orbital Body directly orbits. Valid classes
            are Star and OrbitalBody.
        order: Integer
            Indicates that this is the nth orbit from the star (e.g. Earth
            would have a value of 3).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
    """

    def __init__(
            self,
            star,
            parentObject,
            order,
            orbitType):
        self.systemHex = star.systemHex
        self.systemHex.planets.append(self)
        self.star = star
        self.star.planets.append(self)
        self.parentObject = parentObject
        self.order = order
        self.orbitType = orbitType
        self.satellites = []
        self.properName = None
        self.desirability = {}
        self.habitation = {}
        self.population = None
        self.populationNumber = 0
        self.alienPopulation = {}
        self.governmentRoll = None
        self.government = None
        self.lawLevelRoll = None
        self.lawLevel = None
        self.industryRoll = None
        self.industry = None
        self.industryPopulationEffect = 0
        self.pollution = 0
        self.tradeCodes = set()
        self.starportRoll = None
        self.starport = None
        self.governorsEstate = None
        self.embassy = None
        self.hospital = None
        self.libraryArchive = None
        self.megacorpHeadquarters = None
        self.navalBase = None
        self.pirateBase = None
        self.psionicsInstitute = None
        self.researchInstallation = None
        self.sacredSite = None
        self.scoutBase = None
        self.specialEnclave = None
        self.travellersAidSocietyHostel = None
        self.ruins = set()
        self.settlement = 0
        self.minimumTechLevel = None
        self.baseDesirability = 0

        if self.parentObject == self.star:
            self.name = self.star.name + " " + str(self.order)
        else:
            self.name = self.parentObject.name + "-" + str(len(self.parentObject.satellites) + 1)
            self.parentObject.satellites.append(self)

    
    def create_satellite(self, planetGroupToCreate):
        if planetGroupToCreate == group.DwarfPlanet:
            create_dwarf_planet(
                self.star,
                self.parentObject,
                self.order,
                self.orbitType)
        elif planetGroupToCreate == group.TerrestrialPlanet:
            create_terrestrial_planet(
                self.star,
                self.parentObject,
                self.order,
                self.orbitType)
        elif planetGroupToCreate == group.HelianPlanet:
            create_helian_planet(
                self.star,
                self.parentObject,
                self.order,
                self.orbitType)


class AsteroidBelt(OrbitalBody):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.group = group.AsteroidBelt
        self.category = category.AsteroidBelt
        self.atmosphere = 0
        self.hydrosphere = 0
        self.biosphere = 0
        self.baseDesirability = roll_xdy(1, 6) - roll_xdy(1, 6)

        # Create dwarf planet member of asteroid belt.
        if roll_xdy(1, 6) >= 5:
            self.create_satellite(group.DwarfPlanet)


class Planet(OrbitalBody):
    """
    Defines a planet that orbits a Star or other OrbitalBody.

    Required Parameters:
        star: Star class instance
            The star that this Orbital Body orbits (even if it already
            orbits another Orbital Body).
        parentObject: Class instance
            The object that this Orbital Body directly orbits. Valid classes
            are Star and OrbitalBody.
        order: Integer
            Indicates that this is the nth orbit from the star (e.g. Earth
            would have a value of 3).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
    """

    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = None
        self.size = None
        self.ageModifier = None
        self.type = None
        self.atmosphere = None
        self.hydrosphere = None
        self.biosphere = None
        self.terrain = []
        self.animals = []
        self.ringSystem = False
        self.homeAlien = None
        self.terraformingAlien = None
        self.terraformingPoints = 0
        self.terraformingPointsUsed = 0
        self.terraformingDone = False
        self.seedWithLife = False


class DwarfPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = roll_xdy(1, 6) - 1

        if self.parentObject == self.star and roll_xdy(1, 6) == 6:
            self.create_satellite(group.DwarfPlanet)


class TerrestrialPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = roll_xdy(1, 6) + 4

        if roll_xdy(1, 6) >= 5:
            self.create_satellite(group.DwarfPlanet)


class HelianPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = min(14, roll_xdy(1, 6) + 9)

        numOfSatellites = roll_xdy(1, 6) - 3
        terrestrialSatellite = roll_xdy(1, 6) == 6

        if terrestrialSatellite and numOfSatellites > 0:
            self.create_satellite(group.TerrestrialPlanet)
            numOfSatellites -= 1

        for _ in range(numOfSatellites):
            self.create_satellite(group.DwarfPlanet)


class JovianPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = 16
        self.hydrosphere = 16

        numOfSatellites = roll_xdy(1, 6)

        if roll_xdy(1, 6):
            if roll_xdy(1, 6) == 6:
                self.create_satellite(group.HelianPlanet)
            else:
                self.create_satellite(group.TerrestrialPlanet)
            numOfSatellites -= 1

        for _ in range(numOfSatellites):
            self.create_satellite(group.DwarfPlanet)


class Acheronian(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Acheronian
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Telluric
        self.type = type.Acheronian


    def set_atmosphere(self):
        self.atmosphere = 1
        

    def set_hydrosphere(self):
        self.hydrosphere = 0


    def set_biosphere(self):
        self.biosphere = 0


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

        r = chemistryArean[roll]
        
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

        r = chemistryArid[roll]
        
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


class Asphodelian(HelianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Asphodelian
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.GeoHelian
        self.type = type.Asphodelian


    def set_atmosphere(self):
        self.atmosphere = 1
        

    def set_hydrosphere(self):
        self.hydrosphere = 0


    def set_biosphere(self):
        self.biosphere = 0


class Chthonian(JovianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Chthonian
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Chthonian


    def set_atmosphere(self):
        self.atmosphere = 1
        

    def set_hydrosphere(self):
        self.hydrosphere = 0


    def set_biosphere(self):
        self.biosphere = 0


class Hebean(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Hebean
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Geotidal
        self.type = (type.Hebean if coin_flip else type.Idunnian)


    def set_atmosphere(self):
        roll = roll_xdy(1, 6) + self.size - 6
        self.atmosphere = max(0, (10 if roll >= 2 else roll))
        

    def set_hydrosphere(self):
        self.hydrosphere = max(0, roll_xdy(2, 6) + self.size - 11)


    def set_biosphere(self):
        self.biosphere = 0


class Helian(HelianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Helian
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = (className.GeoHelian if coin_flip else className.Nebulous)


    def set_atmosphere(self):
        self.atmosphere = 13
        

    def set_hydrosphere(self):
        roll = roll_xdy(1, 6)
        if roll <= 2:
            self.hydrosphere = 0
        elif roll <= 4:
            self.hydrosphere = roll_xdy(1, 6) - 1
        else:
            self.hydrosphere = 15


    def set_biosphere(self):
        self.biosphere = 0


class JaniLithic(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.JaniLithic
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Epistellar
        self.type = type.JaniLithic


    def set_atmosphere(self):
        if coin_flip:
            self.atmosphere = 1
        else:
            self.atmosphere = 10
        

    def set_hydrosphere(self):
        self.hydrosphere = 0


    def set_biosphere(self):
        self.biosphere = 0


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

            r = chemistryJovian[roll]
            
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


class Meltball(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Meltball
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        r = chemistryMeltball[roll_xdy(1, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        self.atmosphere = 1
        

    def set_hydrosphere(self):
        self.hydrosphere = 15


    def set_biosphere(self):
        self.biosphere = 0


class Oceanic(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Oceanic
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

        if self.orbitType == orbitType.OuterZone:
            roll += 2

        r = chemistryOceanic[roll][roll_xdy(1, 6)]
        
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

        r = chemistryPanthalassic[roll][roll_xdy(2, 6)]
        
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

        r = chemistryPromethean[roll]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        if self.biosphere >= 3 and self.chemistry == chemistry.Water:
            self.atmosphere = max(2, min(9, roll_xdy(2, 6) + self.size - 7))
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


class Rockball(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Rockball
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        r = chemistryRockball[roll_xdy(1, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]


    def set_atmosphere(self):
        self.atmosphere = 0
        

    def set_hydrosphere(self):
        roll = roll_xdy(2, 6)
        if self.star.luminosityClass == luminosityClass.L:
            roll += 1
        if self.orbitType == orbitType.Epistellar:
            roll -= 2
        elif self.orbitType == orbitType.OuterZone:
            roll += 2

        self.hydrosphere = max(0, roll_xdy(2, 6) + self.size - 11)


    def set_biosphere(self):
        self.biosphere = 0


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
            
        r = chemistrySnowball[roll]
        
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


class Stygian(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Stygian
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Geopassive
        self.type = type.Stygian


    def set_atmosphere(self):
        self.atmosphere = 0
        

    def set_hydrosphere(self):
        self.hydrosphere = 0


    def set_biosphere(self):
        self.biosphere = 0


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
        elif self.star.luminosityClass == luminosityClass.L:
            roll += 5
        if self.orbitType == orbitType.OuterZone:
            roll += 2

        r = chemistryTectonic[roll][roll_xdy(2, 6)]
        
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


class Telluric(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Telluric
        self.set_chemistry_age_modifier_class_type()
        self.set_atmosphere()
        self.set_hydrosphere()
        self.set_biosphere()


    def set_chemistry_age_modifier_class_type(self):
        self.className = className.Telluric
        self.type = (type.Phosphorian if coin_flip else type.Cytherean)


    def set_atmosphere(self):
        self.atmosphere = 12
        

    def set_hydrosphere(self):
        self.hydrosphere = (0 if roll_xdy(1, 6) <= 4 else 15)


    def set_biosphere(self):
        self.biosphere = 0


class Vesperian(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Vesperian
        self.set_chemistry_age_modifier_class_type()
        self.set_hydrosphere()
        self.set_biosphere()
        self.set_atmosphere()


    def set_chemistry_age_modifier_class_type(self):
        r = chemistryVesperian[roll_xdy(2, 6)]
        
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

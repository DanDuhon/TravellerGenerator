import animal
import alien
from diceroller import roll_xdy
from lookuptable import LookupTable

allPlanets = []


dwarfCategoryDict = {
    "Epistellar": LookupTable(
        (3, LookupTable(6, "Rockball")),
        (5, LookupTable(6, "Meltball")),
        (6, LookupTable(
            (4, "Hebean"),
            (6, "Promethean")))),
    "Inner Zone": LookupTable(
        (4, LookupTable(6, "Rockball")),
        (6, LookupTable(6, "Arean")),
        (7, LookupTable(6, "Meltball")),
        (8, LookupTable(
            (4, "Hebean"),
            (6, "Promethean")))),
    "Outer Zone": LookupTable(
        (0, LookupTable(6, "Rockball")),
        (4, LookupTable(6, "Snowball")),
        (6, LookupTable(6, "Rockball")),
        (7, LookupTable(6, "Meltball")),
        (8, LookupTable(
            (3, "Hebean"),
            (5, "Arean"),
            (6, "Promethean"))))
}


terrestrialCategoryDict = {
    "Epistellar": LookupTable(
        (4, "Jani-Lithic"),
        (5, "Vesperian"),
        (6, "Telluric")),
    "Inner Zone": LookupTable(
        (4, "Telluric"),
        (6, "Arid"),
        (7, "Tectonic"),
        (9, "Oceanic"),
        (10, "Tectonic"),
        (12, "Telluric")),
    "Outer Zone": LookupTable(
        (4, "Arid"),
        (6, "Tectonic"),
        (8, "Oceanic"))
}


categoryDescriptionDict = {
    "Acheronian": "These are worlds that were directly affected by a star's transition from the main sequence; the atmosphere and oceans have been boiled away, leaving a scorched, dead planet.",
    "Arean": "These are worlds with little liquid, that move through a slow geological cycle of a gradual build-up, a short wet and clement period, and a long decline.",
    "Arid": "These are worlds with limited amounts of surface liquid, that maintain an equilibrium with the help of their tectonic activity and their biosphere.",
    "Asphodelian": "These are worlds that were directly affected by a star's transition from the main sequence; their atmosphere has been boiled away, leaving the surface exposed.",
    "Chthonian": "These are worlds that were directly affected by a star's transition from the main sequence, or that have simply spent too long in a tight epistellar orbit; their atmospheres have been stripped away.",
    "Hebean": "These are highly active worlds, due to tidal flexing, but with some regions of stability; the larger ones may be able to maintain some atmosphere and surface liquid.",
    "Helian": "These are typical helian or \"subgiant\" worlds – large enough to retain helium atmospheres.",
    "Jani-Lithic": "These worlds, tide-locked to the primary, are rocky, dry, and geologically active.",
    "Jovian": "These are huge worlds with helium-hydrogen envelopes and compressed cores; the largest emit more heat than they absorb.",
    "Meltball": "These are dwarfs with molten or semi-molten surfaces, either from extreme tidal flexing, or extreme approach to a star.",
    "Oceanic": "These are worlds with a continuous hydrological cycle and deep oceans, due to either dense greenhouse atmosphere or active plate tectonics.",
    "Panthalassic": "These are massive worlds, aborted gas giants, largely composed of water and hydrogen.",
    "Promethean": "These are worlds that, through tidal-flexing, have a geological cycle similar to plate tectonics, that supports surface liquid and atmosphere.",
    "Rockball": "These are mostly dormant worlds, with surfaces largely unchanged since the early period of planetary formation.",
    "Snowball": "These worlds are composed of mostly ice and some rock. They may have varying degrees of activity, ranging from completely cold and still to cryo-volcanically active with extensive subsurface oceans.",
    "Stygian": "These are worlds that were directly affected by a star's transition from the main sequence; they are melted and blasted lumps.",
    "Tectonic": "These are worlds with active plate tectonics and large bodies of surface liquid, allowing for stable atmospheres and a high likelihood of life.",
    "Telluric": "These are worlds with geoactivity but no hydrological cycle at all, leading to dense runaway-greenhouse atmospheres.",
    "Vesperian": "These worlds are tide-locked to their primary, but at a distance that permits surface liquid and the development of life."
}


chemistryDict = {
    "Acheronian": LookupTable(100, LookupTable(100, (None, None, "Telluric", "Acheronian"))),
    "Arean": LookupTable(
                    (4, LookupTable(100, ("Water", 0, "Geocyclic", "Arean"))),
                    (6, LookupTable(100, ("Ammonia", 1, "Geocyclic", "Utgardian"))),
                    (100, LookupTable(100, ("Methane", 3, "Geocyclic", "Titanian")))),
    "Arid": LookupTable(
                    (6, LookupTable(100, ("Water", 0, "Arid", "Darwinian"))),
                    (8, LookupTable(100, ("Ammonia", 1, "Arid", "Saganian"))),
                    (100, LookupTable(100, ("Methane", 3, "Arid", "Asimovian")))),
    "Asphodelian": LookupTable(100, LookupTable(100, (None, None, "Geo-Helian", "Asphodelian"))),
    "Asteroid Belt": LookupTable(100, LookupTable(100, (None, None, "Asteroid Belt", "Asteroid Belt"))),
    "Chthonian": LookupTable(100, LookupTable(100, (None, None, "Chthonian", None))),
    "Hebean": LookupTable(
                    (3, LookupTable(100, (None, None, "Geotidal", "Hebean"))),
                    (100, LookupTable(100, (None, None, "Geotidal", "Idunnian")))),
    "Helian": LookupTable(
                    (3, LookupTable(100, (None, None, "Geo-Helian", None))),
                    (100, LookupTable(100, (None, None, "Nebulous", None)))),
    "Jani-Lithic": LookupTable(100, LookupTable(100, (None, None, "Epistellar", "Jani-Lithic"))),
    "Jovian": LookupTable(
                    (3, LookupTable(100, ("Water", None, "Dwarf Jovian", "Brammian"))),
                    (100, LookupTable(100, ("Ammonia", None, "Dwarf Jovian", "Khonsonian")))),
    "Meltball": LookupTable(
                    (3, LookupTable(
                        (2, (None, None, "Geothermic", "Phaethonic")),
                        (4, (None, None, "Geothermic", "Apollonian")),
                        (100, (None, None, "Geothermic", "Sethian")))),
                    (100, LookupTable(
                        (3, (None, None, "Geotidal", "Hephaestian")),
                        (100, (None, None, "Geotidal", "Lokian"))))),
    "Oceanic": LookupTable(
                    (6, LookupTable(
                        (3, ("Water", 0, "Oceanic", "Pelagic")),
                        (100, ("Water", 0, "Tectonic", "Bathy-Gaian")))),
                    (8, LookupTable(
                        (3, ("Ammonia", 1, "Oceanic", "Nunnic")),
                        (100, ("Ammonia", 1, "Tectonic", "Bathy-Amunian")))),
                    (100, LookupTable(
                        (3, ("Methane", 3, "Oceanic", "Teathic")),
                        (100, ("Methane", 3, "Tectonic", "Bathy-Tartarian"))))),
    "Panthalassic": LookupTable(
                    (6, LookupTable(
                        (8, ("Water", 0, "Panthalassic", None)),
                        (11, ("Sulfur", 0, "Panthalassic", None)),
                        (100, ("Chlorine", 0, "Panthalassic", None)))),
                    (8, LookupTable(100, ("Methane", 1, "Panthalassic", None))),
                    (100, LookupTable(100, ("Methane", 3, "Panthalassic", None)))),
    "Promethean": LookupTable(
                    (4, LookupTable(100, ("Water", 0, "Geotidal", "Promethean"))),
                    (6, LookupTable(100, ("Ammonia", 1, "Geotidal", "Burian"))),
                    (100, LookupTable(100, ("Methane", 3, "Geotidal", "Atlan")))),
    "Rockball": LookupTable(
                    (2, LookupTable(100, (None, None, "Geopassive", "Ferrinian"))),
                    (4, LookupTable(100, (None, None, "Geopassive", "Lithic"))),
                    (100, LookupTable(100, (None, None, "Geopassive", "Carbonian")))),
    "Snowball": LookupTable(
                    (4, LookupTable(100, ("Water", 0, "Geopassive", "Gelidian"))),
                    (6, LookupTable(100, ("Ammonia", 1, "Geothermic", "Erisian"))),
                    (100, LookupTable(100, ("Methane", 3, "Geotidal", "Plutonian")))),
    "Stygian": LookupTable(100, LookupTable(100, (None, None, "Geopassive", "Stygian"))),
    "Tectonic": LookupTable(
                    (8, LookupTable(
                        (8, ("Water", 0, "Tectonic", "Gaian")),
                        (11, ("Sulfur", 0, "Tectonic", "Thio-Gaian")),
                        (100, ("Chlorine", 0, "Tectonic", "Chloritic-Gaian")))),
                    (11, LookupTable(100, ("Ammonia", 1, "Tectonic", "Amunian"))),
                    (100, LookupTable(100, ("Methane", 3, "Tectonic", "Tartarian")))),
    "Telluric": LookupTable(
                    (3, LookupTable(100, (None, None, "Telluric", "Phosphorian"))),
                    (100, LookupTable(100, (None, None, "Telluric", "Cytherean")))),
    "Vesperian": LookupTable(
                    (11, LookupTable(100, ("Water", None, "Epistellar", "Vesperian"))),
                    (100, LookupTable(100, ("Chlorine", None, "Epistellar", "Vesperian"))))
}


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


starportTable = LookupTable((2, "X"),
                            (4, "E"),
                            (6, "D"),
                            (8, "C"),
                            (10, "B"),
                            (100, "A"))


tradeCodesDict = {
    "Ag": "Agricultural",
    "As": "Asteroid Belt",
    "De": "Desert",
    "Fl": "Fluid Oceans",
    "Ga": "Garden",
    "Hi": "High Population",
    "Ht": "High Technology",
    "Ic": "Ice-Capped",
    "In": "Industrial",
    "Lo": "Low Population",
    "Lt": "Low Technology",
    "Na": "Non-Agricultural",
    "Ni": "Non-Industrial",
    "Po": "Poor",
    "Ri": "Rich",
    "St": "Sterile",
    "Wa": "Water World",
    "Va": "Vacuum",
    "Zo": "Zoo",
}


def create_asteroid_belt(
        star,
        order,
        orbitType,
        alienSurvivalPercent):
    """
    Creates an asteroid belt.

    Required Parameters:
        star: Star class instance
            The star around which the asteroid belt orbits.
        order: Integer
            Indicates that this is the nth orbit from the star (e.g. Earth
            would have a value of 3).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        alienSurvivalPercent: Integer
            An integer that represents the percent chance that
            an intelligent species will survive to Tech Level 10.
    """

    newPlanet = OrbitalBody(
        star=star,
        parentObject=star,
        order=order,
        orbitType=orbitType)

    newPlanet.size = 25
    newPlanet.category = "Asteroid Belt"
    newPlanet.groupName = "Asteroid Belt"
    newPlanet.className = "Asteroid Belt"
    newPlanet.typeName = "Asteroid Belt"
    newPlanet.chemistry = None
    newPlanet.ageModifier = None
    newPlanet.atmosphere = 0
    newPlanet.hydrosphere = 0
    newPlanet.biosphere = 0
    newPlanet.terrain = newPlanet.planet_terrain()
    newPlanet.baseDesirability = roll_xdy(1, 6) - roll_xdy(1, 6)
    newPlanet.satellites = []

    if roll_xdy(1, 6) <= 4:
        create_dwarf_planet(
            star=newPlanet.star,
            parentObject=newPlanet,
            order=newPlanet.order,
            orbitType=newPlanet.orbitType,
            alienSurvivalPercent=alienSurvivalPercent)

        
def create_dwarf_planet(
        star,
        parentObject,
        order,
        orbitType,
        alienSurvivalPercent):
    """
    Creates a dwarf planet.

    Required Parameters:
        star: Star class instance
            The star around which the planet orbits.
        parentObject: Class instance
            The object that this Orbital Body directly orbits. Valid classes
            are Star and OrbitalBody.
        order: Integer
            Indicates that this is the nth orbit from the star (e.g. Earth
            would have a value of 3).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        alienSurvivalPercent: Integer
            An integer that represents the percent chance that
            an intelligent species will survive to Tech Level 10.
    """

    newPlanet = OrbitalBody(
        star=star,
        parentObject=parentObject,
        order=order,
        orbitType=orbitType)

    newPlanet.groupName = "Dwarf"
    newPlanet.category = newPlanet.dwarf_category()
    newPlanet.size = newPlanet.planet_size()
    newPlanet.className, newPlanet.chemistry, newPlanet.ageModifier, newPlanet.type, newPlanet.atmosphere, newPlanet.biosphere, newPlanet.hydrosphere, newPlanet.subsurfaceOceans = newPlanet.class_chemistry_atmosphere_hydrosphere_biosphere()
    newPlanet.terrain = newPlanet.planet_terrain()

    if newPlanet.biosphere >= 9:
        newPlanet.animals = newPlanet.planet_animals()

    if newPlanet.biosphere >= 12:
        alien.create_alien(newPlanet, alienSurvivalPercent)

    newPlanet.satellites = []

    if newPlanet.parentObject == newPlanet.star and roll_xdy(1, 6) == 6:
        create_dwarf_planet(
            star=newPlanet.star,
            parentObject=newPlanet.parentObject,
            order=newPlanet.order,
            orbitType=newPlanet.orbitType,
            alienSurvivalPercent=alienSurvivalPercent)

        
def create_terrestrial_planet(
        star,
        parentObject,
        order,
        orbitType,
        alienSurvivalPercent):
    """
    Creates a terrestrial planet.

    Required Parameters:
        star: Star class instance
            The star around which the planet orbits.
        parentObject: Class instance
            The object that this Orbital Body directly orbits. Valid classes
            are Star and OrbitalBody.
        order: Integer
            Indicates that this is the nth orbit from the star (e.g. Earth
            would have a value of 3).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        alienSurvivalPercent: Integer
            An integer that represents the percent chance that
            an intelligent species will survive to Tech Level 10.
    """

    newPlanet = OrbitalBody(
        star=star,
        parentObject=parentObject,
        order=order,
        orbitType=orbitType)

    newPlanet.groupName = "Terrestrial"
    newPlanet.terrestrial_category()
    newPlanet.planet_size()
    newPlanet.className, newPlanet.chemistry, newPlanet.ageModifier, newPlanet.type, newPlanet.atmosphere, newPlanet.biosphere, newPlanet.hydrosphere, newPlanet.subsurfaceOceans = newPlanet.class_chemistry_atmosphere_hydrosphere_biosphere()
    newPlanet.terrain = newPlanet.planet_terrain()

    if newPlanet.biosphere >= 9:
        newPlanet.planet_animals()

    if newPlanet.biosphere >= 12:
        alien.create_alien(newPlanet, alienSurvivalPercent)

    newPlanet.satellites = []

    if newPlanet.parentObject == newPlanet.star and roll_xdy(1, 6) >= 1:
        create_dwarf_planet(
            star=newPlanet.star,
            parentObject=newPlanet,
            order=newPlanet.order,
            orbitType=newPlanet.orbitType,
            alienSurvivalPercent=alienSurvivalPercent)

        
def create_helian_planet(
        star,
        parentObject,
        order,
        orbitType,
        alienSurvivalPercent):
    """
    Creates a helian planet.

    Required Parameters:
        star: Star class instance
            The star around which the planet orbits.
        parentObject: Class instance
            The object that this Orbital Body directly orbits. Valid classes
            are Star and OrbitalBody.
        order: Integer
            Indicates that this is the nth orbit from the star (e.g. Earth
            would have a value of 3).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        alienSurvivalPercent: Integer
            An integer that represents the percent chance that
            an intelligent species will survive to Tech Level 10.
    """

    newPlanet = OrbitalBody(
        star=star,
        parentObject=parentObject,
        order=order,
        orbitType=orbitType)

    newPlanet.groupName = "Helian"
    newPlanet.helian_category()
    newPlanet.planet_size()
    newPlanet.className, newPlanet.chemistry, newPlanet.ageModifier, newPlanet.type, newPlanet.atmosphere, newPlanet.biosphere, newPlanet.hydrosphere, newPlanet.subsurfaceOceans = newPlanet.class_chemistry_atmosphere_hydrosphere_biosphere()
    newPlanet.terrain = newPlanet.planet_terrain()

    if newPlanet.biosphere >= 9:
        newPlanet.planet_animals()

    if newPlanet.biosphere >= 12:
        alien.create_alien(newPlanet, alienSurvivalPercent)

    newPlanet.satellites = []

    if newPlanet.parentObject == newPlanet.star:
        satelliteRoll1 = roll_xdy(1, 6)
        satelliteRoll2 = roll_xdy(1, 6)

        if satelliteRoll2 == 6 and satelliteRoll1 - 3 > 0:
            create_terrestrial_planet(
                star=newPlanet.star,
                parentObject=newPlanet,
                order=newPlanet.order,
                orbitType=newPlanet.orbitType,
                alienSurvivalPercent=alienSurvivalPercent)

        for _ in range(newPlanet.dwarf_satellites(satelliteRoll1, satelliteRoll2)):
                create_dwarf_planet(
                    star=newPlanet.star,
                    parentObject=newPlanet,
                    order=newPlanet.order,
                    orbitType=newPlanet.orbitType,
                    alienSurvivalPercent=alienSurvivalPercent)

        
def create_jovian_planet(
        star,
        order,
        orbitType,
        alienSurvivalPercent):
    """
    Creates a jovian planet (gas giant).

    Required Parameters:
        star: Star class instance
            The star around which the planet orbits.
        order: Integer
            Indicates that this is the nth orbit from the star (e.g. Earth
            would have a value of 3).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        alienSurvivalPercent: Integer
            An integer that represents the percent chance that
            an intelligent species will survive to Tech Level 10.
    """

    newPlanet = OrbitalBody(
        star=star,
        parentObject=star,
        order=order,
        orbitType=orbitType)

    newPlanet.groupName = "Jovian"
    newPlanet.jovian_category()
    newPlanet.size = 16
    newPlanet.className, newPlanet.chemistry, newPlanet.ageModifier, newPlanet.type, newPlanet.atmosphere, newPlanet.biosphere, newPlanet.hydrosphere, newPlanet.subsurfaceOceans = newPlanet.class_chemistry_atmosphere_hydrosphere_biosphere()

    if roll_xdy(1, 6) <= 4:
        newPlanet.ringSystem = "Minor"
    else:
        newPlanet.ringSystem = "Complex"

    newPlanet.satellites = []

    satelliteRoll1 = roll_xdy(1, 6)
    satelliteRoll2 = roll_xdy(1, 6)
    satelliteRoll3 = roll_xdy(1, 6)

    if satelliteRoll2 == 6 and satelliteRoll3 == 6:
        create_helian_planet(
            star=newPlanet.star,
            parentObject=newPlanet,
            order=newPlanet.order,
            orbitType=newPlanet.orbitType,
            alienSurvivalPercent=alienSurvivalPercent)
    
    if satelliteRoll2 == 6 and satelliteRoll3 <= 5:
        create_terrestrial_planet(
            star=newPlanet.star,
            parentObject=newPlanet,
            order=newPlanet.order,
            orbitType=newPlanet.orbitType,
            alienSurvivalPercent=alienSurvivalPercent)
    
    for _ in range(newPlanet.dwarf_satellites(satelliteRoll1, satelliteRoll2)):
            create_dwarf_planet(
                star=newPlanet.star,
                parentObject=newPlanet,
                order=newPlanet.order,
                orbitType=newPlanet.orbitType,
                alienSurvivalPercent=alienSurvivalPercent)

    newPlanet.star.systemHex.fuelUnrefinedAvailable = True

        
def create_terra(star):
    """
    Creates the home planet of Terrans (humans).

    Required Parameters:
        star: Star class instance
            The star around which the planet orbits.
    """

    newPlanet = OrbitalBody(
        star=star,
        parentObject=star,
        order=star.epistellarOrbits + star.innerZoneOrbits + 1,
        orbitType="Inner Zone")

    newPlanet.groupName = "Terrestrial"
    newPlanet.properName = "Terra"
    newPlanet.category = "Tectonic"
    newPlanet.size = 8
    newPlanet.chemistry = "Water"
    newPlanet.ageModifier = 0
    newPlanet.className = "Tectonic"
    newPlanet.type = "Gaian"
    newPlanet.atmosphere = 6
    newPlanet.hydrosphere = 7
    newPlanet.subsurfaceOceans = False
    newPlanet.biosphere = 12
    newPlanet.terrain = [
        "Beach/Shore",
        "Clear",
        "Deep Ocean",
        "Desert",
        "Forest",
        "Hills",
        "Jungle",
        "Mountains",
        "Open Ocean",
        "Plains",
        "Rainforest",
        "Riverbank",
        "Rough/Broken",
        "Shallow Ocean",
        "Swamp Marsh",
        "Woods"]
    newPlanet.animals = ["The animals of Earth."]
    newPlanet.satellites = []
    newPlanet.terraformingDone = True

        
def create_luna(star):
    """
    Creates the Terran moon.

    Required Parameters:
        star: Star class instance
            The star around which the planet orbits.
    """

    newPlanet = OrbitalBody(
        star=star,
        parentObject=star.planets[-1],
        order=star.planets[-1].order,
        orbitType="Inner Zone")

    newPlanet.groupName = "Dwarf"
    newPlanet.properName = "Luna"
    newPlanet.category = "Rockball"
    newPlanet.size = 2
    newPlanet.chemistry = None
    newPlanet.ageModifier = None
    newPlanet.className = "Geopassive"
    newPlanet.type = "Lithic"
    newPlanet.atmosphere = 0
    newPlanet.hydrosphere = 0
    newPlanet.subsurfaceOceans = False
    newPlanet.biosphere = 0
    newPlanet.terrain = ["Clear", "Hills", "Mountains", "Rough/Broken"]
    newPlanet.animals = []
    newPlanet.satellites = []
    newPlanet.alien = None
    newPlanet.terraformingDone = True


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
        allPlanets.append(self)
        self.systemHex = star.systemHex
        self.systemHex.planets.append(self)
        self.star.planets.append(self)
        self.star = star
        self.parentObject = parentObject
        self.order = order
        self.orbitType = orbitType
        self.category = None
        self.size = None
        self.ageModifier = None
        self.type = None
        self.groupName = None
        self.className = None
        self.typeName = None
        self.atmosphere = None
        self.biosphere = None
        self.hydrosphere = None
        self.subsurfaceOceans = None
        self.terrain = set()
        self.animals = []
        self.ringSystem = None
        self.satellites = []
        self.alien = None
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
        self.terraformingAlien = None
        self.terraformingPoints = 0
        self.terraformingPointsUsed = 0
        self.terraformingDone = False
        self.minimumTechLevel = None
        self.seedWithLife = False
        self.baseDesirability = 0

        if self.parentObject == self.star:
            self.name = self.parentObject.name + " " + str(self.order)
        else:
            self.name = self.parentObject.name + "-" + str(len(self.parentObject.satellites) + 1)
            self.parentObject.satellites.append(self)


    def dwarf_category(self):
        """
        Returns the category of a planet based on dwarfCategoryDict.
        """

        if self.order <= self.star.expansionAffectedOrbits:
            return "Stygian"

        roll = roll_xdy(1, 6)

        if self.orbitType == "Epistellar":
            if self.parentObject != self.star and self.parentObject.groupName == "Asteroid Belt":
                roll -= 2
        elif self.orbitType == "Inner Zone":
            if self.parentObject != self.star and self.parentObject.groupName == "Asteroid Belt":
                roll -= 2
            elif self.parentObject != self.star and self.parentObject.groupName == "Helian":
                roll += 1
            elif self.parentObject != self.star and self.parentObject.groupName == "Jovian":
                roll += 2
        else:  # Outer Zone
            if self.parentObject != self.star and self.parentObject.groupName == "Asteroid Belt":
                roll -= 1
            elif self.parentObject != self.star and self.parentObject.groupName == "Helian":
                roll += 1
            elif self.parentObject != self.star and self.parentObject.groupName == "Jovian":
                roll += 2

        return dwarfCategoryDict[self.orbitType][roll][roll_xdy(1, 6)]


    def terrestrial_category(self):
        """
        Returns the category of a planet based on terrestrialCategoryDict.
        """

        roll = roll_xdy(1, 6)

        if self.order <= self.star.expansionAffectedOrbits:
            return "Acheronian"
        elif self.orbitType == "Inner Zone":
            roll += roll_xdy(1, 6)
        elif self.orbitType == "Outer Zone":
            if self.parentObject != self.star:
                roll += 2

        return terrestrialCategoryDict[self.orbitType][roll]


    def helian_category(self):
        """
        Returns the category of a Helian planet.
        """

        if self.order <= self.star.expansionAffectedOrbits:
            return "Asphodelian"
        elif self.orbitType == "Epistellar" and roll_xdy(1, 6) == 6:
            return "Asphodelian"
        elif self.orbitType == "Inner Zone" and roll_xdy(1, 6) >= 5:
            return "Panthalassic"
        else:  # Outer Zone and other rolls
            return "Helian"


    def jovian_category(self):
        """
        Returns the category of a Jovian planet.
        """

        if self.order <= self.star.expansionAffectedOrbits:
            return "Chthonian"
        elif self.orbitType == "Epistellar" and roll_xdy(1, 6) == 6:
            return "Chthonian"
        else:  # Inner Zone, Outer Zone, and other rolls
            return "Jovian"


    def planet_size(self):
        """
        Returns the size value of a planet based on group.
        """

        if self.groupName == "Dwarf":
            return roll_xdy(1, 6) - 1
        elif self.groupName == "Terrestrial":
            return roll_xdy(1, 6) + 4
        elif self.groupName == "Helian":
            return min(14, roll_xdy(1, 6) + 9)
        else:
            raise ValueError("Unrecognized group: " + str(self.groupName))


    def class_chemistry_atmosphere_hydrosphere_biosphere(self):
        """
        Returns the planet's chemistry, atmosphere, hydrosphere, and biosphere
        values. Not all planet categories have the same order of operations,
        so it is in a loop to accommodate the planets that determine these
        things in a different order so I can have just one of these functions.
        """

        className = self.className
        chemistry = self.chemistry
        ageModifier = self.ageModifier
        planetType = self.type
        atmosphere = self.atmosphere
        biosphere = self.biosphere
        hydrosphere = self.hydrosphere
        subsurfaceOceans = self.subsurfaceOceans

        while not isinstance(className, str) or not isinstance(atmosphere, int) or not isinstance(biosphere, int) or not isinstance(hydrosphere, int):
            if not isinstance(className, str):
                chemistry, ageModifier, className, planetType = self.planet_chemistry_age_modifier_class_type(biosphere=biosphere)

            if not isinstance(atmosphere, int):
                atmosphere = self.planet_atmosphere(biosphere=biosphere, chemistry=chemistry)

            if not isinstance(biosphere, int):
                biosphere = self.planet_biosphere()

            if not isinstance(hydrosphere, int):
                hydrosphere, subsurfaceOceans = self.planet_hydrosphere_subsurface_oceans()

            if biosphere > 0 and ((isinstance(atmosphere, int) and atmosphere <= 1 and self.subsurfaceOceans == False)
                                    or hydrosphere == 0
                                    or self.star.luminosityClass == "M-Ve"):
                biosphere = 0
                
                # The atmosphere of these categories is dependent on the biosphere.
                # If the biosphere was forced to 0, recalculate the value for
                # atmosphere.
                if self.category in [
                    "Arid",
                    "Promethean",
                    "Tectonic",
                    "Vesperian"]:
                    atmosphere = self.planet_atmosphere()

        return className, chemistry, ageModifier, planetType, atmosphere, biosphere, hydrosphere, subsurfaceOceans


    def planet_chemistry_age_modifier_class_type(self, biosphere):
        """
        Returns chemistry, ageModifier, className, and type:
            chemistry: String
                The prominent chemical substance on the planet.
            ageModifier: Integer
                Used in calculating the hydrosphere and biosphere of the planet.
            className: String
                The class name of the planet.
            type: String
                The type name of the planet.

        Required Parameters:
            biosphere: Integer
                The current calculated biosphere value.
        """

        if self.category == "Jovian" and biosphere is None:
            return None, None, None, None

        if self.category == "Jovian" and biosphere == 0:
            return None, None, "Jovian", None

        roll = roll_xdy(1, 6)
        
        if self.star.luminosityClass == "L":
            if self.category == "Jovian":
                roll += 1
            elif self.category in ["Arean", "Promethean", "Snowball"]:
                roll += 2
            elif self.category in ["Arid", "Oceanic", "Panthalassic", "Tectonic"]:
                roll += 5
        elif self.star.luminosityClass == "K-V" and self.category in ["Arid", "Oceanic", "Panthalassic", "Tectonic"]:
            roll += 2
        elif self.star.luminosityClass == "M-V" and self.category in ["Arid", "Oceanic", "Panthalassic", "Tectonic"]:
            roll += 4

        if self.orbitType == "Epistellar" and self.category in ["Jovian", "Epistellar"]:
            roll -= 2
        elif self.orbitType == "Outer Zone" and self.category in ["Arean", "Arid", "Jovian", "Oceanic", "Promethean", "Snowball", "Tectonic"]:
            roll += 2

        r = chemistryDict[self.category][roll][roll_xdy(1, 6)]
                
        return r[0], r[1], r[2], r[3]


    def planet_atmosphere(self, biosphere, chemistry):
        """
        Returns the planet's atmosphere value.

        Required Parameters:
            biosphere: Integer
                The current biosphere value of the planet.
            chemistry: String
                The current chemistry type of the planet.
        """

        if self.category in ["Rockball", "Asteroid Belt", "Stygian"]:
            return 0
        
        elif self.category in ["Acheronian", "Asphodelian", "Chthonian", "Meltball"]:
            return 1
        
        elif self.category == "Arean":
            roll = roll_xdy(1, 6) - (2 if self.star.luminosityClass == "D" else 0)
            return (1 if roll <= 3 else 10)
        
        elif isinstance(biosphere, int) and self.category == "Arid":
            if biosphere >= 3 and self.chemistry == "Water":
                roll = roll_xdy(2, 6) - 7 + self.size
                return min([9, max([2, roll])])
            else:
                return 10
        
        elif self.category == "Hebean":
            roll = max(0, roll_xdy(1, 6) + self.size - 6)
            return (10 if roll >= 2 else roll)
        
        elif self.category == "Helian":
            return 13
        
        elif self.category == "Jani-Lithic":
            return (1 if roll_xdy(1, 6) <= 3 else 10)
        
        elif self.category == "Jovian":
            return 16
        
        elif self.category == "Meltball":
            return 1
        
        elif self.category == "Oceanic":
            if self.chemistry == "Water":
                roll = roll_xdy(2, 6) + self.size - 6
                if self.star.luminosityClass in ["F-IV", "G-IV", "K-IV", "K-V"]:
                    roll -= 1
                elif self.star.luminosityClass == "M-V":
                    roll -= 2
                elif self.star.luminosityClass == "L":
                    roll -= 3
                return min([12, max([1, roll])])
            else:
                roll = roll_xdy(1, 6)
                return (1 if roll == 1 else 10 if roll <= 4 else 12)
        
        elif self.category == "Panthalassic":
            return min([13, roll_xdy(1, 6) + 8])
        
        elif isinstance(biosphere, int) and self.category == "Promethean":
            if self.chemistry == "Water" and biosphere >= 3:
                return min([9, max([2, roll_xdy(2, 6) + self.size - 7])])
            else:
                return 10
        
        elif self.category == "Snowball":
            return (0 if roll_xdy(1, 6) <= 4 else 1)

        elif isinstance(biosphere, int) and self.category == "Tectonic":
            if biosphere >= 3 and chemistry == "Water":
                return min([9, max([2, roll_xdy(2, 6) + self.size - 7])])
            elif biosphere >= 3 and chemistry in ["Sulfur", "Chlorine"]:
                return 11
            else:
                return 10

        elif self.category == "Telluric":
            return 12

        elif isinstance(biosphere, int) and self.category == "Vesperian":
            if biosphere >= 3 and chemistry == "Water":
                return min([9, max([2, roll_xdy(2, 6) + self.size - 7])])
            elif biosphere >= 3 and chemistry == "Chlorine":
                return 11
            else:
                return 10


    def planet_biosphere(self, atmosphere, subsurfaceOceans, hydrosphere, ageModifier):
        """
        Returns the planet's biosphere value.

        Required Parameters:
            atmosphere: Integer
                The current value of the atmosphere.
            subsurfaceOceans: Boolean
                Whether this planet currently has subsurface oceans.
            hydrosphere: Integer
                The current value of the hydrosphere.
            ageModifier: Integer
                The current chemistry age modifier of the planet.
        """

        if ((atmosphere == 0
                and not subsurfaceOceans)
            or hydrosphere == 0
            or "M-Ve" in [s.luminosityClass for s in self.systemHex.stars]):
            return 0

        elif self.category == "Arean":
            if self.star.systemHex.age >= 4 + ageModifier and atmosphere == 10:
                return max([0, roll_xdy(1, 6) + self.size - 2])
            elif self.star.systemHex.age >= roll_xdy(1, 3) + ageModifier:
                return ([max(0, roll_xdy(1, 6) - 4) if atmosphere == 1 else roll_xdy(1, 3)])
            else:
                return 0

        elif self.category == "Arid":
            if self.star.systemHex.age >= 4 + ageModifier:
                return max([0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == "D" else 0)])
            elif self.star.systemHex.age >= roll_xdy(1, 3) + ageModifier:
                return roll_xdy(1, 3)
            else:
                return 0

        elif self.category == "Jovian":
            roll = roll_xdy(1, 6) + (2 if self.orbitType == "Inner Zone" else 0)

            if roll >= 6:
                if self.star.systemHex.age >= roll_xdy(1, 6):
                    return roll_xdy(1, 3)
                elif self.star.systemHex.age >= 7:
                    return max([0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == "D" else 0)])
                else:
                    return 0
            else:
                return 0

        elif self.category == "Oceanic":
            if self.star.systemHex.age >= 4 + ageModifier:
                return max([0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == "D" else 0)])
            elif self.star.systemHex.age >= roll_xdy(1, 3) + ageModifier:
                return roll_xdy(1, 3)
            else:
                return 0

        elif self.category == "Panthalassic":
            if self.star.systemHex.age >= 4 + ageModifier:
                return roll_xdy(2, 6)
            elif self.star.systemHex.age >= roll_xdy(1, 3) + ageModifier:
                return roll_xdy(1, 3)
            else:
                return 0

        elif self.category == "Promethean":
            if self.star.systemHex.age >= 4 + ageModifier:
                return max([0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == "D" else 0)])
            elif self.star.systemHex.age >= roll_xdy(1, 3) + ageModifier:
                return roll_xdy(1, 3)
            else:
                return 0

        elif self.category == "Snowball":
            if self.subsurfaceOceans and self.star.systemHex.age >= 6 + ageModifier:
                return max(0, roll_xdy(1, 6) + self.size - 2)
            elif self.subsurfaceOceans and self.star.systemHex.age >= roll_xdy(1, 6):
                return max(0, roll_xdy(1, 6) - 3)
            else:
                return 0

        elif self.category == "Tectonic":
            if self.star.systemHex.age >= 4 + ageModifier:
                return max([0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == "D" else 0)])
            elif self.star.systemHex.age >= roll_xdy(1, 3) + ageModifier:
                return roll_xdy(1, 3)
            else:
                return 0

        elif self.category == "Vesperian":
            if self.star.systemHex.age >= 4:
                return roll_xdy(2, 6)
            elif self.star.systemHex.age >= roll_xdy(1, 3):
                return roll_xdy(1, 3)
            else:
                return 0
        else:
            return 0


    def planet_hydrosphere_subsurface_oceans(self, atmosphere):
        """
        Returns hydrosphere, subsurfaceOceans.
            hydrosphere: Integer
                The hydrosphere value of the planet.
            subsurfaceOceans: Boolean
                Flag indicating whether liquid oceans exist beneath a frozen surface.

        Required Parameters:
            atmosphere: Integer
                The current value of the planet's atmosphere.
        """

        if self.category == "Arean":
            return max(0, roll_xdy(2, 3) + self.size - 7 - (4 if atmosphere == 1 else 0)), False

        elif self.category == "Arid":
            return roll_xdy(1, 3), False

        elif self.category == "Hebean":
            return min(11, max(0, roll_xdy(2, 6) + self.size - 11)), False

        elif self.category == "Helian":
            roll = roll_xdy(1, 6)
            return (0, False if roll <= 2 else roll_xdy(2, 6) - 2, False if roll <= 4 else 15, False)

        elif self.category == "Jovian":
            return 16, False

        elif self.category == "Meltball":
            return 15, False

        elif self.category == "Oceanic":
            return (11, True if atmosphere == 1 else 11, False)

        elif self.category == "Panthalassic":
            return 11, False

        elif self.category == "Promethean":
            return roll_xdy(2, 6) - 2, False

        elif self.category == "Rockball":
            roll = roll_xdy(2, 6) + self.size - 11

            if self.star.luminosityClass == "L":
                roll += 1

            if self.orbitType == "Epistellar":
                roll -= 2
            elif self.orbitType == "Outer Zone":
                roll += 2

            return min(11, max(0, roll)), False

        elif self.category == "Snowball":
            return (10, False if roll_xdy(1, 6) <= 3 else roll_xdy(2, 6) - 2, True)

        elif self.category == "Tectonic":
            return roll_xdy(2, 6) - 2, False

        elif self.category == "Telluric":
            return (0, False if roll_xdy(1, 6) <= 4 else 15, False)

        elif self.category == "Vesperian":
            return roll_xdy(2, 6) - 2, False
        else:
            return 0, False


    def dwarf_satellites(self, roll1, roll2):
        """
        Returns the number of dwarf planet satellites orbiting a planet.
        This only applies to Helian and Jovian planets, as they are the only
        types of planets that generate multiple satellites.
        """

        return (max([0, roll1 - (3 if self.groupName == "Helian" else 0) - (1 if roll2 == 6 else 0)]))

    def calculate_desirability(self, alien, nearbyColony):
        """
        Returns the planet's desirability score, which is used to determine
        the extent of colonization. This can be different per Alien.

        Required Parameters:
            alien: Alien class instance
                The alien considering colonization of this planet.
            nearbyColony: Boolean
                Indicates where there is a colony within one jump
                of this planet's system.
        """

        desirability = 0
        modifiedDistance = int(round(
            self.systemHex.distanceFromAlienHomeSystem[alien] / (
                (1 if alien.currentTechLevel == 9 else (
                    alien.currentTechLevel - 9))),
            0)) - (1 if nearbyColony else 0)

        # Distance penalty
        if modifiedDistance > 3 + alien.reactionModifier:
            desirability -= (modifiedDistance - 3 + alien.reactionModifier)

        # Penalty for not having an easy source of fuel in the system
        if not any([self.systemHex.fuelUnrefinedAvailable, self.systemHex.fuelRefinedAvailable]):
            desirability -= 1

        # Penalty for having a flare star in the system
        desirability -= self.systemHex.flareStarDesirabilityPenalty

        # Lifebelt bonus
        if self.orbitType == "Inner Zone":
            if self.star.luminosityClass in ["A-V", "F-V", "K-V"]:
                desirability += 2
            elif self.star.luminosityClass == "M-V":
                desirability += 1

        # Dry world penalty
        if self.hydrosphere in [None, 0]:
            desirability -= 1

        # Extreme environment penalty
        if ((self.size > 12 and self.size != alien.homePlanet.size)
            or (self.atmosphere > 11 and self.atmosphere != alien.homePlanet.atmosphere)
                or (self.hydrosphere == 15 and alien.homePlanet.hydrosphere != 15)):
            desirability -= 2

        # High gravity penalty
        if self.size >= alien.homePlanet.size + 2 and self.atmosphere <= 15:
            desirability -= 1

        # Tiny world penalty
        if self.size == 0:
            desirability -= 1

        # Habitable World bonuses
        if (self.chemistry == alien.homePlanet.chemistry
                and 1 <= self.size <= min(14, alien.homePlanet.size + 3)):
            # Garden world
            if (max(1, alien.homePlanet.size - 3) <= self.size <= min(15, alien.homePlanet.size + 2)
                and (self.atmosphere in acceptableAtmospheres[alien.homePlanet.atmosphere]
                    or (self.subsurfaceOceans and alien.animalClass == "Aquatic"))
                and max((5 if alien.animalClass == "Aquatic" else 2), alien.homePlanet.hydrosphere - 3) <= self.hydrosphere <= min((11 if alien.animalClass == "Aquatic" else 8), alien.homePlanet.hydrosphere + 3)):
                desirability += 5
            # Water world
            elif (2 <= self.atmosphere <= 9
                  and 10 <= self.hydrosphere <= 11
                  and alien.animalClass != "Aquatic"):
                desirability += 3
            # Poor world
            elif (2 <= self.atmosphere <= 6
                  and (2 if alien.animalClass == "Aquatic" else 0) <= self.hydrosphere <= max((4 if alien.animalClass == "Aquatic" else 3), alien.homePlanet.hydrosphere - 4)):
                desirability += 2
            # Other
            elif (2 <= self.atmosphere <= 9
                  and (2 if alien.animalClass == "Aquatic" else 0) <= self.hydrosphere <= 11):
                desirability += 4
        # Not currently habitable, but at least these worlds can be terraformed
        elif (2 <= self.size <= 12
              and self.orbitType == "Inner Zone"
              and self.hydrosphere < 11
              and self.atmosphere < 13
              and self.category not in ["Acheronian", "Asphodelian", "Stygian"]
              and "M-Ve" not in [s.luminosityClass for s in self.systemHex.stars]):
            desirability += 1

        # Ideal atmosphere bonus
        if self.atmosphere == alien.homePlanet.atmosphere:
            desirability += 1

        return desirability

    def calculate_desirability_jovian_asteroid_belt(self, alien, nearbyColony):
        """
        Returns the planet's desirability score, which is used to determine
        the extent of colonization. This can be different per Alien.
        This applies only to Jovians and Asteroid Belts as you don't live
        "on" them, but in stations.

        Required Parameters:
            alien: Alien class instance
                The alien considering colonization of this planet.
            nearbyColony: Boolean
                Indicates where there is a colony within one jump
                of this planet's system.
        """

        desirability = self.baseDesirability
        modifiedDistance = int(round(
            self.systemHex.distanceFromAlienHomeSystem[alien] / (
                (1 if alien.currentTechLevel == 9 else (
                    alien.currentTechLevel - 9))),
            0)) - (1 if nearbyColony else 0)

        # Distance penalty
        if modifiedDistance > 3 + alien.reactionModifier:
            desirability -= modifiedDistance

        # Penalty for not having an easy source of fuel in the system
        if not any([self.systemHex.fuelUnrefinedAvailable, self.systemHex.fuelRefinedAvailable]):
            desirability -= 1

        colonyInSystem = any(p.groupName not in ["Jovian", "Asteroid Belt"] and alien in p.habitation.keys() and p.habitation[alien] in ["Colony", "Homeworld"] for p in self.systemHex.planets)
        outpostInSystem = any(p.groupName not in ["Jovian", "Asteroid Belt"] and alien in p.habitation.keys() and p.habitation[alien] == "Outpost" for p in self.systemHex.planets)

        if not colonyInSystem and not outpostInSystem:
            desirability -= 3
        elif not colonyInSystem and outpostInSystem:
            desirability -= 1

        return desirability

    def calculate_habitation(
            self,
            alien,
            alienSurvivalPercent,
            maxTechLevel,
            maxReactionModifier,
            outpostPossible):
        """
        Sets the type of Habitation an Alien will have on the planet.
        Not applicable for Homeworld because that is set at the time of Alien creation.

        Required Parameters:
            alien: Alien class instance
                The alien considering colonization of this planet.
            alienSurvivalPercent: Integer
                An integer representing the percent chance of an
                alien surviving to Tech Level 10.
            maxTechLevel: Integer
                The maximum possible Tech Level.
            maxReactionModifier: Integer
                The maximum Reaction Modifier across all non-extinct
                aliens.
            outpostPossible: Boolean
                Indicates where an Outpost can be created.
        """

        if self == alien.homePlanet:
            if not alien.extinct:
                self.systemHex.create_surrounding_systems(alienSurvivalPercent, maxTechLevel, maxReactionModifier)
            self.habitation[alien] = "Homeworld"
            alien.planets[self]["habitation"] = "Homeworld"
            return

        homeSystem = alien.homePlanet.systemHex == self.systemHex
        hab = None

        if not self.alien or not self.alien.extinct:
            if alien.currentTechLevel >= 10 or (alien.currentTechLevel == 9 and homeSystem):
                if alien.planets[self]["colonyRoll"] - 2 <= alien.planets[self]["desirability"]:
                    hab = "Colony"
                    self.systemHex.create_surrounding_systems(alienSurvivalPercent, maxTechLevel, maxReactionModifier)
                elif outpostPossible and alien.planets[self]["outpostRoll"] - (1 if homeSystem else 0) <= alien.currentTechLevel + alien.planets[self]["desirability"] - 10:
                    hab = "Outpost"
                    self.systemHex.create_surrounding_systems(alienSurvivalPercent, maxTechLevel, maxReactionModifier)
                else:
                    hab = None
        else:
            hab = None

        # If an alien is in the process of terraforming and they
        # have made the planet temporarily worse, they won't
        # abandon it. Otherwise, a lower level of habitation
        # causes ruins to be present on the planet.
        previousHabitation = self.habitation.get(alien)
        if previousHabitation and not hab and self.terraformingAlien == alien:
            hab = "Outpost"

        return hab

    def terraform_planet(self, alien):
        """
        Changes something about the planet to increase desirability over the long run.

        Required Parameters:
            alien: Alien class instance
                The alien doing the terraforming.

        Returns True if something was changed, otherwise returns False.
        """
        
        # If there's no chemistry, nothing has to be changed, it just happens
        # as part of terraforming
        if not self.chemistry:
            self.chemistry = alien.homePlanet.chemistry
        # If the chemistry is wrong, reduce Hydrosphere to 1, then convert
        elif self.chemistry != alien.homePlanet.chemistry:
            if self.hydrosphere > 1:
                self.hydrosphere -= 1
                return True
            else:
                self.chemistry = alien.homePlanet.chemistry
                return True

        # Remove Dry World penalty
        if self.hydrosphere == 0:
            self.hydrosphere += 1
            return True

        # Get Atmosphere into the Habitable range.
        # If Hydrosphere 2+ and Atmosphere 12-13, reduce Hydrosphere to 1
        # then reduce the Atmosphere
        if self.atmosphere == 13 and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
            self.atmosphere -= 1
            return True
        elif self.atmosphere == 12 and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
            if 2 <= self.hydrosphere <= 10:
                self.hydrosphere -= 1
                return True
            elif self.hydrosphere < 2:
                self.atmosphere -= 1
                return True
        elif self.atmosphere > 9 and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
            self.atmosphere -= 1
            return True
        elif self.atmosphere < 2 and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
            self.atmosphere += 1
            return True

        # At this point, the planet should have one of the Habitable World bonuses
        # If it's Poor, improve it to Other by raising Hydrosphere
        if self.hydrosphere <= max((4 if alien.animalClass == "Aquatic" else 3), alien.homePlanet.hydrosphere - 4):
            self.hydrosphere += 1
            return True

        # If it's Water World and Hydrosphere 10, reduce Hydrosphere to improve it to Other
        # Does not apply to Aquatics
        if self.hydrosphere == 10 and alien.animalClass != "Aquatic":
            self.hydrosphere -= 1
            return True

        # If the planet's size would allow it to be a Garden world, work
        # towards that
        if max(1, alien.homePlanet.size - 3) <= self.size <= min(15, alien.homePlanet.size + 2):
            # Lower Hydrosphere if it's too high
            if self.hydrosphere > min((11 if alien.animalClass == "Aquatic" else 8), alien.homePlanet.hydrosphere + 3):
                self.hydrosphere -= 1
                return True
            # Raise Hydrosphere if it's too low
            if self.hydrosphere < max((5 if alien.animalClass == "Aquatic" else 2), alien.homePlanet.hydrosphere - 3):
                self.hydrosphere += 1
                return True
            # Lower Atmosphere if it's too high
            if any([alien.homePlanet.atmosphere == 2 and self.atmosphere > 4,
                    alien.homePlanet.atmosphere == 3 and self.atmosphere > 5,
                    alien.homePlanet.atmosphere == 4 and self.atmosphere > 7,
                    alien.homePlanet.atmosphere == 5 and self.atmosphere > 6,
                    alien.homePlanet.atmosphere == 6 and self.atmosphere > 8,
                    alien.homePlanet.atmosphere == 7 and self.atmosphere > 9,
                    alien.homePlanet.atmosphere == 8 and self.atmosphere > 9,
                    alien.homePlanet.atmosphere == 9 and self.atmosphere > 9]):
                self.atmosphere -= 1
                return True
            # Raise Atmosphere if it's too low
            if any([alien.homePlanet.atmosphere == 2 and self.atmosphere < 2,
                    alien.homePlanet.atmosphere == 3 and self.atmosphere < 3,
                    alien.homePlanet.atmosphere == 4 and self.atmosphere < 2,
                    alien.homePlanet.atmosphere == 5 and self.atmosphere < 3,
                    alien.homePlanet.atmosphere == 6 and self.atmosphere < 5,
                    alien.homePlanet.atmosphere == 7 and self.atmosphere < 4]):
                self.atmosphere += 1
                return True

        # Get the Atmosphere to match the homeworld's
        if self.atmosphere > alien.homePlanet.atmosphere:
            self.atmosphere -= 1
            return True
        elif self.atmosphere < alien.homePlanet.atmosphere:
            self.atmosphere += 1
            return True

        # If the planet has only microscopic life,
        # work to eliminate enough of it so life
        # can be imported from elsewhere.
        if 2 < self.biosphere < 7:
            self.biosphere -= 1
            if self.biosphere <= 2:
                self.seedWithLife = True
            return True

        # If nothing was done, the planet has been
        # terraformed as much as it can, set a flag
        # so we don't run this method for this instance
        # anymore.
        self.terraformingDone = True
        return False
        

    def planet_terrain(self):
        """
        Returns a list of terrains found on the planet.
        """

        terrain = []

        if self.hydrosphere <= 8:
            terrain.append("Mountains")
            terrain.append("Rough/Broken")
            terrain.append("Hills")
            terrain.append("Clear")

        if self.atmosphere >= 2 and (2 <= self.hydrosphere <= 8):
            terrain.append("Beach/Shore")

        if (self.atmosphere >= 2 and 5 <=
                self.hydrosphere <= 11) or self.subsurfaceOceans:
            terrain.append("Deep Ocean")

        if self.biosphere >= 9 and self.hydrosphere <= 4 and 2 <= self.atmosphere <= 7:
            terrain.append("Desert")

        if self.biosphere >= 9 and self.atmosphere >= 4 and 3 <= self.hydrosphere <= 8:
            terrain.append("Forest")

        if self.biosphere >= 9 and self.atmosphere >= 4 and 4 <= self.hydrosphere <= 8:
            terrain.append("Jungle")

        if (self.atmosphere >= 2 and 3 <=
                self.hydrosphere <= 11) or self.subsurfaceOceans:
            terrain.append("Open Ocean")

        if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 7:
            terrain.append("Plains")

        if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
            terrain.append("Rainforest")

        if self.atmosphere >= 2 and 3 <= self.hydrosphere <= 8:
            terrain.append("Riverbank")

        if (self.atmosphere >= 2 and 2 <= self.hydrosphere <= 10) or (
                self.subsurfaceOceans and self.hydrosphere <= 10):
            terrain.append("Shallow Ocean")

        if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
            terrain.append("Swamp/Marsh")

        if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 8:
            terrain.append("Woods")

        return terrain
        

    def planet_animals(self):
        """
        Adds animals for each terrain.
        """

        animals = []
        for terrain in self.terrain:
            if terrain == "Beach/Shore":
                for _ in range(3):
                    animals.append(animal.Amphibian(planet=self, terrain=terrain))
                    animals.append(animal.Aquatic(planet=self, terrain=terrain))
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
            elif terrain == "Clear":
                for _ in range(3):
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Mammal(planet=self, terrain=terrain))
            elif terrain == "Deep Ocean":
                for _ in range(3):
                    animals.append(animal.Aquatic(planet=self, terrain=terrain))
            elif terrain == "Desert":
                for _ in range(3):
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Reptile(planet=self, terrain=terrain))
            elif terrain == "Forest":
                for _ in range(3):
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Fungal(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Mammal(planet=self, terrain=terrain))
            elif terrain == "Hills":
                for _ in range(3):
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Mammal(planet=self, terrain=terrain))
                    animals.append(animal.Reptile(planet=self, terrain=terrain))
            elif terrain == "Jungle":
                for _ in range(3):
                    animals.append(animal.Amphibian(planet=self, terrain=terrain))
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Fungal(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Reptile(planet=self, terrain=terrain))
            elif terrain == "Mountains":
                for _ in range(3):
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
            elif terrain == "Open Ocean":
                for _ in range(3):
                    animals.append(animal.Aquatic(planet=self, terrain=terrain))
            elif terrain == "Plains":
                for _ in range(3):
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Mammal(planet=self, terrain=terrain))
                    animals.append(animal.Reptile(planet=self, terrain=terrain))
            elif terrain == "Rainforest":
                for _ in range(3):
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Fungal(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Reptile(planet=self, terrain=terrain))
            elif terrain == "Riverbank":
                for _ in range(3):
                    animals.append(animal.Amphibian(planet=self, terrain=terrain))
                    animals.append(animal.Aquatic(planet=self, terrain=terrain))
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Mammal(planet=self, terrain=terrain))
                    animals.append(animal.Reptile(planet=self, terrain=terrain))
            elif terrain == "Rough/Broken":
                for _ in range(3):
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Reptile(planet=self, terrain=terrain))
            elif terrain == "Shallow Ocean":
                for _ in range(3):
                    animals.append(animal.Amphibian(planet=self, terrain=terrain))
                    animals.append(animal.Aquatic(planet=self, terrain=terrain))
                    animals.append(animal.Avian(planet=self, terrain=terrain))
            elif terrain == "Swamp/Marsh":
                for _ in range(3):
                    animals.append(animal.Amphibian(planet=self, terrain=terrain))
                    animals.append(animal.Aquatic(planet=self, terrain=terrain))
                    animals.append(animal.Avian(planet=self, terrain=terrain))
                    animals.append(animal.Fungal(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Reptile(planet=self, terrain=terrain))
            elif terrain == "Woods":
                for _ in range(3):
                    animals.append(animal.Fungal(planet=self, terrain=terrain))
                    animals.append(animal.Insect(planet=self, terrain=terrain))
                    animals.append(animal.Mammal(planet=self, terrain=terrain))

        return animals


    def planet_population(self, alien):
        """
        Sets the alien populations for the planet.
        This sets both the relative and actual population.
        Actual population modifies the relative population
        using the alien's Pack score from its animal base.
        Homeworld population has random variations because
        the desirability of the homeworld should never
        change.
        """

        previousPopulation = self.population
        popNum = 0
        if not self.habitation[alien]:
            return

        if alien not in self.alienPopulation:
            return {"homeworldRoll": roll_xdy(2, 6),
                "colonyRoll": roll_xdy(1, 3) - roll_xdy(1, 3),
                "outpostRoll": roll_xdy(1, 3),
                "relative": None,
                "actual": None}
        
        if alien.extinct:
            return {"homeworldRoll": None,
                "colonyRoll": None,
                "outpostRoll": None,
                "relative": 0,
                "actual": 0}
        # If the alien has abandonded this planet but previously had a population
        # there, remove the population.
        elif not self.habitation[alien] and (len(self.alienPopulation[alien]["relative"]) > 1 and self.alienPopulation[alien]["relative"][-1] != 0):
            return {"homeworldRoll": self.alienPopulation[alien]["homeworldRoll"],
                "colonyRoll": self.alienPopulation[alien]["colonyRoll"],
                "outpostRoll": self.alienPopulation[alien]["outpostRoll"],
                "relative": 0,
                "actual": 0}
        elif self.habitation[alien] == "Homeworld":
            # This ensures the homeworld population changes a little over time.
            homeworldPopRoll = roll_xdy(1, 3) - roll_xdy(1, 3)
            if alien.planets[self]["desirability"] + homeworldPopRoll > self.alienPopulation[alien]["homeworldRoll"]:
                basePop = min(12, alien.planets[self]["desirability"] + homeworldPopRoll)
            else:
                basePop = self.alienPopulation[alien]["homeworldRoll"]
        elif self.habitation[alien] == "Colony":
            if alien.currentTechLevel + self.settlement - 9 > alien.planets[self]["desirability"] + self.alienPopulation[alien]["colonyRoll"]:
                basePop = max(4, min(12, alien.planets[self]["desirability"] + self.alienPopulation[alien]["colonyRoll"]))
            else:
                basePop = max(4, alien.currentTechLevel + self.settlement - 9)
        elif self.habitation[alien] == "Outpost":
            basePop = max(1, min(4, alien.planets[self]["desirability"] + self.alienPopulation[alien]["outpostRoll"]))

        # This is the first digit of the population number.
        popString = str(roll_xdy(1, 9))

        # This generates the rest of the population numbers (can use 0 here).
        # Industry can affect population, see planet_industry_effects.
        for _ in range(basePop + self.industryPopulationEffect + 1):
            popString += str(roll_xdy(1, 10) - 1)

        self.alienPopulation[alien]["relative"] = int(popString)
        self.alienPopulation[alien]["actual"] = int(int(popString) * alien.populationModifier)
        alien.planets[self]["population"] = self.alienPopulation[alien]["actual"]

        # Sum up the population numbers so we can get a score and actual
        # population number for the planet as a whole.
        if self.alienPopulation:
            populationNumbers = []
            populationRelative = []
            for a in self.alienPopulation:
                populationNumbers.append(self.alienPopulation[a]["actual"])
                populationRelative.append(self.alienPopulation[a]["relative"])
                
            self.populationNumber = sum(populationNumbers)
            
            if self.populationNumber == 0:
                self.population = 0
            else:
                self.population = len(str(sum(populationRelative))) - 1


    def planet_government(self):
        """
        Sets the planet's government.
        """

        previousGovernment = self.government

        # The roll is only made once so it doesn't radically change constantly.
        if not self.governmentRoll:
            self.governmentRoll = roll_xdy(2, 6) - 7

        if "Homeworld" in self.habitation.values():
            if self.terraformingAlien.currentTechLevel == 0:
                self.government = 0
            elif roll_xdy(1, 6) <= self.terraformingAlien.currentTechLevel - 9:
                self.government = 7
            else:
                self.government = max(0, self.population + self.governmentRoll)
        elif "Colony" in self.habitation.values():
            self.government = max(0, self.population + self.governmentRoll)
        elif "Outpost" in self.habitation.values():
            if self.population == 0:
                self.government = 0
            else: self.government = min(6, max(0, self.population + self.governmentRoll))
        else:
            self.government = 0


    def planet_law_level(self):
        """
        Sets the planet's law level.
        """

        previousLawLevel = self.lawLevel

        # The roll is only made once so it doesn't radically change constantly.
        if not self.lawLevelRoll:
            self.lawLevelRoll = roll_xdy(2, 6) - 7

        if self.government == 0:
            self.lawLevel = 0
        else:
            self.lawLevel = max(0, self.government + self.lawLevelRoll)


    def planet_industry(self):
        """
        Sets the planet's industry.
        """

        previousIndustry = self.industry

        # The roll is only made once so it doesn't radically change constantly.
        if not self.industryRoll:
            self.industryRoll = roll_xdy(2, 6) - 7

        if self.population == 0:
            self.industry = 0
        else:
            industry = self.population + self.industryRoll
            
            if 1 <= self.lawLevel <= 3:
                industry += 1
            elif 6 <= self.lawLevel <= 9:
                industry -= 1
            elif 10 <= self.lawLevel <= 13:
                industry -= 2
            elif self.lawLevel >= 14:
                industry -= 3

            if 12 <= self.terraformingAlien.currentTechLevel <= 14:
                industry += 1
            elif self.terraformingAlien.currentTechLevel >= 15:
                industry += 2

            if self.hydrosphere == 15 or self.atmosphere not in acceptableAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
                industry += 1

            self.industry = max(0, industry)

            # Determine if a new industrial effect needs to be applied.
            if not previousIndustry:
                previousIndustry = -1
                
            if (self.industry == 0
                or (1 <= self.industry <= 3 and (previousIndustry < 1 or previousIndustry > 3))
                or (4 <= self.industry <= 9 and (previousIndustry < 4 or previousIndustry > 9))
                or (self.industry >= 10 and previousIndustry < 10)):
                return True
            
        return False


    def planet_industry_effects(self):
        """
        Modifies the planet's population based on Industry
        and also sets whether the planet has industrial pollution.
        """

        roll = roll_xdy(1, 2)
        
        if self.industry == 0:
            self.industryPopulationEffect = -1
            self.pollution = False
        elif 1 <= self.industry <= 3:
            self.industryPopulationEffect = 0
            self.pollution = False
        elif 4 <= self.industry <= 9:
            self.industryPopulationEffect = 1
            self.pollution = True
        elif self.industry >= 10 and roll == 1:
            self.industryPopulationEffect = 1
            self.pollution = False
        elif self.industry >= 10 and roll == 2:
            self.industryPopulationEffect = 2
            self.pollution = True


    def planet_trade_codes(self, maxTechLevel):
        """
        Sets the planet's trade codes.

        Required Parameters:
            maxTechLevel: Integer
                The maximum possible Tech Level.
        """

        if (4 <= self.atmosphere <= 9
                and 4 <= self.hydrosphere <= 8
                and 5 <= self.population <= 7):
            if "Ag" not in self.tradeCodes:
                self.tradeCodes.add("Ag")
        else:
            if "Ag" in self.tradeCodes:
                self.tradeCodes.discard("Ag")
        
        if self.category == "Asteroid Belt":
            if "As" not in self.tradeCodes:
                self.tradeCodes.add("As")
        else:
            if "As" in self.tradeCodes:
                self.tradeCodes.discard("As")
        
        if (2 <= self.atmosphere <= 13
                and self.hydrosphere == 0):
            if "De" not in self.tradeCodes:
                self.tradeCodes.add("De")
        else:
            if "De" in self.tradeCodes:
                self.tradeCodes.discard("De")
        
        if ((self.atmosphere >= 10
                    or self.chemistry != "Water")
                and 1 <= self.hydrosphere <= 11):
            if "Fl" not in self.tradeCodes:
                self.tradeCodes.add("Fl")
        else:
            if "Fl" in self.tradeCodes:
                self.tradeCodes.discard("Fl")
        
        if (max(1, self.terraformingAlien.homePlanet.size - 3) <= self.size <= min(15, self.terraformingAlien.homePlanet.size + 2)
                and self.atmosphere in acceptableAtmospheres[self.terraformingAlien.homePlanet.atmosphere]
                and max((5 if self.terraformingAlien.animalClass == "Aquatic" else 2), self.terraformingAlien.homePlanet.hydrosphere - 3) <= self.hydrosphere <= min((11 if self.terraformingAlien.animalClass == "Aquatic" else 8), self.terraformingAlien.homePlanet.hydrosphere + 3)):
            if "Ga" not in self.tradeCodes:
                self.tradeCodes.add("Ga")
        else:
            if "Ga" in self.tradeCodes:
                self.tradeCodes.discard("Ga")
        
        if self.population >= 9:
            if "Hi" not in self.tradeCodes:
                self.tradeCodes.add("Hi")
        else:
            if "Hi" in self.tradeCodes:
                self.tradeCodes.discard("Hi")
        
        if self.industry >= maxTechLevel - 3:
            if "Ht" not in self.tradeCodes:
                self.tradeCodes.add("Ht")
        else:
            if "Ht" in self.tradeCodes:
                self.tradeCodes.discard("Ht")
        
        if (self.atmosphere <= 1
                and self.hydrosphere >= 1):
            if "Ic" not in self.tradeCodes:
                self.tradeCodes.add("Ic")
        else:
            if "Ic" in self.tradeCodes:
                self.tradeCodes.discard("Ic")
        
        if (self.population >= 9
                and self.industry >= 6):
            if "In" not in self.tradeCodes:
                self.tradeCodes.add("In")
        else:
            if "In" in self.tradeCodes:
                self.tradeCodes.discard("In")
        
        if 1 <= self.population <= 3:
            if "Lo" not in self.tradeCodes:
                self.tradeCodes.add("Lo")
        else:
            if "Lo" in self.tradeCodes:
                self.tradeCodes.discard("Lo")
        
        if self.industry <= 5:
            if "Lt" not in self.tradeCodes:
                self.tradeCodes.add("Lt")
        else:
            if "Lt" in self.tradeCodes:
                self.tradeCodes.discard("Lt")
        
        if ((self.atmosphere <= 3
                    or self.atmosphere >= 11)
                and (self.hydrosphere <= 3
                    or self.hydrosphere >= 11)
                and self.population >= 6):
            if "Na" not in self.tradeCodes:
                self.tradeCodes.add("Na")
        else:
            if "Na" in self.tradeCodes:
                self.tradeCodes.discard("Na")
        
        if 4 <= self.population <= 6:
            if "Ni" not in self.tradeCodes:
                self.tradeCodes.add("Ni")
        else:
            if "Ni" in self.tradeCodes:
                self.tradeCodes.discard("Ni")
        
        if (2 <= self.atmosphere <= 5
                and self.hydrosphere <= 3):
            if "Po" not in self.tradeCodes:
                self.tradeCodes.add("Po")
        else:
            if "Po" in self.tradeCodes:
                self.tradeCodes.discard("Po")
        
        if (6 <= self.population <= 8
                and self.atmosphere in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]):
            if "Ri" not in self.tradeCodes:
                self.tradeCodes.add("Ri")
        else:
            if "Ri" in self.tradeCodes:
                self.tradeCodes.discard("Ri")
        
        if self.biosphere == 0:
            if "St" not in self.tradeCodes:
                self.tradeCodes.add("St")
        else:
            if "St" in self.tradeCodes:
                self.tradeCodes.discard("St")
        
        if (self.atmosphere >= 2
                and 10 <= self.hydrosphere <= 11):
            if "Wa" not in self.tradeCodes:
                self.tradeCodes.add("Wa")
        else:
            if "Wa" in self.tradeCodes:
                self.tradeCodes.discard("Wa")
        
        if self.atmosphere == 0:
            if "Va" not in self.tradeCodes:
                self.tradeCodes.add("Va")
        else:
            if "Va" in self.tradeCodes:
                self.tradeCodes.discard("Va")
        
        if self.biosphere >= 7:
            if "Zo" not in self.tradeCodes:
                self.tradeCodes.add("Zo")
        else:
            if "Zo" in self.tradeCodes:
                self.tradeCodes.discard("Zo")


    def planet_starport(self):
        """
        Sets the planet's starport.
        """

        previousStarport = self.starport

        # The roll is only made once so it doesn't radically change constantly.
        if not self.starportRoll:
            self.starportRoll = roll_xdy(2, 6) - 7

        score = self.starportRoll + self.industry
        if "Ag" in self.tradeCodes:
            score += 1
        if "Ga" in self.tradeCodes:
            score += 1
        if "Hi" in self.tradeCodes:
            score += 1
        if "Ht" in self.tradeCodes:
            score += 1
        if "In" in self.tradeCodes:
            score += 1
        if "Na" in self.tradeCodes:
            score += 1
        if "Ri" in self.tradeCodes:
            score += 1
        if self.terraformingAlien.currentTechLevel >= 12:
            score += 1
        if self.terraformingAlien.currentTechLevel >= 15:
            score += 1
        if "Po" in self.tradeCodes:
            score -= 1
        if self.terraformingAlien.currentTechLevel <= 9:
            score -= 1

        # An Outpost world with Population 0 automatically has the equivalent of an E-class starport,
        # in the form of an unmanned navigation beacon and emergency supply cache.
        # Any world with Industry 5+ must have at least the equivalent of an E-class starport,
        # in its airstrips or surface shipping ports.
        # Any uninhabitable world with Population 1+ must have at least the equivalent of an E-class starport,
        # in its airlocks and docking ports.
        if (score < 3
                and ("Outpost" in self.habitation.values()
                    or self.industry >= 5
                    or self.atmosphere not in acceptableAtmospheres[self.terraformingAlien.homePlanet.atmosphere])):
            score = 3

        self.starport = starportTable[score]

        if self.starport in ["D", "C"]:
            self.star.systemHex.fuelUnrefinedAvailable = True

        if self.starport in ["B", "A"]:
            self.star.systemHex.fuelRefinedAvailable = True

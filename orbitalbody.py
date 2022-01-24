import globalvariables
import asteroidbelt
import planet
from diceroller import roll_xdy


def create_orbital_body(star,
        order,
        orbitType):
    roll = roll_xdy(1, 6)
    roll -= (1 if star.spectralType == globalvariables.luminosityClass.L else 0)

    if roll <= 1:
        asteroidbelt.create_asteroid_belt(
            star,
            star,
            order,
            orbitType)
    else:
        planet.create_planet(
            star,
            star,
            order,
            orbitType)


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
        if planetGroupToCreate == globalvariables.group.DwarfPlanet:
            planet.create_dwarf_planet(
                self.star,
                self.parentObject,
                self.order,
                self.orbitType)
        elif planetGroupToCreate == globalvariables.group.TerrestrialPlanet:
            planet.create_terrestrial_planet(
                self.star,
                self.parentObject,
                self.order,
                self.orbitType)
        elif planetGroupToCreate == globalvariables.group.HelianPlanet:
            planet.create_helian_planet(
                self.star,
                self.parentObject,
                self.order,
                self.orbitType)

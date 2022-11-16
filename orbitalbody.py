from animal import create_amphibian, create_aquatic, create_avian, create_fungal, create_insect, create_mammal, create_reptile
from alien import create_alien
from globalstuff import roll_xdy, coin_flip, group, luminosityClass
from globalstuff import category, className, type, chemistry, orbitType
from globalstuff import LookupTable, starport, terrain, animalClass
from globalstuff import habitation, tradeCode, maxTechLevel, alienSurvivalPercent


allBodies = []

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
            star,
            order,
            orbitType,
            roll=roll)


def create_planet(star, parentObject, order, orbitType, roll=100, groupToCreate=None):
    if not roll and not groupToCreate:
        raise ValueError

    if roll <= 2 or groupToCreate == group.DwarfPlanet:
        create_dwarf_planet(star, parentObject, order, orbitType)
    elif roll <= 3 or groupToCreate == group.TerrestrialPlanet:
        create_terrestrial_planet(star, parentObject, order, orbitType)
    elif roll <= 4 or groupToCreate == group.HelianPlanet:
        create_helian_planet(star, parentObject, order, orbitType)
    else:
        create_jovian_planet(star, parentObject, order, orbitType)


def create_dwarf_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        Stygian(star, parentObject, order, orbitType)
        
    roll = roll_xdy(1, 6)
    roll2 = roll_xdy(1, 6)

    # If this planet is part of an asteroid belt
    if (star != parentObject and parentObject.group == group.AsteroidBelt):
        roll -= 2

    if orbitType == orbitType.Epistellar:
        create_epistellar_dwarf_planet(star, parentObject, order, orbitType, roll, roll2)
        
    # If this planet is orbiting a helian planet
    if (star != parentObject and parentObject.group == group.HelianPlanet):
        roll += 1
    # If this planet is orbiting a jovian planet
    elif (star != parentObject and parentObject.group == group.JovianPlanet):
        roll += 2

    if orbitType == orbitType.InnerZone:
        create_inner_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2)
    elif orbitType == orbitType.OuterZone:
        create_outer_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2)


def create_terrestrial_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        Acheronian(star, parentObject, order, orbitType)
        
    if orbitType == orbitType.Epistellar:
        create_epistellar_terrestrial_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == orbitType.InnerZone:
        create_inner_zone_terrestrial_planet(star, parentObject, order, orbitType, roll_xdy(2, 6))
    elif orbitType == orbitType.OuterZone:
        create_outer_zone_terrestrial_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))


def create_helian_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        Asphodelian(star, parentObject, order, orbitType)
        
    if orbitType == orbitType.Epistellar:
        create_epistellar_helian_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == orbitType.InnerZone:
        create_inner_zone_helian_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == orbitType.OuterZone:
        create_outer_zone_helian_planet(star, parentObject, order, orbitType)


def create_jovian_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        Chthonian(star, parentObject, order, orbitType)
        
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
        Asphodelian(star, parentObject, order, orbitType)


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
        star.orbitalBodies[-1],
        star.orbitalBodies[-1].order,
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
            The type of orbit the OrbitalBody is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
    """

    def __init__(
            self,
            star,
            parentObject,
            order,
            orbitType):
        allBodies.append(self)
        self.systemHex = star.systemHex
        self.systemHex.orbitalBodies.append(self)
        self.star = star
        self.star.orbitalBodies.append(self)
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
        # The roll is only made once so it doesn't radically change constantly.
        self.governmentRoll = roll_xdy(2, 6) - 7
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
        create_planet(
            self.star,
            self,
            self.order,
            self.orbitType,
            groupToCreate=planetGroupToCreate)

    def calculate_habitation(
            self,
            alien,
            maxReactionModifier,
            outpostPossible):
        """
        Returns the type of Habitation an Alien will have on the orbital body.

        Required Parameters:
            alien: Alien class instance
                The alien considering colonization of this orbital body.
            maxReactionModifier: Integer
                The maximum Reaction Modifier across all non-extinct
                aliens.
            outpostPossible: Boolean
                Indicates where an Outpost can be created.
        """
        if self.properName == "Terra" and alien.name != "Terran":
            pass
        if self == alien.homePlanet:
            if not alien.extinct:
                self.systemHex.create_surrounding_systems(maxReactionModifier)
            self.habitation[alien] = habitation.Homeworld
            alien.orbitalBodies[self]["habitation"] = habitation.Homeworld
            self.terraformingAlien = self.homeAlien
            return

        homeSystem = alien.homePlanet.systemHex == self.systemHex
        hab = None

        if not self.homeAlien or not self.homeAlien.extinct:
            if alien.currentTechLevel >= 10 or (alien.currentTechLevel == 9 and homeSystem):
                if alien.orbitalBodies[self]["colonyRoll"] - 2 <= alien.orbitalBodies[self]["desirability"]:
                    hab = habitation.Colony
                    self.terraformingAlien = alien
                    self.systemHex.create_surrounding_systems(maxReactionModifier)
                elif outpostPossible and alien.orbitalBodies[self]["outpostRoll"] - (1 if homeSystem else 0) <= alien.currentTechLevel + alien.orbitalBodies[self]["desirability"] - 10:
                    hab = habitation.Outpost
                    self.terraformingAlien = alien
                    self.systemHex.create_surrounding_systems(maxReactionModifier)
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
            hab = habitation.Outpost

        return hab


    def set_population(self):
        """
        Sets the alien populations for the orbital body.
        This sets both the relative and actual population.
        Actual population modifies the relative population
        using the alien's Pack score from its animal base.
        Homeworld population has random variations because
        the desirability of the homeworld should never
        change.
        """

        previousPopulation = self.population
        popNum = 0

        for alien in self.habitation:
            if not self.habitation[alien]:
                self.alienPopulation[alien] = None
                continue
        
            if alien.extinct:
                self.alienPopulation[alien] = {
                    "homeworldRoll": None,
                    "colonyRoll": None,
                    "outpostRoll": None,
                    "relative": 0,
                    "actual": 0
                }
                self.alienPopulation[alien]["relative"] = 0
                self.alienPopulation[alien]["actual"] = 0
                continue

            # If the alien has abandonded this orbital body but previously had a population
            # there, remove the population.
            if not self.habitation[alien] and (len(self.alienPopulation[alien]["relative"]) > 1 and self.alienPopulation[alien]["relative"][-1] != 0):
                self.alienPopulation[alien]["relative"] = 0
                self.alienPopulation[alien]["actual"] = 0
                continue

            if alien not in self.alienPopulation:
                self.alienPopulation[alien] = {
                    "colonyRoll": roll_xdy(1, 3) - roll_xdy(1, 3),
                    "outpostRoll": roll_xdy(1, 3),
                    "relative": None,
                    "actual": None
                }

                if self.habitation[alien] == habitation.Homeworld:
                    self.alienPopulation[alien]["homeworldRoll"] = roll_xdy(2, 6)

            if self.habitation[alien] == habitation.Homeworld:
                # This ensures the homeworld population changes a little over time.
                homeworldPopRoll = roll_xdy(1, 3) - roll_xdy(1, 3)
                if alien.orbitalBodies[self]["desirability"] + homeworldPopRoll > self.alienPopulation[alien]["homeworldRoll"]:
                    basePop = min(12, alien.orbitalBodies[self]["desirability"] + homeworldPopRoll)
                else:
                    basePop = self.alienPopulation[alien]["homeworldRoll"]
            elif self.habitation[alien] == habitation.Colony:
                if alien.currentTechLevel + self.settlement - 9 > alien.orbitalBodies[self]["desirability"] + self.alienPopulation[alien]["colonyRoll"]:
                    basePop = max(4, min(12, alien.orbitalBodies[self]["desirability"] + self.alienPopulation[alien]["colonyRoll"]))
                else:
                    basePop = max(4, alien.currentTechLevel + self.settlement - 9)
            elif self.habitation[alien] == habitation.Outpost:
                basePop = max(1, min(4, alien.orbitalBodies[self]["desirability"] + self.alienPopulation[alien]["outpostRoll"]))

            # This is the first digit of the population number.
            popString = str(roll_xdy(1, 9))

            # This generates the rest of the population numbers (can use 0 here).
            # Industry can affect population, see set_industry_effects.
            for _ in range(basePop + self.industryPopulationEffect + 1):
                popString += str(roll_xdy(1, 10) - 1)

            self.alienPopulation[alien]["relative"] = int(popString)
            self.alienPopulation[alien]["actual"] = int(int(popString) * alien.populationModifier)
            alien.orbitalBodies[self]["population"] = self.alienPopulation[alien]["actual"]

        # Sum up the population numbers so we can get a score and actual
        # population number for the orbital body as a whole.
        if self.alienPopulation:
            populationNumbers = []
            populationRelative = []
            for a in self.alienPopulation:
                if self.alienPopulation[a]:
                    populationNumbers.append(self.alienPopulation[a]["actual"])
                    populationRelative.append(self.alienPopulation[a]["relative"])
                
            self.populationNumber = sum(populationNumbers)
            
            if self.populationNumber == 0:
                self.population = 0
            else:
                self.population = len(str(sum(populationRelative))) - 1


    def set_government(self):
        """
        Sets the government.
        """

        previousGovernment = self.government

        if habitation.Homeworld in self.habitation.values():
            if self.terraformingAlien.currentTechLevel == 0:
                self.government = 0
            elif roll_xdy(1, 6) <= self.terraformingAlien.currentTechLevel - 9:
                self.government = 7
            else:
                self.government = max(0, self.population + self.governmentRoll)
        elif habitation.Colony in self.habitation.values():
            self.government = max(0, self.population + self.governmentRoll)
        elif habitation.Outpost in self.habitation.values():
            if self.population == 0:
                self.government = 0
            else: self.government = min(6, max(0, self.population + self.governmentRoll))
        else:
            self.government = 0


    def set_law_level(self):
        """
        Sets the law level.
        """

        previousLawLevel = self.lawLevel

        # The roll is only made once so it doesn't radically change constantly.
        if not self.lawLevelRoll:
            self.lawLevelRoll = roll_xdy(2, 6) - 7

        if self.government == 0:
            self.lawLevel = 0
        else:
            self.lawLevel = max(0, self.government + self.lawLevelRoll)


    def set_industry(self):
        """
        Sets the industry level.
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


    def set_industry_effects(self):
        """
        Modifies the population based on Industry
        and also sets whether the orbital body has industrial pollution
        (does not apply to Asteroid Belts or Jovians).
        """
        
        if self.industry == 0:
            self.industryPopulationEffect = -1
            self.pollution = False
        elif 1 <= self.industry <= 3:
            self.industryPopulationEffect = 0
            self.pollution = False
        elif 4 <= self.industry <= 9:
            self.industryPopulationEffect = 1
            self.pollution = (True if self.group in [group.DwarfPlanet, group.TerrestrialPlanet, group.HelianPlanet] else False)
        elif self.industry >= 10:
            if coin_flip:
                self.industryPopulationEffect = 1
                self.pollution = False
            else:
                self.industryPopulationEffect = 2
                self.pollution = (True if self.group in [group.DwarfPlanet, group.TerrestrialPlanet, group.HelianPlanet] else False)


    def set_trade_codes(self):
        """
        Sets the trade codes.
        """

        if (4 <= self.atmosphere <= 9
                and 4 <= self.hydrosphere <= 8
                and 5 <= self.population <= 7):
            if tradeCode.Ag not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Ag)
        else:
            if tradeCode.Ag in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Ag)
        
        if self.category == category.AsteroidBelt:
            if tradeCode.As not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.As)
        else:
            if tradeCode.As in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.As)
        
        if (2 <= self.atmosphere <= 13
                and self.hydrosphere == 0):
            if tradeCode.De not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.De)
        else:
            if tradeCode.De in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.De)
        
        if ((self.atmosphere >= 10
                    or self.chemistry != chemistry.Water)
                and 1 <= self.hydrosphere <= 11):
            if tradeCode.Fl not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Fl)
        else:
            if tradeCode.Fl in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Fl)
        
        if (max(1, self.terraformingAlien.homePlanet.size - 3) <= self.size <= min(15, self.terraformingAlien.homePlanet.size + 2)
                and self.atmosphere in acceptableAtmospheres[self.terraformingAlien.homePlanet.atmosphere]
                and max((5 if self.terraformingAlien.animalClass == animalClass.Aquatic else 2), self.terraformingAlien.homePlanet.hydrosphere - 3) <= self.hydrosphere <= min((11 if self.terraformingAlien.animalClass == animalClass.Aquatic else 8), self.terraformingAlien.homePlanet.hydrosphere + 3)):
            if tradeCode.Ga not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Ga)
        else:
            if tradeCode.Ga in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Ga)
        
        if self.population >= 9:
            if tradeCode.Hi not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Hi)
        else:
            if tradeCode.Hi in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Hi)
        
        if self.industry >= maxTechLevel - 3:
            if tradeCode.Ht not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Ht)
        else:
            if tradeCode.Ht in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Ht)
        
        if (self.atmosphere <= 1
                and self.hydrosphere >= 1):
            if tradeCode.Ic not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Ic)
        else:
            if tradeCode.Ic in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Ic)
        
        if (self.population >= 9
                and self.industry >= 6):
            if tradeCode.In not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.In)
        else:
            if tradeCode.In in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.In)
        
        if 1 <= self.population <= 3:
            if tradeCode.Lo not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Lo)
        else:
            if tradeCode.Lo in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Lo)
        
        if self.industry <= 5:
            if tradeCode.Lt not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Lt)
        else:
            if tradeCode.Lt in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Lt)
        
        if ((self.atmosphere <= 3
                    or self.atmosphere >= 11)
                and (self.hydrosphere <= 3
                    or self.hydrosphere >= 11)
                and self.population >= 6):
            if tradeCode.Na not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Na)
        else:
            if tradeCode.Na in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Na)
        
        if 4 <= self.population <= 6:
            if tradeCode.Ni not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Ni)
        else:
            if tradeCode.Ni in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Ni)
        
        if (2 <= self.atmosphere <= 5
                and self.hydrosphere <= 3):
            if tradeCode.Po not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Po)
        else:
            if tradeCode.Po in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Po)
        
        if (6 <= self.population <= 8
                and self.atmosphere in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]):
            if tradeCode.Ri not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Ri)
        else:
            if tradeCode.Ri in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Ri)
        
        if self.biosphere == 0:
            if tradeCode.St not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.St)
        else:
            if tradeCode.St in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.St)
        
        if (self.atmosphere >= 2
                and 10 <= self.hydrosphere <= 11):
            if tradeCode.Wa not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Wa)
        else:
            if tradeCode.Wa in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Wa)
        
        if self.atmosphere == 0:
            if tradeCode.Va not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Va)
        else:
            if tradeCode.Va in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Va)
        
        if self.biosphere >= 7:
            if tradeCode.Zo not in self.tradeCodes:
                self.tradeCodes.add(tradeCode.Zo)
        else:
            if tradeCode.Zo in self.tradeCodes:
                self.tradeCodes.discard(tradeCode.Zo)


    def set_starport(self):
        """
        Sets the starport.
        """

        previousStarport = self.starport

        # The roll is only made once so it doesn't radically change constantly.
        if not self.starportRoll:
            self.starportRoll = roll_xdy(2, 6) - 7

        score = self.starportRoll + self.industry
        if tradeCode.Ag in self.tradeCodes:
            score += 1
        if tradeCode.Ga in self.tradeCodes:
            score += 1
        if tradeCode.Hi in self.tradeCodes:
            score += 1
        if tradeCode.Ht in self.tradeCodes:
            score += 1
        if tradeCode.In in self.tradeCodes:
            score += 1
        if tradeCode.Na in self.tradeCodes:
            score += 1
        if tradeCode.Ri in self.tradeCodes:
            score += 1
        if self.terraformingAlien.currentTechLevel >= 12:
            score += 1
        if self.terraformingAlien.currentTechLevel >= 15:
            score += 1
        if tradeCode.Po in self.tradeCodes:
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
                and (habitation.Outpost in self.habitation.values()
                    or self.industry >= 5
                    or self.atmosphere not in acceptableAtmospheres[self.terraformingAlien.homePlanet.atmosphere])):
            score = 3

        self.starport = starportTable[score]

        if self.starport in [starport.D, starport.C]:
            self.star.systemHex.fuelUnrefinedAvailable = True

        if self.starport in [starport.B, starport.A]:
            self.star.systemHex.fuelRefinedAvailable = True


class AsteroidBelt(OrbitalBody):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.group = group.AsteroidBelt
        self.category = category.AsteroidBelt
        self.size = 25
        self.homeAlien = None
        self.terraformingAlien = None
        self.atmosphere = 0
        self.hydrosphere = 0
        self.subsurfaceOceans = None
        self.chemistry = None
        self.biosphere = 0
        self.baseDesirability = roll_xdy(1, 6) - roll_xdy(1, 6)

        # Create dwarf planet member of asteroid belt.
        if roll_xdy(1, 6) >= 5:
            self.create_satellite(group.DwarfPlanet)


    def calculate_desirability(self, alien, nearbyColony):
        """
        Sets the orbital body's desirability score, which is used to determine
        the extent of colonization. This can be different per Alien.
        This version applies only to Jovians and Asteroid Belts as you
        don't live "on" them, but in stations.

        Required Parameters:
            alien: Alien class instance
                The alien considering colonization of this orbital body.
            nearbyColony: Boolean
                Indicates where there is a colony within one jump
                of this orbital body's system.
        """

        desirability = self.baseDesirability

        # If the distance from the alien home system hasn't been
        # calculated yet, calculate it and store it.
        if alien not in self.systemHex.distanceFromAlienHomeSystem:
            self.systemHex.set_distance_from_homeworld(alien)

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

        colonyInSystem = any(p.group not in [group.JovianPlanet, group.AsteroidBelt] and alien in p.habitation.keys() and p.habitation[alien] in [habitation.Colony, habitation.Homeworld] for p in self.systemHex.orbitalBodies)
        outpostInSystem = any(p.group not in [group.JovianPlanet, group.AsteroidBelt] and alien in p.habitation.keys() and p.habitation[alien] == habitation.Outpost for p in self.systemHex.orbitalBodies)

        if not colonyInSystem and not outpostInSystem:
            desirability -= 3
        elif not colonyInSystem and outpostInSystem:
            desirability -= 1

        return desirability


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
        self.subsurfaceOceans = None
        self.biosphere = None
        self.chemistry = None
        self.terrain = []
        self.animals = []
        self.ringSystem = False
        self.homeAlien = None
        self.terraformingAlien = None
        self.terraformingPoints = 0
        self.terraformingPointsUsed = 0
        self.terraformingDone = False
        self.seedWithLife = False


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
        desirability = self.baseDesirability

        # If the distance from the alien home system hasn't been
        # calculated yet, calculate it and store it.
        if alien not in self.systemHex.distanceFromAlienHomeSystem:
            self.systemHex.set_distance_from_homeworld(alien)

        modifiedDistance = max([0, int(round(
            self.systemHex.distanceFromAlienHomeSystem[alien] / (
                (1 if alien.currentTechLevel == 9 else (
                    alien.currentTechLevel - 9))),
            0)) - (1 if nearbyColony else 0)])

        # Distance penalty
        if modifiedDistance > 3 + alien.reactionModifier:
            desirability -= (modifiedDistance - 3 + alien.reactionModifier)

        # Penalty for not having an easy source of fuel in the system
        if not any([self.systemHex.fuelUnrefinedAvailable, self.systemHex.fuelRefinedAvailable]):
            desirability -= 1

        # Penalty for having a flare star in the system
        desirability -= self.systemHex.flareStarDesirabilityPenalty

        # Lifebelt bonus
        if self.orbitType == orbitType.InnerZone:
            if self.star.luminosityClass in [luminosityClass.A_V, luminosityClass.F_V, luminosityClass.K_V]:
                desirability += 2
            elif self.star.luminosityClass == luminosityClass.M_V:
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
                    or (self.subsurfaceOceans and alien.animalClass == animalClass.Aquatic))
                and max((5 if alien.animalClass == animalClass.Aquatic else 2), alien.homePlanet.hydrosphere - 3) <= self.hydrosphere <= min((11 if alien.animalClass == animalClass.Aquatic else 8), alien.homePlanet.hydrosphere + 3)):
                desirability += 5
            # Water world
            elif (2 <= self.atmosphere <= 9
                  and 10 <= self.hydrosphere <= 11
                  and alien.animalClass != animalClass.Aquatic):
                desirability += 3
            # Poor world
            elif (2 <= self.atmosphere <= 6
                  and (2 if alien.animalClass == animalClass.Aquatic else 0) <= self.hydrosphere <= max((4 if alien.animalClass == animalClass.Aquatic else 3), alien.homePlanet.hydrosphere - 4)):
                desirability += 2
            # Other
            elif (2 <= self.atmosphere <= 9
                  and (2 if alien.animalClass == animalClass.Aquatic else 0) <= self.hydrosphere <= 11):
                desirability += 4
        # Not currently habitable, but at least these worlds can be terraformed
        elif (2 <= self.size <= 12
              and self.orbitType == orbitType.InnerZone
              and self.hydrosphere < 11
              and self.atmosphere < 13
              and self.category not in [category.Acheronian, category.Asphodelian, category.Stygian]
              and luminosityClass.M_Ve not in [s.luminosityClass for s in self.systemHex.stars]):
            desirability += 1

        # Ideal atmosphere bonus
        if self.atmosphere == alien.homePlanet.atmosphere:
            desirability += 1

        return desirability
        

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
        if (self.atmosphere == 13
            and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]):
            self.atmosphere -= 1
            return True
        elif (self.atmosphere == 12
            and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]):
            if 2 <= self.hydrosphere <= 10:
                self.hydrosphere -= 1
                return True
            elif self.hydrosphere < 2:
                self.atmosphere -= 1
                return True
        elif (self.atmosphere > 9
            and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]):
            self.atmosphere -= 1
            return True
        elif (self.atmosphere < 2
            and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]):
            self.atmosphere += 1
            return True

        # At this point, the planet should have one of the Habitable World bonuses
        # If it's Poor, improve it to Other by raising Hydrosphere
        if self.hydrosphere <= max((4 if alien.animalClass == animalClass.Aquatic else 3), alien.homePlanet.hydrosphere - 4):
            self.hydrosphere += 1
            return True

        # If it's Water World and Hydrosphere 10, reduce Hydrosphere to improve it to Other
        # Does not apply to Aquatics
        if self.hydrosphere == 10 and alien.animalClass != animalClass.Aquatic:
            self.hydrosphere -= 1
            return True

        # If the planet's size would allow it to be a Garden world, work
        # towards that
        if max(1, alien.homePlanet.size - 3) <= self.size <= min(15, alien.homePlanet.size + 2):
            # Lower Hydrosphere if it's too high
            if self.hydrosphere > min((11 if alien.animalClass == animalClass.Aquatic else 8), alien.homePlanet.hydrosphere + 3):
                self.hydrosphere -= 1
                return True
            # Raise Hydrosphere if it's too low
            if self.hydrosphere < max((5 if alien.animalClass == animalClass.Aquatic else 2), alien.homePlanet.hydrosphere - 3):
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
        

    def set_terrain(self):
        """
        Sets the list of terrains found on the orbital body.
        """

        t = []

        if self.hydrosphere <= 8:
            t.append(terrain.Mountains)
            t.append(terrain.RoughBroken)
            t.append(terrain.Hills)
            t.append(terrain.Clear)

        if self.atmosphere >= 2 and (2 <= self.hydrosphere <= 8):
            t.append(terrain.BeachShore)

        if (self.atmosphere >= 2 and 5 <=
                self.hydrosphere <= 11) or self.subsurfaceOceans:
            t.append(terrain.DeepOcean)

        if self.biosphere >= 9 and self.hydrosphere <= 4 and 2 <= self.atmosphere <= 7:
            t.append(terrain.Desert)

        if self.biosphere >= 9 and self.atmosphere >= 4 and 3 <= self.hydrosphere <= 8:
            t.append(terrain.Forest)

        if self.biosphere >= 9 and self.atmosphere >= 4 and 4 <= self.hydrosphere <= 8:
            t.append(terrain.Jungle)

        if (self.atmosphere >= 2 and 3 <=
                self.hydrosphere <= 11) or self.subsurfaceOceans:
            t.append(terrain.OpenOcean)

        if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 7:
            t.append(terrain.Plains)

        if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
            t.append(terrain.Rainforest)

        if self.atmosphere >= 2 and 3 <= self.hydrosphere <= 8:
            t.append(terrain.Riverbank)

        if (self.atmosphere >= 2 and 2 <= self.hydrosphere <= 10) or (
                self.subsurfaceOceans and self.hydrosphere <= 10):
            t.append(terrain.ShallowOcean)

        if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
            t.append(terrain.SwampMarsh)

        if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 8:
            t.append(terrain.Woods)

        self.terrain = t
        
        
    def add_animals(self):
        """
        Adds animals for each terrain.
        """

        for t in self.terrain:
            if t == terrain.BeachShore:
                for _ in range(3):
                    self.animals.append(create_amphibian(self, t))
                    self.animals.append(create_aquatic(self, t))
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_insect(self, t))
            elif t == terrain.Clear:
                for _ in range(3):
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_mammal(self, t))
            elif t == terrain.DeepOcean:
                for _ in range(3):
                    self.animals.append(create_aquatic(self, t))
            elif t == terrain.Desert:
                for _ in range(3):
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_reptile(self, t))
            elif t == terrain.Forest:
                for _ in range(3):
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_fungal(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_mammal(self, t))
            elif t == terrain.Hills:
                for _ in range(3):
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_mammal(self, t))
                    self.animals.append(create_reptile(self, t))
            elif t == terrain.Jungle:
                for _ in range(3):
                    self.animals.append(create_amphibian(self, t))
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_fungal(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_reptile(self, t))
            elif t == terrain.Mountains:
                for _ in range(3):
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_insect(self, t))
            elif t == terrain.OpenOcean:
                for _ in range(3):
                    self.animals.append(create_aquatic(self, t))
            elif t == terrain.Plains:
                for _ in range(3):
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_mammal(self, t))
                    self.animals.append(create_reptile(self, t))
            elif t == terrain.Rainforest:
                for _ in range(3):
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_fungal(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_reptile(self, t))
            elif t == terrain.Riverbank:
                for _ in range(3):
                    self.animals.append(create_amphibian(self, t))
                    self.animals.append(create_aquatic(self, t))
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_mammal(self, t))
                    self.animals.append(create_reptile(self, t))
            elif t == terrain.RoughBroken:
                for _ in range(3):
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_reptile(self, t))
            elif t == terrain.ShallowOcean:
                for _ in range(3):
                    self.animals.append(create_amphibian(self, t))
                    self.animals.append(create_aquatic(self, t))
                    self.animals.append(create_avian(self, t))
            elif t == terrain.SwampMarsh:
                for _ in range(3):
                    self.animals.append(create_amphibian(self, t))
                    self.animals.append(create_aquatic(self, t))
                    self.animals.append(create_avian(self, t))
                    self.animals.append(create_fungal(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_reptile(self, t))
            elif t == terrain.Woods:
                for _ in range(3):
                    self.animals.append(create_fungal(self, t))
                    self.animals.append(create_insect(self, t))
                    self.animals.append(create_mammal(self, t))


class DwarfPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = roll_xdy(1, 6) - 1
        self.group = group.DwarfPlanet

        if self.parentObject == self.star and roll_xdy(1, 6) == 6:
            self.create_satellite(group.DwarfPlanet)


class TerrestrialPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = roll_xdy(1, 6) + 4
        self.group = group.TerrestrialPlanet

        if self.parentObject == self.star and roll_xdy(1, 6) >= 5:
            self.create_satellite(group.DwarfPlanet)


class HelianPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = min(14, roll_xdy(1, 6) + 9)
        self.group = group.HelianPlanet

        if self.parentObject == self.star:
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
        self.group = group.JovianPlanet
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
            

    def calculate_desirability(self, alien, nearbyColony):
        """
        Sets the orbital body's desirability score, which is used to determine
        the extent of colonization. This can be different per Alien.
        This version applies only to Jovians and Asteroid Belts as you
        don't live "on" them, but in stations.

        Required Parameters:
            alien: Alien class instance
                The alien considering colonization of this orbital body.
            nearbyColony: Boolean
                Indicates where there is a colony within one jump
                of this orbital body's system.
        """

        desirability = self.baseDesirability

        # If the distance from the alien home system hasn't been
        # calculated yet, calculate it and store it.
        if alien not in self.systemHex.distanceFromAlienHomeSystem:
            self.systemHex.set_distance_from_homeworld(alien)

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

        colonyInSystem = any(p.group not in [group.JovianPlanet, group.AsteroidBelt] and alien in p.habitation.keys() and p.habitation[alien] in [habitation.Colony, habitation.Homeworld] for p in self.systemHex.orbitalBodies)
        outpostInSystem = any(p.group not in [group.JovianPlanet, group.AsteroidBelt] and alien in p.habitation.keys() and p.habitation[alien] == habitation.Outpost for p in self.systemHex.orbitalBodies)

        if not colonyInSystem and not outpostInSystem:
            desirability -= 3
        elif not colonyInSystem and outpostInSystem:
            desirability -= 1

        return desirability


class Acheronian(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Acheronian
        self.className = className.Telluric
        self.type = type.Acheronian
        self.atmosphere = 1
        self.hydrosphere = 0
        self.biosphere = 0
        self.set_terrain()


class Arean(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Arean
        
        # Chemistry
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

        # Atmosphere
        if roll_xdy(1, 6) - (2 if self.star.luminosityClass == luminosityClass.D else 0):
            self.atmosphere = 1
        else:
            self.atmosphere = 10
        
        # Hydrosphere
        self.hydrosphere = max(0, roll_xdy(2, 3) + self.size - 7 - (4 if self.atmosphere == 1 else 0))

        # Biosphere
        if self.systemHex.age >= 4 + self.ageModifier and self.atmosphere == 10:
            self.biosphere = max(0, roll_xdy(1, 6) + self.size - 2)
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = max(0, roll_xdy(1, 6) - 4) if self.atmosphere == 1 else roll_xdy(1, 3)
        else:
            self.biosphere = 0

        self.set_terrain()
        if self.biosphere > 8:
            self.add_animals()
        if self.biosphere > 11:
            create_alien(self, alienSurvivalPercent)


class Arid(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Arid

        # Chemistry
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

        # Hydrosphere
        self.hydrosphere = roll_xdy(1, 3)

        # Biosphere
        if self.systemHex.age >= 4 + self.ageModifier:
            self.biosphere = max([0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0)])
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

        # Atmosphere
        if self.biosphere >= 3 and self.chemistry == chemistry.Water:
            self.atmosphere = max(2, min(9, roll_xdy(2, 6) - 7 + self.size))
        else:
            self.atmosphere = 10

        self.set_terrain()
        if self.biosphere > 8:
            self.add_animals()
        if self.biosphere > 11:
            create_alien(self, alienSurvivalPercent)


class Asphodelian(HelianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Asphodelian
        self.className = className.GeoHelian
        self.type = type.Asphodelian
        self.atmosphere = 1
        self.hydrosphere = 0
        self.biosphere = 0
        self.set_terrain()


class Chthonian(JovianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Chthonian
        self.className = className.Chthonian
        self.atmosphere = 1
        self.hydrosphere = 0
        self.biosphere = 0
        self.set_terrain()


class Hebean(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Hebean

        # Chemistry
        self.className = className.Geotidal
        self.type = (type.Hebean if coin_flip else type.Idunnian)

        # Atmosphere
        roll = roll_xdy(1, 6) + self.size - 6
        self.atmosphere = max(0, (10 if roll >= 2 else roll))

        # Hydrosphere
        self.hydrosphere = max(0, roll_xdy(2, 6) + self.size - 11)

        # Biosphere
        self.biosphere = 0

        self.set_terrain()


class Helian(HelianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Helian

        # Chemistry
        self.className = (className.GeoHelian if coin_flip else className.Nebulous)

        # Atmosphere
        self.atmosphere = 13

        # Hydrosphere
        roll = roll_xdy(1, 6)
        if roll <= 2:
            self.hydrosphere = 0
        elif roll <= 4:
            self.hydrosphere = roll_xdy(1, 6) - 1
        else:
            self.hydrosphere = 15

        # Biosphere
        self.biosphere = 0

        self.set_terrain()


class JaniLithic(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.JaniLithic

        # Chemistry
        self.className = className.Epistellar
        self.type = type.JaniLithic

        # Atmosphere
        if coin_flip:
            self.atmosphere = 1
        else:
            self.atmosphere = 10

        # Hydrosphere
        self.hydrosphere = 0

        # Biosphere
        self.biosphere = 0

        self.set_terrain()


class Jovian(JovianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Jovian
        # Atmosphere
        self.atmosphere = 16

        # Hydrosphere
        self.hydrosphere = 16

        # Biosphere
        if roll_xdy(1, 6) <= 5:
            self.biosphere = 0
        else:
            if self.systemHex.age >= 7:
                self.biosphere = roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0)
            elif self.systemHex.age >= roll_xdy(1, 6):
                self.biosphere = roll_xdy(1, 3)
            else:
                self.biosphere = 0

        # Chemistry
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


class Meltball(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Meltball

        # Chemistry
        r = chemistryMeltball[roll_xdy(1, 6)][roll_xdy(1, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]

        # Atmosphere
        self.atmosphere = 1

        # Hydrosphere
        self.hydrosphere = 15

        # Biosphere
        self.biosphere = 0

        self.set_terrain()


class Oceanic(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Oceanic

        # Chemistry
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

        # Atmosphere
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

        # Biosphere
        if self.systemHex.age >= 4 + self.ageModifier:
            self.biosphere = max(0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0))
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

        # Hydrosphere
        self.hydrosphere = 11

        if self.biosphere > 0:
            self.subsurfaceOceans = True

        self.set_terrain()
        if self.biosphere > 8:
            self.add_animals()
        if self.biosphere > 11:
            create_alien(self, alienSurvivalPercent)


class Panthalassic(HelianPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Panthalassic

        # Chemistry
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

        # Atmosphere
        self.atmosphere = min(13, roll_xdy(1, 6) + 8)

        # Hydrosphere
        self.hydrosphere = 11

        # Biosphere
        if self.systemHex.age >= 4 + self.ageModifier:
            self.biosphere = roll_xdy(2, 6)
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

        self.set_terrain()
        if self.biosphere > 8:
            self.add_animals()
        if self.biosphere > 11:
            create_alien(self, alienSurvivalPercent)


class Promethean(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Promethean

        # Chemistry
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

        # Biosphere
        if self.systemHex.age >= 4 + self.ageModifier:
            self.biosphere = roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0)
        elif self.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

        # Atmosphere
        if self.biosphere >= 3 and self.chemistry == chemistry.Water:
            self.atmosphere = max(2, min(9, roll_xdy(2, 6) + self.size - 7))
        else:
            self.atmosphere = 10

        # Hydrosphere
        self.hydrosphere = roll_xdy(2, 6) - 2

        self.set_terrain()
        if self.biosphere > 8:
            self.add_animals()
        if self.biosphere > 11:
            create_alien(self, alienSurvivalPercent)


class Rockball(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Rockball

        # Chemistry
        r = chemistryRockball[roll_xdy(1, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]

        # Atmosphere
        self.atmosphere = 0

        # Hydrosphere
        roll = roll_xdy(2, 6)
        if self.star.luminosityClass == luminosityClass.L:
            roll += 1
        if self.orbitType == orbitType.Epistellar:
            roll -= 2
        elif self.orbitType == orbitType.OuterZone:
            roll += 2

        self.hydrosphere = max(0, roll + self.size - 11)

        # Biosphere
        self.biosphere = 0

        self.set_terrain()


class Snowball(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Snowball

        # Chemistry
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

        # Atmosphere
        self.atmosphere = (0 if roll_xdy(1, 6) <= 4 else 1)

        # Hydrosphere
        if coin_flip:
            self.hydrosphere = roll_xdy(2, 6) - 2
            self.subsurfaceOceans = True
        else:
            self.hydrosphere = 10

        # Biosphere
        if not self.subsurfaceOceans:
            self.biosphere = 0
        elif self.systemHex.age >= 6 + self.ageModifier:
            self.biosphere = max(0, roll_xdy(1, 6) + self.size - 2)
        elif self.systemHex.age >= roll_xdy(1, 6):
            self.biosphere = max(0, roll_xdy(1, 6) - 3)
        else:
            self.biosphere = 0

        self.set_terrain()
        if self.biosphere > 8:
            self.add_animals()
        if self.biosphere > 11:
            create_alien(self, alienSurvivalPercent)


class Stygian(DwarfPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Stygian
        self.className = className.Geopassive
        self.type = type.Stygian
        self.atmosphere = 0
        self.hydrosphere = 0
        self.biosphere = 0
        self.set_terrain()


class Tectonic(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Tectonic

        # Chemistry
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

        # Biosphere
        if self.systemHex.age >= 4 + self.ageModifier:
            self.biosphere = max(0, roll_xdy(2, 6) - (3 if self.star.luminosityClass == luminosityClass.D else 0))
        else:
            self.biosphere = 0

        # Atmosphere
        if self.biosphere >= 3:
            if self.chemistry == chemistry.Water:
                self.atmosphere = max(2, min(9, roll_xdy(2, 6) + self.size - 7))
            elif self.chemistry in [chemistry.Sulfur, chemistry.Chlorine]:
                self.atmosphere = 11
            else:
                self.atmosphere = 10
        else:
            self.atmosphere = 10

        # Hydrosphere
        self.hydrosphere = roll_xdy(2, 6) - 2

        self.set_terrain()
        if self.biosphere > 8:
            self.add_animals()
        if self.biosphere > 11:
            create_alien(self, alienSurvivalPercent)


class Telluric(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Telluric
        self.className = className.Telluric
        self.type = (type.Phosphorian if coin_flip else type.Cytherean)
        self.atmosphere = 12
        self.hydrosphere = (0 if roll_xdy(1, 6) <= 4 else 15)
        self.biosphere = 0
        self.set_terrain()


class Vesperian(TerrestrialPlanet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.category = category.Vesperian

        # Chemistry
        r = chemistryVesperian[roll_xdy(2, 6)]
        
        self.chemistry = r[0]
        self.ageModifier = r[1]
        self.className = r[2]
        self.type = r[3]

        # Biosphere
        if self.systemHex.age >= 4:
            self.biosphere = roll_xdy(2, 6)
        elif self.systemHex.age >= roll_xdy(1, 3):
            self.biosphere = roll_xdy(1, 3)
        else:
            self.biosphere = 0

        # Atmosphere
        if self.biosphere >= 3:
            if self.chemistry == chemistry.Water:
                self.atmosphere = max(2, min(9, roll_xdy(2, 6) + self.size - 7))
            else:
                self.atmosphere = 11
        else:
            self.atmosphere = 10

        # Hydrosphere
        self.hydrosphere = roll_xdy(2, 6) - 2

        self.set_terrain()
        if self.biosphere > 8:
            self.add_animals()
        if self.biosphere > 11:
            create_alien(self, alienSurvivalPercent)

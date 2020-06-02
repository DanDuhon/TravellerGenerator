import animal
import alien
import star
import systemhex
from diceroller import roll_xdy
from lookuptable import LookupTable

allPlanets = []


dwarfCategoryDict = {
    "Epistellar": LookupTable(
        (3, "Rockball"),
        (5, "Meltball"),
        (6, LookupTable(
            (4, "Hebean"),
            (6, "Promethean")))),
    "Inner Zone": LookupTable(
        (4, "Rockball"),
        (6, "Arean"),
        (7, "Meltball"),
        (8, LookupTable(
            (4, "Hebean"),
            (6, "Promethean")))),
    "Outer Zone": LookupTable(
        (0, "Rockball"),
        (4, "Snowball"),
        (6, "Rockball"),
        (7, "Meltball"),
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
    "Acheronian": "These are worlds that were directly affected by their primary's transition from the main sequence; the atmosphere and oceans have been boiled away, leaving a scorched, dead planet.",
    "Arean": "These are worlds with little liquid, that move through a slow geological cycle of a gradual build-up, a short wet and clement period, and a long decline.",
    "Arid": "These are worlds with limited amounts of surface liquid, that maintain an equilibrium with the help of their tectonic activity and their biosphere.",
    "Asphodelian": "These are worlds that were directly affected by their primary's transition from the main sequence; their atmosphere has been boiled away, leaving the surface exposed.",
    "Chthonian": "These are worlds that were directly affected by their primary's transition from the main sequence, or that have simply spent too long in a tight epistellar orbit; their atmospheres have been stripped away.",
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
    "Stygian": "These are worlds that were directly affected by their primary's transition from the main sequence; they are melted and blasted lumps.",
    "Tectonic": "These are worlds with active plate tectonics and large bodies of surface liquid, allowing for stable atmospheres and a high likelihood of life.",
    "Telluric": "These are worlds with geoactivity but no hydrological cycle at all, leading to dense runaway-greenhouse atmospheres.",
    "Vesperian": "These worlds are tide-locked to their primary, but at a distance that permits surface liquid and the development of life."}


def create_asteroid_belt(
        star,
        parentObject,
        order,
        orbitType,
        alienSurvivalPercent):
    newPlanet = OrbitalBody(
        star=star,
        parentObject=parentObject,
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
    newPlanet.planet_terrain_animals()
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
    newPlanet = OrbitalBody(
        star=star,
        parentObject=parentObject,
        order=order,
        orbitType=orbitType)

    newPlanet.groupName = "Dwarf"
    newPlanet.category = newPlanet.dwarf_category()
    newPlanet.size = newPlanet.planet_size()
    newPlanet.set_class_chemistry_atmosphere_hydrosphere_biosphere()
    newPlanet.planet_terrain_animals()

    if newPlanet.biosphere >= 12:
        alien.create_alien(newPlanet, alienSurvivalPercent)

    newPlanet.satellites = []

    if (newPlanet.parentObject == newPlanet.star or newPlanet.parentObject.groupName != "Dwarf") and roll_xdy(1, 6) == 6:
        create_dwarf_planet(
            star=newPlanet.star,
            parentObject=newPlanet,
            order=newPlanet.order,
            orbitType=newPlanet.orbitType,
            alienSurvivalPercent=alienSurvivalPercent)

        
def create_terrestrial_planet(
        star,
        parentObject,
        order,
        orbitType,
        alienSurvivalPercent):
    newPlanet = OrbitalBody(
        star=star,
        parentObject=parentObject,
        order=order,
        orbitType=orbitType)

    newPlanet.groupName = "Terrestrial"
    newPlanet.category = newPlanet.terrestrial_category()
    newPlanet.size = newPlanet.planet_size()
    newPlanet.set_class_chemistry_atmosphere_hydrosphere_biosphere()
    newPlanet.planet_terrain_animals()

    if newPlanet.biosphere >= 12:
        alien.create_alien(newPlanet, alienSurvivalPercent)

    newPlanet.satellites = []

    if roll_xdy(1, 6) >= 1:
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
    newPlanet = OrbitalBody(
        star=star,
        parentObject=parentObject,
        order=order,
        orbitType=orbitType)

    newPlanet.groupName = "Helian"
    newPlanet.category = newPlanet.helian_category()
    newPlanet.size = newPlanet.planet_size()
    newPlanet.set_class_chemistry_atmosphere_hydrosphere_biosphere()
    newPlanet.planet_terrain_animals()

    if newPlanet.biosphere >= 12:
        alien.create_alien(newPlanet, alienSurvivalPercent)

    newPlanet.satellites = []

    satelliteRoll1 = roll_xdy(1, 6)
    satelliteRoll2 = roll_xdy(1, 6)

    for _ in range(newPlanet.dwarf_satellites(satelliteRoll1, satelliteRoll2)):
            create_dwarf_planet(
                star=newPlanet.star,
                parentObject=newPlanet,
                order=newPlanet.order,
                orbitType=newPlanet.orbitType,
                alienSurvivalPercent=alienSurvivalPercent)
    if satelliteRoll2 == 6 and satelliteRoll1 - 3 > 0:
        create_terrestrial_planet(
            star=newPlanet.star,
            parentObject=newPlanet,
            order=newPlanet.order,
            orbitType=newPlanet.orbitType,
            alienSurvivalPercent=alienSurvivalPercent)

        
def create_jovian_planet(
        star,
        parentObject,
        order,
        orbitType,
        alienSurvivalPercent):
    newPlanet = OrbitalBody(
        star=star,
        parentObject=parentObject,
        order=order,
        orbitType=orbitType)

    newPlanet.groupName = "Jovian"
    newPlanet.category = newPlanet.jovian_category()
    newPlanet.size = newPlanet.planet_size()
    newPlanet.set_class_chemistry_atmosphere_hydrosphere_biosphere()
    newPlanet.planet_terrain_animals()

    if newPlanet.biosphere >= 12:
        alien.create_alien(newPlanet, alienSurvivalPercent)

    if roll_xdy(1, 6) <= 4:
        newPlanet.ringSystem = "Minor"
    else:
        newPlanet.ringSystem = "Complex"

    newPlanet.satellites = []

    satelliteRoll1 = roll_xdy(1, 6)
    satelliteRoll2 = roll_xdy(1, 6)
    satelliteRoll3 = roll_xdy(1, 6)

    for _ in range(newPlanet.dwarf_satellites(satelliteRoll1, satelliteRoll2)):
            create_dwarf_planet(
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
    if satelliteRoll2 == 6 and satelliteRoll3 == 6:
        create_helian_planet(
            star=newPlanet.star,
            parentObject=newPlanet,
            order=newPlanet.order,
            orbitType=newPlanet.orbitType,
            alienSurvivalPercent=alienSurvivalPercent)


class OrbitalBody():
    """
    Defines an object that orbits a Star or other OrbitalBody.

    Parameters:
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
        self.star = star
        self.parentObject = parentObject
        self.order = order
        self.orbitType = orbitType
        self.category = None
        self.size = None
        self.category = None
        self.groupName = None
        self.className = None
        self.typeName = None
        self.atmosphere = None
        self.biosphere = None
        self.hydrosphere = None
        self.subsurfaceOceans = None
        self.terrain = []
        self.animals = []
        self.ringSystem = None
        self.satellites = []
        self.alien = None
        self.properName = None
        self.desirability = {}
        self.habitation = {}
        self.ruins = set()
        self.settlement = 0
        self.terraformingAlien = None
        self.terraformingPoints = 0
        self.terraformingPointsUsed = 0
        self.terraformingDone = False

        if self.parentObject == self.star:
            self.name = self.parentObject.name + " " + str(self.order)
            self.star.planets.append(self)
        else:
            self.name = self.parentObject.name + "-" + str(len(self.parentObject.satellites) + 1)
            self.parentObject.satellites.append(self)


    def dwarf_category(self):
        """
        Returns the category of a planet based on dwarfCategoryDict.
        """
        roll = roll_xdy(1, 6)

        if self.order <= self.star.expansionAffectedOrbits:
            return "Stygian"
        elif self.orbitType == "Epistellar":
            if self.parentObject != self.star and self.parentObject.groupName == "Asteroid Belt":
                roll -= 2

            if roll == 6:
                return dwarfCategoryDict[self.orbitType][roll][roll_xdy(1, 6)]
        elif self.orbitType == "Inner Zone":
            if self.parentObject != self.star and self.parentObject.groupName == "Asteroid Belt":
                roll -= 2
            elif self.parentObject != self.star and self.parentObject.groupName == "Helian":
                roll += 1
            elif self.parentObject != self.star and self.parentObject.groupName == "Jovian":
                roll += 2

            if roll == 8:
                return dwarfCategoryDict[self.orbitType][roll][roll_xdy(1, 6)]
        else:  # Outer Zone
            if self.parentObject != self.star and self.parentObject.groupName == "Asteroid Belt":
                roll -= 1
            elif self.parentObject != self.star and self.parentObject.groupName == "Helian":
                roll += 1
            elif self.parentObject != self.star and self.parentObject.groupName == "Jovian":
                roll += 2

            if roll == 8:
                return dwarfCategoryDict[self.orbitType][roll][roll_xdy(1, 6)]

        return dwarfCategoryDict[self.orbitType][roll]


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
        elif self.groupName == "Jovian":
            return 16
        elif self.groupName == "Asteroid Belt":
            return 25
        else:
            raise ValueError("Unrecognized group: " + str(self.groupName))


    def set_class_chemistry_atmosphere_hydrosphere_biosphere(self):
        """
        Sets the planet's chemistry, atmosphere, hydrosphere, and biosphere
        values. Not all planet categories have the same order of operations,
        so it is in a loop to accommodate the planets that determine these
        things in a different order.
        """
        while self.className is None or self.atmosphere is None or self.biosphere is None or self.hydrosphere is None:
            if self.className is None:
                chemistryAgeModifierClassType = self.planet_chemistry_age_modifier_class_type()
                self.chemistry = chemistryAgeModifierClassType[0]
                self.ageModifier = chemistryAgeModifierClassType[1]
                self.className = chemistryAgeModifierClassType[2]
                self.type = chemistryAgeModifierClassType[3]

            if self.atmosphere is None:
                self.atmosphere = self.planet_atmosphere()

            if self.biosphere is None:
                self.biosphere = self.planet_biosphere()

            if self.hydrosphere is None:
                hydrosphereSubsurfaceOceans = self.planet_hydrosphere_subsurface_oceans()
                self.hydrosphere = hydrosphereSubsurfaceOceans[0]
                self.subsurfaceOceans = hydrosphereSubsurfaceOceans[1]

            if self.biosphere > 0 and ((self.atmosphere == 0 and not self.subsurfaceOceans)
                                       or self.hydrosphere == 0
                                       or self.star.luminosityClass == "M-Ve"):
                self.biosphere = 0
                # The atmosphere of these categories is dependent on the biosphere.
                # If the biosphere was forced to 0, recalculate the value for
                # atmosphere.
                if self.category in [
                    "Arid",
                    "Promethean",
                    "Tectonic",
                    "Vesperian"]:
                    self.atmosphere = self.planet_atmosphere()


    def planet_chemistry_age_modifier_class_type(self):
        """
        Returns a tuple of (chemistry, ageModifier, className, type):
            chemistry: String
                The prominent chemical substance on the planet.
            ageModifier: Integer
                Used in calculating the hydrosphere and biosphere of the planet.
            className: String
                The class name of the planet.
            type: String
                The type name of the planet.
        """
        if self.category == "Acheronian":
            return (None, None, "Telluric", "Acheronian")
        elif self.category == "Arean":
            roll = roll_xdy(1, 6)
            if self.star.luminosityClass == "L":
                roll += 2
            if self.orbitType == "Outer Zone":
                roll += 2

            if roll <= 4:
                return ("Water", 0, "Geocyclic", "Arean")
            elif roll <= 6:
                return ("Ammonia", 1, "Geocyclic", "Utgardian")
            else:
                return ("Methane", 3, "Geocyclic", "Titanian")
        elif self.category == "Arid":
            roll = roll_xdy(1, 6)
            if self.star.luminosityClass == "K-V":
                roll += 2
            elif self.star.luminosityClass == "M-V":
                roll += 4
            elif self.star.luminosityClass == "L":
                roll += 5
            if self.orbitType == "Outer Zone":
                roll += 2

            if roll <= 6:
                return ("Water", 0, "Arid", "Darwinian")
            elif roll <= 8:
                return ("Ammonia", 1, "Arid", "Saganian")
            else:
                return ("Methane", 3, "Arid", "Asimovian")
        elif self.category == "Asphodelian":
            return (None, None, "Geo-Helian", "Asphodelian")
        elif self.category == "Asteroid Belt":
            return (None, None, "Asteroid Belt", "Asteroid Belt")
        elif self.category == "Chthonian":
            return (None, None, "Chthonian", None)
        elif self.category == "Hebean":
            if roll_xdy(1, 2) == 1:
                return (None, None, "Geotidal", "Hebean")
            else:
                return (None, None, "Geotidal", "Idunnian")
        elif self.category == "Helian":
            if roll_xdy(1, 2) == 1:
                return (None, None, "Geo-Helian", None)
            else:
                return (None, None, "Nebulous", None)
        elif self.category == "Jani-Lithic":
            return (None, None, "Epistellar", "Jani-Lithic")
        elif self.category == "Jovian":
            if isinstance(self.biosphere, int):
                if self.biosphere > 0:
                    roll = roll_xdy(1, 6)
                    if self.star.luminosityClass == "L":
                        roll += 1
                    if self.orbitType == "Epistellar":
                        roll -= 2
                    elif self.orbitType == "Outer Zone":
                        roll += 2

                    if roll <= 3:
                        return ("Water", None, "Dwarf Jovian", "Brammian")
                    else:
                        return ("Ammonia", None, "Dwarf Jovian", "Khonsonian")
                else:
                    return (None, None, "Jovian", None)
            else:
                return (None, None, None, None)
        elif self.category == "Meltball":
            if roll_xdy(1, 2) == 1:
                roll = roll_xdy(1, 3)
                if roll == 1:
                    return (None, None, "Geothermic", "Phaethonic")
                elif roll == 2:
                    return (None, None, "Geothermic", "Apollonian")
                else:
                    return (None, None, "Geothermic", "Sethian")
            else:
                if roll_xdy(1, 2) == 1:
                    return (None, None, "Geotidal", "Hephaestian")
                else:
                    return (None, None, "Geotidal", "Lokian")
        elif self.category == "Oceanic":
            roll = roll_xdy(1, 6)
            if self.star.luminosityClass == "K-V":
                roll += 2
            elif self.star.luminosityClass == "M-V":
                roll += 4
            elif self.star.luminosityClass == "L":
                roll += 5
            if self.orbitType == "Outer Zone":
                roll += 2

            if roll <= 6:
                if roll_xdy(1, 2) == 1:
                    return ("Water", 0, "Oceanic", "Pelagic")
                else:
                    return ("Water", 0, "Tectonic", "Bathy-Gaian")
            elif roll <= 8:
                if roll_xdy(1, 2) == 1:
                    return ("Ammonia", 1, "Oceanic", "Nunnic")
                else:
                    return ("Ammonia", 1, "Tectonic", "Bathy-Amunian")
            else:
                if roll_xdy(1, 2) == 1:
                    return ("Methane", 3, "Oceanic", "Teathic")
                else:
                    return ("Methane", 3, "Tectonic", "Bathy-Tartarian")
        elif self.category == "Panthalassic":
            roll = roll_xdy(1, 6)
            if self.star.luminosityClass == "K-V":
                roll += 2
            elif self.star.luminosityClass == "M-V":
                roll += 4
            elif self.star.luminosityClass == "L":
                roll += 5

            if roll <= 6:
                roll = roll_xdy(2, 6)
                if roll <= 8:
                    return ("Water", 0, "Panthalassic", None)
                elif roll <= 11:
                    return ("Sulfur", 0, "Panthalassic", None)
                else:
                    return ("Chlorine", 0, "Panthalassic", None)
            elif roll <= 8:
                return ("Methane", 1, "Panthalassic", None)
            else:
                return ("Methane", 3, "Panthalassic", None)
        elif self.category == "Promethean":
            roll = roll_xdy(1, 6)
            if self.star.luminosityClass == "L":
                roll += 2
            if self.orbitType == "Epistellar":
                roll -= 2
            elif self.orbitType == "Outer Zone":
                roll += 2

            if roll <= 4:
                return ("Water", 0, "Geotidal", "Promethean")
            elif roll <= 6:
                return ("Ammonia", 1, "Geotidal", "Burian")
            else:
                return ("Methane", 3, "Geotidal", "Atlan")
        elif self.category == "Rockball":
            roll = roll_xdy(1, 3)
            if roll == 1:
                return (None, None, "Geopassive", "Ferrinian")
            elif roll == 2:
                return (None, None, "Geopassive", "Lithic")
            else:
                return (None, None, "Geopassive", "Carbonian")
        elif self.category == "Snowball":
            roll = roll_xdy(1, 6)
            if self.star.luminosityClass == "L":
                roll += 2
            if self.orbitType == "Outer Zone":
                roll += 2

            if roll <= 4:
                return ("Water", 0, "Geopassive", "Gelidian")
            elif roll <= 6:
                return ("Ammonia", 1, "Geothermic", "Erisian")
            else:
                return ("Methane", 3, "Geotidal", "Plutonian")
        elif self.category == "Stygian":
            return (None, None, "Geopassive", "Stygian")
        elif self.category == "Tectonic":
            roll = roll_xdy(1, 6)
            if self.star.luminosityClass == "K-V":
                roll += 2
            elif self.star.luminosityClass == "M-V":
                roll += 4
            elif self.star.luminosityClass == "L":
                roll += 5
            if self.orbitType == "Outer Zone":
                roll += 2

            if roll <= 6:
                roll = roll_xdy(2, 6)
                if roll <= 8:
                    return ("Water", 0, "Tectonic", "Gaian")
                elif roll <= 11:
                    return ("Sulfur", 0, "Tectonic", "Thio-Gaian")
                else:
                    return ("Chlorine", 0, "Tectonic", "Chloritic-Gaian")
            elif roll <= 8:
                return ("Ammonia", 1, "Tectonic", "Amunian")
            else:
                return ("Methane", 3, "Tectonic", "Tartarian")
        elif self.category == "Telluric":
            if roll_xdy(1, 2) == 1:
                return (None, None, "Telluric", "Phosphorian")
            else:
                return (None, None, "Telluric", "Cytherean")
        elif self.category == "Vesperian":
            roll = roll_xdy(2, 6)
            if roll <= 11:
                return ("Water", None, "Epistellar", "Vesperian")
            else:
                return ("Chlorine", None, "Epistellar", "Vesperian")
        else:
            return (None, None, None, None)


    def planet_atmosphere(self):
        """
        Returns the planet's atmosphere value.
        """
        if self.category in ["Rockball", "Asteroid Belt", "Stygian"]:
            return 0
        elif self.category in ["Acheronian", "Asphodelian", "Chthonian", "Meltball"]:
            return 1
        elif self.category == "Arean":
            roll = roll_xdy(1, 6)
            if self.star.luminosityClass == "D":
                roll -= 2

            if roll <= 3:
                return 1
            else:
                return 10
        elif isinstance(self.biosphere, int) and self.category == "Arid":
            if self.biosphere >= 3 and self.chemistry == "Water":
                roll = roll_xdy(2, 6) - 7 + self.size

                if roll < 2:
                    return 2
                elif roll > 9:
                    return 9
                else:
                    return roll
            else:
                return 10
        elif self.category == "Hebean":
            roll = roll_xdy(1, 6) + self.size - 6

            if roll <= 0:
                return 0
            elif roll >= 2:
                return 10
            else:
                return roll
        elif self.category == "Helian":
            return 13
        elif self.category == "Jani-Lithic":
            roll = roll_xdy(1, 6)

            if roll <= 3:
                return 1
            else:
                return 10
        elif self.category == "Jovian":
            return 16
        elif self.category == "Meltball":
            return 1
        elif self.category == "Oceanic":
            if self.chemistry == "Water":
                roll = roll_xdy(2, 6) + self.size - 6
                if self.star.luminosityClass == "K-V":
                    roll -= 1
                elif self.star.luminosityClass == "M-V":
                    roll -= 2
                elif self.star.luminosityClass == "L":
                    roll -= 3
                elif self.star.luminosityClass in ["F-IV", "G-IV", "K-IV"]:
                    roll -= 1

                if roll <= 1:
                    return 1
                elif roll >= 12:
                    return 12
                else:
                    return roll
            else:
                roll = roll_xdy(1, 6)

                if roll == 1:
                    return 1
                elif roll <= 4:
                    return 10
                else:
                    return 12
        elif self.category == "Panthalassic":
            roll = roll_xdy(1, 6) + 8

            if roll >= 13:
                return 13
            else:
                return roll
        elif isinstance(self.biosphere, int) and self.category == "Promethean":
            if self.chemistry == "Water" and self.biosphere >= 3:
                roll = roll_xdy(2, 6) + self.size - 7

                if roll <= 2:
                    return 2
                elif roll >= 9:
                    return 9
                else:
                    return roll
            else:
                return 10
        elif self.category == "Snowball":
            roll = roll_xdy(1, 6)

            if roll <= 4:
                return 0
            else:
                return 1
        elif isinstance(self.biosphere, int) and self.category == "Tectonic":
            if self.biosphere >= 3 and self.chemistry == "Water":
                roll = roll_xdy(2, 6) + self.size - 7

                if roll <= 2:
                    return 2
                elif roll >= 9:
                    return 9
                else:
                    return roll
            elif self.biosphere >= 3 and self.chemistry in ["Sulfur", "Chlorine"]:
                return 11
            else:
                return 10
        elif self.category == "Telluric":
            return 12
        elif isinstance(self.biosphere, int) and self.category == "Vesperian":
            if self.biosphere >= 3 and self.chemistry == "Water":
                roll = roll_xdy(2, 6) + self.size - 7

                if roll <= 2:
                    return 2
                elif roll >= 9:
                    return 9
                else:
                    return roll
            elif self.biosphere >= 3 and self.chemistry == "Chlorine":
                return 11
            else:
                return 10


    def planet_biosphere(self):
        """
        Returns the planet's biosphere value.
        """
        if ((self.atmosphere == 0
                and not self.subsurfaceOceans) or self.hydrosphere == 0 or "M-Ve" in [s.luminosityClass for s in self.systemHex.stars]):
            return 0
        elif self.category == "Arean":
            if self.star.systemHex.age >= 4 + self.ageModifier and self.atmosphere == 10:
                roll = roll_xdy(1, 6) + self.size - 2

                if roll <= 0:
                    return 0
                else:
                    return roll
            elif self.star.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
                if self.atmosphere == 1:
                    roll = roll_xdy(1, 6) - 4

                    if roll <= 0:
                        return 0
                    else:
                        return roll
                else:
                    return roll_xdy(1, 3)
            else:
                return 0
        elif self.category == "Arid":
            if self.star.systemHex.age >= 4 + self.ageModifier:
                roll = roll_xdy(2, 6)
                if self.star.luminosityClass == "D":
                    roll -= 3

                if roll <= 0:
                    return 0
                else:
                    return roll
            elif self.star.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
                return roll_xdy(1, 3)
            else:
                return 0
        elif self.category == "Jovian":
            roll = roll_xdy(1, 6)
            if self.orbitType == "Inner Zone":
                roll += 2

            if roll >= 6:
                if self.star.systemHex.age >= roll_xdy(1, 6):
                    return roll_xdy(1, 3)
                elif self.star.systemHex.age >= 7:
                    roll = roll_xdy(2, 6)
                    if self.star.luminosityClass == "D":
                        roll -= 3

                    if roll <= 0:
                        return 0
                    else:
                        return roll
                else:
                    return 0
            else:
                return 0
        elif self.category == "Oceanic":
            if self.star.systemHex.age >= 4 + self.ageModifier:
                roll = roll_xdy(2, 6)
                if self.star.luminosityClass == "D":
                    roll -= 3

                if roll <= 0:
                    return 0
                else:
                    return roll
            elif self.star.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
                return roll_xdy(1, 3)
            else:
                return 0
        elif self.category == "Panthalassic":
            if self.star.systemHex.age >= 4 + self.ageModifier:
                return roll_xdy(2, 6)
            elif self.star.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
                return roll_xdy(1, 3)
            else:
                return 0
        elif self.category == "Promethean":
            if self.star.systemHex.age >= 4 + self.ageModifier:
                roll = roll_xdy(2, 6)
                if self.star.luminosityClass == "D":
                    roll -= 3

                if roll <= 0:
                    return 0
                else:
                    return roll
            elif self.star.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
                return roll_xdy(1, 3)
            else:
                return 0
        elif self.category == "Snowball":
            if self.subsurfaceOceans and self.star.systemHex.age >= 6 + self.ageModifier:
                roll = roll_xdy(1, 6) + self.size - 2

                if roll <= 0:
                    return 0
                else:
                    return roll
            elif self.subsurfaceOceans and self.star.systemHex.age >= roll_xdy(1, 6):
                roll = roll_xdy(1, 6) - 3

                if roll <= 0:
                    return 0
                else:
                    return roll
            else:
                return 0
        elif self.category == "Tectonic":
            if self.star.systemHex.age >= 4 + self.ageModifier:
                roll = roll_xdy(2, 6)
                if self.star.luminosityClass == "D":
                    roll -= 3

                if roll <= 0:
                    return 0
                else:
                    return roll
            elif self.star.systemHex.age >= roll_xdy(1, 3) + self.ageModifier:
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


    def planet_hydrosphere_subsurface_oceans(self):
        """
        Returns a tuple of (hydrosphere, subsurfaceOceans).
            hydrosphere: Integer
                The hydrosphere value of the planet.
            subsurfaceOceans: Boolean
                Flag indicating whether liquid oceans exist beneath a frozen surface.
        """
        if self.category == "Arean":
            roll = roll_xdy(2, 3) + self.size - 7
            if self.atmosphere == 1:
                roll -= 4

            if roll <= 0:
                return (0, False)
            else:
                return (roll, False)
        elif self.category == "Arid":
            return (roll_xdy(1, 3), False)
        elif self.category == "Hebean":
            roll = roll_xdy(2, 6) + self.size - 11

            if roll <= 0:
                return (0, False)
            if roll >= 11:
                return (11, False)
            else:
                return (roll, False)
        elif self.category == "Helian":
            roll = roll_xdy(1, 6)

            if roll <= 2:
                return (0, False)
            elif roll <= 4:
                return (roll_xdy(2, 6) - 1, False)
            else:
                return (15, False)
        elif self.category == "Jovian":
            return (16, False)
        elif self.category == "Meltball":
            return (15, False)
        elif self.category == "Oceanic":
            if self.atmosphere == 1:
                return (11, True)
            else:
                return (11, False)
        elif self.category == "Panthalassic":
            return (11, False)
        elif self.category == "Promethean":
            return (roll_xdy(2, 6) - 2, False)
        elif self.category == "Rockball":
            roll = roll_xdy(2, 6) + self.size - 11
            if self.star.luminosityClass == "L":
                roll += 1

            if self.orbitType == "Epistellar":
                roll -= 2
            elif self.orbitType == "Outer Zone":
                roll += 2

            if roll <= 0:
                return (0, False)
            if roll >= 11:
                return (11, False)
            else:
                return (roll, False)
        elif self.category == "Snowball":
            if roll_xdy(1, 6) <= 3:
                return (10, False)
            else:
                return (roll_xdy(2, 6) - 2, True)
        elif self.category == "Tectonic":
            return (roll_xdy(2, 6) - 2, False)
        elif self.category == "Telluric":
            roll = roll_xdy(1, 6)
            if roll <= 4:
                return (0, False)
            else:
                return (15, False)
        elif self.category == "Vesperian":
            return (roll_xdy(2, 6) - 2, False)
        else:
            return (0, False)


    def dwarf_satellites(self, roll1, roll2):
        """
        Returns the number of dwarf planet satellites orbiting a planet.
        This only applies to Helian and Jovian planets, as they are the only
        types of planets that generate multiple satellites.
        """
        if self.groupName == "Helian":
            if roll1 - 3 > 0:
                if roll2 == 6:
                    return roll1 - 4
                else:
                    return roll1 - 3
            else:
                return 0
        else:  # Jovian
            if roll2 == 6:
                return roll1 - 1
            else:
                return roll1

    def calculate_desirability(self, alien, nearbyColony):
        """
        Sets the planet's desirability score, which is used to determine
        the extent of colonization. This can be different per Alien.

        Parameters:
            alien: Alien class instance
                The alien considering colonization of this planet.
        """
        desirability = 0
        modifiedDistance = round(
            self.systemHex.distanceFromAlienHomeSystem[alien] / (
                (1 if alien.currentTechLevel == 9 else (
                    alien.currentTechLevel - 9))),
            0) - (1 if nearbyColony else 0)

        # Distance penalty
        if modifiedDistance > 3 + alien.reactionModifier:
            desirability -= modifiedDistance

        # Penalty for not having an easy source of fuel in the system
        if not self.systemHex.fuelAvailable:
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
                and 1 <= self.size <= min([14, alien.homePlanet.size + 3])):
            # Garden world
            if (max([1, alien.homePlanet.size - 3]) <= self.size <= min([15, alien.homePlanet.size + 2])
                and any([alien.homePlanet.atmosphere == self.atmosphere,
                          alien.homePlanet.atmosphere == 2 and self.atmosphere in [2, 4],
                          alien.homePlanet.atmosphere == 3 and self.atmosphere in [3, 5],
                          alien.homePlanet.atmosphere == 4 and self.atmosphere in [2, 4, 7],
                          alien.homePlanet.atmosphere == 5 and self.atmosphere in [3, 5, 6],
                          alien.homePlanet.atmosphere == 6 and self.atmosphere in [5, 6, 8],
                          alien.homePlanet.atmosphere == 7 and self.atmosphere in [4, 7, 9],
                          alien.homePlanet.atmosphere == 8 and self.atmosphere in [6, 8],
                          alien.homePlanet.atmosphere == 9 and self.atmosphere in [7, 9],
                          self.subsurfaceOceans and alien.animalClass == "Aquatic"])
                and max([(5 if alien.animalClass == "Aquatic" else 2), alien.homePlanet.hydrosphere - 3]) <= self.hydrosphere <= min([(11 if alien.animalClass == "Aquatic" else 8), alien.homePlanet.hydrosphere + 3])):
                desirability += 5
            # Water world
            elif (2 <= self.atmosphere <= 9
                  and 10 <= self.hydrosphere <= 11
                  and alien.animalClass != "Aquatic"):
                desirability += 3
            # Poor world
            elif (2 <= self.atmosphere <= 6
                  and (2 if alien.animalClass == "Aquatic" else 0) <= self.hydrosphere <= max([(4 if alien.animalClass == "Aquatic" else 3), alien.homePlanet.hydrosphere - 4])):
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

        Parameters:
            alien: Alien class instance
                The alien considering colonization of this planet.
        """
        desirability = 0
        modifiedDistance = round(
            self.systemHex.distanceFromAlienHomeSystem[alien] / (
                (1 if alien.currentTechLevel == 9 else (
                    alien.currentTechLevel - 9))),
            0) - (1 if nearbyColony else 0)

        # Distance penalty
        if modifiedDistance > 3 + alien.reactionModifier:
            desirability -= modifiedDistance

        # Penalty for not having an easy source of fuel in the system
        if not self.systemHex.fuelAvailable:
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

        Parameters:
            alien: Alien class instance
                The alien considering colonization of this planet.
        """
        if self == alien.homePlanet:
            if not alien.extinct:
                self.systemHex.create_surrounding_systems(alienSurvivalPercent, maxTechLevel, maxReactionModifier)
            return "Homeworld"

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

        Parameters:
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
        if self.atmosphere == 13:
            self.atmosphere -= 1
            return True
        elif self.atmosphere == 12:
            if 2 <= self.hydrosphere <= 10:
                self.hydrosphere -= 1
                return True
            elif self.hydrosphere < 2:
                self.atmosphere -= 1
                return True
        elif self.atmosphere > 9:
            self.atmosphere -= 1
            return True
        elif self.atmosphere < 2:
            self.atmosphere += 1
            return True

        # At this point, the planet should have one of the Habitable World bonuses
        # If it's Poor, improve it to Other by raising Hydrosphere
        if self.hydrosphere <= max([(4 if alien.animalClass == "Aquatic" else 3), alien.homePlanet.hydrosphere - 4]):
            self.hydrosphere += 1
            return True

        # If it's Water World and Hydrosphere 10, reduce Hydrosphere to improve it to Other
        # Does not apply to Aquatics
        if self.hydrosphere == 10 and alien.animalClass != "Aquatic":
            self.hydrosphere -= 1
            return True

        # If the planet's size would allow it to be a Garden world, work
        # towards that
        if max([1, alien.homePlanet.size - 3]) <= self.size <= min([15, alien.homePlanet.size + 2]):
            # Lower Hydrosphere if it's too high
            if self.hydrosphere > min([(11 if alien.animalClass == "Aquatic" else 8), alien.homePlanet.hydrosphere + 3]):
                self.hydrosphere -= 1
                return True
            # Raise Hydrosphere if it's too low
            if self.hydrosphere < max([(5 if alien.animalClass == "Aquatic" else 2), alien.homePlanet.hydrosphere - 3]):
                self.hydrosphere -= 1
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

        # If nothing was done, the planet has been
        # terraformed as much as it can, set a flag
        # so we don't run this method for this instance
        # anymore.
        self.terraformingDone = True
        return False
        

    def planet_terrain_animals(self):
        """
        Adds terrain to the planet and animals for each terrain,
        if the biosphere value is high enough.
        """
        if self.atmosphere >= 2 and (2 <= self.hydrosphere <= 8):
            self.terrain.append("Beach/Shore")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Amphibian(planet=self, terrain="Beach/Shore"))
                    self.animals.append(animal.Aquatic(planet=self, terrain="Beach/Shore"))
                    self.animals.append(animal.Avian(planet=self, terrain="Beach/Shore"))
                    self.animals.append(animal.Insect(planet=self, terrain="Beach/Shore"))

        if self.hydrosphere <= 8:
            self.terrain.append("Clear")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Amphibian(planet=self, terrain="Clear"))
                    self.animals.append(animal.Aquatic(planet=self, terrain="Clear"))
                    self.animals.append(animal.Avian(planet=self, terrain="Clear"))
                    self.animals.append(animal.Insect(planet=self, terrain="Clear"))
                    self.animals.append(animal.Mammal(planet=self, terrain="Clear"))

        if (self.atmosphere >= 2 and 5 <=
                self.hydrosphere <= 11) or self.subsurfaceOceans:
            self.terrain.append("Deep Ocean")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Aquatic(planet=self, terrain="Deep Ocean"))

        if self.biosphere >= 9 and self.hydrosphere <= 4 and 2 <= self.atmosphere <= 7:
            self.terrain.append("Desert")
            for _ in range(3):
                self.animals.append(animal.Avian(planet=self, terrain="Desert"))
                self.animals.append(animal.Insect(planet=self, terrain="Desert"))
                self.animals.append(animal.Reptile(planet=self, terrain="Desert"))

        if self.biosphere >= 9 and self.atmosphere >= 4 and 3 <= self.hydrosphere <= 8:
            self.terrain.append("Forest")
            for _ in range(3):
                self.animals.append(animal.Avian(planet=self, terrain="Forest"))
                self.animals.append(animal.Fungal(planet=self, terrain="Forest"))
                self.animals.append(animal.Insect(planet=self, terrain="Forest"))
                self.animals.append(animal.Mammal(planet=self, terrain="Forest"))

        if self.hydrosphere <= 8:
            self.terrain.append("Hills")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Avian(planet=self, terrain="Hills"))
                    self.animals.append(animal.Insect(planet=self, terrain="Hills"))
                    self.animals.append(animal.Mammal(planet=self, terrain="Hills"))
                    self.animals.append(animal.Reptile(planet=self, terrain="Hills"))

        if self.biosphere >= 9 and self.atmosphere >= 4 and 4 <= self.hydrosphere <= 8:
            self.terrain.append("Jungle")
            for _ in range(3):
                self.animals.append(animal.Amphibian(planet=self, terrain="Jungle"))
                self.animals.append(animal.Avian(planet=self, terrain="Jungle"))
                self.animals.append(animal.Fungal(planet=self, terrain="Jungle"))
                self.animals.append(animal.Insect(planet=self, terrain="Jungle"))
                self.animals.append(animal.Reptile(planet=self, terrain="Jungle"))
        if self.hydrosphere <= 8:
            self.terrain.append("Mountains")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Avian(planet=self, terrain="Mountains"))
                    self.animals.append(animal.Insect(planet=self, terrain="Mountains"))

        if (self.atmosphere >= 2 and 3 <=
                self.hydrosphere <= 11) or self.subsurfaceOceans:
            self.terrain.append("Open Ocean")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Aquatic(planet=self, terrain="Open Ocean"))

        if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 7:
            self.terrain.append("Plains")
            for _ in range(3):
                self.animals.append(animal.Avian(planet=self, terrain="Plains"))
                self.animals.append(animal.Insect(planet=self, terrain="Plains"))
                self.animals.append(animal.Mammal(planet=self, terrain="Plains"))
                self.animals.append(animal.Reptile(planet=self, terrain="Plains"))

        if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
            self.terrain.append("Rainforest")
            for _ in range(3):
                self.animals.append(animal.Avian(planet=self, terrain="Rainforest"))
                self.animals.append(animal.Fungal(planet=self, terrain="Rainforest"))
                self.animals.append(animal.Insect(planet=self, terrain="Rainforest"))
                self.animals.append(animal.Reptile(planet=self, terrain="Rainforest"))

        if self.atmosphere >= 2 and 3 <= self.hydrosphere <= 8:
            self.terrain.append("Riverbank")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Amphibian(planet=self, terrain="Riverbank"))
                    self.animals.append(animal.Aquatic(planet=self, terrain="Riverbank"))
                    self.animals.append(animal.Avian(planet=self, terrain="Riverbank"))
                    self.animals.append(animal.Insect(planet=self, terrain="Riverbank"))
                    self.animals.append(animal.Mammal(planet=self, terrain="Riverbank"))
                    self.animals.append(animal.Reptile(planet=self, terrain="Riverbank"))

        if self.hydrosphere <= 8:
            self.terrain.append("Rough/Broken")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Avian(planet=self, terrain="Rough/Broken"))
                    self.animals.append(animal.Insect(planet=self, terrain="Rough/Broken"))
                    self.animals.append(animal.Reptile(planet=self, terrain="Rough/Broken"))

        if (self.atmosphere >= 2 and 2 <= self.hydrosphere <= 10) or (
                self.subsurfaceOceans and self.hydrosphere <= 10):
            self.terrain.append("Shallow Ocean")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Amphibian(planet=self, terrain="Shallow Ocean"))
                    self.animals.append(animal.Aquatic(planet=self, terrain="Shallow Ocean"))
                    self.animals.append(animal.Avian(planet=self, terrain="Shallow Ocean"))

        if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
            self.terrain.append("Swamp/Marsh")
            for _ in range(3):
                self.animals.append(animal.Amphibian(planet=self, terrain="Swamp/Marsh"))
                self.animals.append(animal.Aquatic(planet=self, terrain="Swamp/Marsh"))
                self.animals.append(animal.Avian(planet=self, terrain="Swamp/Marsh"))
                self.animals.append(animal.Fungal(planet=self, terrain="Swamp/Marsh"))
                self.animals.append(animal.Insect(planet=self, terrain="Swamp/Marsh"))
                self.animals.append(animal.Reptile(planet=self, terrain="Swamp/Marsh"))

        if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 8:
            self.terrain.append("Woods")
            for _ in range(3):
                self.animals.append(animal.Fungal(planet=self, terrain="Woods"))
                self.animals.append(animal.Insect(planet=self, terrain="Woods"))
                self.animals.append(animal.Mammal(planet=self, terrain="Woods"))

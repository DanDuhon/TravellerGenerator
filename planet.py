import animal
import alien
import star
from diceroller import roll_xdy
from lookuptable import LookupTable

allPlanets = []

def dwarf_satellites(group, roll1, roll2):
    """
    Returns the number of dwarf planet satellites orbiting a planet.
    This only applies to Helian and Jovian planets, as they are the only
    types of planets that generate multiple satellites.

    Parameters:
        group: String
            Planet group (e.g. Helian, Jovian).
        roll1: Integer
            1d6 rolled to determine how many satellites exist.
        roll2: Integer
            1d6 rolled to determine the types of satellites.
    """
    if group == "Helian":
        if roll1 - 3 > 0:
            if roll2 == 6:
                return roll1 - 4
            else:
                return roll1 - 3
        else:
            return 0
    else: # Jovian
        if roll2 == 6:
            return roll1 - 1
        else:
            return roll1

planetSizeDict = {
    "Acheronian": sum(roll_xdy(1, 6)) + 4,
    "Arean": sum(roll_xdy(1, 6)) - 1,
    "Arid": sum(roll_xdy(1, 6)) + 4,
    "Asphodelian": sum(roll_xdy(1, 6)) + 9,
    "Chthonian": 16,
    "Hebean": sum(roll_xdy(1, 6)) - 1,
    "Helian": sum(roll_xdy(1, 6)) + 9,
    "Jani-Lithic": sum(roll_xdy(1, 6)) + 4,
    "Jovian": 16,
    "Meltball": sum(roll_xdy(1, 6)) - 1,
    "Oceanic": sum(roll_xdy(1, 6)) + 4,
    "Panthalassic": sum(roll_xdy(1, 6)) + 9,
    "Promethean": sum(roll_xdy(1, 6)) - 1,
    "Rockball": sum(roll_xdy(1, 6)) - 1,
    "Snowball": sum(roll_xdy(1, 6)) - 1,
    "Stygian": sum(roll_xdy(1, 6)) - 1,
    "Tectonic": sum(roll_xdy(1, 6)) + 4,
    "Telluric": sum(roll_xdy(1, 6)) + 4,
    "Vesperian": sum(roll_xdy(1, 6)) + 4
    }

def planet_chemistry_age_modifier_class_type(category, luminosityClass, orbitType, biosphere):
    """
    Returns the planet's chemistry type, chemistry age modifier, planet class,
    and planet type.

    Parameters:
        category: String
            The category name of the planet.
        luminosityClass: String
            The luminosity class of the star the planet orbits (if multiple,
            use the primary star).
        orbitType: String
            The type of orbit the planet is in around its star
            (i.e. Epistellar, Inner Zone, Outer Zone).
        biosphere: Integer
            The calculated value of the biosphere of the planet.  Some planets
            only have a chemistry value if the biosphere is above a certain
            threshold.
    
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
    if category == "Acheronian":
        return (None, None, "Telluric", "Acheronian")
    elif category == "Arean":
        roll = sum(roll_xdy(1, 6))
        if luminosityClass == "L":
            roll += 2
        if orbitType == "Outer Zone":
            roll += 2

        if roll <= 4:
            return ("Water", 0, "Geocyclic", "Arean")
        elif roll <= 6:
            return ("Ammonia", 1, "Geocyclic", "Utgardian")
        else:
            return ("Methane", 3, "Geocyclic", "Titanian")
    elif category == "Arid":
        roll = sum(roll_xdy(1, 6))
        if luminosityClass == "K-V":
            roll += 2
        elif luminosityClass == "M-V":
            roll += 4
        elif luminosityClass == "L":
            roll += 5
        if orbitType == "Outer Zone":
            roll += 2

        if roll <= 6:
            return ("Water", 0, "Arid", "Darwinian")
        elif roll <= 8:
            return ("Ammonia", 1, "Arid", "Saganian")
        else:
            return ("Methane", 3, "Arid", "Asimovian")
    elif category == "Asphodelian":
        return (None, None, "Geo-Helian", "Asphodelian")
    elif category == "Chthonian":
        return (None, None, "Chthonian", None)
    elif category == "Hebean":
        if sum(roll_xdy(1, 2)) == 1:
            return (None, None, "Geotidal", "Hebean")
        else:
            return (None, None, "Geotidal", "Idunnian")
    elif category == "Helian":
        if sum(roll_xdy(1, 2)) == 1:
            return (None, None, "Geo-Helian", None)
        else:
            return (None, None, "Nebulous", None)
    elif category == "Jani-Lithic":
        return (None, None, "Epistellar", "Jani-Lithic")
    elif category == "Jovian":
        if biosphere is not None:
            if biosphere > 0:
                roll = sum(roll_xdy(1, 6))
                if luminosityClass == "L":
                    roll += 1
                if orbitType == "Epistellar":
                    roll -= 2
                elif orbitType == "Outer Zone":
                    roll += 2

                if roll <= 3:
                    return ("Water", None, "Dwarf Jovian", "Brammian")
                else:
                    return ("Ammonia", None, "Dwarf Jovian", "Khonsonian")
            else:
                return (None, None, "Jovian", None)
        else:
            return (None, None, None, None)
    elif category == "Meltball":
        if sum(roll_xdy(1, 2)) == 1:
            roll = sum(roll_xdy(1, 3))
            if roll == 1:
                return (None, None, "Geothermic", "Phaethonic")
            elif roll == 2:
                return (None, None, "Geothermic", "Apollonian")
            else:
                return (None, None, "Geothermic", "Sethian")
        else:
            if sum(roll_xdy(1, 2)) == 1:
                return (None, None, "Geotidal", "Hephaestian")
            else:
                return (None, None, "Geotidal", "Lokian")
    elif category == "Oceanic":
        roll = sum(roll_xdy(1, 6))
        if luminosityClass == "K-V":
            roll += 2
        elif luminosityClass == "M-V":
            roll += 4
        elif luminosityClass == "L":
            roll += 5
        if orbitType == "Outer Zone":
            roll += 2

        if roll <= 6:
            if sum(roll_xdy(1, 2)) == 1:
                return ("Water", 0, "Oceanic", "Pelagic")
            else:
                return ("Water", 0, "Tectonic", "Bathy-Gaian")
        elif roll <= 8:
            if sum(roll_xdy(1, 2)) == 1:
                return ("Ammonia", 1, "Oceanic", "Nunnic")
            else:
                return ("Ammonia", 1, "Tectonic", "Bathy-Amunian")
        else:
            if sum(roll_xdy(1, 2)) == 1:
                return ("Methane", 3, "Oceanic", "Teathic")
            else:
                return ("Methane", 3, "Tectonic", "Bathy-Tartarian")
    elif category == "Panthalassic":
        roll = sum(roll_xdy(1, 6))
        if luminosityClass == "K-V":
            roll += 2
        elif luminosityClass == "M-V":
            roll += 4
        elif luminosityClass == "L":
            roll += 5

        if roll <= 6:
            roll = sum(roll_xdy(2, 6))
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
    elif category == "Promethean":
        roll = sum(roll_xdy(1, 6))
        if luminosityClass == "L":
            roll += 2
        if orbitType == "Epistellar":
            roll -= 2
        elif orbitType == "Outer Zone":
            roll += 2

        if roll <= 4:
            return ("Water", 0, "Geotidal", "Promethean")
        elif roll <= 6:
            return ("Ammonia", 1, "Geotidal", "Burian")
        else:
            return ("Methane", 3, "Geotidal", "Atlan")
    elif category == "Rockball":
        roll = sum(roll_xdy(1, 3))
        if roll == 1:
            return (None, None, "Geopassive", "Ferrinian")
        elif roll == 2:
            return (None, None, "Geopassive", "Lithic")
        else:
            return (None, None, "Geopassive", "Carbonian")
    elif category == "Snowball":
        roll = sum(roll_xdy(1, 6))
        if luminosityClass == "L":
            roll += 2
        if orbitType == "Outer Zone":
            roll += 2

        if roll <= 4:
            return ("Water", 0, "Geopassive", "Gelidian")
        elif roll <= 6:
            return ("Ammonia", 1, "Geothermic", "Erisian")
        else:
            return ("Methane", 3, "Geotidal", "Plutonian")
    elif category == "Stygian":
        return (None, None, "Geopassive", "Stygian")
    elif category == "Tectonic":
        roll = sum(roll_xdy(1, 6))
        if luminosityClass == "K-V":
            roll += 2
        elif luminosityClass == "M-V":
            roll += 4
        elif luminosityClass == "L":
            roll += 5
        if orbitType == "Outer Zone":
            roll += 2

        if roll <= 6:
            roll = sum(roll_xdy(2, 6))
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
    elif category == "Telluric":
        if sum(roll_xdy(1, 2)) == 1:
            return (None, None, "Telluric", "Phosphorian")
        else:
            return (None, None, "Telluric", "Cytherean")
    elif category == "Vesperian":
        roll = sum(roll_xdy(2, 6))
        if roll <= 11:
            return ("Water", None, "Epistellar", "Vesperian")
        else:
            return ("Chlorine", None, "Epistellar", "Vesperian")
    else:
        return (None, None, None, None)

def planet_atmosphere(category, luminosityClass, size, chemistry, biosphere = None):
    """
    Returns the planet's atmosphere value.
    
    Requird Parameters:
        category: String
            The category of the planet.
        luminosityClass: String
            The luminosity class of the star the planet orbits  (if multiple,
            use the primary star).
        size: Integer
            The size of the planet.
        chemistry: String
            The prominent chemical substance on the planet.

    Optional Parameters:
        biosphere: Integer
            The numerical value of the planet's biosphere.
            Default: None
    """
    if category in [ "Rockball", "Asteroid Belt", "Stygian" ]:
        return 0
    if category in [ "Acheronian", "Asphodelian", "Chthonian", "Meltball" ]:
        return 1
    elif category == "Arean":
        roll = sum(roll_xdy(1, 6))
        if luminosityClass == "D":
            roll -= 2

        if roll <= 3:
            return 1
        else:
            return 10
    elif biosphere is not None and category == "Arid":
        if biosphere >= 3 and chemistry == "Water":
            roll = sum(roll_xdy(2, 6)) - 7 + size

            if roll < 2:
                return 2
            elif roll > 9:
                return 9
            else:
                return roll
        else:
            return 10
    elif category == "Hebean":
        roll = sum(roll_xdy(1, 6)) + size - 6

        if roll <= 0:
            return 0
        elif roll >= 2:
            return 10
        else:
            return roll
    elif category == "Helian":
        return 13
    elif category == "Jani-Lithic":
        roll = sum(roll_xdy(1, 6))

        if roll <= 3:
            return 1
        else:
            return 10
    elif category == "Jovian":
        return 16
    elif category == "Meltball":
        return 1
    elif category == "Oceanic":
        if chemistry == "Water":
            roll = sum(roll_xdy(2, 6)) + size - 6
            if luminosityClass == "K-V":
                roll -= 1
            elif luminosityClass == "M-V":
                roll -= 2
            elif luminosityClass == "L":
                roll -= 3
            elif luminosityClass in [ "F-IV", "G-IV", "K-IV" ]:
                roll -= 1

            if roll <= 1:
                return 1
            elif roll >= 12:
                return 12
            else:
                return roll
        else:
            roll = sum(roll_xdy(1, 6))

            if roll == 1:
                return 1
            elif roll <= 4:
                return 10
            else:
                return 12
    elif category == "Panthalassic":
        roll = sum(roll_xdy(1, 6)) + 8

        if roll >= 13:
            return 13
        else:
            return roll
    elif biosphere is not None and category == "Promethean":
        if chemistry == "Water" and biosphere >= 3:
            roll = sum(roll_xdy(2, 6)) + size - 7

            if roll <= 2:
                return 2
            elif roll >= 9:
                return 9
            else:
                return roll
        else:
            return 10
    elif category == "Snowball":
        roll = sum(roll_xdy(1, 6))

        if roll <=4:
            return 0
        else:
            return 1
    elif biosphere is not None and category == "Tectonic":
        if biosphere >= 3 and chemistry == "Water":
            roll = sum(roll_xdy(2, 6)) + size - 7

            if roll <= 2:
                return 2
            elif roll >= 9:
                return 9
            else:
                return roll
        elif biosphere >= 3 and chemistry in [ "Sulfur", "Chlorine" ]:
            return 11
        else:
            return 10
    elif category == "Telluric":
        return 12
    elif biosphere is not None and category == "Vesperian":
        if biosphere >= 3 and chemistry == "Water":
            roll = sum(roll_xdy(2, 6)) + size - 7

            if roll <= 2:
                return 2
            elif roll >= 9:
                return 9
            else:
                return roll
        elif biosphere >= 3 and chemistry == "Chlorine":
            return 11
        else:
            return 10
    
def planet_biosphere (category, systemAge, luminosityClass, orbitType, size, ageModifier, atmosphere, subsurfaceOceans):
    """
    Returns the planet's biosphere value.

    Parameters:
        category: String
            The category of the planet.
        systemAge: Integer
            Number from systemhex module representing how old the star system
            is.
        luminosityClass: String
            The luminosity class of the star the planet is orbiting (if
            multiple, use the primary star).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        size: Integer
            The size value of the planet.
        ageModifier: Integer
            The chemical age modifier of the planet.
        atmosphere: Integer
            The atmosphere value of the planet.
        subsurfaceOceans: Boolean
            Flag indicating whether the planet has subsurface oceans.
    """
    if category == "Arean":
        if systemAge >= 4 + ageModifier and atmosphere == 10:
            roll = sum(roll_xdy(1, 6)) + size - 2

            if roll <= 0:
                return 0
            else:
                return roll
        elif systemAge >= sum(roll_xdy(1, 3)) + ageModifier:
            if atmosphere == 1:
                roll = sum(roll_xdy(1, 6)) - 4

                if roll <= 0:
                    return 0
                else:
                    return roll
            else:
                return sum(roll_xdy(1, 3))
        else:
            return 0
    elif category == "Arid":
        if systemAge >= 4 + ageModifier:
            roll = sum(roll_xdy(2, 6))
            if luminosityClass == "D":
                roll -= 3

            if roll <= 0:
                return 0
            else:
                return roll
        elif systemAge >= sum(roll_xdy(1, 3)) + ageModifier:
            return sum(roll_xdy(1, 3))
        else:
            return 0
    elif category == "Jovian":
        roll = sum(roll_xdy(1, 6))
        if orbitType == "Inner Zone":
            roll += 2

        if roll >= 6:
            if systemAge >= sum(roll_xdy(1, 6)):
                return sum(roll_xdy(1, 3))
            elif systemAge >= 7:
                roll = sum(roll_xdy(2, 6))
                if luminosityClass == "D":
                    roll -= 3

                if roll <= 0:
                    return 0
                else:
                    return roll
            else:
                return 0
        else:
            return 0
    elif category == "Oceanic":
        if systemAge >= 4 + ageModifier:
            roll = sum(roll_xdy(2, 6))
            if luminosityClass == "D":
                roll -= 3

            if roll <= 0:
                return 0
            else:
                return roll
        elif systemAge >= sum(roll_xdy(1, 3)) + ageModifier:
            return sum(roll_xdy(1, 3))
        else:
            return 0
    elif category == "Panthalassic":
        if systemAge >= 4 + ageModifier:
            return sum(roll_xdy(2, 6))
        elif systemAge >= sum(roll_xdy(1, 3)) + ageModifier:
            return sum(roll_xdy(1, 3))
        else:
            return 0
    elif category == "Promethean":
        if systemAge >= 4 + ageModifier:
            roll = sum(roll_xdy(2, 6))
            if luminosityClass == "D":
                roll -= 3

            if roll <= 0:
                return 0
            else:
                return roll
        elif systemAge >= sum(roll_xdy(1, 3)) + ageModifier:
            return sum(roll_xdy(1, 3))
        else:
            return 0
    elif category == "Snowball":
        if subsurfaceOceans and systemAge >= 6 + ageModifier:
            roll = sum(roll_xdy(1, 6)) + size - 2

            if roll <= 0:
                return 0
            else:
                return roll
        elif subsurfaceOceans and systemAge >= sum(roll_xdy(1, 6)):
            roll = sum(roll_xdy(1, 6)) - 3

            if roll <= 0:
                return 0
            else:
                return roll
        else:
            return 0
    elif category == "Tectonic":
        if systemAge >= 4 + ageModifier:
            roll = sum(roll_xdy(2, 6))
            if luminosityClass == "D":
                roll -= 3

            if roll <= 0:
                return 0
            else:
                return roll
        elif systemAge >= sum(roll_xdy(1, 3)) + ageModifier:
            return sum(roll_xdy(1, 3))
        else:
            return 0
    elif category == "Vesperian":
        if systemAge >= 4:
            return sum(roll_xdy(2, 6))
        elif systemAge >= sum(roll_xdy(1, 3)):
            return sum(roll_xdy(1, 3))
        else:
            return 0
    else:
        return 0
        
def planet_hydrosphere_subsurface_oceans(category, luminosityClass, orbitType, size, atmosphere):
    """
    Returns a tuple of (hydrosphere integer, subsurfaceOceans Boolean).

    Parameters:
        category: String
            The category of the planet.
        luminosityClass: String
            The luminosity class of the star the planet is orbiting (if
            multiple, use the primary star).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        size: Integer
            The size value of the planet.
        atmosphere: Integer
            The atmosphere value of the planet.
    """
    if category == "Arean":
        roll = sum(roll_xdy(2, 3)) + size - 7
        if atmosphere == 1:
            roll -= 4

        if roll <= 0:
            return (0, False)
        else:
            return (roll, False)
    elif category == "Arid":
        return (sum(roll_xdy(1, 3)), False)
    elif category == "Hebean":
        roll = sum(roll_xdy(2, 6)) + size - 11

        if roll <= 0:
            return (0, False)
        if roll >= 11:
            return (11, False)
        else:
            return (roll, False)
    elif category == "Helian":
        roll = sum(roll_xdy(1, 6))

        if roll <= 2:
            return (0, False)
        elif roll <= 4:
            return (sum(roll_xdy(2, 6)) - 1, False)
        else:
            return (15, False)
    elif category == "Jovian":
        return (16, False)
    elif category == "Meltball":
        return (15, False)
    elif category == "Oceanic":
        if atmosphere == 1:
            return (11, True)
        else:
            return (11, False)
    elif category == "Panthalassic":
        return (11, False)
    elif category == "Promethean":
        return (sum(roll_xdy(2, 6)) - 2, False)
    elif category == "Rockball":
        roll = sum(roll_xdy(2, 6)) + size - 11
        if luminosityClass == "L":
            roll += 1

        if orbitType == "Epistellar":
            roll -= 2
        elif orbitType == "Outer Zone":
            roll += 2

        if roll <= 0:
            return (0, False)
        if roll >= 11:
            return (11, False)
        else:
            return (roll, False)
    elif category == "Snowball":
        if sum(roll_xdy(1, 6)) <= 3:
            return (10, False)
        else:
            return (sum(roll_xdy(2, 6)) - 2, True)
    elif category == "Tectonic":
        return (sum(roll_xdy(2, 6)) - 2, False)
    elif category == "Telluric":
        roll = sum(roll_xdy(1, 6))
        if roll <= 4:
            return (0, False)
        else:
            return (15, False)
    elif category == "Vesperian":
        return (sum(roll_xdy(2, 6)) - 2, False)
    else:
        return (0, False)

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

def dwarf_category(orbitType, parentObject):
    """
    Returns the category of a planet based on dwarfCategoryDict.

    Parameters:
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        parentType: Class instance
            The orbit object that caused this planet to be created. Valid
            classes are Star, AsteroidBelt, DwarfPlanet, TerrestrialPlanet,
            HelianPlanet, JovianPlanet.
    """
    roll = sum(roll_xdy(1, 6))
            
    if orbitType == "Epistellar":
        if isinstance(parentObject, AsteroidBelt):
            roll -= 2

        if roll == 6:
            return dwarfCategoryDict[orbitType][roll][sum(roll_xdy(1, 6))]
    elif orbitType == "Inner Zone":
        if isinstance(parentObject, AsteroidBelt):
            roll -= 2
        elif isinstance(parentObject, HelianPlanet):
            roll += 1
        elif isinstance(parentObject, JovianPlanet):
            roll += 2

        if roll == 8:
            return dwarfCategoryDict[orbitType][roll][sum(roll_xdy(1, 6))]
    else: # Outer Zone
        if isinstance(parentObject, AsteroidBelt):
            roll -= 1
        elif isinstance(parentObject, HelianPlanet):
            roll += 1
        elif isinstance(parentObject, JovianPlanet):
            roll += 2

        if roll == 8:
            return dwarfCategoryDict[orbitType][roll][sum(roll_xdy(1, 6))]
        
    return dwarfCategoryDict[orbitType][roll]

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

def terrestrial_category(orbitType, parentObject, star):
    """
    Returns the category of a planet based on terrestrialCategoryDict.

    Parameters:
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        parentType: Class instance
            The orbit object that caused this planet to be created. Valid
            classes are Star, HelianPlanet, JovianPlanet.
    """
    roll = sum(roll_xdy(1, 6))
            
    if orbitType == "Inner Zone":
        roll += sum(roll_xdy(1, 6))
    elif orbitType == "Outer Zone":
        if parentObject != star:
            roll += 2
        
    return terrestrialCategoryDict[orbitType][roll]

def helian_category(orbitType):
    """
    Returns the category of a Helian planet.

    Parameters:
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
    """
    if orbitType == "Epistellar" and sum(roll_xdy(1, 6)) == 6:
        return "Asphodelian"
    elif orbitType == "Inner Zone" and sum(roll_xdy(1, 6)) >= 5:
        return "Panthalassic"
    else: # Outer Zone and other rolls
        return "Helian"

def jovian_category(orbitType):
    """
    Returns the category of a Jovian planet.

    Parameters:
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
    """
    if orbitType == "Epistellar" and sum(roll_xdy(1, 6)) == 6:
        return "Chthonian"
    else: # Inner Zone, Outer Zone, and other rolls
        return "Jovian"

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
    "Vesperian": "These worlds are tide-locked to their primary, but at a distance that permits surface liquid and the development of life."
    }

class OrbitalBody():
    """
    Defines an object that orbits a Star or other OrbitalBody.

    Parameters:
        star: Star class instance
            The star that this Orbital Body orbits (even if it already
            orbits another Orbital Body).
        parentObject: Class instance
            The object that this Orbital Body directly orbits. Valid classes
            are Star, AsteroidBelt, DwarfPlanet, TerrestrialPlanet,
            HelianPlanet, JovianPlanet.
        order: Integer
            Indicates that this is the nth orbit from the star (e.g. Earth
            would have a value of 3).
        orbitType: String
            The type of orbit the planet is in (i.e. Epistellar, Inner Zone,
            Outer Zone)
        luminosityClass: String
            The luminosity class of the star the planet is orbiting (if
            multiple, use the primary star).
        expansionAffectedOrbits: Integer
            If the star this Orbital Body orbits is one of several types,
            this will determine how many Orbital Bodies (via order) are
            affected by the star's expansion.
        systemAge: Integer
            Number from systemhex module representing how old the star system
            is.
    """
    def __init__ (self, starInstance, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge):
        allPlanets.append(self)
        self.systemHex = starInstance.systemHex
        self.star = starInstance
        self.parentObject = parentObject
        self.order = order
        self.orbitType = orbitType
        self.category = None
        self.size = None
        self.className = None
        self.atmosphere = None
        self.biosphere = None
        self.hydrosphere = None
        self.subsurfaceOceans = None
        self.terrain = []
        self.animals = []
        self.satellites = []
        self.alien = None
        self.properName = None
        if parentObject == starInstance:
            self.name = parentObject.name + " " + str(order)
        else:
            self.name = parentObject.name + "-" + str(len(parentObject.satellites) + 1)
        
    def set_class_chemistry_atmosphere_hydrosphere_biosphere(self, systemAge, luminosityClass):
        """
        Sets the planet's chemistry, atmosphere, hydrosphere, and biosphere
        values. Not all planet categories have the same order of operations.
        The below order is the most common, but it is in a loop to accommodate
        the planets that determine these things in a different order.

        Parameters:
            systemAge: Integer
                The age of the system hex.
            luminosityClass: String
                The luminosity class of the star the planet orbits (if multiple,
                use the primary star).
        """
        while self.className is None or self.atmosphere is None or self.biosphere is None or self.hydrosphere is None:
            if self.className is None:
                chemistryAgeModifierClassType = planet_chemistry_age_modifier_class_type(category = self.category, luminosityClass = luminosityClass, orbitType = self.orbitType, biosphere = self.biosphere)
                self.chemistry = chemistryAgeModifierClassType[0]
                self.ageModifier = chemistryAgeModifierClassType[1]
                self.className = chemistryAgeModifierClassType[2]
                self.type = chemistryAgeModifierClassType[3]

            if self.atmosphere is None:
                self.atmosphere = planet_atmosphere(category = self.category, luminosityClass = luminosityClass, size = self.size, chemistry = self.chemistry, biosphere = self.biosphere)

            if self.biosphere is None:
                self.biosphere = planet_biosphere(category = self.category, systemAge = systemAge, luminosityClass = luminosityClass, orbitType = self.orbitType, size = self.size, ageModifier = self.ageModifier, atmosphere = self.atmosphere, subsurfaceOceans = self.subsurfaceOceans)

            if self.hydrosphere is None:
                hydrosphereSubsurfaceOceans = planet_hydrosphere_subsurface_oceans(category = self.category, luminosityClass = luminosityClass, orbitType = self.orbitType, size = self.size, atmosphere = self.atmosphere)
                self.hydrosphere = hydrosphereSubsurfaceOceans[0]
                self.subsurfaceOceans = hydrosphereSubsurfaceOceans[1]

    def planet_terrain_animals(self):
        """
        Adds terrain to the planet and animals for each terrain,
        if the biosphere value is high enough.
        """
    
        if self.atmosphere >= 2 and (2 <= self.hydrosphere <= 8):
            self.terrain.append("Beach/Shore")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Amphibian(planet = self, terrain = "Beach/Shore"))
                    self.animals.append(animal.Aquatic(planet = self, terrain = "Beach/Shore"))
                    self.animals.append(animal.Avian(planet = self, terrain = "Beach/Shore"))
                    self.animals.append(animal.Insect(planet = self, terrain = "Beach/Shore"))
    
        if self.hydrosphere <= 8:
            self.terrain.append("Clear")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Amphibian(planet = self, terrain = "Clear"))
                    self.animals.append(animal.Aquatic(planet = self, terrain = "Clear"))
                    self.animals.append(animal.Avian(planet = self, terrain = "Clear"))
                    self.animals.append(animal.Insect(planet = self, terrain = "Clear"))
                    self.animals.append(animal.Mammal(planet = self, terrain = "Clear"))
    
        if (self.atmosphere >= 2 and 5 <= self.hydrosphere <= 11) or self.subsurfaceOceans:
            self.terrain.append("Deep Ocean")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Aquatic(planet = self, terrain = "Deep Ocean"))
    
        if self.biosphere >= 9 and self.hydrosphere <= 4 and 2 <= self.atmosphere <= 7:
            self.terrain.append("Desert")
            for _ in range(3):
                self.animals.append(animal.Avian(planet = self, terrain = "Desert"))
                self.animals.append(animal.Insect(planet = self, terrain = "Desert"))
                self.animals.append(animal.Reptile(planet = self, terrain = "Desert"))
    
        if self.biosphere >= 9 and self.atmosphere >= 4 and 3 <= self.hydrosphere <= 8:
            self.terrain.append("Forest")
            for _ in range(3):
                self.animals.append(animal.Avian(planet = self, terrain = "Forest"))
                self.animals.append(animal.Fungal(planet = self, terrain = "Forest"))
                self.animals.append(animal.Insect(planet = self, terrain = "Forest"))
                self.animals.append(animal.Mammal(planet = self, terrain = "Forest"))
    
        if self.hydrosphere <= 8:
            self.terrain.append("Hills")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Avian(planet = self, terrain = "Hills"))
                    self.animals.append(animal.Insect(planet = self, terrain = "Hills"))
                    self.animals.append(animal.Mammal(planet = self, terrain = "Hills"))
                    self.animals.append(animal.Reptile(planet = self, terrain = "Hills"))
    
        if self.biosphere >= 9 and self.atmosphere >= 4 and 4 <= self.hydrosphere <= 8:
            self.terrain.append("Jungle")
            for _ in range(3):
                self.animals.append(animal.Amphibian(planet = self, terrain = "Jungle"))
                self.animals.append(animal.Avian(planet = self, terrain = "Jungle"))
                self.animals.append(animal.Fungal(planet = self, terrain = "Jungle"))
                self.animals.append(animal.Insect(planet = self, terrain = "Jungle"))
                self.animals.append(animal.Reptile(planet = self, terrain = "Jungle"))
    
        if self.hydrosphere  <= 8:
            self.terrain.append("Mountains")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Avian(planet = self, terrain = "Mountains"))
                    self.animals.append(animal.Insect(planet = self, terrain = "Mountains"))
    
        if (self.atmosphere>= 2 and 3 <= self.hydrosphere <= 11) or self.subsurfaceOceans:
            self.terrain.append("Open Ocean")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Aquatic(planet = self, terrain = "Open Ocean"))
    
        if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 7:
            self.terrain.append("Plains")
            for _ in range(3):
                self.animals.append(animal.Avian(planet = self, terrain = "Plains"))
                self.animals.append(animal.Insect(planet = self, terrain = "Plains"))
                self.animals.append(animal.Mammal(planet = self, terrain = "Plains"))
                self.animals.append(animal.Reptile(planet = self, terrain = "Plains"))
    
        if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
            self.terrain.append("Rainforest")
            for _ in range(3):
                self.animals.append(animal.Avian(planet = self, terrain = "Rainforest"))
                self.animals.append(animal.Fungal(planet = self, terrain = "Rainforest"))
                self.animals.append(animal.Insect(planet = self, terrain = "Rainforest"))
                self.animals.append(animal.Reptile(planet = self, terrain = "Rainforest"))
    
        if self.atmosphere >= 2 and 3 <= self.hydrosphere <= 8:
            self.terrain.append("Riverbank")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Amphibian(planet = self, terrain = "Riverbank"))
                    self.animals.append(animal.Aquatic(planet = self, terrain = "Riverbank"))
                    self.animals.append(animal.Avian(planet = self, terrain = "Riverbank"))
                    self.animals.append(animal.Insect(planet = self, terrain = "Riverbank"))
                    self.animals.append(animal.Mammal(planet = self, terrain = "Riverbank"))
                    self.animals.append(animal.Reptile(planet = self, terrain = "Riverbank"))
    
        if self.hydrosphere <= 8:
            self.terrain.append("Rough/Broken")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Avian(planet = self, terrain = "Rough/Broken"))
                    self.animals.append(animal.Insect(planet = self, terrain = "Rough/Broken"))
                    self.animals.append(animal.Reptile(planet = self, terrain = "Rough/Broken"))
    
        if (self.atmosphere >= 2 and 2 <= self.hydrosphere <= 10) or self.subsurfaceOceans:
            self.terrain.append("Shallow Ocean")
            if self.biosphere >= 9:
                for _ in range(3):
                    self.animals.append(animal.Amphibian(planet = self, terrain = "Shallow Ocean"))
                    self.animals.append(animal.Aquatic(planet = self, terrain = "Shallow Ocean"))
                    self.animals.append(animal.Avian(planet = self, terrain = "Shallow Ocean"))
    
        if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
            self.terrain.append("Swamp/Marsh")
            for _ in range(3):
                self.animals.append(animal.Amphibian(planet = self, terrain = "Swamp/Marsh"))
                self.animals.append(animal.Aquatic(planet = self, terrain = "Swamp/Marsh"))
                self.animals.append(animal.Avian(planet = self, terrain = "Swamp/Marsh"))
                self.animals.append(animal.Fungal(planet = self, terrain = "Swamp/Marsh"))
                self.animals.append(animal.Insect(planet = self, terrain = "Swamp/Marsh"))
                self.animals.append(animal.Reptile(planet = self, terrain = "Swamp/Marsh"))
    
        if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 8:
            self.terrain.append("Woods")
            for _ in range(3):
                self.animals.append(animal.Fungal(planet = self, terrain = "Woods"))
                self.animals.append(animal.Insect(planet = self, terrain = "Woods"))
                self.animals.append(animal.Mammal(planet = self, terrain = "Woods"))

class DwarfPlanet(OrbitalBody):
    """
    Defines a dwarf planet.

    Parameters:
        All parameters for __init__ are used in the OrbitalBody parent class.
    """
    def __init__ (self, star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge, alienSurvivalPercent, maxTechLevel):
        super(DwarfPlanet, self).__init__ (star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge)

        if expansionAffectedOrbits >= order:
            self.category = "Stygian"
        else:
            self.category = dwarf_category(self.orbitType, self.parentObject)

        self.size = planetSizeDict[self.category]

        self.set_class_chemistry_atmosphere_hydrosphere_biosphere(systemAge, luminosityClass)
            
        self.planet_terrain_animals()

        if self.biosphere >= 12:
            alien.create_alien(self, alienSurvivalPercent)

        if sum(roll_xdy(1, 6)) == 6 and not isinstance(parentObject, DwarfPlanet):
            self.satellites.append(DwarfPlanet(star = self.star, parentObject = self, order = self.order, orbitType = self.orbitType, luminosityClass = luminosityClass, expansionAffectedOrbits = expansionAffectedOrbits, systemAge = systemAge, alienSurvivalPercent = alienSurvivalPercent, maxTechLevel = maxTechLevel))

class AsteroidBelt(OrbitalBody):
    """
    Defines an asteroid belt.

    Parameters:
        All parameters for __init__ are used in the OrbitalBody parent class.
    """
    def __init__ (self, star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge, alienSurvivalPercent, maxTechLevel):
        super(AsteroidBelt, self).__init__ (star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge)
        self.category = "Asteroid Belt"
        self.size = 0
        self.className = "Asteroid Belt"
        self.atmosphere = 0
        self.biosphere = 0
        self.hydrosphere = 0
        self.subsurfaceOceans = False

        if sum(roll_xdy(1, 6)) <= 4:
            self.satellites.append(DwarfPlanet(star = self.star, parentObject = self, order = self.order, orbitType = self.orbitType, luminosityClass = luminosityClass, expansionAffectedOrbits = expansionAffectedOrbits, systemAge = systemAge, alienSurvivalPercent = alienSurvivalPercent, maxTechLevel = maxTechLevel))

        for s in self.satellites:
            self.satellites.extend(s.satellites)

class TerrestrialPlanet(OrbitalBody):
    """
    Defines a terrestrial planet.

    Parameters:
        All parameters for __init__ are used in the OrbitalBody parent class.
    """
    def __init__ (self, star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge, alienSurvivalPercent, maxTechLevel):
        super(TerrestrialPlanet, self).__init__ (star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge)

        if expansionAffectedOrbits >= order:
            self.category = "Acheronian"
        else:
            self.category = terrestrial_category(self.orbitType, self.parentObject, self.star)
            
        self.size = planetSizeDict[self.category]
        
        self.set_class_chemistry_atmosphere_hydrosphere_biosphere(systemAge, luminosityClass)
            
        self.planet_terrain_animals()

        if self.biosphere >= 12:
            alien.create_alien(self, alienSurvivalPercent)

        if sum(roll_xdy(1, 6)) >= 5:
            self.satellites.append(DwarfPlanet(star = self.star, parentObject = self, order = self.order, orbitType = self.orbitType, luminosityClass = luminosityClass, expansionAffectedOrbits = expansionAffectedOrbits, systemAge = systemAge, alienSurvivalPercent = alienSurvivalPercent, maxTechLevel = maxTechLevel))

        for s in self.satellites:
            self.satellites.extend(s.satellites)
            for s2 in s.satellites:
                self.satellites.extend(s2.satellites)

class HelianPlanet(OrbitalBody):
    """
    Defines a helian planet.

    Parameters:
        All parameters for __init__ are used in the OrbitalBody parent class.
    """
    def __init__ (self, star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge, alienSurvivalPercent, maxTechLevel):
        super(HelianPlanet, self).__init__ (star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge)

        if expansionAffectedOrbits >= order:
            self.category = "Asphodelian"
        else:
            self.category = helian_category(self.orbitType)

        self.size = planetSizeDict[self.category]
        
        self.set_class_chemistry_atmosphere_hydrosphere_biosphere(systemAge, luminosityClass)
            
        self.planet_terrain_animals()

        if self.biosphere >= 12:
            alien.create_alien(self, alienSurvivalPercent)

        satelliteRoll1 = sum(roll_xdy(1, 6))
        satelliteRoll2 = sum(roll_xdy(1, 6))

        for _ in range(dwarf_satellites("Helian", satelliteRoll1, satelliteRoll2)):
            self.satellites.append(DwarfPlanet(star = self.star, parentObject = self, order = self.order, orbitType = self.orbitType, luminosityClass = luminosityClass, expansionAffectedOrbits = expansionAffectedOrbits, systemAge = systemAge, alienSurvivalPercent = alienSurvivalPercent, maxTechLevel = maxTechLevel))
        if satelliteRoll2 == 6 and satelliteRoll1 - 3 > 0:
            self.satellites.append(TerrestrialPlanet(star = self.star, parentObject = self, order = self.order, orbitType = self.orbitType, luminosityClass = luminosityClass, expansionAffectedOrbits = expansionAffectedOrbits, systemAge = systemAge, alienSurvivalPercent = alienSurvivalPercent, maxTechLevel = maxTechLevel))

        for s in self.satellites:
            self.satellites.extend(s.satellites)
            for s2 in s.satellites:
                self.satellites.extend(s2.satellites)
                for s3 in s2.satellites:
                    self.satellites.extend(s3.satellites)

class JovianPlanet(OrbitalBody):
    """
    Defines a jovian planet.

    Parameters:
        All parameters for __init__ are used in the OrbitalBody parent class.
    """
    def __init__ (self, star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge, alienSurvivalPercent, maxTechLevel):
        super(JovianPlanet, self).__init__ (star, parentObject, order, orbitType, luminosityClass, expansionAffectedOrbits, systemAge)

        if expansionAffectedOrbits >= order:
            self.category = "Chthonian"
        else:
            self.category = jovian_category(self.orbitType)

        self.size = planetSizeDict[self.category]
        
        self.set_class_chemistry_atmosphere_hydrosphere_biosphere(systemAge, luminosityClass)

        if sum(roll_xdy(1, 6)) <= 4:
            self.ringSystem = "Minor"
        else:
            self.ringSystem = "Complex"
            
        satelliteRoll1 = sum(roll_xdy(1, 6))
        satelliteRoll2 = sum(roll_xdy(1, 6))
        satelliteRoll3 = sum(roll_xdy(1, 6))

        for _ in range(dwarf_satellites("Jovian", satelliteRoll1, satelliteRoll2)):
            self.satellites.append(DwarfPlanet(star = self.star, parentObject = self, order = self.order, orbitType = self.orbitType, luminosityClass = luminosityClass, expansionAffectedOrbits = expansionAffectedOrbits, systemAge = systemAge, alienSurvivalPercent = alienSurvivalPercent, maxTechLevel = maxTechLevel))
        if satelliteRoll2 == 6 and satelliteRoll3 <= 5:
            self.satellites.append(TerrestrialPlanet(star = self.star, parentObject = self, order = self.order, orbitType = self.orbitType, luminosityClass = luminosityClass, expansionAffectedOrbits = expansionAffectedOrbits, systemAge = systemAge, alienSurvivalPercent = alienSurvivalPercent, maxTechLevel = maxTechLevel))
        if satelliteRoll2 == 6 and satelliteRoll3 == 6:
            self.satellites.append(HelianPlanet(star = self.star, parentObject = self, order = self.order, orbitType = self.orbitType, luminosityClass = luminosityClass, expansionAffectedOrbits = expansionAffectedOrbits, systemAge = systemAge, alienSurvivalPercent = alienSurvivalPercent, maxTechLevel = maxTechLevel))

        for s in self.satellites:
            self.satellites.extend(s.satellites)
            for s2 in s.satellites:
                self.satellites.extend(s2.satellites)
                for s3 in s2.satellites:
                    self.satellites.extend(s3.satellites)
                    for s4 in s3.satellites:
                        self.satellites.extend(s4.satellites)

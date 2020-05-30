import random
import statistics

import animal
import planet
import systemhex
import namegenerator
from diceroller import roll_xdy

allAliens = []


class Alien():
    """
    Defines an alien. Aliens have their basis in an animal. An animal is
    generated first, then the intelligence is raised to 7, strength and
    dexterity are lowered, and a score for determining tech level is
    generated.

    Parameters:
        homePlanet: Class instance
            The planet on which the alien species originated.
        animalClass: String
            The class of animal (e.g. Amphibian, Insect, Mammal).
        strength: Integer
            Strength stat value from animal generation.
        dexterity: Integer
            Dexterity stat value from animal generation.
        endurance: Integer
            Endurance stat value from animal generation.
        size: String
            Weight value from animal generation.
        athletics: Integer
            Athletics skill value from animal generation.
        deception: Integer
            Deception skill value from animal generation.
        meleeNaturalWeapons: Integer
            Melee Natural Weapons skill value from animal generation.
        persuade: Integer
            Persuade skill value from animal generation.
        recon: Integer
            Recon skill value from animal generation.
        stealth: Integer
            Stealth skill value from animal generation.
        survival: Integer
            Survival skill value from animal generation.
        naturalWeapons: List of strings
            Weapons list from animal generation.
        exoticNaturalWeapons: List of strings
            Exotic weapons list from animal generation.
        naturalWeaponDice: Integer
            Weapon dice value from animal generation.
        naturalWeaponDamageModifier: Integer
            Weapon damage modifier value from animal generation.
        initiative: Integer
            Initiative value from animal generation.
        quirks: List of strings
            List of quirks from animal generation.
        extinct: Boolean
            Whether the alien species has gone extinct or not.
        reactionModifier: Integer
            The reaction modifier from the animal.
        aggressionModifier: Integer
            The calculated aggression modifier of the alien, based on animal
            behaviors.
        techLevelScore: Integer
            The calculated tech level score of the alien.
    """

    def __init__(
            self,
            homePlanet,
            animalBasis,
            animalClass,
            strength,
            dexterity,
            endurance,
            size,
            athletics,
            deception,
            meleeNaturalWeapons,
            persuade,
            recon,
            stealth,
            survival,
            naturalWeapons,
            exoticNaturalWeapons,
            naturalWeaponDice,
            naturalWeaponDamageModifier,
            initiative,
            quirks,
            extinct,
            reactionModifier,
            aggressionModifier,
            techLevelScore):
        allAliens.append(self)
        self.name = namegenerator.alienNGrams.generate_name()
        self.homePlanet = homePlanet
        self.animalBasis = animalBasis
        self.animalClass = animalClass
        self.strength = strength
        self.dexterity = dexterity
        self.endurance = endurance
        self.intellect = 7
        self.size = size
        self.athletics = athletics
        self.deception = deception
        self.meleeNaturalWeapons = meleeNaturalWeapons
        self.persuade = persuade
        self.recon = recon
        self.stealth = stealth
        self.survival = survival
        self.naturalWeapons = naturalWeapons
        self.exoticNaturalWeapons = exoticNaturalWeapons
        self.naturalWeaponDice = naturalWeaponDice
        self.naturalWeaponDamageModifier = naturalWeaponDamageModifier
        self.initiative = initiative
        self.quirks = quirks
        self.extinct = extinct
        self.reactionModifier = reactionModifier
        self.aggressionModifier = aggressionModifier
        self.techLevelScore = techLevelScore
        self.maxTechLevel = 0
        self.currentTechLevel = 0
        self.exploredSystems = set()
        self.planets = dict()

        for s in systemhex.allSystems:
            s.distanceFromAlienHomeSystem[self] = systemhex.distance_between_systems(s, self.homePlanet.systemHex)


def create_terra_luna_humans(star, maxTechLevel):
    """
    This will return "Earth", the origin of humans.
    It will also create the moon and humans.

    Parameters:
        star: Star class instance
            The star that Terra orbits.
            the star it is orbiting.
        maxTechLevel: Integer
            The user-provided maximum tech level for any species.
    """
    # Terra
    planet.create_terrestrial_planet(
        star=star,
        parentObject=star,
        order=star.epistellarOrbits + star.innerZoneOrbits + 1,
        orbitType="Inner Zone",
        alienSurvivalPercent=0)

    terra = star.planets[-1]

    terra.properName = "Terra"
    terra.category = "Tectonic"
    terra.size = 8
    terra.chemistry = "Water"
    terra.ageModifier = 0
    terra.className = "Tectonic"
    terra.type = "Gaian"
    terra.atmosphere = 6
    terra.hydrosphere = 7
    terra.subsurfaceOceans = False
    terra.biosphere = 12
    terra.terrain = [
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
    terra.animals = ["The animals of Earth."]

    # Remove any satellites that were created.
    for s in terra.satellites:
        for s2 in s.satellites:
            if s2 in planet.allPlanets:
                planet.allPlanets.remove(s2)
            s.satellites.remove(s2)
        if s in planet.allPlanets:
            planet.allPlanets.remove(s)
        terra.satellites.remove(s)

    # Luna
    planet.create_dwarf_planet(
        star=star,
        parentObject=terra,
        order=terra.order,
        orbitType="Inner Zone",
        alienSurvivalPercent=0)

    luna = terra.satellites[-1]

    luna.properName = "Luna"
    luna.category = "Rockball"
    luna.size = 2
    luna.chemistry = None
    luna.ageModifier = None
    luna.className = "Geopassive"
    luna.type = "Lithic"
    luna.atmosphere = 0
    luna.hydrosphere = 0
    luna.subsurfaceOceans = False
    luna.biosphere = 0
    luna.terrain = ["Clear", "Hills", "Mountains", "Rough/Broken"]
    luna.animals = []
    luna.satellites = []
    luna.alien = None

    # Humans
    if len([alien.techLevelScore for alien in allAliens if not alien.extinct]) > 0:
        avgTechLevelScore = round(statistics.mean(
            [alien.techLevelScore for alien in allAliens if not alien.extinct]), 0)
        terra.alien = Alien(terra, None, "Mammal",
                7, 7, 7, 6, 0, 0, 0, 0, 0, 0, 0,
                set(), set(), 1, 0, 0,
                set(), False, 0, 0, avgTechLevelScore + roll_xdy(1, 6))
    else:
        terra.alien = Alien(terra, None, "Mammal",
                7, 7, 7, 6, 0, 0, 0, 0, 0, 0, 0,
                set(), set(), 1, 0, 0,
                set(), False, 0, 0, 10)

    terra.alien.name = "Terran"
    terra.habitation[terra.alien] = "Homeworld"
    terra.alien.planets[terra] = {"outpostRoll": None,
                                  "colonyRoll": None,
                                  "desirability": 8,
                                  "habitation": "Homeworld"}
    terra.settlement = 100

    return terra


def create_alien(alienPlanet, alienSurvivalPercent):
    """
    Returns an Alien class instance to be added to a planet.

    Parameters:
        alienPlanet: OrbitalBody subclass instance
            The planet that is the alien's homeworld.
        alienSurvivalPercent: Integer
            A number representing the percent chance that an alien species
            will survive to discover jump technology.
    """
    # Build a list of animal classes and terrains that are possible for this
    # planet, then pick one at random.
    possibleAliens = list(set([(animal.animalClass, animal.terrain) for animal in alienPlanet.animals if animal.animalClass in [
        "Amphibian", "Aquatic", "Insect", "Mammal", "Reptile"]]))

    alienClass, alienTerrain = random.choice(possibleAliens)

    if alienClass == "Amphibian":
        animalToConvert = animal.Amphibian(planet=alienPlanet, terrain=alienTerrain)
    elif alienClass == "Aquatic":
        animalToConvert = animal.Aquatic(planet=alienPlanet, terrain=alienTerrain)
    elif alienClass == "Insect":
        animalToConvert = animal.Insect(planet=alienPlanet, terrain=alienTerrain)
    elif alienClass == "Mammal":
        animalToConvert = animal.Mammal(planet=alienPlanet, terrain=alienTerrain)
    elif alienClass == "Reptile":
        animalToConvert = animal.Reptile(planet=alienPlanet, terrain=alienTerrain)
        # This particular quirk does not seem suitable to intelligent species
        # that have to construct things.
        # Remove it if we happen to generate an intelligent reptile that has
        # it.
        if "Capable of flying, these reptiles have adapted body structures that generate heat through wind friction, allowing them to stay warm during flight. They do not sleep, they never land intentionally and will die within 1d6 hours if grounded." in animalToConvert.quirks:
            animalToConvert.quirks.remove(
                "Capable of flying, these reptiles have adapted body structures that generate heat through wind friction, allowing them to stay warm during flight. They do not sleep, they never land intentionally and will die within 1d6 hours if grounded.")
            animalToConvert.primaryMovement = "Walk"

    # Chimpanzees (the existing animal closest to us, genetically) are about
    # 35% stronger than humans, on average. I'm going to say that we traded
    # strength and dexterity for intelligence, and aliens will do that as well.
    strength = round((animalToConvert.strength * 100) / 135, 0)
    dexterity = round((animalToConvert.dexterity * 100) / 135, 0)

    # This is intended to give an edge to species that are aggressive, but not
    # too aggressive. This will be used to determine tech level and how quickly
    # a species explores outwards from colonized planets.
    behaviorAggressionNumbers = []
    for behavior in animalToConvert.behaviors:
        if behavior == "Carrion-Eater":
            behaviorAggressionNumbers.append(11)
        elif behavior in ["Filter", "Intermittent", "Reducer"]:
            behaviorAggressionNumbers.append(10)
        elif behavior == "Gatherer":
            behaviorAggressionNumbers.append(9)
        elif behavior in ["Grazer", "Hunter", "Intimidator"]:
            behaviorAggressionNumbers.append(8)
        elif behavior in ["Pouncer", "Chaser", "Trapper", "Siren", "Hijacker"]:
            behaviorAggressionNumbers.append(7)
        elif behavior == "Killer":
            behaviorAggressionNumbers.append(6)
        elif behavior == "Eater":
            behaviorAggressionNumbers.append(5)

    aggressionModifier = int(
        round(statistics.mean(behaviorAggressionNumbers), 0))

    # Tech level score will be used to determine tech level.
    # This is so that species with higher instincts and pack scores have an
    # edge, but no one is completely left in the dust.
    survivalRoll = roll_xdy(1, 100)
    if survivalRoll <= alienSurvivalPercent:
        extinct = False
        techLevelScore = (animalToConvert.pack + animalToConvert.instinct +
            (aggressionModifier - 9 if aggressionModifier < 9 else 9 - aggressionModifier))
    else:
        extinct = True
        techLevelScore = 0

    alienPlanet.alien = Alien(
        homePlanet=alienPlanet,
        animalBasis=animalToConvert,
        animalClass=animalToConvert.animalClass,
        strength=strength,
        dexterity=dexterity,
        endurance=animalToConvert.endurance,
        size=animalToConvert.size,
        athletics=animalToConvert.athletics,
        deception=animalToConvert.deception,
        meleeNaturalWeapons=animalToConvert.meleeNaturalWeapons,
        persuade=animalToConvert.persuade,
        recon=animalToConvert.recon,
        stealth=animalToConvert.stealth,
        survival=animalToConvert.survival,
        naturalWeapons=animalToConvert.weapons,
        exoticNaturalWeapons=animalToConvert.exoticWeapons,
        naturalWeaponDice=animalToConvert.weaponDice,
        naturalWeaponDamageModifier=animalToConvert.weaponDamageModifier,
        initiative=animalToConvert.initiative,
        quirks=animalToConvert.quirks,
        extinct=extinct,
        reactionModifier=animalToConvert.reactionModifier,
        aggressionModifier=aggressionModifier,
        techLevelScore=techLevelScore)
    alienPlanet.habitation[alienPlanet.alien] = "Homeworld"
    alienPlanet.alien.planets[alienPlanet] = {"outpostRoll": None,
        "colonyRoll": None,
        "desirability": 8,
        "habitation": "Homeworld"}

    if extinct:
        alienPlanet.ruins.add(planet.alien)
    else:
        alienPlanet.settlement = 100

    # Due to how similar on paper the animal would be to the alien,
    # remove the animal from the list of all animals.
    animal.allAnimals.remove(animalToConvert)


def set_tech_level(maxTechLevel):
    """
    Sets the tech level of the alien, limited by the absolute max tech level
    as defined by the user.

    Parameter:
        maxTechLevel: Integer
            The highest possible tech level that any species can achieve
            right now.
    """
    maxTechLevelScore = max([alien.techLevelScore for alien in allAliens])
    divisor = maxTechLevel / 2

    # Complicated equation to figure out a reasonably balanced tech level.
    # Garbage comment, I know, but I don't even remember how I came up with this.
    # Aliens that went extinct get a tech level between 1 and 9.  At 0, there
    # probably wouldn't be any evidence.  At 10, they could colonize other
    # systems and then killing them all off becomes really hard.
    for alien in allAliens:
        if alien.extinct:
            tl = roll_xdy(1, 9)
            alien.maxTechLevel = tl
            alien.currentTechLevel = tl
        else:
            alien.maxTechLevel = int(round((((((alien.techLevelScore / maxTechLevelScore) * maxTechLevel) + (
                (1 - (alien.techLevelScore / maxTechLevelScore)) * 10)) / 2) / divisor) * maxTechLevel, 0))
            alien.currentTechLevel = alien.maxTechLevel - (maxTechLevel - 9)

import alien
import dwarfplanet
import terrestrialplanet
import helianplanet
import jovianplanet
from orbitalbody import OrbitalBody
from globalstuff import LookupTable, roll_xdy, starport


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


def create_planet(star, order, orbitType, roll):
    if roll <= 2:
        dwarfplanet.create_dwarf_planet(star, star, order, orbitType)
    elif roll <= 3:
        terrestrialplanet.create_terrestrial_planet(star, star, order, orbitType)
    elif roll <= 4:
        helianplanet.create_helian_planet(star, star, order, orbitType)
    else:
        jovianplanet.create_jovian_planet(star, star, order, orbitType)


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
        self.terrain = []
        self.animals = []
        self.ringSystem = False
        self.homeAlien = None
        self.terraformingAlien = None
        self.terraformingPoints = 0
        self.terraformingPointsUsed = 0
        self.terraformingDone = False
        self.seedWithLife = False


    # def calculate_desirability(self, alien, nearbyColony):
    #     """
    #     Sets the planet's desirability score, which is used to determine
    #     the extent of colonization. This can be different per Alien.

    #     Required Parameters:
    #         alien: Alien class instance
    #             The alien considering colonization of this planet.
    #         nearbyColony: Boolean
    #             Indicates where there is a colony within one jump
    #             of this planet's system.
    #     """

    #     desirability = self.baseDesirability

    #     # If the distance from the alien home system hasn't been
    #     # calculated yet, calculate it and store it.
    #     if alien not in self.systemHex.distanceFromAlienHomeSystem:
    #         self.systemHex.set_distance_from_homeworld(alien)

    #     modifiedDistance = max([0, int(round(
    #         self.systemHex.distanceFromAlienHomeSystem[alien] / (
    #             (1 if alien.currentTechLevel == 9 else (
    #                 alien.currentTechLevel - 9))),
    #         0)) - (1 if nearbyColony else 0)])

    #     # Distance penalty
    #     if modifiedDistance > 3 + alien.reactionModifier:
    #         desirability -= (modifiedDistance - 3 + alien.reactionModifier)

    #     # Penalty for not having an easy source of fuel in the system
    #     if not any([self.systemHex.fuelUnrefinedAvailable, self.systemHex.fuelRefinedAvailable]):
    #         desirability -= 1

    #     # Penalty for having a flare star in the system
    #     desirability -= self.systemHex.flareStarDesirabilityPenalty

    #     # Lifebelt bonus
    #     if self.orbitType == "Inner Zone":
    #         if self.star.luminosityClass in ["A-V", "F-V", "K-V"]:
    #             desirability += 2
    #         elif self.star.luminosityClass == "M-V":
    #             desirability += 1

    #     # Dry world penalty
    #     if self.hydrosphere in [None, 0]:
    #         desirability -= 1

    #     # Extreme environment penalty
    #     if ((self.size > 12 and self.size != alien.homePlanet.size)
    #         or (self.atmosphere > 11 and self.atmosphere != alien.homePlanet.atmosphere)
    #             or (self.hydrosphere == 15 and alien.homePlanet.hydrosphere != 15)):
    #         desirability -= 2

    #     # High gravity penalty
    #     if self.size >= alien.homePlanet.size + 2 and self.atmosphere <= 15:
    #         desirability -= 1

    #     # Tiny world penalty
    #     if self.size == 0:
    #         desirability -= 1

    #     # Habitable World bonuses
    #     if (self.chemistry == alien.homePlanet.chemistry
    #             and 1 <= self.size <= min(14, alien.homePlanet.size + 3)):
    #         # Garden world
    #         if (max(1, alien.homePlanet.size - 3) <= self.size <= min(15, alien.homePlanet.size + 2)
    #             and (self.atmosphere in acceptableAtmospheres[alien.homePlanet.atmosphere]
    #                 or (self.subsurfaceOceans and alien.animalClass == "Aquatic"))
    #             and max((5 if alien.animalClass == "Aquatic" else 2), alien.homePlanet.hydrosphere - 3) <= self.hydrosphere <= min((11 if alien.animalClass == "Aquatic" else 8), alien.homePlanet.hydrosphere + 3)):
    #             desirability += 5
    #         # Water world
    #         elif (2 <= self.atmosphere <= 9
    #               and 10 <= self.hydrosphere <= 11
    #               and alien.animalClass != "Aquatic"):
    #             desirability += 3
    #         # Poor world
    #         elif (2 <= self.atmosphere <= 6
    #               and (2 if alien.animalClass == "Aquatic" else 0) <= self.hydrosphere <= max((4 if alien.animalClass == "Aquatic" else 3), alien.homePlanet.hydrosphere - 4)):
    #             desirability += 2
    #         # Other
    #         elif (2 <= self.atmosphere <= 9
    #               and (2 if alien.animalClass == "Aquatic" else 0) <= self.hydrosphere <= 11):
    #             desirability += 4
    #     # Not currently habitable, but at least these worlds can be terraformed
    #     elif (2 <= self.size <= 12
    #           and self.orbitType == "Inner Zone"
    #           and self.hydrosphere < 11
    #           and self.atmosphere < 13
    #           and self.category not in ["Acheronian", "Asphodelian", "Stygian"]
    #           and "M-Ve" not in [s.luminosityClass for s in self.systemHex.stars]):
    #         desirability += 1

    #     # Ideal atmosphere bonus
    #     if self.atmosphere == alien.homePlanet.atmosphere:
    #         desirability += 1

    #     self.desirability[alien] = desirability
    #     return desirability

    # def calculate_desirability_jovian_asteroid_belt(self, alien, nearbyColony):
    #     """
    #     Sets the planet's desirability score, which is used to determine
    #     the extent of colonization. This can be different per Alien.
    #     This applies only to Jovians and Asteroid Belts as you don't live
    #     "on" them, but in stations.

    #     Required Parameters:
    #         alien: Alien class instance
    #             The alien considering colonization of this planet.
    #         nearbyColony: Boolean
    #             Indicates where there is a colony within one jump
    #             of this planet's system.
    #     """

    #     desirability = self.baseDesirability

    #     # If the distance from the alien home system hasn't been
    #     # calculated yet, calculate it and store it.
    #     if alien not in self.systemHex.distanceFromAlienHomeSystem:
    #         self.systemHex.set_distance_from_homeworld(alien)

    #     modifiedDistance = int(round(
    #         self.systemHex.distanceFromAlienHomeSystem[alien] / (
    #             (1 if alien.currentTechLevel == 9 else (
    #                 alien.currentTechLevel - 9))),
    #         0)) - (1 if nearbyColony else 0)

    #     # Distance penalty
    #     if modifiedDistance > 3 + alien.reactionModifier:
    #         desirability -= modifiedDistance

    #     # Penalty for not having an easy source of fuel in the system
    #     if not any([self.systemHex.fuelUnrefinedAvailable, self.systemHex.fuelRefinedAvailable]):
    #         desirability -= 1

    #     colonyInSystem = any(p.groupName not in ["Jovian", "Asteroid Belt"] and alien in p.habitation.keys() and p.habitation[alien] in ["Colony", "Homeworld"] for p in self.systemHex.planets)
    #     outpostInSystem = any(p.groupName not in ["Jovian", "Asteroid Belt"] and alien in p.habitation.keys() and p.habitation[alien] == "Outpost" for p in self.systemHex.planets)

    #     if not colonyInSystem and not outpostInSystem:
    #         desirability -= 3
    #     elif not colonyInSystem and outpostInSystem:
    #         desirability -= 1

    #     self.desirability[alien] = desirability
    #     return desirability

    # def calculate_habitation(
    #         self,
    #         alien,
    #         alienSurvivalPercent,
    #         maxTechLevel,
    #         maxReactionModifier,
    #         outpostPossible):
    #     """
    #     Sets the type of Habitation an Alien will have on the planet.
    #     Not applicable for Homeworld because that is set at the time of Alien creation.

    #     Required Parameters:
    #         alien: Alien class instance
    #             The alien considering colonization of this planet.
    #         alienSurvivalPercent: Integer
    #             An integer representing the percent chance of an
    #             alien surviving to Tech Level 10.
    #         maxTechLevel: Integer
    #             The maximum possible Tech Level.
    #         maxReactionModifier: Integer
    #             The maximum Reaction Modifier across all non-extinct
    #             aliens.
    #         outpostPossible: Boolean
    #             Indicates where an Outpost can be created.
    #     """

    #     if self == alien.homePlanet:
    #         if not alien.extinct:
    #             self.systemHex.create_surrounding_systems(alienSurvivalPercent=alienSurvivalPercent, maxTechLevel=maxTechLevel, maxReactionModifier=maxReactionModifier)
    #         self.habitation[alien] = "Homeworld"
    #         alien.planets[self]["habitation"] = "Homeworld"
    #         return

    #     homeSystem = alien.homePlanet.systemHex == self.systemHex
    #     hab = None

    #     if not self.alien or not self.alien.extinct:
    #         if alien.currentTechLevel >= 10 or (alien.currentTechLevel == 9 and homeSystem):
    #             if alien.planets[self]["colonyRoll"] - 2 <= alien.planets[self]["desirability"]:
    #                 hab = "Colony"
    #                 self.systemHex.create_surrounding_systems(alienSurvivalPercent=alienSurvivalPercent, maxTechLevel=maxTechLevel, maxReactionModifier=maxReactionModifier)
    #             elif outpostPossible and alien.planets[self]["outpostRoll"] - (1 if homeSystem else 0) <= alien.currentTechLevel + alien.planets[self]["desirability"] - 10:
    #                 hab = "Outpost"
    #                 self.systemHex.create_surrounding_systems(alienSurvivalPercent=alienSurvivalPercent, maxTechLevel=maxTechLevel, maxReactionModifier=maxReactionModifier)
    #             else:
    #                 hab = None
    #     else:
    #         hab = None

    #     # If an alien is in the process of terraforming and they
    #     # have made the planet temporarily worse, they won't
    #     # abandon it. Otherwise, a lower level of habitation
    #     # causes ruins to be present on the planet.
    #     previousHabitation = self.habitation.get(alien)
    #     if previousHabitation and not hab and self.terraformingAlien == alien:
    #         hab = "Outpost"

    #     return hab

    # def terraform_planet(self, alien):
    #     """
    #     Changes something about the planet to increase desirability over the long run.

    #     Required Parameters:
    #         alien: Alien class instance
    #             The alien doing the terraforming.

    #     Returns True if something was changed, otherwise returns False.
    #     """
        
    #     # If there's no chemistry, nothing has to be changed, it just happens
    #     # as part of terraforming
    #     if not self.chemistry:
    #         self.chemistry = alien.homePlanet.chemistry
    #     # If the chemistry is wrong, reduce Hydrosphere to 1, then convert
    #     elif self.chemistry != alien.homePlanet.chemistry:
    #         if self.hydrosphere > 1:
    #             self.hydrosphere -= 1
    #             return True
    #         else:
    #             self.chemistry = alien.homePlanet.chemistry
    #             return True

    #     # Remove Dry World penalty
    #     if self.hydrosphere == 0:
    #         self.hydrosphere += 1
    #         return True

    #     # Get Atmosphere into the Habitable range.
    #     # If Hydrosphere 2+ and Atmosphere 12-13, reduce Hydrosphere to 1
    #     # then reduce the Atmosphere
    #     if self.atmosphere == 13 and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
    #         self.atmosphere -= 1
    #         return True
    #     elif self.atmosphere == 12 and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
    #         if 2 <= self.hydrosphere <= 10:
    #             self.hydrosphere -= 1
    #             return True
    #         elif self.hydrosphere < 2:
    #             self.atmosphere -= 1
    #             return True
    #     elif self.atmosphere > 9 and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
    #         self.atmosphere -= 1
    #         return True
    #     elif self.atmosphere < 2 and self.atmosphere not in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
    #         self.atmosphere += 1
    #         return True

    #     # At this point, the planet should have one of the Habitable World bonuses
    #     # If it's Poor, improve it to Other by raising Hydrosphere
    #     if self.hydrosphere <= max((4 if alien.animalClass == "Aquatic" else 3), alien.homePlanet.hydrosphere - 4):
    #         self.hydrosphere += 1
    #         return True

    #     # If it's Water World and Hydrosphere 10, reduce Hydrosphere to improve it to Other
    #     # Does not apply to Aquatics
    #     if self.hydrosphere == 10 and alien.animalClass != "Aquatic":
    #         self.hydrosphere -= 1
    #         return True

    #     # If the planet's size would allow it to be a Garden world, work
    #     # towards that
    #     if max(1, alien.homePlanet.size - 3) <= self.size <= min(15, alien.homePlanet.size + 2):
    #         # Lower Hydrosphere if it's too high
    #         if self.hydrosphere > min((11 if alien.animalClass == "Aquatic" else 8), alien.homePlanet.hydrosphere + 3):
    #             self.hydrosphere -= 1
    #             return True
    #         # Raise Hydrosphere if it's too low
    #         if self.hydrosphere < max((5 if alien.animalClass == "Aquatic" else 2), alien.homePlanet.hydrosphere - 3):
    #             self.hydrosphere += 1
    #             return True
    #         # Lower Atmosphere if it's too high
    #         if any([alien.homePlanet.atmosphere == 2 and self.atmosphere > 4,
    #                 alien.homePlanet.atmosphere == 3 and self.atmosphere > 5,
    #                 alien.homePlanet.atmosphere == 4 and self.atmosphere > 7,
    #                 alien.homePlanet.atmosphere == 5 and self.atmosphere > 6,
    #                 alien.homePlanet.atmosphere == 6 and self.atmosphere > 8,
    #                 alien.homePlanet.atmosphere == 7 and self.atmosphere > 9,
    #                 alien.homePlanet.atmosphere == 8 and self.atmosphere > 9,
    #                 alien.homePlanet.atmosphere == 9 and self.atmosphere > 9]):
    #             self.atmosphere -= 1
    #             return True
    #         # Raise Atmosphere if it's too low
    #         if any([alien.homePlanet.atmosphere == 2 and self.atmosphere < 2,
    #                 alien.homePlanet.atmosphere == 3 and self.atmosphere < 3,
    #                 alien.homePlanet.atmosphere == 4 and self.atmosphere < 2,
    #                 alien.homePlanet.atmosphere == 5 and self.atmosphere < 3,
    #                 alien.homePlanet.atmosphere == 6 and self.atmosphere < 5,
    #                 alien.homePlanet.atmosphere == 7 and self.atmosphere < 4]):
    #             self.atmosphere += 1
    #             return True

    #     # Get the Atmosphere to match the homeworld's
    #     if self.atmosphere > alien.homePlanet.atmosphere:
    #         self.atmosphere -= 1
    #         return True
    #     elif self.atmosphere < alien.homePlanet.atmosphere:
    #         self.atmosphere += 1
    #         return True

    #     # If the planet has only microscopic life,
    #     # work to eliminate enough of it so life
    #     # can be imported from elsewhere.
    #     if 2 < self.biosphere < 7:
    #         self.biosphere -= 1
    #         if self.biosphere <= 2:
    #             self.seedWithLife = True
    #         return True

    #     # If nothing was done, the planet has been
    #     # terraformed as much as it can, set a flag
    #     # so we don't run this method for this instance
    #     # anymore.
    #     self.terraformingDone = True
    #     return False
        

    # def planet_terrain(self):
    #     """
    #     Sets the list of terrains found on the planet.
    #     """

    #     terrain = []

    #     if self.hydrosphere <= 8:
    #         terrain.append("Mountains")
    #         terrain.append("Rough/Broken")
    #         terrain.append("Hills")
    #         terrain.append("Clear")

    #     if self.atmosphere >= 2 and (2 <= self.hydrosphere <= 8):
    #         terrain.append("Beach/Shore")

    #     if (self.atmosphere >= 2 and 5 <=
    #             self.hydrosphere <= 11) or self.subsurfaceOceans:
    #         terrain.append("Deep Ocean")

    #     if self.biosphere >= 9 and self.hydrosphere <= 4 and 2 <= self.atmosphere <= 7:
    #         terrain.append("Desert")

    #     if self.biosphere >= 9 and self.atmosphere >= 4 and 3 <= self.hydrosphere <= 8:
    #         terrain.append("Forest")

    #     if self.biosphere >= 9 and self.atmosphere >= 4 and 4 <= self.hydrosphere <= 8:
    #         terrain.append("Jungle")

    #     if (self.atmosphere >= 2 and 3 <=
    #             self.hydrosphere <= 11) or self.subsurfaceOceans:
    #         terrain.append("Open Ocean")

    #     if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 7:
    #         terrain.append("Plains")

    #     if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
    #         terrain.append("Rainforest")

    #     if self.atmosphere >= 2 and 3 <= self.hydrosphere <= 8:
    #         terrain.append("Riverbank")

    #     if (self.atmosphere >= 2 and 2 <= self.hydrosphere <= 10) or (
    #             self.subsurfaceOceans and self.hydrosphere <= 10):
    #         terrain.append("Shallow Ocean")

    #     if self.biosphere >= 9 and self.atmosphere >= 4 and 5 <= self.hydrosphere <= 8:
    #         terrain.append("Swamp/Marsh")

    #     if self.biosphere >= 9 and self.atmosphere >= 2 and 2 <= self.hydrosphere <= 8:
    #         terrain.append("Woods")

    #     self.terrain = terrain
        

    # def planet_animals(self):
    #     """
    #     Adds animals for each terrain.
    #     """

    #     animals = []
    #     for terrain in self.terrain:
    #         if terrain == "Beach/Shore":
    #             for _ in range(3):
    #                 animals.append(animal.Amphibian(planet=self, terrain=terrain))
    #                 animals.append(animal.Aquatic(planet=self, terrain=terrain))
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #         elif terrain == "Clear":
    #             for _ in range(3):
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Mammal(planet=self, terrain=terrain))
    #         elif terrain == "Deep Ocean":
    #             for _ in range(3):
    #                 animals.append(animal.Aquatic(planet=self, terrain=terrain))
    #         elif terrain == "Desert":
    #             for _ in range(3):
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Reptile(planet=self, terrain=terrain))
    #         elif terrain == "Forest":
    #             for _ in range(3):
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Fungal(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Mammal(planet=self, terrain=terrain))
    #         elif terrain == "Hills":
    #             for _ in range(3):
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Mammal(planet=self, terrain=terrain))
    #                 animals.append(animal.Reptile(planet=self, terrain=terrain))
    #         elif terrain == "Jungle":
    #             for _ in range(3):
    #                 animals.append(animal.Amphibian(planet=self, terrain=terrain))
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Fungal(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Reptile(planet=self, terrain=terrain))
    #         elif terrain == "Mountains":
    #             for _ in range(3):
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #         elif terrain == "Open Ocean":
    #             for _ in range(3):
    #                 animals.append(animal.Aquatic(planet=self, terrain=terrain))
    #         elif terrain == "Plains":
    #             for _ in range(3):
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Mammal(planet=self, terrain=terrain))
    #                 animals.append(animal.Reptile(planet=self, terrain=terrain))
    #         elif terrain == "Rainforest":
    #             for _ in range(3):
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Fungal(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Reptile(planet=self, terrain=terrain))
    #         elif terrain == "Riverbank":
    #             for _ in range(3):
    #                 animals.append(animal.Amphibian(planet=self, terrain=terrain))
    #                 animals.append(animal.Aquatic(planet=self, terrain=terrain))
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Mammal(planet=self, terrain=terrain))
    #                 animals.append(animal.Reptile(planet=self, terrain=terrain))
    #         elif terrain == "Rough/Broken":
    #             for _ in range(3):
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Reptile(planet=self, terrain=terrain))
    #         elif terrain == "Shallow Ocean":
    #             for _ in range(3):
    #                 animals.append(animal.Amphibian(planet=self, terrain=terrain))
    #                 animals.append(animal.Aquatic(planet=self, terrain=terrain))
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #         elif terrain == "Swamp/Marsh":
    #             for _ in range(3):
    #                 animals.append(animal.Amphibian(planet=self, terrain=terrain))
    #                 animals.append(animal.Aquatic(planet=self, terrain=terrain))
    #                 animals.append(animal.Avian(planet=self, terrain=terrain))
    #                 animals.append(animal.Fungal(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Reptile(planet=self, terrain=terrain))
    #         elif terrain == "Woods":
    #             for _ in range(3):
    #                 animals.append(animal.Fungal(planet=self, terrain=terrain))
    #                 animals.append(animal.Insect(planet=self, terrain=terrain))
    #                 animals.append(animal.Mammal(planet=self, terrain=terrain))

    #     self.animals = animals


    # def planet_population(self):
    #     """
    #     Sets the alien populations for the planet.
    #     This sets both the relative and actual population.
    #     Actual population modifies the relative population
    #     using the alien's Pack score from its animal base.
    #     Homeworld population has random variations because
    #     the desirability of the homeworld should never
    #     change.
    #     """

    #     previousPopulation = self.population
    #     popNum = 0

    #     for alien in self.habitation:
    #         if not self.habitation[alien]:
    #             self.alienPopulation[alien] = None
    #             continue
        
    #         if alien.extinct:
    #             self.alienPopulation[alien] = {
    #                 "homeworldRoll": None,
    #                 "colonyRoll": None,
    #                 "outpostRoll": None,
    #                 "relative": 0,
    #                 "actual": 0
    #             }
    #             self.alienPopulation[alien]["relative"] = 0
    #             self.alienPopulation[alien]["actual"] = 0
    #             continue

    #         # If the alien has abandonded this planet but previously had a population
    #         # there, remove the population.
    #         if not self.habitation[alien] and (len(self.alienPopulation[alien]["relative"]) > 1 and self.alienPopulation[alien]["relative"][-1] != 0):
    #             self.alienPopulation[alien]["relative"] = 0
    #             self.alienPopulation[alien]["actual"] = 0
    #             continue

    #         if alien not in self.alienPopulation:
    #             self.alienPopulation[alien] = {
    #                 "colonyRoll": roll_xdy(1, 3) - roll_xdy(1, 3),
    #                 "outpostRoll": roll_xdy(1, 3),
    #                 "relative": None,
    #                 "actual": None
    #             }

    #             if self.habitation[alien] == "Homeworld":
    #                 self.alienPopulation[alien]["homeworldRoll"] = roll_xdy(2, 6)

    #         if self.habitation[alien] == "Homeworld":
    #             # This ensures the homeworld population changes a little over time.
    #             homeworldPopRoll = roll_xdy(1, 3) - roll_xdy(1, 3)
    #             if alien.planets[self]["desirability"] + homeworldPopRoll > self.alienPopulation[alien]["homeworldRoll"]:
    #                 basePop = min(12, alien.planets[self]["desirability"] + homeworldPopRoll)
    #             else:
    #                 basePop = self.alienPopulation[alien]["homeworldRoll"]
    #         elif self.habitation[alien] == "Colony":
    #             if alien.currentTechLevel + self.settlement - 9 > alien.planets[self]["desirability"] + self.alienPopulation[alien]["colonyRoll"]:
    #                 basePop = max(4, min(12, alien.planets[self]["desirability"] + self.alienPopulation[alien]["colonyRoll"]))
    #             else:
    #                 basePop = max(4, alien.currentTechLevel + self.settlement - 9)
    #         elif self.habitation[alien] == "Outpost":
    #             basePop = max(1, min(4, alien.planets[self]["desirability"] + self.alienPopulation[alien]["outpostRoll"]))

    #         # This is the first digit of the population number.
    #         popString = str(roll_xdy(1, 9))

    #         # This generates the rest of the population numbers (can use 0 here).
    #         # Industry can affect population, see planet_industry_effects.
    #         for _ in range(basePop + self.industryPopulationEffect + 1):
    #             popString += str(roll_xdy(1, 10) - 1)

    #         self.alienPopulation[alien]["relative"] = int(popString)
    #         self.alienPopulation[alien]["actual"] = int(int(popString) * alien.populationModifier)
    #         alien.planets[self]["population"] = self.alienPopulation[alien]["actual"]

    #     # Sum up the population numbers so we can get a score and actual
    #     # population number for the planet as a whole.
    #     if self.alienPopulation:
    #         populationNumbers = []
    #         populationRelative = []
    #         for a in self.alienPopulation:
    #             if self.alienPopulation[a]:
    #                 populationNumbers.append(self.alienPopulation[a]["actual"])
    #                 populationRelative.append(self.alienPopulation[a]["relative"])
                
    #         self.populationNumber = sum(populationNumbers)
            
    #         if self.populationNumber == 0:
    #             self.population = 0
    #         else:
    #             self.population = len(str(sum(populationRelative))) - 1


    # def planet_government(self):
    #     """
    #     Sets the planet's government.
    #     """

    #     previousGovernment = self.government

    #     # The roll is only made once so it doesn't radically change constantly.
    #     if not self.governmentRoll:
    #         self.governmentRoll = roll_xdy(2, 6) - 7

    #     if "Homeworld" in self.habitation.values():
    #         if self.terraformingAlien.currentTechLevel == 0:
    #             self.government = 0
    #         elif roll_xdy(1, 6) <= self.terraformingAlien.currentTechLevel - 9:
    #             self.government = 7
    #         else:
    #             self.government = max(0, self.population + self.governmentRoll)
    #     elif "Colony" in self.habitation.values():
    #         self.government = max(0, self.population + self.governmentRoll)
    #     elif "Outpost" in self.habitation.values():
    #         if self.population == 0:
    #             self.government = 0
    #         else: self.government = min(6, max(0, self.population + self.governmentRoll))
    #     else:
    #         self.government = 0


    # def planet_law_level(self):
    #     """
    #     Sets the planet's law level.
    #     """

    #     previousLawLevel = self.lawLevel

    #     # The roll is only made once so it doesn't radically change constantly.
    #     if not self.lawLevelRoll:
    #         self.lawLevelRoll = roll_xdy(2, 6) - 7

    #     if self.government == 0:
    #         self.lawLevel = 0
    #     else:
    #         self.lawLevel = max(0, self.government + self.lawLevelRoll)


    # def planet_industry(self):
    #     """
    #     Sets the planet's industry.
    #     """

    #     previousIndustry = self.industry

    #     # The roll is only made once so it doesn't radically change constantly.
    #     if not self.industryRoll:
    #         self.industryRoll = roll_xdy(2, 6) - 7

    #     if self.population == 0:
    #         self.industry = 0
    #     else:
    #         industry = self.population + self.industryRoll
            
    #         if 1 <= self.lawLevel <= 3:
    #             industry += 1
    #         elif 6 <= self.lawLevel <= 9:
    #             industry -= 1
    #         elif 10 <= self.lawLevel <= 13:
    #             industry -= 2
    #         elif self.lawLevel >= 14:
    #             industry -= 3

    #         if 12 <= self.terraformingAlien.currentTechLevel <= 14:
    #             industry += 1
    #         elif self.terraformingAlien.currentTechLevel >= 15:
    #             industry += 2

    #         if self.hydrosphere == 15 or self.atmosphere not in acceptableAtmospheres[self.terraformingAlien.homePlanet.atmosphere]:
    #             industry += 1

    #         self.industry = max(0, industry)

    #         # Determine if a new industrial effect needs to be applied.
    #         if not previousIndustry:
    #             previousIndustry = -1
                
    #         if (self.industry == 0
    #             or (1 <= self.industry <= 3 and (previousIndustry < 1 or previousIndustry > 3))
    #             or (4 <= self.industry <= 9 and (previousIndustry < 4 or previousIndustry > 9))
    #             or (self.industry >= 10 and previousIndustry < 10)):
    #             return True
            
    #     return False


    # def planet_industry_effects(self):
    #     """
    #     Modifies the planet's population based on Industry
    #     and also sets whether the planet has industrial pollution.
    #     """

    #     roll = roll_xdy(1, 2)
        
    #     if self.industry == 0:
    #         self.industryPopulationEffect = -1
    #         self.pollution = False
    #     elif 1 <= self.industry <= 3:
    #         self.industryPopulationEffect = 0
    #         self.pollution = False
    #     elif 4 <= self.industry <= 9:
    #         self.industryPopulationEffect = 1
    #         self.pollution = True
    #     elif self.industry >= 10 and roll == 1:
    #         self.industryPopulationEffect = 1
    #         self.pollution = False
    #     elif self.industry >= 10 and roll == 2:
    #         self.industryPopulationEffect = 2
    #         self.pollution = True


    # def planet_trade_codes(self, maxTechLevel):
    #     """
    #     Sets the planet's trade codes.

    #     Required Parameters:
    #         maxTechLevel: Integer
    #             The maximum possible Tech Level.
    #     """

    #     if (4 <= self.atmosphere <= 9
    #             and 4 <= self.hydrosphere <= 8
    #             and 5 <= self.population <= 7):
    #         if "Ag" not in self.tradeCodes:
    #             self.tradeCodes.add("Ag")
    #     else:
    #         if "Ag" in self.tradeCodes:
    #             self.tradeCodes.discard("Ag")
        
    #     if self.category == "Asteroid Belt":
    #         if "As" not in self.tradeCodes:
    #             self.tradeCodes.add("As")
    #     else:
    #         if "As" in self.tradeCodes:
    #             self.tradeCodes.discard("As")
        
    #     if (2 <= self.atmosphere <= 13
    #             and self.hydrosphere == 0):
    #         if "De" not in self.tradeCodes:
    #             self.tradeCodes.add("De")
    #     else:
    #         if "De" in self.tradeCodes:
    #             self.tradeCodes.discard("De")
        
    #     if ((self.atmosphere >= 10
    #                 or self.chemistry != "Water")
    #             and 1 <= self.hydrosphere <= 11):
    #         if "Fl" not in self.tradeCodes:
    #             self.tradeCodes.add("Fl")
    #     else:
    #         if "Fl" in self.tradeCodes:
    #             self.tradeCodes.discard("Fl")
        
    #     if (max(1, self.terraformingAlien.homePlanet.size - 3) <= self.size <= min(15, self.terraformingAlien.homePlanet.size + 2)
    #             and self.atmosphere in acceptableAtmospheres[self.terraformingAlien.homePlanet.atmosphere]
    #             and max((5 if self.terraformingAlien.animalClass == "Aquatic" else 2), self.terraformingAlien.homePlanet.hydrosphere - 3) <= self.hydrosphere <= min((11 if self.terraformingAlien.animalClass == "Aquatic" else 8), self.terraformingAlien.homePlanet.hydrosphere + 3)):
    #         if "Ga" not in self.tradeCodes:
    #             self.tradeCodes.add("Ga")
    #     else:
    #         if "Ga" in self.tradeCodes:
    #             self.tradeCodes.discard("Ga")
        
    #     if self.population >= 9:
    #         if "Hi" not in self.tradeCodes:
    #             self.tradeCodes.add("Hi")
    #     else:
    #         if "Hi" in self.tradeCodes:
    #             self.tradeCodes.discard("Hi")
        
    #     if self.industry >= maxTechLevel - 3:
    #         if "Ht" not in self.tradeCodes:
    #             self.tradeCodes.add("Ht")
    #     else:
    #         if "Ht" in self.tradeCodes:
    #             self.tradeCodes.discard("Ht")
        
    #     if (self.atmosphere <= 1
    #             and self.hydrosphere >= 1):
    #         if "Ic" not in self.tradeCodes:
    #             self.tradeCodes.add("Ic")
    #     else:
    #         if "Ic" in self.tradeCodes:
    #             self.tradeCodes.discard("Ic")
        
    #     if (self.population >= 9
    #             and self.industry >= 6):
    #         if "In" not in self.tradeCodes:
    #             self.tradeCodes.add("In")
    #     else:
    #         if "In" in self.tradeCodes:
    #             self.tradeCodes.discard("In")
        
    #     if 1 <= self.population <= 3:
    #         if "Lo" not in self.tradeCodes:
    #             self.tradeCodes.add("Lo")
    #     else:
    #         if "Lo" in self.tradeCodes:
    #             self.tradeCodes.discard("Lo")
        
    #     if self.industry <= 5:
    #         if "Lt" not in self.tradeCodes:
    #             self.tradeCodes.add("Lt")
    #     else:
    #         if "Lt" in self.tradeCodes:
    #             self.tradeCodes.discard("Lt")
        
    #     if ((self.atmosphere <= 3
    #                 or self.atmosphere >= 11)
    #             and (self.hydrosphere <= 3
    #                 or self.hydrosphere >= 11)
    #             and self.population >= 6):
    #         if "Na" not in self.tradeCodes:
    #             self.tradeCodes.add("Na")
    #     else:
    #         if "Na" in self.tradeCodes:
    #             self.tradeCodes.discard("Na")
        
    #     if 4 <= self.population <= 6:
    #         if "Ni" not in self.tradeCodes:
    #             self.tradeCodes.add("Ni")
    #     else:
    #         if "Ni" in self.tradeCodes:
    #             self.tradeCodes.discard("Ni")
        
    #     if (2 <= self.atmosphere <= 5
    #             and self.hydrosphere <= 3):
    #         if "Po" not in self.tradeCodes:
    #             self.tradeCodes.add("Po")
    #     else:
    #         if "Po" in self.tradeCodes:
    #             self.tradeCodes.discard("Po")
        
    #     if (6 <= self.population <= 8
    #             and self.atmosphere in idealAtmospheres[self.terraformingAlien.homePlanet.atmosphere]):
    #         if "Ri" not in self.tradeCodes:
    #             self.tradeCodes.add("Ri")
    #     else:
    #         if "Ri" in self.tradeCodes:
    #             self.tradeCodes.discard("Ri")
        
    #     if self.biosphere == 0:
    #         if "St" not in self.tradeCodes:
    #             self.tradeCodes.add("St")
    #     else:
    #         if "St" in self.tradeCodes:
    #             self.tradeCodes.discard("St")
        
    #     if (self.atmosphere >= 2
    #             and 10 <= self.hydrosphere <= 11):
    #         if "Wa" not in self.tradeCodes:
    #             self.tradeCodes.add("Wa")
    #     else:
    #         if "Wa" in self.tradeCodes:
    #             self.tradeCodes.discard("Wa")
        
    #     if self.atmosphere == 0:
    #         if "Va" not in self.tradeCodes:
    #             self.tradeCodes.add("Va")
    #     else:
    #         if "Va" in self.tradeCodes:
    #             self.tradeCodes.discard("Va")
        
    #     if self.biosphere >= 7:
    #         if "Zo" not in self.tradeCodes:
    #             self.tradeCodes.add("Zo")
    #     else:
    #         if "Zo" in self.tradeCodes:
    #             self.tradeCodes.discard("Zo")


    # def planet_starport(self):
    #     """
    #     Sets the planet's starport.
    #     """

    #     previousStarport = self.starport

    #     # The roll is only made once so it doesn't radically change constantly.
    #     if not self.starportRoll:
    #         self.starportRoll = roll_xdy(2, 6) - 7

    #     score = self.starportRoll + self.industry
    #     if "Ag" in self.tradeCodes:
    #         score += 1
    #     if "Ga" in self.tradeCodes:
    #         score += 1
    #     if "Hi" in self.tradeCodes:
    #         score += 1
    #     if "Ht" in self.tradeCodes:
    #         score += 1
    #     if "In" in self.tradeCodes:
    #         score += 1
    #     if "Na" in self.tradeCodes:
    #         score += 1
    #     if "Ri" in self.tradeCodes:
    #         score += 1
    #     if self.terraformingAlien.currentTechLevel >= 12:
    #         score += 1
    #     if self.terraformingAlien.currentTechLevel >= 15:
    #         score += 1
    #     if "Po" in self.tradeCodes:
    #         score -= 1
    #     if self.terraformingAlien.currentTechLevel <= 9:
    #         score -= 1

    #     # An Outpost world with Population 0 automatically has the equivalent of an E-class starport,
    #     # in the form of an unmanned navigation beacon and emergency supply cache.
    #     # Any world with Industry 5+ must have at least the equivalent of an E-class starport,
    #     # in its airstrips or surface shipping ports.
    #     # Any uninhabitable world with Population 1+ must have at least the equivalent of an E-class starport,
    #     # in its airlocks and docking ports.
    #     if (score < 3
    #             and ("Outpost" in self.habitation.values()
    #                 or self.industry >= 5
    #                 or self.atmosphere not in acceptableAtmospheres[self.terraformingAlien.homePlanet.atmosphere])):
    #         score = 3

    #     self.starport = starportTable[score]

    #     if self.starport in ["D", "C"]:
    #         self.star.systemHex.fuelUnrefinedAvailable = True

    #     if self.starport in ["B", "A"]:
    #         self.star.systemHex.fuelRefinedAvailable = True

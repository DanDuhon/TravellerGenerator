import itertools

import star
import planet
import namegenerator
import alien
from diceroller import roll_xdy
from lookuptable import LookupTable

allSystems = []
allCoordinates = {}

numberOfStarsTable = LookupTable((10, 1), (15, 2), (21, 3))


class System():
    """
    Defines a system hex. Each hex has a horizontal and vertical coordinate
    that is visible to the user. It also has a cube coordinate, which is
    used for determining distance between hexes. Each system can generate
    an automatic brown dwarf star, a primary star, or both. A system can
    contain up to 4 stars, but the stars (named "companion stars") that are
    neither the primary star nor the automatic brown dwarf star will be
    generated inside the Star class.

    Required parameters:
        horizontalCoord: Integer
            The horizontal coordinate in the hex grid.
        verticalCoord: Integer
            The vertical coordinate in the hex grid.
        openClusterBonus: Integer
            A 0 or +3 bonus to the number of stars calculation. Open Clusters
            are vast areas with large amount of gasses that results in more
            stars.
        alienSurvivalPercent: Integer
            Represents a percentage. This gets passed along through to the
            planets and then aliens to determine how likely it is that the
            alien species has gone extinct.
        maxTechLevel: Integer
            Indicate the maximum tech level of intelligent species.  This gets
            passed along through the planet to the alien module to determine
            the tech level of each species.
    """

    def __init__(
            self,
            horizontalCoord,
            verticalCoord,
            openClusterBonus,
            alienSurvivalPercent,
            maxTechLevel):
        allSystems.append(self)
        self.horizontalCoord = horizontalCoord
        self.verticalCoord = verticalCoord
        self.cubeCoord = (self.horizontalCoord * -1) - self.verticalCoord
        self.coordinates = (self.horizontalCoord,
                            self.verticalCoord,
                            self.cubeCoord)
        allCoordinates[(self.horizontalCoord,
                        self.verticalCoord,
                        self.cubeCoord)] = self
        self.age = roll_xdy(3, 6) - 3
        self.name = namegenerator.astralNGrams.generate_name()
        self.distanceFromAlienHomeSystem = {}
        self.fuelAvailable = False

        if roll_xdy(1, 2) == 1:
            self.numberOfStars = numberOfStarsTable[roll_xdy(3, 6) + openClusterBonus]
        else:
            self.numberOfStars = 0

        if roll_xdy(1, 2) == 1:
            self.brownDwarf = True
        else:
            self.brownDwarf = False

        self.stars = []
        # Only the primary star and automatic brown dwarf are created at this level.
        # Companion stars to the primary star will be created from within the
        # Star class.
        if self.numberOfStars > 0:
            self.stars.append(star.Star(
                systemHex=self,
                systemName=self.name,
                systemAge=self.age,
                starNumber=1,
                alienSurvivalPercent=alienSurvivalPercent,
                maxTechLevel=maxTechLevel,
                primary=True,
                numberOfStars=self.numberOfStars))
            self.stars.extend(self.stars[0].companions)
        if self.brownDwarf:
            self.numberOfStars += 1
            self.stars.append(star.Star(
                systemHex=self,
                systemName=self.name,
                systemAge=self.age,
                starNumber=self.numberOfStars,
                alienSurvivalPercent=alienSurvivalPercent,
                maxTechLevel=maxTechLevel,
                autoBrownDwarf=self.brownDwarf,
                primaryOrbit="Distant"))

        self.flareStarDesirabilityPenalty = 0
        for s in self.stars:
            if s.luminosityClass == "M-Ve":
                self.flareStarDesirabilityPenalty = roll_xdy(1, 3)
                break

        self.planets = []
        self.animals = []
        self.homeSystemOfAliens = []
        for starInstance in self.stars:
            self.planets.extend(starInstance.planets)

            for planetInstance in starInstance.planets:
                self.animals.extend(planetInstance.animals)
                if planetInstance.alien is not None:
                    self.homeSystemOfAliens.append(planetInstance.alien)

        for p in self.planets:
            if isinstance(p, planet.JovianPlanet) or p.chemistry == "Water":
                self.fuelAvailable = True
                break

        for a in alien.allAliens:
            self.distanceFromAlienHomeSystem[a] = distance_between_systems(self, a.homePlanet.systemHex)
        self.systemsAtRange = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        for k in self.systemsAtRange:
            for x in range(-k, k + 1):
                for y in range(max(-k, -x - k), min(k, -x + k) + 1):
                    self.systemsAtRange[k].append((self.horizontalCoord + x, self.verticalCoord + y))

    def create_surrounding_systems(
            self,
            openClusterTuple,
            alienSurvivalPercent,
            maxTechLevel,
            maxReactionModifier):
        hexRange = (3 + maxReactionModifier) * (maxTechLevel - 9)
        for x in range(-hexRange, hexRange + 1):
            for y in range(max(-hexRange, -x - hexRange), min(hexRange, -x + hexRange) + 1):
                if (self.horizontalCoord + x, self.verticalCoord + y, ((self.horizontalCoord + x) * -1) - (self.verticalCoord + y)) not in allCoordinates:
                    h = self.horizontalCoord + x
                    v = self.verticalCoord + y
                    openClusterBonus = 0
                    if openClusterTuple[0] and h >= openClusterTuple[2] and openClusterTuple[1] and v >= openClusterTuple[2]:
                        openClusterBonus = 3
                    elif not openClusterTuple[0] and h <= openClusterTuple[2] and not openClusterTuple[1] and v <= openClusterTuple[2]:
                        openClusterBonus = 3
                    System(
                        self.horizontalCoord + x,
                        self.verticalCoord + y,
                        openClusterBonus,
                        alienSurvivalPercent,
                        maxTechLevel)


def distance_between_systems(system1, system2):
    """
    Calculates the distance between two Systems.  This is the absolute
    shortest route, not necessarily the route that is traversable by
    spaceships.

    Parameters:
        system1: System class instance
            One system to get the distance between.
        system2: System class instance
            The other system to get the distance between.
    """
    return int((abs(system1.horizontalCoord - system2.horizontalCoord)
                + abs(system1.verticalCoord - system2.verticalCoord)
                + abs(system1.cubeCoord - system2.cubeCoord)) / 2)

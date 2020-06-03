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


def create_normal_system(
        horizontalCoord,
        verticalCoord,
        alienSurvivalPercent,
        maxTechLevel):
    """
    Creates a system in a hex that is not in an Open Cluster.

    Parameters:
        horizontalCoord: Integer
            The horizontal or x-axis coordinate of the new system.
        verticalCoord: Integer
            The vertical or y-axis coordinate of the new system.
        alienSurvivalPercent: Integer
            An integer that represents the percent chance that
            an intelligent species will survive to Tech Level 10.
        maxTechLevel: Integer
            An integer representing the maximum achievable Tech Level
            by an intelligence species.
    """
    System(
        horizontalCoord=horizontalCoord,
        verticalCoord=verticalCoord,
        openCluster=False,
        alienSurvivalPercent=alienSurvivalPercent,
        maxTechLevel=maxTechLevel)


def create_cluster_system(
        horizontalCoord,
        verticalCoord,
        alienSurvivalPercent,
        maxTechLevel):
    """
    Creates a system in a hex that is in an Open Cluster, meaning
    there will be more stars per system on average.

    Parameters:
        horizontalCoord: Integer
            The horizontal or x-axis coordinate of the new system.
        verticalCoord: Integer
            The vertical or y-axis coordinate of the new system.
        alienSurvivalPercent: Integer
            An integer that represents the percent chance that
            an intelligent species will survive to Tech Level 10.
        maxTechLevel: Integer
            An integer representing the maximum achievable Tech Level
            by an intelligence species.
    """
    System(
        horizontalCoord=horizontalCoord,
        verticalCoord=verticalCoord,
        openCluster=True,
        alienSurvivalPercent=alienSurvivalPercent,
        maxTechLevel=maxTechLevel)


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
    return int((abs(system1.coordinates[0] - system2.coordinates[0])
                + abs(system1.coordinates[1] - system2.coordinates[1])
                + abs(system1.coordinates[2] - system2.coordinates[2])) / 2)


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
        openCluster: Boolean
            Indicates a bonus to the number of stars calculation. Open Clusters
            contain a large amount of gasses that results in more stars.
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
            openCluster,
            alienSurvivalPercent,
            maxTechLevel):
        allSystems.append(self)
        self.coordinates = (horizontalCoord,
                            verticalCoord,
                            -horizontalCoord - verticalCoord)
        allCoordinates[self.coordinates] = self
        self.age = roll_xdy(3, 6) - 3
        self.name = namegenerator.astralNGrams.generate_name()
        self.distanceFromAlienHomeSystem = {}
        self.alienNearbyColony = {}
        self.fuelAvailable = False

        if roll_xdy(3, 6) == 18:
            openCluster = True
            createOpenClusterSystems = True
        else:
            openCluster = False
            createOpenClusterSystems = False

        if roll_xdy(1, 6) + (2 if openCluster else 0) > 3:
            self.numberOfStars = numberOfStarsTable[roll_xdy(3, 6) + (3 if openCluster else 0)]
        else:
            self.numberOfStars = 0

        if roll_xdy(1, 2) == 1:
            self.brownDwarf = True
        else:
            self.brownDwarf = False

        self.stars = []
        self.planets = []
        
        # Only the primary star and automatic brown dwarf are created at this level.
        # Companion stars to the primary star will be created from within the
        # Star class.
        if self.numberOfStars > 0:
            star.create_primary_star(
                systemHex=self,
                alienSurvivalPercent=alienSurvivalPercent,
                maxTechLevel=maxTechLevel)

        if self.numberOfStars > 1:
            for x in range(self.numberOfStars - 1):
                star.create_companion_star(
                    systemHex=self,
                    alienSurvivalPercent=alienSurvivalPercent,
                    maxTechLevel=maxTechLevel,
                    primaryOrbit=self.stars[0].companionOrbits[x],
                    primarySpectralTypeRoll=self.stars[0].spectralTypeRoll)
                
        if self.brownDwarf:
            self.numberOfStars += 1
            star.create_brown_dwarf_star(
                systemHex=self,
                alienSurvivalPercent=alienSurvivalPercent,
                maxTechLevel=maxTechLevel)
                
        self.flareStarDesirabilityPenalty = 0
        for s in self.stars:
            if s.luminosityClass == "M-Ve":
                self.flareStarDesirabilityPenalty = roll_xdy(1, 3)
                break

        for a in [a for a in alien.allAliens if not a.extinct]:
            self.distanceFromAlienHomeSystem[a] = distance_between_systems(self, a.homePlanet.systemHex)
        self.systemsAtRange = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        for k in self.systemsAtRange:
            for x in range(-k, k + 1):
                for y in range(max(-k, -x - k), min(k, -x + k) + 1):
                    self.systemsAtRange[k].append((self.coordinates[0] + x, self.coordinates[1] + y))

        if createOpenClusterSystems:
            hexRange = roll_xdy(2, 6)
            for x in range(-hexRange, hexRange + 1):
                for y in range(max(-hexRange, -x - hexRange), min(hexRange, -x + hexRange) + 1):
                    h = self.coordinates[0] + x
                    v = self.coordinates[1] + y
                    c = -h - v
                    if (h, v, c) not in allCoordinates:
                        create_cluster_system(
                            horizontalCoord=self.coordinates[0] + x,
                            verticalCoord=self.coordinates[1] + y,
                            alienSurvivalPercent=alienSurvivalPercent,
                            maxTechLevel=maxTechLevel)


    def create_surrounding_systems(
            self,
            alienSurvivalPercent,
            maxTechLevel,
            maxReactionModifier):
        hexRange = (3 + maxReactionModifier) * (maxTechLevel - 9)
        for x in range(-hexRange, hexRange + 1):
            for y in range(max(-hexRange, -x - hexRange), min(hexRange, -x + hexRange) + 1):
                h = self.coordinates[0] + x
                v = self.coordinates[1] + y
                c = -h - v
                if (h, v, c) not in allCoordinates:
                    create_normal_system(
                        horizontalCoord=self.coordinates[0] + x,
                        verticalCoord=self.coordinates[1] + y,
                        alienSurvivalPercent=alienSurvivalPercent,
                        maxTechLevel=maxTechLevel)


    def set_nearby_colony_systems(self, alien):
        hexRange = alien.currentTechLevel - 9
        for coords in self.systemsAtRange[hexRange]:
            allCoordinates[(coords[0], coords[1], -coords[0] - coords[1])].alienNearbyColony[alien] = True

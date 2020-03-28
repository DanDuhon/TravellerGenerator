import star
import namegenerator
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
    def __init__ (self, horizontalCoord, verticalCoord, openClusterBonus, alienSurvivalPercent, maxTechLevel):
        allSystems.append(self)
        self.horizontalCoord = horizontalCoord
        self.verticalCoord = verticalCoord
        self.cubeCoord = (self.horizontalCoord * -1) - self.verticalCoord
        allCoordinates[(self.horizontalCoord, self.verticalCoord, self.cubeCoord)] = self
        self.age = sum(roll_xdy(3, 6)) - 3
        self.name = namegenerator.alienNGrams.generate_name()

        #This lists the system coordinates that are x hexes distant from this system,
        #where x is the dictionary key. Coordinates will be listed even if there is
        #no System for those coordinates.
        self.systemsAtRange = { 0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] }
        for k in self.systemsAtRange.keys():
            for x in range(-k, k + 1):
                for y in range(max(-k, -x - k), min(k, -x + k) + 1):
                    x += self.horizontalCoord
                    y += self.verticalCoord
                    z = -x - y
                    if (abs(self.horizontalCoord - x)
                        + abs(self.verticalCoord - y)
                        + abs(self.cubeCoord - z)) / 2 == k:
                        self.systemsAtRange[k].append((x, y, z))
        
        if sum(roll_xdy(1, 2)) == 1:
            self.numberOfStars = numberOfStarsTable[sum(roll_xdy(3, 6)) + openClusterBonus]
        else:
            self.numberOfStars = 0
        
        if sum(roll_xdy(1, 2)) == 1:
            self.brownDwarf = True
        else:
            self.brownDwarf = False
            
        self.stars = []
        #Only the primary star and automatic brown dwarf are created at this level.
        #Companion stars to the primary star will be created from within the Star class.
        if self.numberOfStars > 0:
            self.stars.append(star.Star(
                systemHex = self,
                systemName = self.name,
                systemAge = self.age,
                starNumber = 1,
                alienSurvivalPercent = alienSurvivalPercent,
                maxTechLevel = maxTechLevel,
                primary = True,
                numberOfStars = self.numberOfStars))
            self.stars.extend(self.stars[0].companions)
        if self.brownDwarf:
            self.numberOfStars += 1
            self.stars.append(star.Star(
                systemHex = self,
                systemName = self.name,
                systemAge = self.age,
                starNumber = self.numberOfStars,
                alienSurvivalPercent = alienSurvivalPercent,
                maxTechLevel = maxTechLevel,
                autoBrownDwarf = self.brownDwarf,
                primaryOrbit = "Distant"))

        self.planets = []
        self.animals = []
        self.homeSystemOfAliens = []
        for starInstance in self.stars:
            self.planets.extend(starInstance.planets)

            for planetInstance in starInstance.planets:
                self.animals.extend(planetInstance.animals)
                if planetInstance.alien is not None:
                    self.homeSystemOfAliens.append(planetInstance.alien)

def distance_between_systems (system1, system2):
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

import star
import namegenerator
from diceroller import roll_xdy
from lookuptable import LookupTable


allSystems = []
allCoordinates = {}
numberOfStarsTable = LookupTable((10, 1), (15, 2), (21, 3))


def create_normal_system(
        horizontalCoord,
        verticalCoord,
        alienSurvivalPercent):
    """
    Creates a system in a hex that is not in an Open Cluster.

    Required Parameters:
        horizontalCoord: Integer
            The horizontal or x-axis coordinate of the new system.
        verticalCoord: Integer
            The vertical or y-axis coordinate of the new system.
        alienSurvivalPercent: Integer
            An integer that represents the percent chance that
            an intelligent species will survive to Tech Level 10.
    """

    system = System(
        horizontalCoord=horizontalCoord,
        verticalCoord=verticalCoord,
        openCluster=False)

    system.create_new_open_cluster(alienSurvivalPercent=alienSurvivalPercent)
    system.numberOfStars = system.set_number_of_stars()
    system.create_primary_star_in_system(alienSurvivalPercent)
    system.create_companion_stars_in_system(alienSurvivalPercent)
    system.create_automatic_brown_dwarf(alienSurvivalPercent)
    system.flareStarDesirabilityPenalty = system.flare_star_desirability_penalty()


def create_cluster_system(
        horizontalCoord,
        verticalCoord,
        alienSurvivalPercent):
    """
    Creates a system in a hex that is in an Open Cluster, meaning
    there will be more stars per system on average.

    Required Parameters:
        horizontalCoord: Integer
            The horizontal or x-axis coordinate of the new system.
        verticalCoord: Integer
            The vertical or y-axis coordinate of the new system.
        alienSurvivalPercent: Integer
            An integer that represents the percent chance that
            an intelligent species will survive to Tech Level 10.
    """

    system = System(
        horizontalCoord=horizontalCoord,
        verticalCoord=verticalCoord,
        openCluster=True)

    system.create_new_open_cluster(alienSurvivalPercent=alienSurvivalPercent)
    system.numberOfStars = system.set_number_of_stars()
    system.create_primary_star_in_system(alienSurvivalPercent)
    system.create_companion_stars_in_system(alienSurvivalPercent)
    system.create_automatic_brown_dwarf(alienSurvivalPercent)
    system.flareStarDesirabilityPenalty = system.flare_star_desirability_penalty()


def distance_between_systems(system1, system2):
    """
    Calculates the distance between two Systems.  This is the absolute
    shortest route, not necessarily the route that is traversable by
    spaceships.

    Required Parameters:
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
    """

    def __init__(
            self,
            horizontalCoord,
            verticalCoord,
            openCluster):
        allSystems.append(self)
        self.coordinates = (horizontalCoord,
                            verticalCoord,
                            -horizontalCoord - verticalCoord)
        allCoordinates[self.coordinates] = self
        self.openCluster = openCluster
        self.age = roll_xdy(3, 6) - 3
        self.numberOfStars = 0
        self.name = namegenerator.astralNGrams.generate_name()
        self.distanceFromAlienHomeSystem = {}
        self.alienNearbyColony = {}
        self.fuelUnrefinedAvailable = False
        self.fuelRefinedAvailable = False
        self.stars = []
        self.planets = []
        self.flareStarDesirabilityPenalty = 0
        self.systemsAtRange = {
            0: [self],
            1: self.set_systems_at_range(1),
            2: self.set_systems_at_range(2),
            3: self.set_systems_at_range(3),
            4: self.set_systems_at_range(4),
            5: self.set_systems_at_range(5),
            6: self.set_systems_at_range(6)
            }
        self.brownDwarf = roll_xdy(1, 2) == 1


    def set_number_of_stars(self):
        """
        Sets the number of (non-automatic brown dwarf) stars in this system.
        """

        autoBrownDwarf = (1 if self.brownDwarf else 0)

        if roll_xdy(1, 6) + (2 if self.openCluster else 0) < 4:
            return 0 + autoBrownDwarf

        return numberOfStarsTable[roll_xdy(3, 6) + (3 if self.openCluster else 0)] + autoBrownDwarf


    def create_new_open_cluster(self, alienSurvivalPercent, maxTechLevel):
        """
        Determine whether this is a new open cluster or not. If yes,
        create surrounding systems as cluster systems rather than normal
        ones.

        Required Parameters:
            alienSurvivalPercent: Integer
                An integer that represents the percent chance that
                an intelligent species will survive to Tech Level 10.
            maxTechLevel: Integer
                An integer representing the maximum achievable Tech Level
                by an intelligence species.
        """
        
        if roll_xdy(3, 6) < 18:
            return

        self.openCluster = True

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


    def set_systems_at_range(self, spacesAway):
        """
        Creates a dictionary of systems that are 0-6 spaces away.
        These values will be reused enough that it's more efficient to
        have this dictionary than calculate it on the fly every time.
        Note that these coordinates are calculated even if the system
        doesn't exist at the time it's run.

        Required Parameters:
            spacesAway: Integer
                The number of spaces away to list systems
                in the dictionary.
        """

        systemsAtRange = []

        for x in range(-spacesAway, spacesAway + 1):
            for y in range(max(-spacesAway, -x - spacesAway), min(spacesAway, -x + spacesAway) + 1):
                systemsAtRange.append((self.coordinates[0] + x, self.coordinates[1] + y))

        return systemsAtRange


    def set_distance_from_homeworld(self, alien):
        """
        Sets the distance of this system to each alien's home system.
        This distiance is used in desirability calculations for colonization.

        Required Parameters:
            alien: Alien class instance
                The alien to calculate distance for.
        """
        
        return distance_between_systems(self, alien.homePlanet.systemHex)


    def create_primary_star_in_system(self, alienSurvivalPercent):
        """
        Creates the primary star in this system, if there is one.

        Required Parameters:
            alienSurvivalPercent: Integer
                An integer that represents the percent chance that
                an intelligent species will survive to Tech Level 10.
        """
        
        if self.numberOfStars > 0 - (1 if self.brownDwarf else 0):
            star.create_primary_star(
                systemHex=self,
                alienSurvivalPercent=alienSurvivalPercent)


    def create_companion_stars_in_system(self, alienSurvivalPercent):
        """
        Creates the companion stars in this system, if there are any.

        Required Parameters:
            alienSurvivalPercent: Integer
                An integer that represents the percent chance that
                an intelligent species will survive to Tech Level 10.
        """
        
        for x in range(self.numberOfStars - 1 - (1 if self.brownDwarf else 0)):
            star.create_companion_star(
                systemHex=self,
                primaryOrbit=self.stars[0].companionOrbits[x],
                alienSurvivalPercent=alienSurvivalPercent)


    def create_automatic_brown_dwarf(self, alienSurvivalPercent):
        """
        Create an automatic brown dwarf.
        This is not considered a companion star, but is "somewhere"
        in the system.

        Required Parameters:
            alienSurvivalPercent: Integer
                An integer that represents the percent chance that
                an intelligent species will survive to Tech Level 10.
        """
        
        if self.brownDwarf:
            star.create_brown_dwarf_star(
                    systemHex=self,
                    alienSurvivalPercent=alienSurvivalPercent)


    def flare_star_desirability_penalty(self):
        """
        Returns the desirability penalty of having a flare
        star in the system if there is one.
        """
        
        return max([0] + [roll_xdy(1, 3) for s in self.stars if s.luminosityClass == "M-Ve"])


    def create_surrounding_systems(
            self,
            maxTechLevel,
            maxReactionModifier):
        """
        Creates nearby systems, based on how far aliens
        will explore.

        Required Parameters:
            maxTechLevel: Integer
                The maximum Tech Level any alien will achieve.
            maxReactionModifier: Integer
                The maximum reaction modifier value across all
                aliens.
        """

        hexRange = (3 + maxReactionModifier) * (maxTechLevel - 9)
        for x in range(-hexRange, hexRange + 1):
            for y in range(max(-hexRange, -x - hexRange), min(hexRange, -x + hexRange) + 1):
                h = self.coordinates[0] + x
                v = self.coordinates[1] + y
                c = -h - v
                if (h, v, c) not in allCoordinates:
                    create_normal_system(
                        horizontalCoord=self.coordinates[0] + x,
                        verticalCoord=self.coordinates[1] + y)


    def set_nearby_colony_systems(self, alien):
        """
        Sets a flag for nearby systems that indicates
        that this alien has a colony nearby.

        Required Parameters:
            alien: Alien class instance
                The alien that has a nearby colony.
        """

        hexRange = alien.currentTechLevel - 9
        for coords in self.systemsAtRange[hexRange]:
            allCoordinates[(coords[0], coords[1], -coords[0] - coords[1])].alienNearbyColony[alien] = True

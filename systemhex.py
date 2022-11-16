import star
import namegenerator
import globalstuff
from globalstuff import roll_xdy, coin_flip, LookupTable, luminosityClass


allSystems = []
allCoordinates = {}
numberOfStarsTable = LookupTable(
    (10, 1),
    (15, 2),
    (100, 3))


def create_normal_system(
        horizontalCoord,
        verticalCoord):
    """
    Creates a system in a hex that is not in an Open Cluster.

    Required Parameters:
        horizontalCoord: Integer
            The horizontal or x-axis coordinate of the new system.
        verticalCoord: Integer
            The vertical or y-axis coordinate of the new system.
    """

    system = System(
        horizontalCoord=horizontalCoord,
        verticalCoord=verticalCoord,
        openCluster=False)

    system.create_new_open_cluster()
    system.set_number_of_stars()


def create_cluster_system(
        horizontalCoord,
        verticalCoord):
    """
    Creates a system in a hex that is in an Open Cluster, meaning
    there will be more stars per system on average.

    Required Parameters:
        horizontalCoord: Integer
            The horizontal or x-axis coordinate of the new system.
        verticalCoord: Integer
            The vertical or y-axis coordinate of the new system.
    """

    system = System(
        horizontalCoord=horizontalCoord,
        verticalCoord=verticalCoord,
        openCluster=True)

    system.create_new_open_cluster()
    system.set_number_of_stars()


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
        self.coordinates = (
            horizontalCoord,
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
        self.orbitalBodies = []
        self.flareStarDesirabilityPenalty = 0
        self.systemsAtRange = {
            0: [self.coordinates],
            1: self.set_systems_at_range(1),
            2: self.set_systems_at_range(2),
            3: self.set_systems_at_range(3),
            4: self.set_systems_at_range(4),
            5: self.set_systems_at_range(5),
            6: self.set_systems_at_range(6)
            }
        self.brownDwarf = coin_flip()


    def set_number_of_stars(self):
        """
        Sets the number of (non-automatic brown dwarf) stars in this system.
        """

        autoBrownDwarf = (1 if self.brownDwarf else 0)

        if roll_xdy(1, 6) + (2 if self.openCluster else 0) < 4:
            self.numberOfStars = 0 + autoBrownDwarf
            return

        self.numberOfStars = numberOfStarsTable[roll_xdy(3, 6) + (3 if self.openCluster else 0)] + autoBrownDwarf

    def create_stars(self, createOrbitalBodies=True):
        """
        Creates the stars in the system and sets the desirability penalty
        for having a flare star in the system, if there is one.

        Optional Parameters:
            createOrbitalBodies: Boolean
                Whether to create the orbital bodies at this time.
                Default: True
        """
        self.create_primary_star_in_system()
        self.create_companion_stars_in_system()
        self.create_automatic_brown_dwarf()
        self.set_flare_star_desirability_penalty()
        if createOrbitalBodies:
            for s in self.stars:
                s.create_orbital_bodies()


    def create_new_open_cluster(self):
        """
        Determine whether this is a new open cluster or not. If yes,
        create surrounding systems as cluster systems rather than normal
        ones.
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
                        verticalCoord=self.coordinates[1] + y)


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
                h = self.coordinates[0] + x
                v = self.coordinates[1] + y
                c = -h - v
                systemsAtRange.append((h, v, c))

        return systemsAtRange


    def set_distance_from_homeworld(self, alien):
        """
        Sets the distance of this system to each alien's home system.
        This distiance is used in desirability calculations for colonization.

        Required Parameters:
            alien: Alien class instance
                The alien to calculate distance for.
        """
        
        self.distanceFromAlienHomeSystem[alien] = distance_between_systems(self, alien.homePlanet.systemHex)


    def create_primary_star_in_system(self):
        """
        Creates the primary star in this system, if there is one.
        """
        
        if self.numberOfStars - (1 if self.brownDwarf else 0) > 0:
            star.create_primary_star(systemHex=self)


    def create_companion_stars_in_system(self):
        """
        Creates the companion stars in this system, if there are any.
        """
        
        for x in range(self.numberOfStars - 1 - (1 if self.brownDwarf else 0)):
            star.create_companion_star(
                systemHex=self,
                primaryOrbit=self.stars[0].companionOrbits[x])


    def create_automatic_brown_dwarf(self):
        """
        Create an automatic brown dwarf.
        This is not considered a companion star, but is "somewhere"
        in the system.
        """
        
        if self.brownDwarf:
            star.create_brown_dwarf_star(systemHex=self)


    def set_flare_star_desirability_penalty(self):
        """
        Sets the desirability penalty of having a flare
        star in the system if there is one.
        """
        
        self.flareStarDesirabilityPenalty = max([0] + [roll_xdy(1, 3) for s in self.stars if s.luminosityClass == luminosityClass.M_Ve])


    def create_surrounding_systems(
            self,
            maxReactionModifier):
        """
        Creates nearby systems, based on how far aliens
        will explore.

        Required Parameters:
            maxReactionModifier: Integer
                The maximum reaction modifier value across all
                aliens.
        """

        hexRange = (4 + maxReactionModifier) * (globalstuff.maxTechLevel - 9)
        
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

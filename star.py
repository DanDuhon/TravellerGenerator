import orbitalbody
from globalstuff import roll_xdy, LookupTable, spectralType, luminosityClass, companionOrbit, orbitType


allStars = []

# Used for star names.
num = {
    1: " Alpha",
    2: " Beta",
    3: " Gamma",
    4: " Delta"
}

spectralTypeTable = LookupTable(
    (2, spectralType.A),
    (3, spectralType.F),
    (4, spectralType.G),
    (5, spectralType.K),
    (13, spectralType.M),
    (100, spectralType.L))

# There are unnecessary LookupTables here (anything with one value),
# but it simplifies the code that uses this from several elifs to one statement.
luminosityClassDict = {
    spectralType.A: LookupTable(
        (2, LookupTable((100, luminosityClass.A_V))),
        (3, LookupTable(
            (2, luminosityClass.F_IV),
            (3, luminosityClass.K_III),
            (100, luminosityClass.D))),
        (15, LookupTable((100, luminosityClass.D)))),
    spectralType.F: LookupTable(
        (5, LookupTable((100, luminosityClass.F_V))),
        (6, LookupTable(
            (4, luminosityClass.G_IV),
            (100, luminosityClass.M_III))),
        (100, LookupTable((100, luminosityClass.D)))),
    spectralType.G: LookupTable(
        (11, LookupTable((100, luminosityClass.G_V))),
        (13, LookupTable(
            (3, luminosityClass.K_IV),
            (100, luminosityClass.M_III))),
        (100, LookupTable((100, luminosityClass.D)))),
    spectralType.K: LookupTable((100, LookupTable((100, luminosityClass.K_V)))),
    spectralType.M: LookupTable(
        (9, LookupTable((100, luminosityClass.M_V))),
        (12, LookupTable((100, luminosityClass.M_Ve))),
        (100, LookupTable((100, luminosityClass.L)))),
    spectralType.L: LookupTable((100, LookupTable((100, luminosityClass.L))))
}

companionOrbitTable = LookupTable(
    (2, companionOrbit.Tight),
    (4, companionOrbit.Close),
    (5, companionOrbit.Moderate),
    (6, companionOrbit.Distant))


def create_primary_star(systemHex):
    """
    Creates a primary star.

    Required Parameters:
        systemHex: System class instance
            The system in which the star is located.
    """

    star = Star(
        systemHex=systemHex,
        primary=True)

    star.set_spectral_type_roll(primary=True)
    star.set_spectral_type()
    star.set_luminosity_class()


def create_companion_star(
        systemHex,
        primaryOrbit):
    """
    Creates a companion star.

    Required Parameters:
        systemHex: System class instance
            The system in which the star is located.
        primaryOrbit:
            The distance from the primary star.
    """

    star = Star(
        systemHex=systemHex,
        primaryOrbit=primaryOrbit)

    star.set_spectral_type_roll(primarySpectralTypeRoll=star.systemHex.stars[0].spectralTypeRoll)
    star.set_spectral_type()
    star.set_luminosity_class()


def create_brown_dwarf_star(systemHex):
    """
    Creates an "automatic" brown dwarf star.

    Required Parameters:
        systemHex: System class instance
            The system in which the star is located.
    """

    star = Star(systemHex=systemHex)

    star.spectralType = spectralType.L
    star.luminosityClass = luminosityClass.L


class Star():
    """
    Defines a star.  Primary stars, automatic brown dwarf stars, and
    companion stars that are "Distant" from the primary star generate
    the orbital bodies that orbit them.

    Required Parameters:
        systemHex: System class instance
            The system in which the star is located.

    Optional Parameters:
        primary: Boolean
            Indicates whether this star is the primary star of the system.
            Primary stars have companion stars and being a primary star
            affects spectral type.
            Default: False
        primaryOrbit: String
            Indicates the distant from the primary star. This affects orbiting
            objects.
            Default: None
    """

    def __init__(
            self,
            systemHex,
            primary=False,
            primaryOrbit=None):
        allStars.append(self)
        self.systemHex = systemHex
        self.systemHex.stars.append(self)
        self.primary = primary
        self.name = systemHex.name + num[len(systemHex.stars)]
        self.spectralTypeRoll = None
        self.spectralType = None
        self.luminosityClass = None
        self.expansionAffectedOrbits = 0
        self.epistellarOrbits = 0
        self.innerZoneOrbits = 0
        self.outerZoneOrbits = 0
        self.primaryOrbit = primaryOrbit
        self.companionOrbits = []
        self.orbitalBodies = []

        self.set_expansion_affected_orbits()
        self.set_companion_orbits()


    def set_spectral_type_roll(self, primary=False, primarySpectralTypeRoll=None):
        """
        Sets the roll value for the star's spectral type.
        The primary star's roll is used to modify each companion star's roll.

        Optional Parameters:
            primary: Boolean
                Indicates whether this star is the primary star in the system.
                Default value: False
            primarySpectralTypeRoll: Integer
                This is the spectralTypeRoll of the primary star in the system.
                Default value: None
        """

        self.spectralTypeRoll = (roll_xdy(2, 6) if primary else primarySpectralTypeRoll + roll_xdy(1, 6) - 1)


    def set_spectral_type(self):
        """
        Sets the star's spectral type.
        """
        
        self.spectralType = spectralTypeTable[self.spectralTypeRoll]


    def set_luminosity_class(self):
        """
        Sets the star's luminosity class.
        """
        
        self.luminosityClass = luminosityClassDict[self.spectralType][self.systemHex.age][roll_xdy(1, 6)]


    def set_expansion_affected_orbits(self):
        """
        Stars of these luminosity classes expanded or are expanding into
        supergiants. This has a detrimental effect on some of the orbital bodies
        that orbit it. Sets the number of orbital bodies affected.
        """

        if self.luminosityClass in [luminosityClass.D, luminosityClass.K_III, luminosityClass.M_III]:
            self.expansionAffectedOrbits = roll_xdy(1, 6)
            return
        
        self.expansionAffectedOrbits = 0


    def set_companion_orbits(self):
        """
        Sets the distance of each companion star.
        """

        self.companionOrbits = [companionOrbitTable[roll_xdy(1, 6)] for _ in range(self.systemHex.numberOfStars - 1 - (1 if self.systemHex.brownDwarf else 0))]


    def set_epistellar_orbits(self):
        """
        Sets the number of objects closely orbiting the star
        based on the star's luminosity class. Bodies orbiting
        a primary star with Close or Moderate companions orbit all
        such stars but are only listed under the primary star
        for simplicity.

        Value range is 0-2.
        """
        if (self.primaryOrbit and self.primaryOrbit != companionOrbit.Distant
            or self.luminosityClass in [
                luminosityClass.L,
                luminosityClass.D,
                luminosityClass.K_III,
                luminosityClass.M_III
                ]):
            self.epistellarOrbits = 0
            return
            
        self.epistellarOrbits = min([2, max([0, roll_xdy(1, 6) - 3 - (1 if self.luminosityClass == luminosityClass.M_V else 0)])])


    def set_inner_zone_orbits(self):
        """
        Sets the number of objects orbiting a star in the "inner zone",
        or "Goldilock's zone", based on the star's luminosity class.
        Bodies orbiting a primary star with Close or Moderate companions
        orbit all such stars but are only listed under the primary star
        for simplicity.

        Value range is 0-5.
        """

        if companionOrbit.Close in self.companionOrbits or (self.primaryOrbit and self.primaryOrbit != companionOrbit.Distant):
            self.innerZoneOrbits = 0
            return
        
        self.innerZoneOrbits = max([0, roll_xdy(1, (3 if self.luminosityClass == luminosityClass.L else 6)) - 1 - (1 if self.luminosityClass == luminosityClass.M_V else 0)])


    def set_outer_zone_orbits(self):
        """
        Sets the number of objects orbiting a star in the outer zone
        based on the star's luminosity class. Bodies orbiting a primary
        star with Close or Moderate companions orbit all such stars but
        are only listed under the primary star for simplicity.

        Value range is 0-5.
        """
        
        if companionOrbit.Moderate in self.companionOrbits or (self.primaryOrbit and self.primaryOrbit != companionOrbit.Distant):
            self.outerZoneOrbits = 0
            return

        self.outerZoneOrbits = max([0, roll_xdy(1, 6) - 1 - (1 if self.luminosityClass in [luminosityClass.L, luminosityClass.M_V] else 0)])


    def create_orbital_bodies(self):
        """
        Creates orbital bodies orbiting this star.
        """
        
        self.set_epistellar_orbits()
        self.set_inner_zone_orbits()
        self.set_outer_zone_orbits()

        for orbit in range(self.epistellarOrbits +
                self.innerZoneOrbits +
                self.outerZoneOrbits):
            if orbit < self.epistellarOrbits:
                ot = orbitType.Epistellar
            elif orbit < self.epistellarOrbits + self.innerZoneOrbits:
                ot = orbitType.InnerZone
            else:
                ot = orbitType.OuterZone

            orbitalbody.create_orbital_body(
                self,
                orbit + 1,
                ot)

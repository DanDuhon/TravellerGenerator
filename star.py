import planet
from diceroller import roll_xdy
from lookuptable import LookupTable

allStars = []

# Used for star names.
num = {
    1: " Alpha",
    2: " Beta",
    3: " Gamma",
    4: " Delta"
}

spectralTypeTable = LookupTable((2, "A"),
                                (3, "F"),
                                (4, "G"),
                                (5, "K"),
                                (13, "M"),
                                (17, "L"))

luminosityClassDict = {
    "A": LookupTable((2, "A-V"),
                     (3, LookupTable((2, "F-IV"),
                                     (3, "K-III"),
                                     (6, "D"))),
                     (15, "D")),
    "F": LookupTable((5, "F-V"),
                     (6, LookupTable((4, "G-IV"),
                                     (6, "M-III"))),
                     (15, "D")),
    "G": LookupTable((11, "G-V"),
                     (13, LookupTable((3, "K-IV"),
                                      (6, "M-III"))),
                     (15, "D")),
    "K": "K-V",
    "M": LookupTable((9, "M-V"),
                     (12, "M-Ve"),
                     (14, "L")),
    "L": "L"
}

companionOrbitTable = LookupTable((2, "Tight"),
                                  (4, "Close"),
                                  (5, "Moderate"),
                                  (6, "Distant"))


def create_primary_star(
        systemHex,
        alienSurvivalPercent):
    star = Star(
        systemHex=systemHex,
        primary=True)

    star.spectralTypeRoll = star.spectral_type(primary=True)
    star.spectralType = star.spectral_type()
    star.luminosityClass = star.luminosity_class()
    star.expansionAffectedOrbits = star.expansion_affected_orbits()
    star.companionOrbits = star.companion_orbits()
    star.epistellarOrbits = star.epistellar_orbits()
    star.innerZoneOrbits = star.inner_zone_orbits()
    star.outerZoneOrbits = star.outer_zone_orbits()
    star.create_planets(alienSurvivalPercent=alienSurvivalPercent)


def create_companion_star(
        systemHex,
        alienSurvivalPercent,
        primaryOrbit):
    star = Star(
        systemHex=systemHex,
        primaryOrbit=primaryOrbit)

    star.spectralTypeRoll = star.spectral_type_roll(primarySpectralTypeRoll=star.systemHex.stars[0].spectralTypeRoll)
    star.spectralType = star.spectral_type()
    star.luminosityClass = star.luminosity_class()
    star.expansionAffectedOrbits = star.expansion_affected_orbits()
    star.epistellarOrbits = star.epistellar_orbits()
    star.innerZoneOrbits = star.inner_zone_orbits()
    star.outerZoneOrbits = star.outer_zone_orbits()
    star.create_planets(alienSurvivalPercent=alienSurvivalPercent)


def create_brown_dwarf_star(
        systemHex,
        alienSurvivalPercent):
    star = Star(
        systemHex=systemHex,
        autoBrownDwarf=True)

    star.spectralType = star.spectral_type(autoBrownDwarf=True)
    star.spectralType = star.spectral_type()
    star.luminosityClass = star.luminosity_class()
    star.epistellarOrbits = star.epistellar_orbits()
    star.innerZoneOrbits = star.inner_zone_orbits()
    star.outerZoneOrbits = star.outer_zone_orbits()
    star.create_planets(alienSurvivalPercent=alienSurvivalPercent)


class Star():
    """
    Defines a star.  Primary stars, automatic brown dwarf stars, and
    companion stars that are "Distant" from the primary star generate
    the planets that orbit them.

    Required Parameters:
        systemHex: SystemHex class instance
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
        # The name of a star is the name of the system hex.
        # If there is more than one star in a system, a roman numeral is
        # appended.
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
        self.planets = []


    def spectral_type_roll(self, autoBrownDwarf=False, primary=False, primarySpectralTypeRoll=None):
        """
        Returns the roll for the star's spectral type.

        Optional Parameters:
            autoBrownDwarf: Boolean
                Indicates whether this star is an "automatic" brown dwarf.
                Default value: False
            primary: Boolean
                Indicates whether this star is the primary star in the system.
                Default value: False
            primarySpectralTypeRoll: Integer
                This is the spectralTypeRoll of the primary star in the system.
                Default value: None
        """

        if autoBrownDwarf:
            return

        return (roll_xdy(2, 6) if primary else primarySpectralTypeRoll + roll_xdy(1, 6) - 1)


    def spectral_type(self, autoBrownDwarf=False):
        """
        Returns the star's spectral type.

        Optional Parameters:
            autoBrownDwarf: Boolean
                Indicates whether this star is an "automatic" brown dwarf.
                Default value: False
        """

        if autoBrownDwarf:
            return "L"
        
        return spectralTypeTable[self.spectralTypeRoll]


    def luminosity_class(self):
        """
        Returns the star's luminosity class.
        """

        if self.spectralType in ["A", "F", "G"]:
            if ((self.spectralType == "A" and self.systemHex.age == 3)
                or (self.spectralType == "F" and self.systemHex.age == 6)
                or (self.spectralType == "G" and 12 <= self.systemHex.age <= 13)):
                return luminosityClassDict[self.spectralType][self.systemHex.age][roll_xdy(1, 6)]
            else:
                return luminosityClassDict[self.spectralType][self.systemHex.age]
        elif self.spectralType == "M":
            return luminosityClassDict[self.spectralType][roll_xdy(2, 6)]
        else:
            return luminosityClassDict[self.spectralType]


    def expansion_affected_orbits(self):
        """
        Stars of these luminosity classes expanded or are expanding into
        supergiants. This has a detrimental effect on some of the planets
        that orbit it. Returns the number of planets affected.
        """

        if self.luminosityClass in ["D", "K-III", "M-III"]:
            return roll_xdy(1, 6)
        
        return 0


    def companion_orbits(self):
        """
        Returns the distance of each companion star.
        """

        return [companionOrbitTable[roll_xdy(1, 6)] for _ in range(self.numberOfStars - 1 - (1 if self.brownDwarf else 0))]


    def epistellar_orbits(self):
        """
        Returns the number of objects closely orbiting the star
        based on the star's luminosity class. Planets orbiting
        a primary star with Close or Moderate companions orbit all
        such stars but are only listed under the primary star
        for simplicity.

        Returns integer 0-2
        """

        if self.luminosityClass in ["L", "D", "K-III", "M-III"] or self.primaryOrbit in ["Close", "Moderate"]:
            return 0
            
        return min([2, max([0, roll_xdy(1, 6) - 3 - (1 if self.luminosityClass == "M-V" else 0)])])


    def inner_zone_orbits(self):
        """
        Returns the number of objects orbiting a star in the "inner zone",
        or "Goldilock's zone", based on the star's luminosity class.
        Planets orbiting a primary star with Close or Moderate companions
        orbit all such stars but are only listed under the primary star
        for simplicity.

        Returns integer 0-5
        """

        if self.primary and "Close" in self.companionOrbits or self.primaryOrbit in ["Close", "Moderate"]:
            return 0

        return max([0, roll_xdy(1, (3 if self.luminosityClass == "L" else 6)) - 1 - (1 if self.luminosityClass == "M-V" else 0)])


    def outer_zone_orbits(self):
        """
        Returns the number of objects orbiting a star in the outer zone
        based on the star's luminosity class. Planets orbiting a primary
        star with Close or Moderate companions orbit all such stars but
        are only listed under the primary star for simplicity.

        Returns integer 0-5
        """

        if self.primary and "Moderate" in self.companionOrbits or self.primaryOrbit in ["Close", "Moderate"]:
            return 0

        return max([0, roll_xdy(1, 6) - 1 - (1 if self.luminosityClass in ["L", "M-V"] else 0)])


    def create_planets(self, alienSurvivalPercent):
        """
        Creates planets orbiting this star.

        Required Parameters:
            alienSurvivalPercent: Integer
                Represents a percentage. This gets passed along through to the
                planets and then aliens to determine how likely it is that the
                alien species has gone extinct.
        """
        
        for orbit in range(self.epistellarOrbits +
                self.innerZoneOrbits +
                self.outerZoneOrbits):
            if orbit < self.epistellarOrbits:
                orbitType = "Epistellar"
            elif orbit < self.epistellarOrbits + self.innerZoneOrbits:
                orbitType = "Inner Zone"
            else:
                orbitType = "Outer Zone"

            roll = roll_xdy(1, 6) - (1 if self.spectralType == "L" else 0)

            if roll <= 1:
                planet.create_asteroid_belt(
                    star=self,
                    order=orbit + 1,
                    orbitType=orbitType,
                    alienSurvivalPercent=alienSurvivalPercent)
            elif roll == 2:
                planet.create_dwarf_planet(
                    star=self,
                    parentObject=self,
                    order=orbit + 1,
                    orbitType=orbitType,
                    alienSurvivalPercent=alienSurvivalPercent)
            elif roll == 3:
                planet.create_terrestrial_planet(
                    star=self,
                    parentObject=self,
                    order=orbit + 1,
                    orbitType=orbitType,
                    alienSurvivalPercent=alienSurvivalPercent)
            elif roll == 4:
                planet.create_helian_planet(
                    star=self,
                    parentObject=self,
                    order=orbit + 1,
                    orbitType=orbitType,
                    alienSurvivalPercent=alienSurvivalPercent)
            else:
                planet.create_jovian_planet(
                    star=self,
                    order=orbit + 1,
                    orbitType=orbitType,
                    alienSurvivalPercent=alienSurvivalPercent)
        

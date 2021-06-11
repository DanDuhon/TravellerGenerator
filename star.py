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
        alienSurvivalPercent,
        maxTechLevel):
    Star(
        systemHex=systemHex,
        alienSurvivalPercent=alienSurvivalPercent,
        maxTechLevel=maxTechLevel,
        primary=True)


def create_companion_star(
        systemHex,
        alienSurvivalPercent,
        maxTechLevel,
        primaryOrbit,
        primarySpectralTypeRoll):
    Star(
        systemHex=systemHex,
        alienSurvivalPercent=alienSurvivalPercent,
        maxTechLevel=maxTechLevel,
        primaryOrbit=primaryOrbit,
        primarySpectralTypeRoll=primarySpectralTypeRoll)


def create_brown_dwarf_star(
        systemHex,
        alienSurvivalPercent,
        maxTechLevel):
    Star(
        systemHex=systemHex,
        alienSurvivalPercent=alienSurvivalPercent,
        maxTechLevel=maxTechLevel,
        autoBrownDwarf=True)


class Star():
    """
    Defines a star.  Primary stars, automatic brown dwarf stars, and
    companion stars that are "Distant" from the primary star generate
    the planets that orbit them.

    Required Parameters:
        systemHex: SystemHex class
            The system in which the star is located.
        alienSurvivalPercent: Integer
            Represents a percentage. This gets passed along through to the
            planets and then aliens to determine how likely it is that the
            alien species has gone extinct.
        maxTechLevel: Integer
            Indicate the maximum tech level of intelligent species.  This gets
            passed along through the planet to the alien module to determine
            the tech level of each species.

    Optional Parameters:
        autoBrownDwarf: Boolean
            Indicates whether this star is an "automatic brown dwarf".  Each
            system has a 50% chance of having one of these.
            Default: False
        primary: Boolean
            Indicates whether this star is the primary star of the system.
            Primary stars have companion stars and being a primary star
            affects spectral type.
            Default: False
        primaryOrbit: String
            Indicates the distant from the primary star. This affects orbiting
            objects.
            Default: None
        primarySpectralTypeRoll: Integer
            The spectral type roll of the primary star. This is used to
            determine the spectral type of companion stars.
            Default: 0
    """

    def __init__(
            self,
            systemHex,
            alienSurvivalPercent,
            maxTechLevel,
            autoBrownDwarf=False,
            primary=False,
            primaryOrbit=None,
            primarySpectralTypeRoll=0):
        allStars.append(self)
        self.systemHex = systemHex
        self.systemHex.stars.append(self)
        # The name of a star is the name of the system hex.
        # If there is more than one star in a system, a roman numeral is
        # appended.
        self.name = systemHex.name + num[len(systemHex.stars)]
        self.epistellarOrbits = 0
        self.innerZoneOrbits = 0
        self.outerZoneOrbits = 0
        self.primaryOrbit = primaryOrbit
        self.companionOrbits = []
        self.planets = []

        # The primary star rolls 2d6 for spectral type.
        # Companion stars roll 1d6 - 1 + the spetral type roll of the primary
        # star.
        if not primary and not autoBrownDwarf:
            self.spectralTypeRoll = primarySpectralTypeRoll + roll_xdy(1, 6) - 1
        else:
            self.spectralTypeRoll = roll_xdy(2, 6)

        if autoBrownDwarf:
            self.spectralType = "L"
        else:
            self.spectralType = spectralTypeTable[self.spectralTypeRoll]

        if self.spectralType in ["A", "F", "G"]:
            if ((self.spectralType == "A" and systemHex.age == 3)
                or (self.spectralType == "F" and systemHex.age == 6)
                or (self.spectralType == "G" and 12 <= systemHex.age <= 13)):
                self.luminosityClass = luminosityClassDict[self.spectralType][systemHex.age][roll_xdy(1, 6)]
            else:
                self.luminosityClass = luminosityClassDict[self.spectralType][systemHex.age]
        elif self.spectralType == "M":
            self.luminosityClass = luminosityClassDict[self.spectralType][roll_xdy(2, 6)]
        else:
            self.luminosityClass = luminosityClassDict[self.spectralType]

        # Stars of these luminosity classes expanded or are expanding into
        # supergiants. This has a detrimental effect on some of the planets
        # that orbit it.
        if self.luminosityClass in ["D", "K-III", "M-III"]:
            self.expansionAffectedOrbits = roll_xdy(1, 6)
        else:
            self.expansionAffectedOrbits = 0

        if primary:
            for _ in range(1, self.systemHex.numberOfStars + 1):
                self.companionOrbits.append(companionOrbitTable[roll_xdy(1, 6)])

            self.epistellarOrbits = self.epistellar_orbits()

            # Stars with a Close distance companion star cannot have Inner Zone
            # orbits.
            if "Close" in self.companionOrbits:
                self.innerZoneOrbits = 0
            else:
                self.innerZoneOrbits = self.inner_zone_orbits()

            # Stars with a Moderate distance companion star cannot have Outer
            # Zone orbits.
            if "Moderate" in self.companionOrbits:
                self.outerZoneOrbits = 0
            else:
                self.outerZoneOrbits = self.outer_zone_orbits()

        # Companion stars with a Distant distance and automatic brown dwarf
        # stars have their own planetary systems.
        # Companion stars that are closer to the primary star than "Distant"
        # do not have their own planetary systems.  Planets that orbit the
        # primary star also orbit the companion star(s) but for organizational
        # purposes we only track the planets under the primary star.
        elif primaryOrbit == "Distant" or autoBrownDwarf:
            self.epistellarOrbits = self.epistellar_orbits()
            self.innerZoneOrbits = self.inner_zone_orbits()
            self.outerZoneOrbits = self.outer_zone_orbits()

        if primary or primaryOrbit == "Distant" or autoBrownDwarf:
            for orbit in range(
                    self.epistellarOrbits +
                    self.innerZoneOrbits +
                    self.outerZoneOrbits):
                if orbit < self.epistellarOrbits:
                    orbitType = "Epistellar"
                elif orbit < self.epistellarOrbits + self.innerZoneOrbits:
                    orbitType = "Inner Zone"
                else:
                    orbitType = "Outer Zone"

                roll = roll_xdy(1, 6)
                if self.spectralType == "L":
                    roll -= 1

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


    def epistellar_orbits(self):
        """
        Returns the number of objects closely orbiting the star
        based on the star's luminosity class.

        Returns integer
        """
        if self.luminosityClass in ["L", "D", "K-III", "M-III"]:
            return 0
        else:
            roll = roll_xdy(1, 6) - 3
            if self.luminosityClass == "M-V":
                roll -= 1

            if roll > 2:
                return 2
            elif roll < 0:
                return 0
            else:
                return roll


    def inner_zone_orbits(self):
        """
        Returns the number of objects orbiting a star in the "inner zone",
        or "Goldilock's zone", based on the star's luminosity class.

        Returns integer
        """
        if self.luminosityClass == "L":
            return roll_xdy(1, 3) - 1
        else:
            roll = roll_xdy(1, 6) - 1
            if self.luminosityClass == "M-V":
                roll -= 1

            if roll < 0:
                return 0
            else:
                return roll


    def outer_zone_orbits(self):
        """
        Returns the number of objects orbiting a star in the outer zone
        based on the star's luminosity class.

        Returns integer
        """
        roll = roll_xdy(1, 6) - 1
        if self.luminosityClass in ["L", "M-V"]:
            roll -= 1

        if roll < 0:
            return 0
        else:
            return roll

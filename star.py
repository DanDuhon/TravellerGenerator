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


def epistellar_orbits(luminosityClass):
    """
    Returns the number of objects closely orbiting the star
    based on the star's luminosity class.

    Parameters:
        luminosityClass: String
        Single letter luminosity class of the star.

    Returns integer
    """
    if luminosityClass in ["L", "D", "K-III", "M-III"]:
        return 0
    else:
        roll = roll_xdy(1, 6) - 3
        if luminosityClass == "M-V":
            roll -= 1

        if roll > 2:
            return 2
        elif roll < 0:
            return 0
        else:
            return roll


def inner_zone_orbits(luminosityClass):
    """
    Returns the number of objects orbiting a star in the "inner zone",
    or "Goldilock's zone", based on the star's luminosity class.

    Parameters:
        luminosityClass: String
        Single letter luminosity class of the star.

    Returns integer
    """
    if luminosityClass == "L":
        return roll_xdy(1, 3) - 1
    else:
        roll = roll_xdy(1, 6) - 1
        if luminosityClass == "M-V":
            roll -= 1

        if roll < 0:
            return 0
        else:
            return roll


def outer_zone_orbits(luminosityClass):
    """
    Returns the number of objects orbiting a star in the outer zone
    based on the star's luminosity class.

    Parameters:
        luminosityClass: String
        Single letter luminosity class of the star.

    Returns integer
    """
    roll = roll_xdy(1, 6) - 1
    if luminosityClass in ["L", "M-V"]:
        roll -= 1

    if roll < 0:
        return 0
    else:
        return roll


class Star():
    """
    Defines a star.  A primary star will also generate companion stars, if any.
    Primary stars, automatic brown dwarf stars, and companion stars that are
    "Distant" from the primary star generate the planets that orbit them.

    Requied Parameters:
        systemHex: SystemHex class
            The system in which the star is located.
        systemName: String
            The name of the system, used to name the star.
        starNumber: Integer
            Indicates the number of the star.  1 is the primary star.
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
        numberOfStars: Integer. Generated in the systemhex module, this
            determines star naming and whether companion stars need to be
            generated.
            Default: 0
        systemAge: Integer
            Generated in the systemhex module, this is a representation of how
            old the stars in this system are and helps determine luminosity
            class.
            Default: 0
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
        primaryPlanets: List of Planet class instances
            If a star is not distant enough from the primary star, the planets
            that orbit the primary star also orbit this companion.
            Default: empty list
    """

    def __init__(
            self,
            systemHex,
            systemName,
            systemAge,
            starNumber,
            alienSurvivalPercent,
            maxTechLevel,
            autoBrownDwarf=False,
            numberOfStars=0,
            primary=False,
            primaryOrbit=None,
            primarySpectralTypeRoll=0,
            primaryPlanets=[]):
        allStars.append(self)
        self.systemHex = systemHex
        # The name of a star is the name of the system hex.
        # If there is more than one star in a system, a roman numeral is
        # appended.
        self.name = systemName + num[starNumber]
        self.starNumber = starNumber
        self.epistellarOrbits = 0
        self.innerZoneOrbits = 0
        self.outerZoneOrbits = 0
        self.primaryOrbit = primaryOrbit
        self.companions = []

        # The primary star rolls 2d6 for spectral type.
        # Companion stars roll 1d6 - 1 + the spetral type roll of the primary
        # star.
        if not primary and not autoBrownDwarf:
            spectralTypeRoll = primarySpectralTypeRoll + roll_xdy(1, 6) - 1
        else:
            spectralTypeRoll = roll_xdy(2, 6)

        if autoBrownDwarf:
            self.spectralType = "L"
        else:
            self.spectralType = spectralTypeTable[spectralTypeRoll]

        if self.spectralType in ["A", "F", "G"]:
            if (self.spectralType == "A" and systemAge == 3) or (self.spectralType ==
                                                                 "F" and systemAge == 6) or (self.spectralType == "G" and 12 <= systemAge <= 13):
                self.luminosityClass = luminosityClassDict[self.spectralType][systemAge][roll_xdy(1, 6)]
            else:
                self.luminosityClass = luminosityClassDict[self.spectralType][systemAge]
        elif self.spectralType == "M":
            self.luminosityClass = luminosityClassDict[self.spectralType][roll_xdy(2, 6)]
        else:
            self.luminosityClass = luminosityClassDict[self.spectralType]

        # Stars of these luminosity classes are expanding into supergiants.
        # This has a detrimental effect on some of the planets that orbit it,
        # since the temperature would greatly increase.
        if self.luminosityClass in ["D", "K-III", "M-III"]:
            self.expansionAffectedOrbits = roll_xdy(1, 6)
        else:
            self.expansionAffectedOrbits = 0

        if primary:
            if numberOfStars > 1:
                self.companion1Orbit = companionOrbitTable[roll_xdy(1, 6)]
                self.companions.append(
                    Star(
                        systemHex=self.systemHex,
                        systemName=systemName,
                        starNumber=2,
                        alienSurvivalPercent=alienSurvivalPercent,
                        maxTechLevel=maxTechLevel,
                        systemAge=systemAge,
                        primaryOrbit=self.companion1Orbit,
                        primarySpectralTypeRoll=spectralTypeRoll))
            else:
                self.companion1Orbit = None

            if numberOfStars > 2:
                self.companion2Orbit = companionOrbitTable[roll_xdy(1, 6)]
                self.companions.append(
                    Star(
                        systemHex=self.systemHex,
                        systemName=systemName,
                        starNumber=3,
                        alienSurvivalPercent=alienSurvivalPercent,
                        maxTechLevel=maxTechLevel,
                        systemAge=systemAge,
                        primaryOrbit=self.companion2Orbit,
                        primarySpectralTypeRoll=spectralTypeRoll))
            else:
                self.companion2Orbit = None

            self.epistellarOrbits = epistellar_orbits(self.luminosityClass)

            # Stars with a Close distance companion star cannot have Inner Zone
            # orbits.
            if self.companion1Orbit == "Close" or self.companion2Orbit == "Close":
                self.innerZoneOrbits = 0
            else:
                self.innerZoneOrbits = inner_zone_orbits(self.luminosityClass)

            # Stars with a Moderate distance companion star cannot have Outer
            # Zone orbits.
            if self.companion1Orbit == "Moderate" or self.companion2Orbit == "Moderate":
                self.outerZoneOrbits = 0
            else:
                self.outerZoneOrbits = outer_zone_orbits(self.luminosityClass)
        # Companion stars with a Distant distance and automatic brown dwarf
        # stars have their own planetary systems.
        elif primaryOrbit == "Distant" or autoBrownDwarf:
            self.epistellarOrbits = epistellar_orbits(self.luminosityClass)
            self.innerZoneOrbits = inner_zone_orbits(self.luminosityClass)
            self.outerZoneOrbits = outer_zone_orbits(self.luminosityClass)

        if primary or primaryOrbit == "Distant":
            self.planets = []
            for x in range(
                    self.epistellarOrbits +
                    self.innerZoneOrbits +
                    self.outerZoneOrbits):
                roll = roll_xdy(1, 6)
                if self.spectralType == "L":
                    roll -= 1

                if roll <= 1:
                    self.planets.append(
                        planet.AsteroidBelt(
                            star=self,
                            parentObject=self,
                            order=x + 1,
                            orbitType="Epistellar" if x < self.epistellarOrbits else "Inner Zone" if x < self.epistellarOrbits +
                                self.innerZoneOrbits else "Outer Zone",
                            luminosityClass=self.luminosityClass,
                            expansionAffectedOrbits=self.expansionAffectedOrbits,
                            systemAge=systemAge,
                            alienSurvivalPercent=alienSurvivalPercent,
                            maxTechLevel=maxTechLevel))
                elif roll == 2:
                    self.planets.append(
                        planet.DwarfPlanet(
                            star=self,
                            parentObject=self,
                            order=x + 1,
                            orbitType="Epistellar" if x < self.epistellarOrbits else "Inner Zone" if x < self.epistellarOrbits +
                                self.innerZoneOrbits else "Outer Zone",
                            luminosityClass=self.luminosityClass,
                            expansionAffectedOrbits=self.expansionAffectedOrbits,
                            systemAge=systemAge,
                            alienSurvivalPercent=alienSurvivalPercent,
                            maxTechLevel=maxTechLevel))
                elif roll == 3:
                    self.planets.append(
                        planet.TerrestrialPlanet(
                            star=self,
                            parentObject=self,
                            order=x + 1,
                            orbitType="Epistellar" if x < self.epistellarOrbits else "Inner Zone" if x < self.epistellarOrbits +
                                self.innerZoneOrbits else "Outer Zone",
                            luminosityClass=self.luminosityClass,
                            expansionAffectedOrbits=self.expansionAffectedOrbits,
                            systemAge=systemAge,
                            alienSurvivalPercent=alienSurvivalPercent,
                            maxTechLevel=maxTechLevel))
                elif roll == 4:
                    self.planets.append(
                        planet.HelianPlanet(
                            star=self,
                            parentObject=self,
                            order=x + 1,
                            orbitType="Epistellar" if x < self.epistellarOrbits else "Inner Zone" if x < self.epistellarOrbits +
                                self.innerZoneOrbits else "Outer Zone",
                            luminosityClass=self.luminosityClass,
                            expansionAffectedOrbits=self.expansionAffectedOrbits,
                            systemAge=systemAge,
                            alienSurvivalPercent=alienSurvivalPercent,
                            maxTechLevel=maxTechLevel))
                else:
                    self.planets.append(
                        planet.JovianPlanet(
                            star=self,
                            parentObject=self,
                            order=x + 1,
                            orbitType="Epistellar" if x < self.epistellarOrbits else "Inner Zone" if x < self.epistellarOrbits +
                                self.innerZoneOrbits else "Outer Zone",
                            luminosityClass=self.luminosityClass,
                            expansionAffectedOrbits=self.expansionAffectedOrbits,
                            systemAge=systemAge,
                            alienSurvivalPercent=alienSurvivalPercent,
                            maxTechLevel=maxTechLevel))
        else:
            # Companion stars that are closer to the primary star than "Distant"
            # do not have their own planetary systems.  Planets that orbit the
            # primary star also orbit the companion star(s).
            self.planets = primaryPlanets

        for planetInstance in self.planets:
            self.planets.extend(planetInstance.satellites)

        self.animals = []
        for planetInstance in self.planets:
            self.animals.extend(planetInstance.animals)

        self.homeStarOfAliens = []
        for planetInstance in self.planets:
            if planetInstance.alien is not None:
                self.homeStarOfAliens.append(planetInstance.alien)

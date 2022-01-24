from enum import Enum


maxTechLevel = 0
alienSurvivalPercent = 0

class spectralType(Enum):
    A = 0
    F = 1
    G = 2
    K = 3
    M = 4
    L = 5

class luminosityClass(Enum):
    A_V = 0
    D = 1
    F_IV = 2
    F_V = 3
    G_IV = 4
    G_V = 5
    K_III = 6
    K_IV = 7
    K_V = 8
    L = 9
    M_III = 10
    M_V = 11
    M_Ve = 12

class companionOrbit(Enum):
    Tight = 0
    Close = 1
    Moderate = 2
    Distant = 3

class group(Enum):
    AsteroidBelt = 0
    DwarfPlanet = 1
    TerrestrialPlanet = 2
    HelianPlanet = 3
    JovianPlanet = 4

class orbitType(Enum):
    Epistellar = 0
    InnerZone = 1
    OuterZone = 2

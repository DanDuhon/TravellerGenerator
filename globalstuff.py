from enum import Enum
from random import randint
from bisect import bisect_left
from collections.abc import Mapping


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

class chemistry(Enum):
    Ammonia = 0
    Chlorine = 1
    Methane = 2
    Sulfur = 3
    Water = 4

class category(Enum):
    Acheronian = 0
    Arean = 1
    Arid = 2
    Asphodelian = 3
    AsteroidBelt = 4
    Chthonian = 5
    Hebean = 6
    Helian = 7
    JaniLithic = 8
    Jovian = 9
    Meltball = 10
    Oceanic = 11
    Panthalassic = 12
    Promethean = 13
    Rockball = 14
    Snowball = 15
    Stygian = 16
    Tectonic = 17
    Telluric = 18
    Vesperian = 19

class className(Enum):
    Arid = 0
    AsteroidBelt = 1
    Chthonian = 2
    DwarfJovian = 3
    Epistellar = 4
    GeoHelian = 5
    Geocyclic = 6
    Geopassive = 7
    Geothermic = 8
    Geotidal = 9
    Jovian = 10
    Oceanic = 11
    Panthalassic = 12
    Nebulous = 13
    Tectonic = 14
    Telluric = 15

class type(Enum):
    Acheronian = 0
    Amunian = 1
    Apollonian = 2
    Arean = 3
    Asimovian = 4
    Asphodelian = 5
    AsteroidBelt = 6
    Atlan = 7
    BathyAmunian = 8
    BathyGaian = 9
    BathyTartarian = 10
    Brammian = 11
    Burian = 12
    Carbonian = 13
    ChloriticGaian = 14
    Cytherean = 15
    Darwinian = 16
    Erisian = 17
    Ferrinian = 18
    Gaian = 19
    Gelidian = 20
    Hebean = 21
    Helian = 22
    Hephaestian = 23
    Idunnian = 24
    JaniLithic = 25
    Khonsonian = 26
    Lithic = 27
    Lokian = 28
    Nunnic = 29
    Pelagic = 30
    Phaethonic = 31
    Phosphorian = 32
    Plutonian = 33
    Promethean = 34
    Saganian = 35
    Sethian = 36
    Stygian = 37
    Tartarian = 38
    Teathic = 39
    ThioGaian = 40
    Titanian = 41
    Utgardian = 42
    Vesperian = 43

class terrain(Enum):
    BeachShore = 0
    Clear = 1
    DeepOcean = 2
    Desert = 3
    Forest = 4
    Hills = 5
    Jungle = 6
    Mountains = 7
    OpenOcean = 8
    Plains = 9
    Rainforest = 10
    Riverbank = 11
    RoughBroken = 12
    ShallowOcean = 13
    SwampMarsh = 14
    Woods = 15

class starport(Enum):
    X = 0
    E = 1
    D = 2
    C = 3
    B = 4
    A = 5

class tradeCode(Enum):
    Ag = 0
    As = 1
    De = 2
    Fl = 3
    Ga = 4
    Hi = 5
    Ht = 6
    Ic = 7
    In = 8
    Lo = 9
    Lt = 10
    Na = 11
    Ni = 12
    Po = 13
    Ri = 14
    St = 15
    Wa = 16
    Va = 17
    Zo = 18


tradeCodeText = {
    tradeCode.Ag: "Agricultural",
    tradeCode.As: "Asteroid Belt",
    tradeCode.De: "Desert",
    tradeCode.Fl: "Fluid Oceans",
    tradeCode.Ga: "Garden",
    tradeCode.Hi: "High Population",
    tradeCode.Ht: "High Technology",
    tradeCode.Ic: "Ice-Capped",
    tradeCode.In: "Industrial",
    tradeCode.Lo: "Low Population",
    tradeCode.Lt: "Low Technology",
    tradeCode.Na: "Non-Agricultural",
    tradeCode.Ni: "Non-Industrial",
    tradeCode.Po: "Poor",
    tradeCode.Ri: "Rich",
    tradeCode.St: "Sterile",
    tradeCode.Wa: "Water World",
    tradeCode.Va: "Vacuum",
    tradeCode.Zo: "Zoo",
}


categoryNameDescriptionDict = {
    category.Acheronian: {
        "name": "Acheronian",
        "description": "These are worlds that were directly affected by a star's transition from the main sequence; the atmosphere and oceans have been boiled away, leaving a scorched, dead planet."
    },
    category.Arean: {
        "name": "Arean",
        "description": "These are worlds with little liquid, that move through a slow geological cycle of a gradual build-up, a short wet and clement period, and a long decline."
    },
    category.Arid: {
        "name": "Arid",
        "description": "These are worlds with limited amounts of surface liquid, that maintain an equilibrium with the help of their tectonic activity and their biosphere."
    },
    category.Asphodelian: {
        "name": "Asphodelian",
        "description": "These are worlds that were directly affected by a star's transition from the main sequence; their atmosphere has been boiled away, leaving the surface exposed."
    },
    category.Chthonian: {
        "name": "Chthonian",
        "description": "These are worlds that were directly affected by a star's transition from the main sequence, or that have simply spent too long in a tight epistellar orbit; their atmospheres have been stripped away."
    },
    category.Hebean: {
        "name": "Hebean",
        "description": "These are highly active worlds, due to tidal flexing, but with some regions of stability; the larger ones may be able to maintain some atmosphere and surface liquid."
    },
    category.Helian: {
        "name": "Helian",
        "description": "These are typical helian or \"subgiant\" worlds - large enough to retain helium atmospheres."
    },
    category.JaniLithic: {
        "name": "Jani-Lithic",
        "description": "These worlds, tide-locked to the primary, are rocky, dry, and geologically active."
    },
    category.Jovian: {
        "name": "Jovian",
        "description": "These are huge worlds with helium-hydrogen envelopes and compressed cores; the largest emit more heat than they absorb."
    },
    category.Meltball: {
        "name": "Meltball",
        "description": "These are dwarfs with molten or semi-molten surfaces, either from extreme tidal flexing, or extreme approach to a star."
    },
    category.Oceanic: {
        "name": "Oceanic",
        "description": "These are worlds with a continuous hydrological cycle and deep oceans, due to either dense greenhouse atmosphere or active plate tectonics."
    },
    category.Panthalassic: {
        "name": "Panthalassic",
        "description": "These are massive worlds, aborted gas giants, largely composed of water and hydrogen."
    },
    category.Promethean: {
        "name": "Promethean",
        "description": "These are worlds that, through tidal-flexing, have a geological cycle similar to plate tectonics, that supports surface liquid and atmosphere."
    },
    category.Rockball: {
        "name": "Rockball",
        "description": "These are mostly dormant worlds, with surfaces largely unchanged since the early period of planetary formation."
    },
    category.Snowball: {
        "name": "Snowball",
        "description": "These worlds are composed of mostly ice and some rock. They may have varying degrees of activity, ranging from completely cold and still to cryo-volcanically active with extensive subsurface oceans."
    },
    category.Stygian: {
        "name": "Stygian",
        "description": "These are worlds that were directly affected by a star's transition from the main sequence; they are melted and blasted lumps."
    },
    category.Tectonic: {
        "name": "Tectonic",
        "description": "These are worlds with active plate tectonics and large bodies of surface liquid, allowing for stable atmospheres and a high likelihood of life."
    },
    category.Telluric: {
        "name": "Telluric",
        "description": "These are worlds with geoactivity but no hydrological cycle at all, leading to dense runaway-greenhouse atmospheres."
    },
    category.Vesperian: {
        "name": "Vesperian",
        "description": "These worlds are tide-locked to their primary, but at a distance that permits surface liquid and the development of life."
    }
}


class LookupTable(Mapping):
    """
    A lookup table with contiguous ranges of small integers as
    keys. Initialize a table by passing pairs (max, value) as
    arguments. The first range starts at -10, and second and subsequent
    ranges start at the end of the previous range.

    >>> t = LookupTable((10, '-10 - 10'), (35, '11 - 35'), (100, '36 - 100'))
    >>> t[10], t[11], t[100]
    ('-10 - 10', '11 - 35', '36 - 100')
    >>> t[0]
    Traceback (most recent call last):
      ...
    KeyError: 0
    >>> next(iter(t.items()))
    (1, '-10 - 10')
    """

    def __init__(self, *table):
        self.table = sorted(table)
        self.max = self.table[-1][0]

    def __getitem__(self, key):
        key = int(key)
        if not -10 <= key <= self.max:
            raise KeyError(key)
        return self.table[bisect_left(self.table, (key,))][1]

    def __iter__(self):
        return iter(range(1, self.max + 1))

    def __len__(self):
        return self.max


def roll_xdy(numberToRoll, dieSides):
    """
    Returns a generator of dice roll results.

    Parameters:
        numberToRoll: Integer
            The number of dice to roll.
        dieSides: Integer
            The number of sides the dice being rolled have.
    """
    total = 0
    for _ in range(numberToRoll):
        total += randint(1, dieSides)
    return total


def coin_flip():
    """
    Returns a True or False with a 50% chance of each.
    """
    return randint(0, 1) == 1

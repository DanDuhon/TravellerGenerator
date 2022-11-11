from enum import Enum, StrEnum, auto
from random import randint
from bisect import bisect_left
from collections.abc import Mapping


maxTechLevel = 0
alienSurvivalPercent = 0


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


class spectralType(StrEnum):
    A = auto()
    F = auto()
    G = auto()
    K = auto()
    M = auto()
    L = auto()

class luminosityClass(StrEnum):
    A_V = auto()
    D = auto()
    F_IV = auto()
    F_V = auto()
    G_IV = auto()
    G_V = auto()
    K_III = auto()
    K_IV = auto()
    K_V = auto()
    L = auto()
    M_III = auto()
    M_V = auto()
    M_Ve = auto()

class companionOrbit(StrEnum):
    Tight = auto()
    Close = auto()
    Moderate = auto()
    Distant = auto()

class group(StrEnum):
    AsteroidBelt = "Asteroid Belt"
    DwarfPlanet = "Dwarf Planet"
    TerrestrialPlanet = "Terrestrial Planet"
    HelianPlanet = "Helian Planet"
    JovianPlanet = "Jovian Planet"

class orbitType(StrEnum):
    Epistellar = auto()
    InnerZone = auto()
    OuterZone = auto()

class chemistry(StrEnum):
    Ammonia = auto()
    Chlorine = auto()
    Methane = auto()
    Sulfur = auto()
    Water = auto()

class category(StrEnum):
    Acheronian = auto()
    Arean = auto()
    Arid = auto()
    Asphodelian = auto()
    AsteroidBelt = auto()
    Chthonian = auto()
    Hebean = auto()
    Helian = auto()
    JaniLithic = auto()
    Jovian = auto()
    Meltball = auto()
    Oceanic = auto()
    Panthalassic = auto()
    Promethean = auto()
    Rockball = auto()
    Snowball = auto()
    Stygian = auto()
    Tectonic = auto()
    Telluric = auto()
    Vesperian = auto()

class className(StrEnum):
    Arid = auto()
    AsteroidBelt = "Asteroid Belt"
    Chthonian = auto()
    DwarfJovian = "Dwarf Jovian"
    Epistellar = auto()
    GeoHelian = "Geo-Helian"
    Geocyclic = auto()
    Geopassive = auto()
    Geothermic = auto()
    Geotidal = auto()
    Jovian = auto()
    Oceanic = auto()
    Panthalassic = auto()
    Nebulous = auto()
    Tectonic = auto()
    Telluric = auto()

class type(StrEnum):
    Acheronian = auto()
    Amunian = auto()
    Apollonian = auto()
    Arean = auto()
    Asimovian = auto()
    Asphodelian = auto()
    AsteroidBelt = auto()
    Atlan = auto()
    BathyAmunian = "Bathy-Amunian"
    BathyGaian = "Bathy-Gaian"
    BathyTartarian = "Bathy-Tartarian"
    Brammian = auto()
    Burian = auto()
    Carbonian = auto()
    ChloriticGaian = "Chloritic-Gaiain"
    Cytherean = auto()
    Darwinian = auto()
    Erisian = auto()
    Ferrinian = auto()
    Gaian = auto()
    Gelidian = auto()
    Hebean = auto()
    Helian = auto()
    Hephaestian = auto()
    Idunnian = auto()
    JaniLithic = "Jani-Lithic"
    Khonsonian = auto()
    Lithic = auto()
    Lokian = auto()
    Nunnic = auto()
    Pelagic = auto()
    Phaethonic = auto()
    Phosphorian = auto()
    Plutonian = auto()
    Promethean = auto()
    Saganian = auto()
    Sethian = auto()
    Stygian = auto()
    Tartarian = auto()
    Teathic = auto()
    ThioGaian = "Thio-Gaian"
    Titanian = auto()
    Utgardian = auto()
    Vesperian = auto()

class terrain(StrEnum):
    BeachShore = "beach/shore"
    Clear = auto()
    DeepOcean = auto()
    Desert = auto()
    Forest = auto()
    Hills = auto()
    Jungle = auto()
    Mountains = auto()
    OpenOcean = "open ocean"
    Plains = auto()
    Rainforest = auto()
    Riverbank = auto()
    RoughBroken = auto()
    ShallowOcean = "shallow ocean"
    SwampMarsh = "swamp/marsh"
    Woods = auto()

class habitation(StrEnum):
    Outpost = auto()
    Colony = auto()
    Homeworld = auto()

class starport(StrEnum):
    X = auto()
    E = auto()
    D = auto()
    C = auto()
    B = auto()
    A = auto()

class tradeCode(StrEnum):
    Ag = auto()
    As = auto()
    De = auto()
    Fl = auto()
    Ga = auto()
    Hi = auto()
    Ht = auto()
    Ic = auto()
    In = auto()
    Lo = auto()
    Lt = auto()
    Na = auto()
    Ni = auto()
    Po = auto()
    Ri = auto()
    St = auto()
    Wa = auto()
    Va = auto()
    Zo = auto()

class animalClass(StrEnum):
    Amphibian = auto()
    Aquatic = auto()
    Avian = auto()
    Fungal = auto()
    Insect = auto()
    Mammal = auto()
    Reptile = auto()

class movement(StrEnum):
    Walk = auto()
    Burrow = auto()
    Swim = auto()
    Fly = auto()

class behavior(StrEnum):
    CarrionEater = "carrion eater"
    Chaser = auto()
    Eater = auto()
    Filter = auto()
    Gatherer = auto()
    Grazer = auto()
    Hunter = auto()
    Hijacker = auto()
    Intimidator = auto()
    Killer = auto()
    Intermittent = auto()
    Pouncer = auto()
    Reducer = auto()
    Siren = auto()
    Trapper = auto()


weight = {
    1: "1 kg",
    2: "3 kg",
    3: "6 kg",
    4: "12 kg",
    5: "25 kg",
    6: "50 kg",
    7: "100 kg",
    8: "200 kg",
    9: "400 kg",
    10: "800 kg",
    11: "1,600 kg",
    12: "3,200 kg",
    13: "5,000 kg",
    14: "8,000 kg",
    15: "10,000 kg"
}


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

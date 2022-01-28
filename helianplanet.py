import asphodelian
import helian
import panthalassic
import globalstuff
from planet import Planet
from diceroller import roll_xdy


class HelianPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = min(14, roll_xdy(1, 6) + 9)

        numOfSatellites = roll_xdy(1, 6) - 3
        terrestrialSatellite = roll_xdy(1, 6) == 6

        if terrestrialSatellite and numOfSatellites > 0:
            self.create_satellite(globalstuff.group.TerrestrialPlanet)
            numOfSatellites -= 1

        for _ in range(numOfSatellites):
            self.create_satellite(globalstuff.group.DwarfPlanet)


def create_epistellar_helian_planet(star, parentObject, order, orbitType, roll):
    if roll <= 5:
        helian.Helian(star, parentObject, order, orbitType)
    else:
        panthalassic.Panthalassic(star, parentObject, order, orbitType)


def create_inner_zone_helian_planet(star, parentObject, order, orbitType, roll):
    if roll <= 4:
        helian.Helian(star, parentObject, order, orbitType)
    else:
        panthalassic.Panthalassic(star, parentObject, order, orbitType)


def create_outer_zone_helian_planet(star, parentObject, order, orbitType, roll):
    helian.Helian(star, parentObject, order, orbitType)


def create_helian_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        asphodelian.Asphodelian(star, parentObject, order, orbitType)
        return
        
    if orbitType == globalstuff.orbitType.Epistellar:
        create_epistellar_helian_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == globalstuff.orbitType.InnerZone:
        create_inner_zone_helian_planet(star, parentObject, order, orbitType, roll_xdy(2, 6))
    elif orbitType == globalstuff.orbitType.OuterZone:
        create_outer_zone_helian_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))

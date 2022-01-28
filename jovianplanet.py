import chthonian
import jovian
import globalstuff
from planet import Planet
from diceroller import roll_xdy


class JovianPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = 16
        self.hydrosphere = 16

        numOfSatellites = roll_xdy(1, 6)

        if roll_xdy(1, 6):
            if roll_xdy(1, 6) == 6:
                self.create_satellite(globalstuff.group.HelianPlanet)
            else:
                self.create_satellite(globalstuff.group.TerrestrialPlanet)
            numOfSatellites -= 1

        for _ in range(numOfSatellites):
            self.create_satellite(globalstuff.group.DwarfPlanet)


def create_epistellar_jovian_planet(star, parentObject, order, orbitType, roll):
    if roll <= 5:
        jovian.Jovian(star, parentObject, order, orbitType)
    else:
        chthonian.Chthonian(star, parentObject, order, orbitType)


def create_inner_zone_jovian_planet(star, parentObject, order, orbitType, roll):
    jovian.Jovian(star, parentObject, order, orbitType)


def create_outer_zone_jovian_planet(star, parentObject, order, orbitType, roll):
    jovian.Jovian(star, parentObject, order, orbitType)


def create_jovian_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        chthonian.Chthonian(star, parentObject, order, orbitType)
        return
        
    if orbitType == globalstuff.orbitType.Epistellar:
        create_epistellar_jovian_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == globalstuff.orbitType.InnerZone:
        create_inner_zone_jovian_planet(star, parentObject, order, orbitType, roll_xdy(2, 6))
    elif orbitType == globalstuff.orbitType.OuterZone:
        create_outer_zone_jovian_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))

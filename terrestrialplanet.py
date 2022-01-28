import acheronian
import arid
import janilithic
import oceanic
import tectonic
import telluric
import vesperian
import globalstuff
from planet import Planet
from diceroller import roll_xdy


class TerrestrialPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = roll_xdy(1, 6) + 4

        if roll_xdy(1, 6) >= 5:
            self.create_satellite(globalstuff.group.DwarfPlanet)


def create_epistellar_terrestrial_planet(star, parentObject, order, orbitType, roll):
    if roll <= 4:
        janilithic.JaniLithic(star, parentObject, order, orbitType)
    elif roll <= 5:
        vesperian.Vesperian(star, parentObject, order, orbitType)
    else:
        telluric.Telluric(star, parentObject, order, orbitType)


def create_inner_zone_terrestrial_planet(star, parentObject, order, orbitType, roll):
    if roll <= 4:
        telluric.Telluric(star, parentObject, order, orbitType)
    elif roll <= 6:
        arid.Arid(star, parentObject, order, orbitType)
    elif roll <= 7:
        tectonic.Tectonic(star, parentObject, order, orbitType)
    elif roll <= 9:
        oceanic.Oceanic(star, parentObject, order, orbitType)
    elif roll <= 10:
        tectonic.Tectonic(star, parentObject, order, orbitType)
    else:
        telluric.Telluric(star, parentObject, order, orbitType)


def create_outer_zone_terrestrial_planet(star, parentObject, order, orbitType, roll):
    if parentObject != star and parentObject.group == globalstuff.group.JovianPlanet:
        roll += 2

    if roll <= 4:
        arid.Arid(star, parentObject, order, orbitType)
    elif roll <= 6:
        tectonic.Tectonic(star, parentObject, order, orbitType)
    else:
        oceanic.Oceanic(star, parentObject, order, orbitType)


def create_terrestrial_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        acheronian.Acheronian(star, parentObject, order, orbitType)
        return
        
    if orbitType == globalstuff.orbitType.Epistellar:
        create_epistellar_terrestrial_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))
    elif orbitType == globalstuff.orbitType.InnerZone:
        create_inner_zone_terrestrial_planet(star, parentObject, order, orbitType, roll_xdy(2, 6))
    elif orbitType == globalstuff.orbitType.OuterZone:
        create_outer_zone_terrestrial_planet(star, parentObject, order, orbitType, roll_xdy(1, 6))

import arean
import hebean
import meltball
import promethean
import rockball
import snowball
import stygian
import globalstuff
from planet import Planet
from diceroller import roll_xdy


class DwarfPlanet(Planet):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.size = roll_xdy(1, 6) - 1

        if self.parentObject == self.star and roll_xdy(1, 6) == 6:
            self.create_satellite(globalstuff.group.DwarfPlanet)


def create_epistellar_dwarf_planet(star, parentObject, order, orbitType, roll, roll2):
    if roll <= 3:
        rockball.Rockball(star, parentObject, order, orbitType)
    elif roll <= 5:
        meltball.Meltball(star, parentObject, order, orbitType)
    elif roll2 <= 4:
        hebean.Hebean(star, parentObject, order, orbitType)
    else:
        promethean.Promethean(star, parentObject, order, orbitType)


def create_inner_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2):
    if roll <= 4:
        rockball.Rockball(star, parentObject, order, orbitType)
    elif roll <= 6:
        arean.Arean(star, parentObject, order, orbitType)
    elif roll <= 7:
        meltball.Meltball(star, parentObject, order, orbitType)
    elif roll2 <= 4:
        hebean.Hebean(star, parentObject, order, orbitType)
    else:
        promethean.Promethean(star, parentObject, order, orbitType)


def create_outer_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2):
    if roll <= 0:
        rockball.Rockball(star, parentObject, order, orbitType)
    elif roll <= 4:
        snowball.Snowball(star, parentObject, order, orbitType)
    elif roll <= 6:
        rockball.Rockball(star, parentObject, order, orbitType)
    elif roll <= 7:
        meltball.Meltball(star, parentObject, order, orbitType)
    elif roll2 <= 3:
        hebean.Hebean(star, parentObject, order, orbitType)
    elif roll2 <= 5:
        arean.Arean(star, parentObject, order, orbitType)
    else:
        promethean.Promethean(star, parentObject, order, orbitType)


def create_dwarf_planet(star, parentObject, order, orbitType):
    if order <= star.expansionAffectedOrbits:
        stygian.Stygian(star, parentObject, order, orbitType)
        return
        
    roll = roll_xdy(1, 6)
    roll2 = roll_xdy(1, 6)

    # If this planet is part of an asteroid belt
    if (star != parentObject
        and parentObject.group == globalstuff.group.AsteroidBelt
        # If this planet is a companion to another dwarf planet
        # but that dwarf planet is part of an asteroid belt
        or (parentObject.group == globalstuff.group.DwarfPlanet
            and parentObject.parentObject.group == globalstuff.group.AsteroidBelt)):
        roll -= 2

    if orbitType == globalstuff.orbitType.Epistellar:
        create_epistellar_dwarf_planet(star, parentObject, order, orbitType, roll, roll2)
        return
        
    # If this planet is orbiting a helian planet
    if (star != parentObject
        and parentObject.group == globalstuff.group.HelianPlanet
        # If this planet is a companion to another dwarf planet
        # but that dwarf planet is orbiting a helian planet
        or (parentObject.group == globalstuff.group.DwarfPlanet
            and parentObject.parentObject.group == globalstuff.group.HelianPlanet)):
        roll += 1
    # If this planet is orbiting a jovian planet
    elif (star != parentObject
        and parentObject.group == globalstuff.group.JovianPlanet
        # If this planet is a companion to another dwarf planet
        # but that dwarf planet is orbiting a jovian planet
        or (parentObject.group == globalstuff.group.DwarfPlanet
            and parentObject.parentObject.group == globalstuff.group.JovianPlanet)):
        roll += 2

    if orbitType == globalstuff.orbitType.InnerZone:
        create_inner_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2)
    elif orbitType == globalstuff.orbitType.OuterZone:
        create_outer_zone_dwarf_planet(star, parentObject, order, orbitType, roll, roll2)

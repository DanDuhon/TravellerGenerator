from globalstuff import group, roll_xdy
from orbitalbody import OrbitalBody


class AsteroidBelt(OrbitalBody):
    def __init__(self, star, parentObject, order, orbitType):
        super().__init__(star, parentObject, order, orbitType)
        self.group = group.AsteroidBelt
        self.atmosphere = 0
        self.hydrosphere = 0
        self.biosphere = 0
        self.baseDesirability = roll_xdy(1, 6) - roll_xdy(1, 6)

        # Create dwarf planet member of asteroid belt.
        if roll_xdy(1, 6) >= 5:
            self.create_satellite()
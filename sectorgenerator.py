import random
import math
import datetime

import systemhex
import star
import alien

#This is to run all the validation code at the end of this script.
validateResults = True

#input variables
initialSectorSize = 10
openClusterPercent = 50
alienSurvivalPercent = 10
maxTechLevel = 15

def sectorgen(initialSectorSize, openClusterPercent, alienSurvivalPercent, maxTechLevel):
    sectorMax = math.ceil(initialSectorSize / 2)
    sectorMin = math.ceil(initialSectorSize / 2) * -1
    right = (random.random() > 0.5)
    up = (random.random() > 0.5)
    openClusterBorder = math.floor(initialSectorSize * openClusterPercent / 100) - sectorMax
    hexes = {}

    for h in range(sectorMin, sectorMax + 1):
        for v in range(sectorMin, sectorMax + 1):
            openClusterBonus = 0
            if (openClusterBonus == 0
               and right and h >= openClusterBorder
               and up and v >= openClusterBorder):
                openClusterBonus = 3
            if (openClusterBonus == 0
               and not right and h <= openClusterBorder
               and not up and v <= openClusterBorder):
                openClusterBonus = 3
                
            hexes.update({ (h, v): systemhex.System(h, v, openClusterBonus, alienSurvivalPercent, maxTechLevel) })

    validTerraTargets = [ targetStar for targetStar in star.allStars
                          if targetStar.luminosityClass not in [ "D", "M-Ve", "L", "K-III", "M-III" ]
                          and ((targetStar.luminosityClass != "M-V"
                                and targetStar.innerZoneOrbits < 5)
                               or (targetStar.luminosityClass == "M-V"
                                   and targetStar.innerZoneOrbits < 4))
                          and ((targetStar.companions == []
                                and targetStar.primaryOrbit is None)
                               or targetStar.primaryOrbit == "Distant")
                          and targetStar.systemHex.age >= 4 ]
    terraTarget = random.choice(validTerraTargets)

    terra = alien.create_terra_luna_humans(terraTarget, maxTechLevel)
    terra.animals = ["The animals of Earth."]
    luna = terra.satellites[0]
    terraTarget.innerZoneOrbits += 1
    terraTarget.planets.append(terra)
    terraTarget.planets.append(luna)
    terraTarget.systemHex.planets.append(terra)
    terraTarget.systemHex.planets.append(luna)
    for p in terraTarget.planets:
        if p.orbitType == "Outer Zone":
            p.order += 1
        if p.parentObject == p.star:
            p.name = p.parentObject.name + " " + str(p.order)
        else:
            p.name = p.parentObject.name + "-" + str(p.parentObject.satellites.index(p) + 1)

    alien.set_tech_level(maxTechLevel)

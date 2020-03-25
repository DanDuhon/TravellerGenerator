import random
import math
import datetime

import systemhex
import star
import planet
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

    #Now that the initial area has been created, we don't want any more Aliens to survive
    #otherwise this could literally go on forever. Not to mention it would be really hard
    #to introduce a new Alien in the middle of the exploration and colonization phase.
    #You'd pretty much have to back out everything done in this section and start it all
    #over. Every time you get a new one.
    alienSurvivalPercent = 0

    #Determine how far a extinct Aliens at Tech Level 9 expanded
    for a in [ a for a in alien.allAliens if a.techLevel == 9 and a.extinct ]:
        for p in a.homePlanet.systemHex.planets:
            if p in a.colonizedPlanets.values():
                continue
            p.desirability[a] = p.set_desirability(a)
            p.habitation[a] = p.set_habitation(a)

    while True:    
        planetsExplored = set()

        for p in [ p for p in planet.allPlanets if set([ "Colony", "Outpost" ]) <= set(p.habitation.values()) ]:
            p.settlement += 1
        
        for a in [ a for a in alien.allAliens if not a.extinct ]:
            colonizedPlanets = set()
            colonizedPlanets.add(a.colonizedPlanets["Homeworld"])
            colonizedPlanets.update(a.colonizedPlanets["Colony"])
            colonizedPlanets.update(a.colonizedPlanets["Outpost"])
            systemsExplored = set()
            for s in set([ i.systemHex for i in colonizedPlanets ]):
                for x in range(3 + a.aggressionModifier):
                    systemsExplored.update(s.systemsAtRange[x])

            for s in systemsExplored:
                if s not in systemhex.allCoordinates:
                    print("Creating new system at " + str(s[0]) + ", " + str(s[1]) + ".") 
                    hexes.update({ (s[0], s[1]): systemhex.System(s[0], s[1], openClusterBonus, alienSurvivalPercent, maxTechLevel) })
                planetsExplored.update([ (a, p) for p in systemhex.allCoordinates[s].planets if a not in p.desirability.keys() ])

        if len(planetsExplored) == 0:
            break

        planetsExplored = list(planetsExplored)
        random.shuffle(planetsExplored)

        for p in planetsExplored:
            p[1].desirability[p[0]] = p[1].set_desirability(p[0])
            p[1].habitation[p[0]] = p[1].set_habitation(p[0])

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
    #over. Every time you get a new alien.
    alienSurvivalPercent = 0

    #Determine how far extinct Aliens at Tech Level 9 expanded
    for a in [ a for a in alien.allAliens if a.maxTechLevel == 9 and a.extinct ]:
        for p in a.homePlanet.systemHex.planets:
            if p in a.colonizedPlanets.values() or p.alien:
                continue
            p.set_desirability(a)
            p.set_habitation(a)
            if p.habitation[a] is not None:
                a.colonizedPlanets[p.habitation[a]].append(p)

    #Exploration and colonization
    #The current Tech Level of the most advanced aliens start at 9, and
    #each other alien's current Tech Level is also appropriately reduced.
    #Loop through Tech Levels exploring and colonizing until the maxTechLevel
    #is reached by the most advanced aliens and no more new colonies or outposts
    #are created.
    while True:
        while True:
            planetsExplored = set()
            colonyPreCount = 0
            outpostPreCount = 0
            
            for a in [ a for a in alien.allAliens if not a.extinct ]:
                colonyPreCount += len(a.colonizedPlanets["Colony"])
                outpostPreCount += len(a.colonizedPlanets["Outpost"])

            #Increase settlement, which tracks how long a planet has been colonized.
            for p in [ p for p in planet.allPlanets if set([ "Colony", "Outpost" ]) <= set(p.habitation.values()) ]:
                p.settlement += 1

            #Reassess the already colonized planets to see if anything has changed.
            for a in [ a for a in alien.allAliens if not a.extinct and a.currentTechLevel >= 9 ]:
                colonizedPlanets = set()
                colonizedPlanets.update(a.colonizedPlanets["Colony"])
                colonizedPlanets.update(a.colonizedPlanets["Outpost"])
                
                #This is probably where terraforming will go.
                #Reminder to check the comments in the habitation method when terraforming is implemented.
                for p in colonizedPlanets:
                    p.set_desirability(a)
                    p.set_habitation(a)

                colonizedPlanets.add(a.colonizedPlanets["Homeworld"])

                #Get a set of all the systems that may have new colonies.
                systemsExplored = set()
                for s in set([ i.systemHex for i in colonizedPlanets ]):
                    #At TL9, you're restricted to your star system.
                    if a.currentTechLevel == 9:
                        systemsExplored.add((s.horizontalCoord, s.verticalCoord, s.cubeCoord))
                    else:
                        for x in range(3 + a.reactionModifier + (1 if any([ True for p in s.planets if p.habitation[a] == "Colony" ]) else 0)):
                            systemsExplored.update(s.systemsAtRange[x])

                #Create new systems if they don't exist.
                for s in systemsExplored:
                    if (s[0], s[1], s[2]) not in systemhex.allCoordinates:
                        hexes.update({ (s[0], s[1]): systemhex.System(s[0], s[1], openClusterBonus, alienSurvivalPercent, maxTechLevel) })
                    planetsExplored.update([ (a, p) for p in systemhex.allCoordinates[s].planets if a not in p.desirability.keys() or p.habitation[a] == None ])

            #I decided I didn't want a particular alien to always have an advantage because
            #of where they appear in the list, so this randomizes it.
            planetsExplored = list(planetsExplored)
            random.shuffle(planetsExplored)

            #This is used to break out of the loop. If there were no changes in the
            #number of outposts and no changes in the number of colonies, break out
            #of the loop. I admit that there are edge cases that would break the
            #loop early, but for now I accept those.
            colonyPostCount = 0
            outpostPostCount = 0
            for a in [ a for a in alien.allAliens if not a.extinct ]:
                colonyPostCount += len(a.colonizedPlanets["Colony"])
                outpostPostCount += len(a.colonizedPlanets["Outpost"])

            for p in planetsExplored:
                p[1].set_desirability(p[0])
                p[1].set_habitation(p[0])
                if p[1].habitation[p[0]] is not None:
                    p[0].colonizedPlanets[p[1].habitation[p[0]]].append(p[1])

            if colonyPreCount == colonyPostCount and outpostPreCount == outpostPostCount:
                break

        if max([ a.currentTechLevel for a in alien.allAliens if not a.extinct ]) == maxTechLevel:
            break

        for a in [ a for a in alien.allAliens if not a.extinct ]:
            a.currentTechLevel += 1

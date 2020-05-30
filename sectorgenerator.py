import random
import math
import datetime

import systemhex
import star
import planet
import animal
import alien
import tkhex
from diceroller import roll_xdy


def sectorgen(
        initialSectorSize,
        alienSurvivalPercent,
        maxTechLevel):
    sectorMax = math.ceil(initialSectorSize / 2)
    sectorMin = -sectorMax

    for h in range(sectorMin, sectorMax + 1):
        for v in range(sectorMin, sectorMax + 1):
            if (h, v, -h - v) not in systemhex.allCoordinates:
                systemhex.create_normal_system(
                    horizontalCoord=h,
                    verticalCoord=v,
                    alienSurvivalPercent=alienSurvivalPercent,
                    maxTechLevel=maxTechLevel)

    validTerraTargets = [targetStar for targetStar in star.allStars
                         if targetStar.luminosityClass not in ["D", "M-Ve", "L", "K-III", "M-III"]
                         and ((targetStar.luminosityClass != "M-V"
                               and targetStar.innerZoneOrbits < 5)
                              or (targetStar.luminosityClass == "M-V"
                                  and targetStar.innerZoneOrbits < 4))
                         and (targetStar.primaryOrbit is None
                              or targetStar.primaryOrbit == "Distant")
                         and "Close" not in targetStar.companionOrbits
                         and targetStar.systemHex.age >= 4]
    terraTarget = random.choice(validTerraTargets)

    terra = alien.create_terra_luna_humans(terraTarget, maxTechLevel)
    terraTarget.innerZoneOrbits += 1
    for p in terraTarget.planets:
        if p.orbitType == "Outer Zone":
            p.order += 1
            p.name = p.parentObject.name + " " + str(p.order)

            for s1 in p.satellites:
                s1.order += 1
                s1.name = s1.parentObject.name + "-" + str(s1.parentObject.satellites.index(s1) + 1)
                for s2 in s1.satellites:
                    s2.order += 1
                    s2.name = s2.parentObject.name + "-" + str(s2.parentObject.satellites.index(s2) + 1)
                    for s3 in s2.satellites:
                        s3.order += 1
                        s3.name = s3.parentObject.name + "-" + str(s3.parentObject.satellites.index(s3) + 1)
                        for s4 in s3.satellites:
                            s4.order += 1
                            s4.name = s4.parentObject.name + "-" + str(s4.parentObject.satellites.index(s4) + 1)

    alien.set_tech_level(maxTechLevel)
    maxReactionModifier = max(
        [a.reactionModifier for a in alien.allAliens if not a.extinct])
    for a in [a for a in alien.allAliens if not a.extinct]:
        a.homePlanet.systemHex.create_surrounding_systems(
            alienSurvivalPercent,
            maxTechLevel,
            maxReactionModifier)

    # Now that the initial area has been created, we don't want any more Aliens to survive
    # otherwise this could literally go on forever. Not to mention it would be really hard
    # to introduce a new Alien in the middle of the exploration and colonization phase.
    # You'd pretty much have to back out everything done in this section and start it all
    # over. Every time you get a new alien.
    alienSurvivalPercent = 0

    # Determine how far extinct Aliens at Tech Level 9 expanded
    for a in [a for a in alien.allAliens if a.maxTechLevel == 9 and a.extinct]:
        for p in a.homePlanet.systemHex.planets:
            a.planets[p] = {
                "outpostRoll": roll_xdy(1, 6),
                "colonyRoll": roll_xdy(2, 6),
                "desirability": None,
                "habitation": None}
            a.planets[p]["desirability"] = p.calculate_desirability(a, True)
            a.planets[p]["habitation"] = p.calculate_habitation(
                a,
                alienSurvivalPercent,
                maxTechLevel,
                maxReactionModifier,
                True)

    # Exploration and colonization
    # The current Tech Level of the most advanced aliens start at 9, and
    # each other alien's current Tech Level is also appropriately reduced.
    # Loop through Tech Levels exploring and colonizing until the maxTechLevel
    # is reached by the most advanced aliens and no more new colonies or outposts
    # are created.
    while True:
        while True:
            aliensExploring = []

            for p in [p for p in planet.allPlanets if {"Outpost", "Colony"} & set(p.habitation.values())]:
                p.settlement += 1

            for a in [a for a in alien.allAliens if not a.extinct and a.currentTechLevel >= 9]:
                preExplored = len(a.exploredSystems)
                preHabitations = {}
                postHabitations = {}
                for p in a.planets:
                    preHabitations[p] = a.planets[p]["habitation"]

                systemsToExplore = set()
                colonizedSystems = set()
                maxRange = a.currentTechLevel - 9
                alreadyChecked = []

                # Check for systems in which to create an Outpost (this can also create a Colony)
                # Outposts need the support of a Colony within 1 Jump
                for p in a.planets:
                    if a.planets[p]["habitation"] in ["Colony", "Homeworld"]:
                        colonizedSystems.add(p.systemHex)

                for sys in colonizedSystems:
                    if not sys.planets or sys in alreadyChecked:
                        continue
                    alreadyChecked.append(sys)
                    for k in range(1, maxRange + 1):
                        for x in range(-k, k + 1):
                            for y in range(max(-k, -x - k), min(k, -x + k) + 1):
                                newSystem = systemhex.allCoordinates[(sys.coordinates[0] + x, sys.coordinates[1] + y, ((sys.coordinates[0] + x) * -1) - (sys.coordinates[1] + y))]
                                if newSystem not in a.exploredSystems:
                                    for p in newSystem.planets:
                                        a.planets[p] = {"outpostRoll": roll_xdy(1, 6),
                                                        "colonyRoll": roll_xdy(2, 6),
                                                        "desirability": None,
                                                        "habitation": None}
                                        a.planets[p]["desirability"] = p.calculate_desirability(a, False)
                                        a.planets[p]["habitation"] = p.calculate_habitation(
                                            a,
                                            alienSurvivalPercent,
                                            maxTechLevel,
                                            maxReactionModifier,
                                            False)
                                    a.exploredSystems.add(newSystem)
                                else:
                                    for p in newSystem.planets:
                                        a.planets[p]["desirability"] = p.calculate_desirability(a, False)
                                        a.planets[p]["habitation"] = p.calculate_habitation(
                                            a,
                                            alienSurvivalPercent,
                                            maxTechLevel,
                                            maxReactionModifier,
                                            False)

                # Check for systems in which to create a Colony (this cannot create an Outpost)
                # Colonies should be self-sufficient, therefore can be farther
                # out
                for p in a.planets:
                    if a.planets[p]["habitation"]:
                        systemsToExplore.add(p.systemHex)

                systemsToCheck = systemsToExplore.copy()
                for _ in range(1, 4 + a.reactionModifier):
                    newSystemsToCheck = []
                    for sys in systemsToCheck:
                        if not sys.planets or sys in alreadyChecked:
                            continue
                        alreadyChecked.append(newSystem)
                        for k in range(maxRange):
                            for x in range(-k, k + 1):
                                for y in range(max(-k, -x - k), min(k, -x + k) + 1):
                                    newSystem = systemhex.allCoordinates[(sys.coordinates[0] + x, sys.coordinates[1] + y, ((sys.coordinates[0] + x) * -1) - (sys.coordinates[1] + y))]
                                    if newSystem.fuelAvailable:
                                        newSystemsToCheck.append(newSystem)
                                    if newSystem not in a.exploredSystems:
                                        for p in newSystem.planets:
                                            a.planets[p] = {"outpostRoll": roll_xdy(1, 6),
                                                            "colonyRoll": roll_xdy(2, 6),
                                                            "desirability": None,
                                                            "habitation": None}
                                            a.planets[p]["desirability"] = p.calculate_desirability(a, False)
                                            a.planets[p]["habitation"] = p.calculate_habitation(
                                                a,
                                                alienSurvivalPercent,
                                                maxTechLevel,
                                                maxReactionModifier,
                                                True)
                                        a.exploredSystems.add(newSystem)
                                    else:
                                        for p in newSystem.planets:
                                            a.planets[p]["desirability"] = p.calculate_desirability(a, False)
                                            a.planets[p]["habitation"] = p.calculate_habitation(
                                                a,
                                                alienSurvivalPercent,
                                                maxTechLevel,
                                                maxReactionModifier,
                                                True)
                    systemsToCheck = newSystemsToCheck

                for p in a.planets:
                    postHabitations[p] = a.planets[p]["habitation"]
                postExplored = len(a.exploredSystems)

                if preExplored != postExplored or postHabitations != preHabitations:
                    aliensExploring.append(a)

            if not len(aliensExploring):
                break

        if max([a.currentTechLevel for a in alien.allAliens if not a.extinct]) == maxTechLevel:
            break

        for a in [a for a in alien.allAliens if not a.extinct]:
            a.currentTechLevel += 1

    # Create the uninhabited space beyond the frontier.
    existingSystems = systemhex.allSystems.copy()
    for s in existingSystems:
        s.create_surrounding_systems(
            alienSurvivalPercent,
            maxTechLevel,
            maxReactionModifier)

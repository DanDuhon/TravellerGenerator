import random
import math
import copy

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

    alien.create_terra_luna_humans(terraTarget, maxTechLevel)
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
            if p.category in ["Jovian", "Asteroid Belt"]:
                a.planets[p]["desirability"] = p.calculate_desirability_jovian_asteroid_belt(a, True)
            else:
                a.planets[p]["desirability"] = p.calculate_desirability(a, True)
            a.planets[p]["habitation"] = p.calculate_habitation(
                a,
                alienSurvivalPercent,
                maxTechLevel,
                maxReactionModifier,
                True)
            p.habitation[a] = a.planets[p]["habitation"]

    # Turn all inhabited planets of extinct aliens to None and add ruins.
    for a in [a for a in alien.allAliens if a.extinct]:
        for p in [p for p in a.planets if a.planets[p]["habitation"]]:
            a.planets[p]["habitation"] = None
            p.habitation[a] = None
            p.terraformingAlien = None
            p.ruins.add(a)

    # Exploration, colonization, and terraforming
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

                terraformingOccurred = False
                
                if (not p.terraformingDone
                    and p.orbitType == "Inner Zone"
                    and 1 <= p.size <= 11
                    and 1 <= p.atmosphere <= 13
                    and p.hydrosphere < 15
                    and p.category not in ["Stygian", "Acheronian", "Asphodelian"]):
                    p.terraformingPoints = -15 + p.settlement + p.terraformingAlien.currentTechLevel
                    if (p.groupName == "Dwarf"
                        and not p.terraformingDone
                        and p.terraformingPoints > p.terraformingPointsUsed):
                        terraformingOccurred = p.terraform_planet(p.terraformingAlien)
                        if terraformingOccurred:
                            p.terraformingPointsUsed += 1
                    elif (p.groupName == "Terrestrial"
                        and not p.terraformingDone
                        and p.terraformingPoints - p.terraformingPointsUsed >= 2):
                        terraformingOccurred = p.terraform_planet(p.terraformingAlien)
                        if terraformingOccurred:
                            p.terraformingPointsUsed += 2
                    elif (p.groupName == "Helian"
                        and not p.terraformingDone
                        and p.terraformingPoints - p.terraformingPointsUsed >= 3):
                        terraformingOccurred = p.terraform_planet(p.terraformingAlien)
                        if terraformingOccurred:
                            p.terraformingPointsUsed += 3

                    if terraformingOccurred:
                        for a in [a for a in alien.allAliens if not a.extinct and a.currentTechLevel >= 9]:
                            if not a.planets.get(p) or a.planets[p].get("habitation"):
                                continue

                            previousHabitation = copy.deepcopy(a.planets.get(p).get("habitation")) if a.planets.get(p) else None
                            a.planets[p]["desirability"] = p.calculate_desirability(a, p.systemHex.alienNearbyColony.get(a))
                            a.planets[p]["habitation"] = p.calculate_habitation(
                                a,
                                alienSurvivalPercent,
                                maxTechLevel,
                                maxReactionModifier,
                                p.systemHex.alienNearbyColony.get(a))
                            p.habitation[a] = a.planets[p]["habitation"]

                            # If an alien is in the process of terraforming and they
                            # have made the planet temporarily worse, they won't
                            # abandon it. Otherwise, a lower level of habitation
                            # causes ruins to be present on the planet.
                            if previousHabitation == "Colony" and a.planets[p]["habitation"] != "Colony":
                                p.ruins.add(a)
                            elif previousHabitation and not a.planets[p]["habitation"]:
                                p.ruins.add(a)

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
                
                for p in [p for p in a.planets if a.planets[p]["habitation"] in ["Colony", "Homeworld"]]:
                    colonizedSystems.add(p.systemHex)
                    p.systemHex.set_nearby_colony_systems(a)

                # Check for planets to colonize. Outposts require the support
                # of a non-Asteroid Belt Colony, but Colonies are generally
                # self-sufficient so they can be created farther out.
                for p in a.planets:
                    if a.planets[p]["habitation"]:
                        systemsToExplore.add(p.systemHex)

                newSystem = a.homePlanet.systemHex

                systemsToCheck = systemsToExplore.copy()
                for _ in range(1, 4 + a.reactionModifier):
                    newSystemsToCheck = []
                    for sys in systemsToCheck:
                        if not sys.planets or sys in alreadyChecked:
                            continue
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
                                            if p.category in ["Jovian", "Asteroid Belt"]:
                                                a.planets[p]["desirability"] = p.calculate_desirability_jovian_asteroid_belt(a, p.systemHex.alienNearbyColony.get(a))
                                            else:
                                                a.planets[p]["desirability"] = p.calculate_desirability(a, p.systemHex.alienNearbyColony.get(a))

                                            a.planets[p]["habitation"] = p.calculate_habitation(
                                                a,
                                                alienSurvivalPercent,
                                                maxTechLevel,
                                                maxReactionModifier,
                                                p.systemHex.alienNearbyColony.get(a))
                                            p.habitation[a] = a.planets[p]["habitation"]
                                            
                                            if not p.terraformingAlien and not p.alien:
                                                p.terraformingAlien = a
                                        a.exploredSystems.add(newSystem)
                        alreadyChecked.append(newSystem)
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

            # With new technology, some places are more desirable.
            # Recheck all explored planets when the TL increases.
            for p in a.planets:
                if p.category in ["Jovian", "Asteroid Belt"]:
                    a.planets[p]["desirability"] = p.calculate_desirability_jovian_asteroid_belt(a, p.systemHex.alienNearbyColony.get(a))
                else:
                    a.planets[p]["desirability"] = p.calculate_desirability(a, p.systemHex.alienNearbyColony.get(a))
                a.planets[p]["habitation"] = p.calculate_habitation(
                    a,
                    alienSurvivalPercent,
                    maxTechLevel,
                    maxReactionModifier,
                    p.systemHex.alienNearbyColony.get(a))
                p.habitation[a] = a.planets[p]["habitation"]
                                            
                if not p.terraformingAlien and not p.alien:
                    p.terraformingAlien = a

    # Create the uninhabited space beyond the frontier.
    existingSystems = systemhex.allSystems.copy()
    for s in existingSystems:
        s.create_surrounding_systems(
            alienSurvivalPercent,
            maxTechLevel,
            maxReactionModifier)

import random
import math
import statistics
import copy

import systemhex
import star
import planet
import animal
import alien
import tkhex
from diceroller import roll_xdy


def sectorgen(
        alienSurvivalPercent,
        maxTechLevel):
    # This creates an initial area in which aliens can
    # survive to TL10. The initial area is on the very
    # low end of what the final area will probably be,
    # allowing surviving aliens to be far apart since
    # no aliens created outside this initial area survive.
    if maxTechLevel == 9:
        initialSectorSize = 1
    elif maxTechLevel == 10:
        initialSectorSize = 10
    elif maxTechLevel == 11:
        initialSectorSize = 17
    elif maxTechLevel == 12:
        initialSectorSize = 50
    elif maxTechLevel == 13:
        initialSectorSize = 70
    elif maxTechLevel == 14:
        initialSectorSize = 94
    elif maxTechLevel == 15:
        initialSectorSize = 118
    sectorMax = math.ceil(initialSectorSize / 2)
    sectorMin = -sectorMax

    validTerraTargets = []

    while not validTerraTargets:
        systemhex.allCoordinates = {}
        systemhex.allSystems = []
        star.allStars = []
        planet.allPlanets = []
        animal.allAnimals = []
        alien.allAliens = []

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
    for p in [p for p in terraTarget.systemHex.planets if (p.star == terraTarget
        and p.orbitType == "Outer Zone"
        and p.name not in ["Terra", "Luna"])]:
        p.order += 1

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

    # Set each surviving alien's population modifier. This determines how many individuals
    # make up a population of this species. Put another way, it makes it so that aliens
    # that tend to group up more than humans have populations higher than humans, while
    # aliens that are less likely to group up have lower populations.
    avgRelativePopulation = statistics.mean([a.relativePopulation for a in alien.allAliens if not a.extinct])
    for a in [a for a in alien.allAliens if not a.extinct]:
        a.populationModifier = a.relativePopulation / avgRelativePopulation

    # Determine how far extinct Aliens at Tech Level 9 expanded
    for a in [a for a in alien.allAliens if a.maxTechLevel == 9 and a.extinct]:
        for p in a.homePlanet.systemHex.planets:
            a.planets[p] = {
                "outpostRoll": roll_xdy(1, 6),
                "colonyRoll": roll_xdy(2, 6),
                "desirability": None,
                "habitation": None,
                "population": None}
            if p.category in ["Jovian", "Asteroid Belt"]:
                p.calculate_desirability_jovian_asteroid_belt(a, True)
            else:
                p.calculate_desirability(a, True)
                
            p.calculate_habitation(
                a,
                alienSurvivalPercent,
                maxTechLevel,
                maxReactionModifier,
                True)

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
            for p in [p for p in planet.allPlanets if {"Outpost", "Colony", "Homeworld"} & set(p.habitation.values())]:
                p.planet_population()
                p.planet_government()
                p.planet_law_level()
                newIndustryEffect = p.planet_industry()
                if newIndustryEffect:
                    p.planet_industry_effects()
                p.planet_trade_codes(maxTechLevel)
                p.planet_starport()
                
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
                            if not a.planets.get(p) or not a.planets[p].get("habitation"):
                                continue

                            previousHabitation = copy.deepcopy(a.planets.get(p).get("habitation")) if a.planets.get(p) else None
                            p.calculate_desirability(a, p.systemHex.alienNearbyColony.get(a))
                            p.calculate_habitation(
                                a,
                                alienSurvivalPercent,
                                maxTechLevel,
                                maxReactionModifier,
                                p.systemHex.alienNearbyColony.get(a))

                            # If an alien is in the process of terraforming and they
                            # have made the planet temporarily worse, they won't
                            # abandon it. Otherwise, a lower level of habitation
                            # causes ruins to be present on the planet.
                            if previousHabitation == "Colony" and a.planets[p]["habitation"] == "Outpost":
                                p.ruins.add(a)
                            elif previousHabitation == "Colony" and not a.planets[p]["habitation"]:
                                p.ruins.add(a)
                            elif previousHabitation == "Outpost" and not a.planets[p]["habitation"]:
                                p.ruins.add(a)

                            if previousHabitation and not a.planets[p]["habitation"] and p.terraformingAlien == a:
                                p.terraformingAlien = None
                                
                if (p.seedWithLife
                    and p.terraformingDone
                    and p.biosphere < 11
                    and 1 <= p.size <= 11
                    and 2 <= p.atmosphere <= 13
                    and p.hydrosphere < 15
                    and p.chemistry
                    and "Colony" in p.habitation.values()):
                    p.biosphere += 1
                        

            for a in [a for a in alien.allAliens if not a.extinct and a.currentTechLevel >= 9]:
                preExplored = len(a.exploredSystems)
                preHabitations = {}
                postHabitations = {}
                for p in a.planets:
                    preHabitations[p] = a.planets[p]["habitation"]

                systemsToExplore = set()
                colonizedSystems = set()
                maxRange = a.currentTechLevel - 8
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
                                    if any([newSystem.fuelUnrefinedAvailable, newSystem.fuelRefinedAvailable]):
                                        newSystemsToCheck.append(newSystem)
                                    if newSystem not in a.exploredSystems:
                                        for p in newSystem.planets:
                                            a.planets[p] = {"outpostRoll": roll_xdy(1, 6),
                                                            "colonyRoll": roll_xdy(2, 6),
                                                            "desirability": None,
                                                            "habitation": None,
                                                            "population": 0}
                                            if p.category in ["Jovian", "Asteroid Belt"]:
                                                p.calculate_desirability_jovian_asteroid_belt(a, p.systemHex.alienNearbyColony.get(a))
                                            else:
                                                p.calculate_desirability(a, p.systemHex.alienNearbyColony.get(a))

                                            p.calculate_habitation(
                                                a,
                                                alienSurvivalPercent,
                                                maxTechLevel,
                                                maxReactionModifier,
                                                p.systemHex.alienNearbyColony.get(a))
                                            
                                            if not p.terraformingAlien and p.habitation[a] and not p.alien:
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
                previousHabitation = copy.deepcopy(a.planets.get(p).get("habitation")) if a.planets.get(p) else None
                if p.category in ["Jovian", "Asteroid Belt"]:
                    p.calculate_desirability_jovian_asteroid_belt(a, p.systemHex.alienNearbyColony.get(a))
                else:
                    p.calculate_desirability(a, p.systemHex.alienNearbyColony.get(a))

                p.calculate_habitation(
                    a,
                    alienSurvivalPercent,
                    maxTechLevel,
                    maxReactionModifier,
                    p.systemHex.alienNearbyColony.get(a))
                                            
                if not p.terraformingAlien and p.habitation[a] and not p.alien:
                    p.terraformingAlien = a

    # Set terrain for planets that are still being terraformed.
    for p in [p for p in planet.allPlanets if p.terraformingPointsUsed > 0 and not p.terraformingDone]:
        p.planet_terrain()

    # Worlds that are habitable and have no major pre-existing
    # lifeforms are seeded with life by colonists.
    animalsForSeeding = [(a.planet.chemistry, a.terrain, a) for a in animal.allAnimals if a.reactionModifier < 0]
    for p in [p for p in planet.allPlanets if (1 <= p.size <= 11
            and 2 <= p.atmosphere <= 13
            and p.hydrosphere < 15
            and p.chemistry
            and p.biosphere >= 9
            and not p.animals)
            and "Colony" in p.habitation.values()]:
        for terrain in p.terrain:
            animalList = [a[2] for a in animalsForSeeding if a[0] == p.chemistry and a[1] == terrain]
            p.animals += random.choices(population=animalList, k=3)

    for p in [p for p in planet.allPlanets if {"Outpost", "Colony", "Homeworld"} & set(p.habitation.values())]:
        p.planet_population()
        p.planet_government()
        p.planet_law_level()
        newIndustryEffect = p.planet_industry()
        if newIndustryEffect:
            p.planet_industry_effects()
        p.planet_trade_codes(maxTechLevel)
        p.planet_starport()

    # Create the unexplored space beyond the frontier.
    existingSystems = systemhex.allSystems.copy()
    for s in existingSystems:
        s.create_surrounding_systems(
            alienSurvivalPercent,
            maxTechLevel,
            maxReactionModifier)

    for s in systemhex.allSystems:
        if any([s.fuelUnrefinedAvailable, s.fuelRefinedAvailable]):
            continue

        for p in s.planets:
            if p.chemistry == "Water":
                s.fuelUnrefinedAvailable = True
                break

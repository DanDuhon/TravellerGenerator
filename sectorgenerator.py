import math
import random
import statistics
import copy

import systemhex
import star
import orbitalbody
import animal
import alien
import globalstuff
from globalstuff import category, group, luminosityClass, orbitType, companionOrbit
from globalstuff import chemistry, habitation, roll_xdy, chemistry


groupTerraformingPoints = {
    group.DwarfPlanet: 1,
    group.TerrestrialPlanet: 2,
    group.HelianPlanet: 3
}


def sectorgen():
    # This creates an initial area in which aliens can
    # survive to TL10. The initial area is on the
    # low end of what the final area will probably be,
    # allowing surviving aliens to be far apart since
    # no aliens created outside this initial area survive.
    if globalstuff.maxTechLevel == 9:
        initialSectorSize = 1
    elif globalstuff.maxTechLevel == 10:
        initialSectorSize = 12
    elif globalstuff.maxTechLevel == 11:
        initialSectorSize = 20
    elif globalstuff.maxTechLevel == 12:
        initialSectorSize = 60
    elif globalstuff.maxTechLevel == 13:
        initialSectorSize = 84
    elif globalstuff.maxTechLevel == 14:
        initialSectorSize = 113
    elif globalstuff.maxTechLevel == 15:
        initialSectorSize = 142
    sectorMax = math.ceil(initialSectorSize / 2)
    sectorMin = -sectorMax
    
    validTerraTargets = []

    while not validTerraTargets:
        systemhex.allCoordinates = {}
        systemhex.allSystems = []

        for h in range(sectorMin, sectorMax + 1):
            for v in range(sectorMin, sectorMax + 1):
                if (h, v, -h - v) not in systemhex.allCoordinates:
                    systemhex.create_normal_system(
                        horizontalCoord=h,
                        verticalCoord=v)

        for s in [s for s in systemhex.allSystems if len(s.stars) != s.numberOfStars]:
            s.create_stars()

        validTerraTargets = [
            targetStar for targetStar in star.allStars
            if targetStar.luminosityClass not in [
                luminosityClass.D,
                luminosityClass.M_Ve,
                luminosityClass.L,
                luminosityClass.K_III,
                luminosityClass.M_III
                ]
                and targetStar.innerZoneOrbits < 5 - (1 if targetStar.luminosityClass == luminosityClass.M_V else 0)
                and (targetStar.primaryOrbit is None
                    or targetStar.primaryOrbit == companionOrbit.Distant)
                and companionOrbit.Close not in targetStar.companionOrbits
                and targetStar.systemHex.age >= 4]

    for s in star.allStars:
        s.create_orbital_bodies()
                            
    terraTarget = random.choice(validTerraTargets)

    alien.create_terra_luna_humans(terraTarget)
    terraTarget.innerZoneOrbits += 1
    for p in [p for p in terraTarget.systemHex.planets if (
        p.star == terraTarget
        and p.orbitType == orbitType.OuterZone
        and p.name not in ["Terra", "Luna"])]:
        p.order += 1

    alien.set_tech_level()
    maxReactionModifier = max(
        [a.reactionModifier for a in alien.allAliens if not a.extinct])
    for a in [a for a in alien.allAliens if not a.extinct]:
        a.homePlanet.systemHex.create_surrounding_systems(maxReactionModifier)

    for s in [s for s in systemhex.allSystems if len(s.stars) != s.numberOfStars]:
        s.create_stars()

    # Now that the initial area has been created, we don't want any more Aliens to survive
    # otherwise this could literally go on forever. Not to mention it would be really hard
    # to introduce a new Alien in the middle of the exploration and colonization phase.
    # You'd pretty much have to back out everything done in this section and start it all
    # over. Every time you get a new alien.
    globalstuff.alienSurvivalPercent = 0

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
            d = p.calculate_desirability(a, True)
            p.desirability[a] = d
            a.planets[p]["desirability"] = d
                
            h = p.calculate_habitation(
                a,
                maxReactionModifier,
                True)
                
            p.habitation[a] = h
            a.planets[p]["habitation"] = h

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
    # Loop through Tech Levels exploring and colonizing until the Max Tech Level
    # is reached by the most advanced aliens and no more new colonies or outposts
    # are created.
    while True:
        while True:
            for p in [p for p in orbitalbody.allBodies if {habitation.Outpost, habitation.Colony, habitation.Homeworld} & set(p.habitation.values())]:
                p.set_population()
                p.set_government()
                p.set_law_level()
                newIndustryEffect = p.set_industry()
                if newIndustryEffect:
                    p.set_industry_effects()
                p.set_trade_codes()
                p.set_starport()
                
            aliensExploring = []

            for p in [p for p in orbitalbody.allBodies if p.group != group.AsteroidBelt and {habitation.Outpost, habitation.Colony} & set(p.habitation.values())]:
                p.settlement += 1

                # terraformingOccurred = False
                
                # if (not p.terraformingDone
                #         and p.orbitType == orbitType.InnerZone
                #         and 1 <= p.size <= 11
                #         and 1 <= p.atmosphere <= 13
                #         and p.hydrosphere < 15
                #         and p.category not in [category.Stygian, category.Acheronian, category.Asphodelian]):
                #     p.terraformingPoints = -15 + p.settlement + p.terraformingAlien.currentTechLevel

                # if (not p.terraformingDone
                #         and p.terraformingPoints > p.terraformingPointsUsed >= groupTerraformingPoints[p.group]):
                #     terraformingOccurred = p.terraform_planet(p.terraformingAlien)
                #     if terraformingOccurred:
                #         p.terraformingPointsUsed += groupTerraformingPoints[p.group]
                #         p.set_terrain()

                #     if terraformingOccurred:
                #         for a in [a for a in alien.allAliens if not a.extinct and a.currentTechLevel >= 9]:
                #             if not a.planets.get(p) or not a.planets[p].get("habitation"):
                #                 continue

                #             previousHabitation = copy.deepcopy(a.planets.get(p).get("habitation")) if a.planets.get(p) else None
                #             d = p.calculate_desirability(a, p.systemHex.alienNearbyColony.get(a))
                #             p.desirability[a] = d
                #             a.planets[p]["desirability"] = d
                #             h = p.calculate_habitation(
                #                 a,
                #                 maxReactionModifier,
                #                 p.systemHex.alienNearbyColony.get(a))
                #             p.habitation[a] = h
                #             a.planets[p]["habitation"] = h

                #             # If an alien is in the process of terraforming and they
                #             # have made the planet temporarily worse, they won't
                #             # abandon it. Otherwise, a lower level of habitation
                #             # causes ruins to be present on the planet.
                #             if previousHabitation == habitation.Colony and a.planets[p]["habitation"] == habitation.Outpost:
                #                 p.ruins.add(a)
                #             elif previousHabitation == habitation.Colony and not a.planets[p]["habitation"]:
                #                 p.ruins.add(a)
                #             elif previousHabitation == habitation.Outpost and not a.planets[p]["habitation"]:
                #                 p.ruins.add(a)

                #             if previousHabitation and not a.planets[p]["habitation"] and p.terraformingAlien == a:
                #                 p.terraformingAlien = None
                                
                # if (p.seedWithLife
                #     and p.terraformingDone
                #     and p.biosphere < 11
                #     and 1 <= p.size <= 11
                #     and 2 <= p.atmosphere <= 13
                #     and p.hydrosphere < 15
                #     and p.chemistry
                #     and habitation.Colony in p.habitation.values()):
                #     p.biosphere += 1
                        

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
                
                for p in [p for p in a.planets if a.planets[p]["habitation"] in [habitation.Colony, habitation.Homeworld]]:
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
                                            d = p.calculate_desirability(a, p.systemHex.alienNearbyColony.get(a))
                                            p.desirability[a] = d
                                            a.planets[p]["desirability"] = d

                                            h = p.calculate_habitation(
                                                a,
                                                maxReactionModifier,
                                                p.systemHex.alienNearbyColony.get(a))
                                            p.habitation[a] = h
                                            a.planets[p]["habitation"] = h
                                            
                                            if not p.terraformingAlien and p.habitation[a] and not p.homeAlien:
                                                p.terraformingAlien = a
                                        a.exploredSystems.add(newSystem)
                        alreadyChecked.append(newSystem)
                    systemsToCheck = newSystemsToCheck

                for p in a.planets:
                    postHabitations[p] = a.planets[p]["habitation"]
                postExplored = len(a.exploredSystems)

                if preExplored != postExplored or postHabitations != preHabitations:
                    aliensExploring.append(a)

            if not aliensExploring:
                break

        if max([a.currentTechLevel for a in alien.allAliens if not a.extinct]) == globalstuff.maxTechLevel:
            break

        for a in [a for a in alien.allAliens if not a.extinct]:
            a.currentTechLevel += 1

            # With new technology, some places are more desirable.
            # Recheck all explored planets when the TL increases.
            for p in a.planets:
                previousHabitation = copy.deepcopy(a.planets.get(p).get("habitation")) if a.planets.get(p) else None
                d = p.calculate_desirability(a, p.systemHex.alienNearbyColony.get(a))
                    
                p.desirability[a] = d
                a.planets[p]["desirability"] = d

                h = p.calculate_habitation(
                    a,
                    maxReactionModifier,
                    p.systemHex.alienNearbyColony.get(a))
                p.habitation[a] = h
                a.planets[p]["habitation"] = h
                                            
                if not p.terraformingAlien and p.habitation[a] and not p.homeAlien:
                    p.terraformingAlien = a

    # Set terrain for planets that are still being terraformed.
    for p in [p for p in orbitalbody.allBodies if type(p) != orbitalbody.AsteroidBelt and p.terraformingPointsUsed > 0 and not p.terraformingDone]:
        p.set_terrain()

    # Worlds that are habitable and have no major pre-existing
    # lifeforms are seeded with life by colonists.
    animalsForSeeding = [(a.planet.chemistry, a.terrain, a) for a in animal.allAnimals if a.reactionModifier < 0]
    for p in [p for p in orbitalbody.allBodies if (1 <= p.size <= 11
            and 2 <= p.atmosphere <= 13
            and p.hydrosphere < 15
            and p.chemistry
            and p.biosphere >= 9
            and not p.animals)
            and habitation.Colony in p.habitation.values()]:
        for terrain in p.terrain:
            animalList = [a[2] for a in animalsForSeeding if a[0] == p.chemistry and a[1] == terrain]
            p.animals += random.choices(population=animalList, k=3)

    for p in [p for p in orbitalbody.allBodies if {habitation.Outpost, habitation.Colony, habitation.Homeworld} & set(p.habitation.values())]:
        p.set_population()
        p.set_government()
        p.set_law_level()
        newIndustryEffect = p.set_industry()
        if newIndustryEffect:
            p.set_industry_effects()
        p.set_trade_codes()
        p.set_starport()

    # Create the unexplored space beyond the frontier.
    existingSystems = systemhex.allSystems.copy()
    for s in existingSystems:
        s.create_surrounding_systems(maxReactionModifier)

    for s in [s for s in systemhex.allSystems if len(s.stars) != s.numberOfStars]:
        s.create_stars()

    for s in systemhex.allSystems:
        if any([s.fuelUnrefinedAvailable, s.fuelRefinedAvailable]):
            continue

        for p in s.planets:
            if p.chemistry == chemistry.Water:
                s.fuelUnrefinedAvailable = True
                break

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


def create_initial_area():
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
        print("Finding a suitable star for Terra.")
        systemhex.allCoordinates = {}
        systemhex.allSystems = []

        for h in range(sectorMin, sectorMax + 1):
            for v in range(sectorMin, sectorMax + 1):
                if (h, v, -h - v) not in systemhex.allCoordinates:
                    systemhex.create_normal_system(
                        horizontalCoord=h,
                        verticalCoord=v)

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

    return validTerraTargets


def alien_expansion_tl9(maxReactionModifier):
    for a in [a for a in alien.allAliens if a.maxTechLevel == 9 and a.extinct]:
        for p in a.homePlanet.systemHex.orbitalBodies:
            a.orbitalBodies[p] = {
                "outpostRoll": roll_xdy(1, 6),
                "colonyRoll": roll_xdy(2, 6),
                "desirability": None,
                "habitation": None,
                "population": None}
            d = p.calculate_desirability(a, True)
            p.desirability[a] = d
            a.orbitalBodies[p]["desirability"] = d
                
            h = p.calculate_habitation(
                a,
                maxReactionModifier,
                True)
                
            p.habitation[a] = h
            a.orbitalBodies[p]["habitation"] = h


def set_habitation_properties():
    for p in [p for p in orbitalbody.allBodies if {habitation.Outpost, habitation.Colony, habitation.Homeworld} & set(p.habitation.values())]:
        p.set_population()
        p.set_government()
        p.set_law_level()
        newIndustryEffect = p.set_industry()
        if newIndustryEffect:
            p.set_industry_effects()
        p.set_trade_codes()
        p.set_starport()


def start_terraforming(planetToTerraform, maxReactionModifier):
    planetToTerraform.settlement += 1

    terraformingOccurred = False
    
    for p in orbitalbody.terraformingPlanets:
        if not p.terraformingAlien:
            continue
        
        p.set_terraforming_points()

    if (not planetToTerraform.terraformingDone
            and planetToTerraform.terraformingPoints > planetToTerraform.terraformingPointsUsed >= groupTerraformingPoints[planetToTerraform.group]):
        terraformingOccurred = planetToTerraform.terraform_planet(planetToTerraform.terraformingAlien)
        if terraformingOccurred:
            planetToTerraform.terraformingPointsUsed += groupTerraformingPoints[planetToTerraform.group]
            planetToTerraform.set_terrain()

        if terraformingOccurred:
            for a in [a for a in alien.allAliens if not a.extinct and a.currentTechLevel >= 9]:
                if not a.orbitalBodies.get(planetToTerraform) or not a.orbitalBodies[planetToTerraform].get("habitation"):
                    continue

                previousHabitation = copy.deepcopy(a.orbitalBodies.get(planetToTerraform).get("habitation")) if a.orbitalBodies.get(planetToTerraform) else None
                d = planetToTerraform.calculate_desirability(a, planetToTerraform.systemHex.alienNearbyColony.get(a))
                planetToTerraform.desirability[a] = d
                a.orbitalBodies[planetToTerraform]["desirability"] = d
                h = planetToTerraform.calculate_habitation(
                    a,
                    maxReactionModifier,
                    planetToTerraform.systemHex.alienNearbyColony.get(a))
                planetToTerraform.habitation[a] = h
                a.orbitalBodies[planetToTerraform]["habitation"] = h

                # If an alien is in the process of terraforming and they
                # have made the orbital body temporarily worse, they won't
                # abandon it. Otherwise, a lower level of habitation
                # causes ruins to be present on the orbital body.
                if previousHabitation == habitation.Colony and a.orbitalBodies[planetToTerraform]["habitation"] == habitation.Outpost:
                    planetToTerraform.ruins.add(a)
                elif previousHabitation == habitation.Colony and not a.orbitalBodies[planetToTerraform]["habitation"]:
                    planetToTerraform.ruins.add(a)
                elif previousHabitation == habitation.Outpost and not a.orbitalBodies[planetToTerraform]["habitation"]:
                    planetToTerraform.ruins.add(a)

                if previousHabitation and not a.orbitalBodies[planetToTerraform]["habitation"] and planetToTerraform.terraformingAlien == a:
                    planetToTerraform.terraformingAlien = None
                    
    if (planetToTerraform.seedWithLife
        and planetToTerraform.terraformingDone
        and planetToTerraform.biosphere < 11
        and planetToTerraform.atmosphere >= 2
        and planetToTerraform.chemistry
        and habitation.Colony in planetToTerraform.habitation.values()):
        planetToTerraform.biosphere += 1


def alien_exploration(alien, maxReactionModifier):
    preExplored = len(alien.exploredSystems)
    preHabitations = {}
    postHabitations = {}
    for p in alien.orbitalBodies:
        preHabitations[p] = alien.orbitalBodies[p]["habitation"]

    systemsToExplore = set()
    colonizedSystems = set()
    maxRange = alien.currentTechLevel - 8
    alreadyChecked = []
    
    for p in [p for p in alien.orbitalBodies if alien.orbitalBodies[p]["habitation"] in [habitation.Colony, habitation.Homeworld]]:
        colonizedSystems.add(p.systemHex)
        p.systemHex.set_nearby_colony_systems(alien)

    # Check for orbital bodies to colonize. Outposts require the support
    # of a non-Asteroid Belt Colony, but Colonies are generally
    # self-sufficient so they can be created farther out.
    for p in alien.orbitalBodies:
        if alien.orbitalBodies[p]["habitation"]:
            systemsToExplore.add(p.systemHex)

    newSystem = alien.homePlanet.systemHex

    systemsToCheck = systemsToExplore.copy()
    for _ in range(1, 4 + alien.reactionModifier):
        newSystemsToCheck = []
        for sys in systemsToCheck:
            if not sys.orbitalBodies or sys in alreadyChecked:
                continue
            for k in range(maxRange):
                for x in range(-k, k + 1):
                    for y in range(max(-k, -x - k), min(k, -x + k) + 1):
                        newSystem = systemhex.allCoordinates[(sys.coordinates[0] + x, sys.coordinates[1] + y, ((sys.coordinates[0] + x) * -1) - (sys.coordinates[1] + y))]
                        if any([newSystem.fuelUnrefinedAvailable, newSystem.fuelRefinedAvailable]):
                            newSystemsToCheck.append(newSystem)
                        if newSystem not in alien.exploredSystems:
                            for p in newSystem.orbitalBodies:
                                alien.orbitalBodies[p] = {"outpostRoll": roll_xdy(1, 6),
                                                "colonyRoll": roll_xdy(2, 6),
                                                "desirability": None,
                                                "habitation": None,
                                                "population": 0}
                                d = p.calculate_desirability(alien, p.systemHex.alienNearbyColony.get(alien))
                                p.desirability[alien] = d
                                alien.orbitalBodies[p]["desirability"] = d

                                h = p.calculate_habitation(
                                    alien,
                                    maxReactionModifier,
                                    p.systemHex.alienNearbyColony.get(alien))
                                p.habitation[alien] = h
                                alien.orbitalBodies[p]["habitation"] = h
                                
                                if not p.terraformingAlien and p.habitation[alien] and not p.homeAlien:
                                    p.terraformingAlien = alien
                            alien.exploredSystems.add(newSystem)
            alreadyChecked.append(newSystem)
        systemsToCheck = newSystemsToCheck

    for p in alien.orbitalBodies:
        postHabitations[p] = alien.orbitalBodies[p]["habitation"]
    postExplored = len(alien.exploredSystems)

    if preExplored != postExplored or postHabitations != preHabitations:
        print(alien.name + "s are still exploring.")
        return alien


def advance_tech_level(alien, maxReactionModifier):
    alien.currentTechLevel += 1
    print(alien.name + "s advance to TL" + str(alien.currentTechLevel) + ".")

    # With new technology, some places are more desirable.
    # Recheck all explored orbital bodies when the TL increases.
    for p in alien.orbitalBodies:
        previousHabitation = copy.deepcopy(alien.orbitalBodies.get(p).get("habitation")) if alien.orbitalBodies.get(p) else None
        d = p.calculate_desirability(alien, p.systemHex.alienNearbyColony.get(alien))
            
        p.desirability[alien] = d
        alien.orbitalBodies[p]["desirability"] = d

        h = p.calculate_habitation(
            alien,
            maxReactionModifier,
            p.systemHex.alienNearbyColony.get(alien))
        p.habitation[alien] = h
        alien.orbitalBodies[p]["habitation"] = h
                                    
        if not p.terraformingAlien and p.habitation[alien] and not p.homeAlien:
            p.terraformingAlien = alien


def transplant_animals():
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


def sectorgen():
    validTerraTargets = create_initial_area()
                            
    terraTarget = random.choice(validTerraTargets)

    alien.create_terra_luna_humans(terraTarget)
    terraTarget.innerZoneOrbits += 1
    for p in [p for p in terraTarget.systemHex.orbitalBodies if(
        p.star == terraTarget
        and p.orbitType == orbitType.OuterZone
        and p.name not in ["Terra", "Luna"])]:
        p.order += 1

    print("Humans created. Creating the rest of the worlds in the inital area.")

    alien.set_tech_level()
    maxReactionModifier = max(
        [a.reactionModifier for a in alien.allAliens if not a.extinct])
    for a in [a for a in alien.allAliens if not a.extinct]:
        a.homePlanet.systemHex.create_surrounding_systems(maxReactionModifier)

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
    alien_expansion_tl9(maxReactionModifier=maxReactionModifier)

    # Exploration, colonization, and terraforming
    # The current Tech Level of the most advanced aliens start at 9, and
    # each other alien's current Tech Level is also appropriately reduced.
    # Loop through Tech Levels exploring and colonizing until the Max Tech Level
    # is reached by the most advanced aliens and no more new colonies or outposts
    # are created.
    while True:
        while True:
            set_habitation_properties()
            aliensExploring = []
            
            for p in [p for p in orbitalbody.allBodies if p.group != group.AsteroidBelt and {habitation.Outpost, habitation.Colony} & set(p.habitation.values())]:
                start_terraforming(planetToTerraform=p, maxReactionModifier=maxReactionModifier)

            for a in [a for a in alien.allAliens if not a.extinct and a.currentTechLevel >= 9]:
                alienExploring = alien_exploration(alien=a, maxReactionModifier=maxReactionModifier)
                if alienExploring:
                    aliensExploring.append(alienExploring)

            if not aliensExploring:
                break

        if max([a.currentTechLevel for a in alien.allAliens if not a.extinct]) == globalstuff.maxTechLevel:
            break

        for a in [a for a in alien.allAliens if not a.extinct]:
            advance_tech_level(alien=a, maxReactionModifier=maxReactionModifier)

    # Set terrain for planets that are still being terraformed.
    for p in [p for p in orbitalbody.allBodies if type(p) != orbitalbody.AsteroidBelt and p.terraformingPointsUsed > 0 and not p.terraformingDone]:
        p.set_terrain()

    # Worlds that are habitable and have no major pre-existing
    # lifeforms are seeded with life by colonists.
    transplant_animals()

    set_habitation_properties()

    # Create the unexplored space beyond the frontier.
    existingSystems = systemhex.allSystems.copy()
    for s in existingSystems:
        s.create_surrounding_systems(maxReactionModifier)

    for s in [s for s in systemhex.allSystems if len(s.stars) != s.numberOfStars]:
        s.create_stars()

    for s in systemhex.allSystems:
        if any([s.fuelUnrefinedAvailable, s.fuelRefinedAvailable]):
            continue

        for p in s.orbitalBodies:
            if p.chemistry == chemistry.Water:
                s.fuelUnrefinedAvailable = True
                break

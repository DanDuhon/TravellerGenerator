import inspect

import systemhex
import star
import orbitalbody
import animal
import alien
import globalstuff


def get_info(object):
    infotext = []
    for x in inspect.getmembers(object):
        if x[0].startswith('_'):
            continue
        if inspect.ismethod(x[1]):
            continue
        infotext.append(": ".join(str(i)[:200] for i in x))
    print(*infotext, sep = "\n")
    print("\n")


def validation(maxTechLevel):
    """Validation checks"""
    print("Validation checks...")
    # System Hex
    for sys in systemhex.allSystems:
        if sys.age < 0 or sys.age > 15:
            get_info(sys)
            raise ValueError("Invalid system age: " + str(sys.age))

        if sys.name is None:
            get_info(sys)
            raise ValueError("System without a name.")

        # if [sys.name for sys in systemhex.allSystems].count(sys.name) > 1:
        #     get_info(sys)
        #     raise ValueError("Duplicate name found: " + sys.name)

        # if [p.name for p in orbitalbody.allBodies].count(sys.name) > 1:
        #     get_info(sys)
        #     raise ValueError("Duplicate name found: " + sys.name)

        if sys.numberOfStars != len(sys.stars):
            get_info(sys)
            raise ValueError("Invalid number of stars. numberOfStars = " +
                             str(sys.numberOfStars) +
                             ", actual number of stars: " +
                             str(len(sys.stars)))

    # Star
    for s in star.allStars:
        # if [st.name for st in star.allStars].count(s.name) > 1:
        #     get_info(s.systemHex)
        #     for st in s.systemHex.stars:
        #         if st != s:
        #             get_info(st)
        #     get_info(s)
        #     raise ValueError("Duplicate name found: " + s.name)

        if s in s.systemHex.stars[1:]:
            if ((s.systemHex.stars[0].spectralType == globalstuff.spectralType.F and s.spectralType == globalstuff.spectralType.A)
                or (s.systemHex.stars[0].spectralType == globalstuff.spectralType.G and s.spectralType in [globalstuff.spectralType.F, globalstuff.spectralType.A])
                or (s.systemHex.stars[0].spectralType == globalstuff.spectralType.K and s.spectralType in [globalstuff.spectralType.G, globalstuff.spectralType.F, globalstuff.spectralType.A])
                or (s.systemHex.stars[0].spectralType == globalstuff.spectralType.M and s.spectralType in [globalstuff.spectralType.K, globalstuff.spectralType.G, globalstuff.spectralType.F, globalstuff.spectralType.A])
                    or (s.systemHex.stars[0].spectralType == globalstuff.spectralType.L and s.spectralType != globalstuff.spectralType.L)):
                get_info(s.systemHex)
                for st in s.systemHex.stars:
                    if st != s:
                        get_info(st)
                    get_info(s)
                raise ValueError(
                    "Companion star has a \"lower\" spectral type than the primary star.")

        if ((s.spectralType == globalstuff.spectralType.A and s.systemHex.age <= 2 and s.luminosityClass != globalstuff.luminosityClass.A_V)
            or (s.spectralType == globalstuff.spectralType.A and s.systemHex.age == 3 and s.luminosityClass not in [globalstuff.luminosityClass.F_IV, globalstuff.luminosityClass.K_III, globalstuff.luminosityClass.D])
            or (s.spectralType == globalstuff.spectralType.A and s.systemHex.age >= 4 and s.luminosityClass != globalstuff.luminosityClass.D)
            or (s.spectralType == globalstuff.spectralType.F and s.systemHex.age <= 5 and s.luminosityClass != globalstuff.luminosityClass.F_V)
            or (s.spectralType == globalstuff.spectralType.F and s.systemHex.age == 6 and s.luminosityClass not in [globalstuff.luminosityClass.G_IV, globalstuff.luminosityClass.M_III])
            or (s.spectralType == globalstuff.spectralType.F and s.systemHex.age >= 7 and s.luminosityClass != globalstuff.luminosityClass.D)
            or (s.spectralType == globalstuff.spectralType.G and s.systemHex.age <= 11 and s.luminosityClass != globalstuff.luminosityClass.G_V)
            or (s.spectralType == globalstuff.spectralType.G and 12 <= s.systemHex.age <= 13 and s.luminosityClass not in [globalstuff.luminosityClass.K_IV, globalstuff.luminosityClass.M_III])
            or (s.spectralType == globalstuff.spectralType.G and s.systemHex.age >= 14 and s.luminosityClass != globalstuff.luminosityClass.D)
            or (s.spectralType == globalstuff.spectralType.K and s.luminosityClass != globalstuff.luminosityClass.K_V)
            or (s.spectralType == globalstuff.spectralType.M and s.luminosityClass not in [globalstuff.luminosityClass.M_V, globalstuff.luminosityClass.M_Ve, globalstuff.spectralType.L])
                or (s.spectralType == globalstuff.spectralType.L and s.luminosityClass != globalstuff.spectralType.L)):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(st)
            get_info(s)
            raise ValueError("Invalid luminosity class")

        if s in s.systemHex.stars[1:] and (
                s.primaryOrbit is None or s.primaryOrbit == globalstuff.companionOrbit.Distant) and len(s.systemHex.stars[0].planets) > 0 and len(s.planets) > 0 and s.systemHex.stars[0].planets == s.planets:
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(st)
            get_info(s)
            raise ValueError(
                "Distant or brown dwarf star has the same planets as the primary star.")

        if ((s.luminosityClass in [globalstuff.luminosityClass.D, globalstuff.spectralType.L, globalstuff.luminosityClass.K_III, globalstuff.luminosityClass.M_III] and (s.epistellarOrbits > 0 or sum(
                [1 for p in s.planets if p.orbitType == globalstuff.orbitType.Epistellar]))) or s.epistellarOrbits > 2):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(st)
            get_info(s)
            raise ValueError("Wrong number of epistellar orbits.")

        if ((globalstuff.companionOrbit.Close in s.companionOrbits and s.innerZoneOrbits > 0)
            or (s.luminosityClass == globalstuff.luminosityClass.M_V and s.innerZoneOrbits > 4)
            or (s.luminosityClass == globalstuff.spectralType.L and s.innerZoneOrbits > 2)
                or s.innerZoneOrbits > 5):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(st)
            get_info(s)
            raise ValueError("Wrong number of inner zone orbits.")

        if ((globalstuff.companionOrbit.Moderate in s.companionOrbits and s.outerZoneOrbits > 0)
            or (s.luminosityClass in [globalstuff.luminosityClass.M_V, globalstuff.spectralType.L] and s.outerZoneOrbits > 4)
                or s.outerZoneOrbits > 5):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(st)
            get_info(s)
            raise ValueError("Wrong number of outer zone orbits.")

        if s.epistellarOrbits != sum(
                [1 for p in s.planets if p.orbitType == globalstuff.orbitType.Epistellar and p.parentObject == s]):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(st)
            get_info(s)
            raise ValueError("Wrong number of epistellar planets.")

        if s.innerZoneOrbits != sum(
                [1 for p in s.planets if p.orbitType == globalstuff.orbitType.InnerZone and p.parentObject == s]):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(st)
            get_info(s)
            raise ValueError("Wrong number of inner zone planets.")

        if s.outerZoneOrbits != sum(
                [1 for p in s.planets if p.orbitType == globalstuff.orbitType.OuterZone and p.parentObject == s]):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(st)
            get_info(s)
            raise ValueError("Wrong number of outer zone planets.")

    # Planets
    # These validations cannot currently deal with terraforming, so planets that have been
    # terraformed may look invalid here. I think it was thoroughly tested prior to
    # implementing terraforming so we're probably ok.
    for p in orbitalbody.allBodies:
        # if [pl.name for pl in orbitalbody.allBodies].count(p.name) > 1:
        #     get_info(p.systemHex)
        #     for st in s.systemHex.stars:
        #         if st != p.star:
        #             get_info(st)
        #     get_info(p.star)
        #     get_info(p)
        #     raise ValueError("Duplicate name found: " + p.name)

        if p.group == globalstuff.group.AsteroidBelt and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 1:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if st != p.star:
                    get_info(st)
            get_info(p.star)
            get_info(p)
            raise ValueError("Asteroid belt has too many satellites.")

        if p.group == globalstuff.group.DwarfPlanet and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 1:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if st != p.star:
                    get_info(st)
            get_info(p.star)
            get_info(p)
            raise ValueError("Dwarf has too many satellites.")

        if p.group == globalstuff.group.TerrestrialPlanet and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 1:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if st != p.star:
                    get_info(st)
            get_info(p.star)
            get_info(p)
            raise ValueError("Terrestrial has too many satellites.")

        if p.group == globalstuff.group.HelianPlanet and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 3:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if st != p.star:
                    get_info(st)
            get_info(p.star)
            get_info(p)
            raise ValueError("Helian has too many satellites.")

        if p.group == globalstuff.group.JovianPlanet and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 6:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if st != p.star:
                    get_info(st)
            get_info(p.star)
            get_info(p)
            raise ValueError("Jovian has too many satellites.")

        if p.star.luminosityClass in [
            globalstuff.luminosityClass.D, globalstuff.luminosityClass.K_III, globalstuff.luminosityClass.M_III] and p.order <= p.star.expansionAffectedOrbits:
            if (p.group == globalstuff.group.DwarfPlanet and p.category != globalstuff.category.Stygian
                or p.group == globalstuff.group.TerrestrialPlanet and p.category != globalstuff.category.Acheronian
                or p.group == globalstuff.group.HelianPlanet and p.category != globalstuff.category.Asphodelian
                or p.group == globalstuff.group.JovianPlanet and p.category != globalstuff.category.Chthonian):
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError(
                    "Planet should have category determined by star, but category is wrong.")

        if p.star.luminosityClass not in [
                globalstuff.luminosityClass.D, globalstuff.luminosityClass.K_III, globalstuff.luminosityClass.M_III] or p.order > p.star.expansionAffectedOrbits:
            if ((p.group == globalstuff.group.DwarfPlanet and p.category == globalstuff.category.Stygian)
                or (p.group == globalstuff.group.TerrestrialPlanet and p.category == globalstuff.category.Acheronian)
                or (p.group == globalstuff.group.HelianPlanet and p.orbitType != globalstuff.orbitType.Epistellar and p.category == globalstuff.category.Asphodelian)
                or (p.group == globalstuff.group.JovianPlanet and p.orbitType != globalstuff.orbitType.Epistellar and p.category == globalstuff.category.Chthonian)):
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError(
                    "Planet should NOT have category determined by star, but category is wrong.")

            if p.group == globalstuff.group.DwarfPlanet:
                if p.orbitType == globalstuff.orbitType.Epistellar:
                    if p.parentObject != p.star and p.parentObject.group == globalstuff.group.AsteroidBelt:
                        if p.category in [globalstuff.category.Hebean, globalstuff.category.Promethean]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if st != p.star:
                                    get_info(st)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Epistellar dwarf planet in an asteroid belt has an invalid category.")

                    if p.category not in [
                            globalstuff.category.Rockball, globalstuff.category.Meltball, globalstuff.category.Hebean, globalstuff.category.Promethean]:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if st != p.star:
                                get_info(st)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError(
                            "Epistellar dwarf planet has an invalid category.")
                elif p.orbitType == globalstuff.orbitType.InnerZone:
                    if p.parentObject != p.star and p.parentObject.group == globalstuff.group.AsteroidBelt:
                        if p.category in [globalstuff.category.Hebean, globalstuff.category.Promethean]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if st != p.star:
                                    get_info(st)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Inner zone dwarf planet in an asteroid belt has an invalid category.")

                    if p.category not in [
                        globalstuff.category.Rockball,
                        globalstuff.category.Meltball,
                        globalstuff.category.Hebean,
                        globalstuff.category.Promethean,
                        globalstuff.category.Arean]:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if st != p.star:
                                get_info(st)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError(
                            "Inner zone dwarf planet has an invalid category.")
                elif p.orbitType == globalstuff.orbitType.OuterZone:
                    if p.parentObject != p.star and p.parentObject.group == globalstuff.group.AsteroidBelt:
                        if p.category in [
                                globalstuff.category.Hebean, globalstuff.category.Promethean, globalstuff.category.Arean, globalstuff.category.Meltball]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if st != p.star:
                                    get_info(st)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Outer zone dwarf planet in an asteroid belt has an invalid category.")

                    if p.category not in [
                        globalstuff.category.Rockball,
                        globalstuff.category.Meltball,
                        globalstuff.category.Hebean,
                        globalstuff.category.Promethean,
                        globalstuff.category.Arean,
                        globalstuff.category.Snowball]:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if st != p.star:
                                get_info(st)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError(
                            "Outer zone dwarf planet has an invalid category.")

            if p.group == globalstuff.group.TerrestrialPlanet:
                if p.orbitType == globalstuff.orbitType.Epistellar and p.category not in [
                        globalstuff.category.JaniLithic, globalstuff.category.Vesperian, globalstuff.category.Telluric]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Epistellar terrestrial planet has an invalid category.")
                if p.orbitType == globalstuff.orbitType.InnerZone and p.category not in [
                        globalstuff.category.Telluric, globalstuff.category.Arid, globalstuff.category.Tectonic, globalstuff.category.Oceanic]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Inner zone terrestiral planet has an invalid category.")
                if p.orbitType == globalstuff.orbitType.OuterZone:
                    if p.parentObject == p.star:
                        if p.category not in [globalstuff.category.Arid, globalstuff.category.Tectonic]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if st != p.star:
                                    get_info(st)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Outer zone terrestrial planet has an invalid category.")
                    else:
                        if p.category not in [globalstuff.category.Arid, globalstuff.category.Tectonic, globalstuff.category.Oceanic]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if st != p.star:
                                    get_info(st)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Outer zone terrestrial planet has an invalid category.")

            if p.group == globalstuff.group.HelianPlanet:
                if p.orbitType == globalstuff.orbitType.Epistellar and p.category not in [
                        globalstuff.category.Helian, globalstuff.category.Asphodelian]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Epistellar helian planet has an invalid category.")
                if p.orbitType == globalstuff.orbitType.InnerZone and p.category not in [
                        globalstuff.category.Helian, globalstuff.category.Panthalassic]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Inner zone helian planet has an invalid category.")
                if p.orbitType == globalstuff.orbitType.OuterZone and p.category != globalstuff.category.Helian:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Outer zone helian planet has an invalid category.")

            if p.group == globalstuff.group.JovianPlanet:
                if p.orbitType == globalstuff.orbitType.Epistellar and p.category not in [
                        globalstuff.category.Jovian, globalstuff.category.Chthonian]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Epistellar jovian planet has an invalid category.")
                if p.orbitType == globalstuff.orbitType.InnerZone and p.category != globalstuff.category.Jovian:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Inner zone jovian planet has an invalid category.")
                if p.orbitType == globalstuff.orbitType.OuterZone and p.category != globalstuff.category.Jovian:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Outer zone jovian planet has an invalid category.")

        # Animals on planets
        if p.group != globalstuff.group.JovianPlanet and p.biosphere >= 9 and len(p.animals) == 0:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if st != p.star:
                    get_info(st)
            get_info(p.star)
            get_info(p)
            raise ValueError("Planet should have animals but doesn't.")

        # Aliens on planets
        if p.group != globalstuff.group.JovianPlanet and p.biosphere == 12 and p.homeAlien is None:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if st != p.star:
                    get_info(st)
            get_info(p.star)
            get_info(p)
            raise ValueError("Planet should have alien but doesn't.")

        # Acheronian
        if p.category == globalstuff.category.Acheronian:
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 1:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Arean
        elif p.category == globalstuff.category.Arean:
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere not in [1, 10] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 4 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.atmosphere == 1 and p.hydrosphere > 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [globalstuff.chemistry.Water, globalstuff.chemistry.Ammonia, globalstuff.chemistry.Methane] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.orbitType == globalstuff.orbitType.OuterZone and p.star.luminosityClass == globalstuff.spectralType.L and p.chemistry == globalstuff.chemistry.Water:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.orbitType != globalstuff.orbitType.OuterZone and p.star.luminosityClass != globalstuff.spectralType.L and p.chemistry == globalstuff.chemistry.Methane:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.atmosphere == 1 and (p.biosphere < 0 or p.biosphere > 2) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Arid
        elif p.category == globalstuff.category.Arid:
            if p.size < 0 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.biosphere >= 3 and p.chemistry == globalstuff.chemistry.Water:
                if (p.atmosphere < 2 or p.atmosphere > 9) and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            else:
                if p.atmosphere != 10 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 1 or p.hydrosphere > 3 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [globalstuff.chemistry.Water, globalstuff.chemistry.Ammonia, globalstuff.chemistry.Methane] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.chemistry != globalstuff.chemistry.Water and (
                p.orbitType != globalstuff.orbitType.OuterZone and p.star.luminosityClass not in [
                    globalstuff.luminosityClass.K_V, globalstuff.luminosityClass.M_V, globalstuff.spectralType.L]):
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.chemistry == globalstuff.chemistry.Methane and p.star.luminosityClass not in [
                globalstuff.luminosityClass.M_V,
                globalstuff.spectralType.L] and (
                (p.star.luminosityClass != globalstuff.luminosityClass.K_V and p.orbitType == globalstuff.orbitType.OuterZone) or (
                    p.star.luminosityClass == globalstuff.luminosityClass.K_V and p.orbitType != globalstuff.orbitType.OuterZone)) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass == globalstuff.luminosityClass.D:
                if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 12 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Asphodelian
        elif p.category == globalstuff.category.Asphodelian:
            if p.size < 10 or p.size > 15:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 1:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Chthonian
        elif p.category == globalstuff.category.Chthonian:
            if p.size != 16:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 1:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Hebean
        elif p.category == globalstuff.category.Hebean:
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere not in [0, 1, 10] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 6 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Helian
        elif p.category == globalstuff.group.HelianPlanet:
            if p.size < 10 or p.size > 15:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 13 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if (p.hydrosphere < 0 or p.hydrosphere in [
                    12, 13, 14] or p.hydrosphere > 15) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Jani-Lithic
        elif p.category == globalstuff.category.JaniLithic:
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere not in [1, 10] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Jovian
        elif p.category == globalstuff.group.JovianPlanet:
            if p.size != 16:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 16:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 16:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [globalstuff.chemistry.Water, globalstuff.chemistry.Ammonia, None]:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere > 0 and p.chemistry not in [globalstuff.chemistry.Water, globalstuff.chemistry.Ammonia]:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere in [0, None] and p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.systemHex.age > 6:
                if p.star.luminosityClass == globalstuff.luminosityClass.D and (
                        p.biosphere < 0 or p.biosphere > 9):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
                if p.star.luminosityClass != globalstuff.luminosityClass.D and (
                        p.biosphere < 0 or p.biosphere > 12):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Meltball
        elif p.category == globalstuff.category.Meltball:
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 1:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 15:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Oceanic
        elif p.category == globalstuff.category.Oceanic:
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.chemistry == globalstuff.chemistry.Water:
                if p.atmosphere < 0 or p.atmosphere > 12 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            else:
                if p.atmosphere not in [1, 10, 12] and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 11 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [globalstuff.chemistry.Water, globalstuff.chemistry.Ammonia, globalstuff.chemistry.Methane] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass in [
                    globalstuff.luminosityClass.M_V, globalstuff.spectralType.L] and p.orbitType == globalstuff.orbitType.OuterZone and p.chemistry == globalstuff.chemistry.Water and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass not in [
                    globalstuff.luminosityClass.K_V,
                    globalstuff.luminosityClass.M_V,
                    globalstuff.spectralType.L] and p.orbitType != globalstuff.orbitType.OuterZone and p.chemistry in [
                    globalstuff.chemistry.Ammonia,
                    globalstuff.chemistry.Methane] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.chemistry == globalstuff.chemistry.Methane and (
                p.star.luminosityClass not in [
                    globalstuff.luminosityClass.M_V,
                    globalstuff.spectralType.L] and (
                    p.star.luminosityClass != globalstuff.luminosityClass.K_V or p.orbitType != globalstuff.orbitType.OuterZone)) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            elif p.star.systemHex.age >= 4 + p.ageModifier:
                if p.star.luminosityClass == globalstuff.luminosityClass.D:
                    if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if st != p.star:
                                get_info(st)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
                else:
                    if globalstuff.luminosityClass.M_Ve not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if st != p.star:
                                get_info(st)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
        # Panthalassic
        elif p.category == globalstuff.category.Panthalassic:
            if p.size < 10 or p.size > 15:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if (p.atmosphere < 9 or p.atmosphere > 13) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 11 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [
                globalstuff.chemistry.Water,
                globalstuff.chemistry.Ammonia,
                globalstuff.chemistry.Methane,
                globalstuff.chemistry.Sulfur,
                globalstuff.chemistry.Chlorine]:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass not in [
                    globalstuff.luminosityClass.K_V,
                    globalstuff.luminosityClass.M_V,
                    globalstuff.spectralType.L] and (
                    p.chemistry == globalstuff.chemistry.Methane or p.ageModifier != 0) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass not in [
                    globalstuff.luminosityClass.M_V, globalstuff.spectralType.L] and p.ageModifier == 3:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.systemHex.age >= 4 + p.ageModifier:
                if globalstuff.luminosityClass.M_Ve not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Promethean
        elif p.category == globalstuff.category.Promethean:
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.biosphere >= 3 and p.chemistry == globalstuff.chemistry.Water:
                if p.atmosphere < 2 or p.atmosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            else:
                if p.atmosphere != 10 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 10 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [globalstuff.chemistry.Water, globalstuff.chemistry.Ammonia, globalstuff.chemistry.Methane] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass != globalstuff.spectralType.L and p.orbitType == globalstuff.orbitType.Epistellar and p.chemistry != globalstuff.chemistry.Water:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass != globalstuff.spectralType.L and p.orbitType != globalstuff.orbitType.OuterZone and p.chemistry == globalstuff.chemistry.Methane and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            elif p.star.systemHex.age >= 4 + p.ageModifier:
                if p.star.luminosityClass == globalstuff.luminosityClass.D:
                    if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if st != p.star:
                                get_info(st)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
                else:
                    if globalstuff.luminosityClass.M_Ve not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if st != p.star:
                                get_info(st)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Rockball
        elif p.category == globalstuff.category.Rockball:
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.star.luminosityClass == globalstuff.spectralType.L:
                if p.orbitType == globalstuff.orbitType.Epistellar and (
                        p.hydrosphere < 0 or p.hydrosphere > 5):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid hydrosphere.")
                elif p.orbitType == globalstuff.orbitType.OuterZone and (p.hydrosphere < 0 or p.hydrosphere > 9):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid hydrosphere.")
            else:
                if p.orbitType == globalstuff.orbitType.Epistellar and (
                        p.hydrosphere < 0 or p.hydrosphere > 4):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid hydrosphere.")
                elif p.orbitType == globalstuff.orbitType.OuterZone and (p.hydrosphere < 0 or p.hydrosphere > 8):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Snowball
        elif p.category == globalstuff.category.Snowball:
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere not in [0, 1] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 10 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [globalstuff.chemistry.Water, globalstuff.chemistry.Ammonia, globalstuff.chemistry.Methane] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.orbitType != globalstuff.orbitType.OuterZone and p.star.luminosityClass != globalstuff.spectralType.L and p.chemistry == globalstuff.chemistry.Methane and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if not p.subsurfaceOceans and p.biosphere > 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.star.systemHex.age >= 6 + p.ageModifier:
                if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
        # Stygian
        elif p.category == globalstuff.category.Stygian:
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Tectonic
        elif p.category == globalstuff.category.Tectonic:
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.biosphere >= 3 and p.chemistry == globalstuff.chemistry.Water:
                if p.atmosphere < 2 or p.atmosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            elif p.biosphere >= 3 and p.chemistry in [globalstuff.chemistry.Sulfur, globalstuff.chemistry.Chlorine] and p.atmosphere != 11 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            elif (p.biosphere < 3 or p.chemistry != globalstuff.chemistry.Water) and (p.biosphere < 3 or p.chemistry not in [globalstuff.chemistry.Sulfur, globalstuff.chemistry.Chlorine]) and p.terraformingPointsUsed == 0:
                if p.atmosphere != 10:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 10 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [
                globalstuff.chemistry.Water,
                globalstuff.chemistry.Ammonia,
                globalstuff.chemistry.Methane,
                globalstuff.chemistry.Sulfur,
                globalstuff.chemistry.Chlorine]:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.systemHex.age >= 4 + p.ageModifier:
                if p.star.luminosityClass == globalstuff.luminosityClass.D:
                    if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if st != p.star:
                                get_info(st)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
                else:
                    if globalstuff.luminosityClass.M_Ve not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if st != p.star:
                                get_info(st)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Telluric
        elif p.category == globalstuff.category.Telluric:
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 12 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere not in [0, 15] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Vesperian
        elif p.category == globalstuff.category.Vesperian:
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.biosphere >= 3 and p.chemistry == globalstuff.chemistry.Water:
                if p.atmosphere < 2 or p.atmosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            elif p.biosphere >= 3 and p.chemistry == globalstuff.chemistry.Chlorine and p.atmosphere != 11 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            elif p.biosphere < 3 or p.chemistry not in [globalstuff.chemistry.Water, globalstuff.chemistry.Chlorine] and p.terraformingPointsUsed == 0:
                if p.atmosphere != 10:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 10 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [globalstuff.chemistry.Water, globalstuff.chemistry.Chlorine] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.systemHex.age >= 4:
                if globalstuff.luminosityClass.M_Ve not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if st != p.star:
                            get_info(st)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if st != p.star:
                        get_info(st)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")

    # Animals
    for a in animal.allAnimals:
        # if [ an.name for an in animal.allAnimals ].count(a.name) > 1:
        #    badAnimal = a
        #    print("Duplicate name found: " + a.name)

        if a.terrain not in a.planet.terrain:
            get_info(a.planet)
            get_info(a)
            raise ValueError("Terrain doesn't exist on the planet.")

        if a.strength < 1:
            get_info(a.planet)
            get_info(a)
            raise ValueError("Invalid strength.")
        if a.dexterity < 1:
            get_info(a.planet)
            get_info(a)
            raise ValueError("Invalid dexterity.")
        if a.endurance < 1:
            get_info(a.planet)
            get_info(a)
            raise ValueError("Invalid endurance.")
        if a.intelligence < 0 or a.intelligence > 2:
            get_info(a.planet)
            get_info(a)
            raise ValueError("Invalid intelligence.")
        if a.instinct < 1:
            get_info(a.planet)
            get_info(a)
            raise ValueError("Invalid instinct.")
        if a.pack < 0:
            get_info(a.planet)
            get_info(a)
            raise ValueError("Invalid pack.")

        if (globalstuff.terrain.OpenOcean in a.terrain or globalstuff.terrain.DeepOcean in a.terrain) and a.primaryMovement != globalstuff.movement.Swim:
            get_info(a.planet)
            get_info(a)
            raise ValueError("Non-swimmer in the ocean.")

        # Amphibian
        if a.animalClass == globalstuff.animalClass.Amphibian:
            if a.diet == globalstuff.diet.Carnivore:
                validBehaviors = [globalstuff.behavior.Pouncer, globalstuff.behavior.Trapper, globalstuff.behavior.Hunter, globalstuff.behavior.Chaser]
                if "These amphibians emit a natural pheromone that other animals find highly attractive." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Herbivore:
                validBehaviors = [globalstuff.behavior.Filter, globalstuff.behavior.Intermittent, globalstuff.behavior.Grazer]
                if "These amphibians emit a natural pheromone that other animals find highly attractive." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Omnivore:
                validBehaviors = [
                    globalstuff.behavior.CarrionEater,
                    globalstuff.behavior.Gatherer,
                    globalstuff.behavior.Eater,
                    globalstuff.behavior.Hunter,
                    globalstuff.behavior.Intermittent,
                    globalstuff.behavior.Reducer]
                if "These amphibians emit a natural pheromone that other animals find highly attractive." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if "These animals make no sound at all, even when they move in natural surroundings." in a.quirks and a.stealth < 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Amphibian stealth invalid due to quirk.")
            if "Seemingly everywhere, forms of this animal can be found in virtually every habitat type on their world." in a.quirks and a.survival < 1:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Amphibian survival invalid due to quirk.")
            if "These amphibians emit a natural pheromone that other animals find highly attractive." in a.quirks and globalstuff.behavior.Siren not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Amphibian Siren behavior missing.")
        # Aquatic
        if a.animalClass == globalstuff.animalClass.Aquatic:
            if a.diet == globalstuff.diet.Carnivore:
                validBehaviors = [globalstuff.behavior.Eater, globalstuff.behavior.Hunter, globalstuff.behavior.Killer, globalstuff.behavior.Chaser]
                if "Posseses a frail physique and has the ability to engage in extremely swift movement." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Pouncer)
                if not all(
                        b in validBehaviors for b in a.behaviors) and "Posseses a frail physique and has the ability to engage in extremely swift movement." not in a.quirks:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Herbivore:
                validBehaviors = [globalstuff.behavior.Filter, globalstuff.behavior.Intermittent, globalstuff.behavior.Grazer]
                if "Posseses a frail physique and has the ability to engage in extremely swift movement." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Pouncer)
                if not all(
                        b in validBehaviors for b in a.behaviors) and "Posseses a frail physique and has the ability to engage in extremely swift movement." not in a.quirks:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Omnivore:
                validBehaviors = [globalstuff.behavior.CarrionEater, globalstuff.behavior.Eater, globalstuff.behavior.Reducer]
                if "Posseses a frail physique and has the ability to engage in extremely swift movement." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Pouncer)
                if not all(
                        b in validBehaviors for b in a.behaviors) and "Posseses a frail physique and has the ability to engage in extremely swift movement." not in a.quirks:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if a.primaryMovement != globalstuff.movement.Swim:
                get_info(a.planet)
                get_info(a)
                raise ValueError(
                    "Aquatic with a primary movement other than swim.")

            if "This creature is never found alone and will die within 1d6 days of natural causes if it cannot find a pack to join." in a.quirks and a.pack == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Aquatic invalid pack because of quirk.")
            if "Posseses a frail physique and has the ability to engage in extremely swift movement" in a.quirks and (
                    globalstuff.behavior.Pouncer not in a.behaviors or a.armor > 0):
                get_info(a.planet)
                get_info(a)
                raise ValueError(
                    "Aquatic Pouncer behavior missing or it has armor and shouldn't.")
            if "Unlike most aquatics, this species reproduces asexually and is never encountered with others of its kind." in a.quirks and a.pack > 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Aquatic pack too high because of quirk.")
            if "Unusually bright and clever." in a.quirks and (
                    a.instinct < 9 or a.intelligence < 2):
                get_info(a.planet)
                get_info(a)
                raise ValueError(
                    "Aquatic instinct or intelligence is too low.")
        # Avian
        if a.animalClass == globalstuff.animalClass.Avian:
            if a.diet == globalstuff.diet.Carnivore:
                validBehaviors = [globalstuff.behavior.Hunter, globalstuff.behavior.Chaser, globalstuff.behavior.Killer, globalstuff.behavior.Pouncer]
                if "These avians have developed a way to emit calls that sound exactly like the cries of wounded prey, using these to lure meals closer." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if "Not just ground bound, this flightless species thrives because of it." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Chaser)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Herbivore:
                validBehaviors = [globalstuff.behavior.Intimidator, globalstuff.behavior.Intermittent, globalstuff.behavior.Grazer]
                if "These avians have developed a way to emit calls that sound exactly like the cries of wounded prey, using these to lure meals closer." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if "Not just ground bound, this flightless species thrives because of it." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Chaser)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Omnivore:
                validBehaviors = [
                    globalstuff.behavior.CarrionEater,
                    globalstuff.behavior.Eater,
                    globalstuff.behavior.Intimidator,
                    globalstuff.behavior.Reducer]
                if "These avians have developed a way to emit calls that sound exactly like the cries of wounded prey, using these to lure meals closer." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if "Not just ground bound, this flightless species thrives because of it." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Chaser)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if "Extremely social, these animals live in immense flocks." in a.quirks and a.pack < 12:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian pack too low.")
            if ("Quite at home on the ground, this species has evolved away from flight." in a.quirks or "Not just ground bound, this flightless species has no F movement rate and thrives because of it." in a.quirks) and a.primaryMovement != globalstuff.movement.Walk:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian that needs to walk.")
            if "These avians have adapted a very unusual way of dealing with enemies." in a.quirks and len(
                    a.exoticWeapons) == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian missing exotic weapon.")
            if "These avians have developed a way to emit calls that sound exactly like the cries of wounded prey." in a.quirks and globalstuff.behavior.Siren not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian missing Siren.")
            if "Environmental pressures have forced this animal to adapt to a hostile environment." in a.quirks and a.armor == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian missing armor.")
        # Fungal
        if a.animalClass == globalstuff.animalClass.Fungal:
            if a.diet == globalstuff.diet.Carnivore:
                validBehaviors = [globalstuff.behavior.Hunter, globalstuff.behavior.Siren, globalstuff.behavior.Killer]
                if "Though capable of physical movement to attack or defend itself, this Fungal species is stationary and cannot change location. If the base species was herbivorous, it is now specialises in luring other fungals to their doom." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if "Almost liquid in structure, this extremely slimy fungal moves at normal speed and is capable of extremely rapid motion when it hunts." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Pouncer)
                if "The scent and outlandish appearance of this fungal terrifies other animals." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Hijacker)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Herbivore:
                validBehaviors = [globalstuff.behavior.Intermittent, globalstuff.behavior.Grazer]
                if "Though capable of physical movement to attack or defend itself, this Fungal species is stationary and cannot change location. If the base species was herbivorous, it is now specialises in luring other fungals to their doom." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if "Almost liquid in structure, this extremely slimy fungal moves at normal speed and is capable of extremely rapid motion when it hunts." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Pouncer)
                if "The scent and outlandish appearance of this fungal terrifies other animals." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Hijacker)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Omnivore:
                validBehaviors = [globalstuff.behavior.CarrionEater, globalstuff.behavior.Eater, globalstuff.behavior.Reducer]
                if "Though capable of physical movement to attack or defend itself, this Fungal species is stationary and cannot change location. If the base species was herbivorous, it is now specialises in luring other fungals to their doom." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if "Almost liquid in structure, this extremely slimy fungal moves at normal speed and is capable of extremely rapid motion when it hunts." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Pouncer)
                if "The scent and outlandish appearance of this fungal terrifies other animals." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Hijacker)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if "This Fungal is an absolutely bizarre colour and smells rancid." in a.quirks and len(
                    a.exoticWeapons) == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Funal missing exotic weapon.")
            if "The Fungal can inflate itself with a light gas, allowing for a slow form of flight." in a.quirks and a.primaryMovement != globalstuff.movement.Fly:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Fungal should fly.")
            if "Though capable of physical movement to attack or defend itself, this Fungal species is stationary and cannot change location." in a.quirks and (
                    globalstuff.behavior.Siren not in a.behaviors or a.primaryMovement != globalstuff.movement.Stationary):
                get_info(a.planet)
                get_info(a)
                raise ValueError(
                    "Fungal missing Siren or can move and shouldn't.")
            if "This species propagates very quickly and easily, dwelling in large family structures with its progeny." in a.quirks and a.numberEncountered == 1:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Fungal can't be found alone.")
            if "Very soft in bodily structure." in a.quirks and a.armor > 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Fungal shouldn't have armor.")
            if "Almost liquid in structure, this extremely slimy fungal moves at normal speed and is capable of extremely rapid motion when it hunts." in a.quirks and globalstuff.behavior.Pouncer not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Fungal missing Pouncer.")
        # Insect
        if a.animalClass == globalstuff.animalClass.Insect:
            if a.diet == globalstuff.diet.Carnivore:
                validBehaviors = [
                    globalstuff.behavior.Pouncer,
                    globalstuff.behavior.Hunter,
                    globalstuff.behavior.Killer,
                    globalstuff.behavior.Trapper,
                    globalstuff.behavior.Chaser]
                if "The insect can generate a hypnotic drone." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if "Solitary by nature. If the insects are herbivores, they just leave their prey to rot and eat the resulting fungus." in a.quirks:
                    validBehaviors.extend([globalstuff.behavior.Pouncer, globalstuff.behavior.Trapper])
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Herbivore:
                validBehaviors = [
                    globalstuff.behavior.Eater,
                    globalstuff.behavior.Intermittent,
                    globalstuff.behavior.Filter,
                    globalstuff.behavior.Gatherer,
                    globalstuff.behavior.Grazer]
                if "The insect can generate a hypnotic drone." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if "Solitary by nature. If the insects are herbivores, they just leave their prey to rot and eat the resulting fungus." in a.quirks:
                    validBehaviors.extend([globalstuff.behavior.Pouncer, globalstuff.behavior.Trapper])
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Omnivore:
                validBehaviors = [globalstuff.behavior.CarrionEater, globalstuff.behavior.Eater, globalstuff.behavior.Reducer]
                if "The insect can generate a hypnotic drone." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Siren)
                if "Solitary by nature. If the insects are herbivores, they just leave their prey to rot and eat the resulting fungus." in a.quirks:
                    validBehaviors.extend([globalstuff.behavior.Pouncer, globalstuff.behavior.Trapper])
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if "Slow moving because of heavy exoskeleton plating." in a.quirks and a.armor == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Insect missing armor.")
            if "These insects form veritable swarms." in a.quirks and a.pack < 2:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Insect pack too low.")
            if "Solitary by nature." in a.quirks and (
                a.pack > 0 or (
                    (a.primaryMovement == globalstuff.movement.Walk and globalstuff.behavior.Trapper not in a.behaviors) or (
                        a.primaryMovement == globalstuff.movement.Fly and globalstuff.behavior.Pouncer not in a.behaviors))):
                get_info(a.planet)
                get_info(a)
                raise ValueError(
                    "Insect pack too high or missing Pouncer or Trapper.")
            if "Acutely self-aware." in a.quirks and a.intelligence < 2:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Insect intelligence too low.")
            if "These insects have a hive mind." in a.quirks and (
                    a.intelligence < 2 or a.pack < 6):
                get_info(a.planet)
                get_info(a)
                raise ValueError(
                    "Insect intelligence too low or pack too low.")
            if "Evolved in a particularly dangerous habitat, these insects developed an unusual defence." in a.quirks and len(
                    a.exoticWeapons) == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Insect missing exotic weapon.")
            if "The insect can generate a hypnotic drone." in a.quirks and globalstuff.behavior.Siren not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Insect missing Siren.")
        # Mammal
        if a.animalClass == globalstuff.animalClass.Mammal:
            if a.diet == globalstuff.diet.Carnivore:
                validBehaviors = [
                    globalstuff.behavior.Pouncer,
                    globalstuff.behavior.Killer,
                    globalstuff.behavior.Trapper,
                    globalstuff.behavior.Chaser,
                    globalstuff.behavior.Hunter,
                    globalstuff.behavior.Hijacker]
                if "This mammal has an unusual mode of travel, be it gliding or swinging between trees in its home environment." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Pouncer)
                if "Unusually vicious, these mammals are hostile to any species but their own." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Killer)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Herbivore:
                validBehaviors = [
                    globalstuff.behavior.Eater, globalstuff.behavior.Intermittent, globalstuff.behavior.Grazer, globalstuff.behavior.Gatherer]
                if "This mammal has an unusual mode of travel, be it gliding or swinging between trees in its home environment." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Pouncer)
                if "Unusually vicious, these mammals are hostile to any species but their own." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Killer)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Omnivore:
                validBehaviors = [
                    globalstuff.behavior.CarrionEater,
                    globalstuff.behavior.Gatherer,
                    globalstuff.behavior.Hunter,
                    globalstuff.behavior.Intimidator,
                    globalstuff.behavior.Reducer]
                if "This mammal has an unusual mode of travel, be it gliding or swinging between trees in its home environment." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Pouncer)
                if "Unusually vicious, these mammals are hostile to any species but their own." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Killer)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if "This mammal has an unusual mode of travel, be it gliding or swinging between trees in its home environment." in a.quirks and a.diet == globalstuff.diet.Omnivore and globalstuff.behavior.Pouncer not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Mammal missing Pouncer.")

            if "Bright even for its class, these mammals show a devious cunning that borders on compulsive mischief." in a.quirks and (
                    a.stealth == -3 or a.deception == -3):
                get_info(a.planet)
                get_info(a)
                raise ValueError("Mammal should have stealth and deception.")

            if "Profuse body hair marks this species as a sign of its innate adaptability." in a.quirks and a.survival < 1:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Mammal should have survival of at least 1.")

            if "Herd-oriented and nomadic, these are mostly peaceful mammals." in a.quirks and a.pack < 1:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Mammal pack is too low.")

            if "These animals have prodigious horns and know how to use them in combat." in a.quirks and (
                    globalstuff.weapon.Horns not in a.weapons or a.meleeNaturalWeapons == -3):
                get_info(a.planet)
                get_info(a)
                raise ValueError(
                    "Mammal should have horns and a rank in melee natural weapons.")

            if "Unusually vicious, these mammals are hostile to any species but their own." in a.quirks and globalstuff.behavior.Killer not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Mammal missing Killer.")

            if "This animal species is on the verge of evolving into sentience." in a.quirks and (
                    a.intelligence < 2 or a.instinct < 12):
                get_info(a.planet)
                get_info(a)
                raise ValueError("Mammal intelligence or instinct too low.")
        # Reptile
        if a.animalClass == globalstuff.animalClass.Reptile:
            if a.diet == globalstuff.diet.Carnivore:
                validBehaviors = [
                    globalstuff.behavior.Pouncer,
                    globalstuff.behavior.Killer,
                    globalstuff.behavior.Intimidator,
                    globalstuff.behavior.Hunter,
                    globalstuff.behavior.Hijacker]
                if "This reptile buries itself in its terrain, blending in and waiting for prey to ensnare." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Trapper)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Herbivore:
                validBehaviors = [globalstuff.behavior.Gatherer, globalstuff.behavior.Intermittent, globalstuff.behavior.Grazer]
                if "This reptile buries itself in its terrain, blending in and waiting for prey to ensnare." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Trapper)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == globalstuff.diet.Omnivore:
                validBehaviors = [
                    globalstuff.behavior.CarrionEater,
                    globalstuff.behavior.Gatherer,
                    globalstuff.behavior.Hijacker,
                    globalstuff.behavior.Hunter,
                    globalstuff.behavior.Reducer]
                if "This reptile buries itself in its terrain, blending in and waiting for prey to ensnare." in a.quirks:
                    validBehaviors.append(globalstuff.behavior.Trapper)
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

                if "Mottled in appearance and adapted to its surroundings." in a.quirks and a.stealth == -3:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Reptile needs stealth.")

                if "Able to go dormant for long periods of time, these reptiles may go for weeks or even months between meals." in a.quirks and a.survival < 1:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Reptile needs survival.")

                if "An oddity even within an evolutionarily diverse class, this reptile has a very complex genetic history." in a.quirks and len(
                        a.exoticWeapons) < 2:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Reptile missing exotic weapon.")

                if "Relative safety in its environment has allowed this species to evolve mentally." in a.quirks and a.intelligence == 0:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Reptile intelligence too low.")

    # Aliens
    if "Terran" not in [al.name for al in alien.allAliens]:
        raise ValueError("Terrans do not exist.")
    for a in alien.allAliens:
        if [al.name for al in alien.allAliens].count(a.name) > 1:
            raise ValueError("Duplicate alien name found: " + a.name)

        if (not a.extinct and (a.currentTechLevel < 0 or a.currentTechLevel > maxTechLevel)) or (
                a.extinct and (a.currentTechLevel < 0 or a.currentTechLevel > 9)):
            raise ValueError("Alien has invalid tech level.")

    print("All validations passed!")

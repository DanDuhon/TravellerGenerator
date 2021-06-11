import inspect

import systemhex
import star
import planet
import animal
import alien


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

        # if [p.name for p in planet.allPlanets].count(sys.name) > 1:
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
        #             get_info(star)
        #     get_info(s)
        #     raise ValueError("Duplicate name found: " + s.name)

        if s in s.systemHex.stars[1:]:
            if ((s.systemHex.stars[0].spectralType == "F" and s.spectralType == "A")
                or (s.systemHex.stars[0].spectralType == "G" and s.spectralType in ["F", "A"])
                or (s.systemHex.stars[0].spectralType == "K" and s.spectralType in ["G", "F", "A"])
                or (s.systemHex.stars[0].spectralType == "M" and s.spectralType in ["K", "G", "F", "A"])
                    or (s.systemHex.stars[0].spectralType == "L" and s.spectralType != "L")):
                get_info(s.systemHex)
                for st in s.systemHex.stars:
                    if st != s:
                        get_info(star)
                    get_info(s)
                raise ValueError(
                    "Companion star has a \"lower\" spectral type than the primary star.")

        if ((s.spectralType == "A" and s.systemHex.age <= 2 and s.luminosityClass != "A-V")
            or (s.spectralType == "A" and s.systemHex.age == 3 and s.luminosityClass not in ["F-IV", "K-III", "D"])
            or (s.spectralType == "A" and s.systemHex.age >= 4 and s.luminosityClass != "D")
            or (s.spectralType == "F" and s.systemHex.age <= 5 and s.luminosityClass != "F-V")
            or (s.spectralType == "F" and s.systemHex.age == 6 and s.luminosityClass not in ["G-IV", "M-III"])
            or (s.spectralType == "F" and s.systemHex.age >= 7 and s.luminosityClass != "D")
            or (s.spectralType == "G" and s.systemHex.age <= 11 and s.luminosityClass != "G-V")
            or (s.spectralType == "G" and 12 <= s.systemHex.age <= 13 and s.luminosityClass not in ["K-IV", "M-III"])
            or (s.spectralType == "G" and s.systemHex.age >= 14 and s.luminosityClass != "D")
            or (s.spectralType == "K" and s.luminosityClass != "K-V")
            or (s.spectralType == "M" and s.luminosityClass not in ["M-V", "M-Ve", "L"])
                or (s.spectralType == "L" and s.luminosityClass != "L")):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(star)
            get_info(s)
            raise ValueError("Invalid luminosity class")

        if s in s.systemHex.stars[1:] and (
                s.primaryOrbit is None or s.primaryOrbit == "Distant") and len(s.systemHex.stars[0].planets) > 0 and len(s.planets) > 0 and s.systemHex.stars[0].planets == s.planets:
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(star)
            get_info(s)
            raise ValueError(
                "Distant or brown dwarf star has the same planets as the primary star.")

        if ((s.luminosityClass in ["D", "L", "K-III", "M-III"] and (s.epistellarOrbits > 0 or sum(
                [1 for p in s.planets if p.orbitType == "Epistellar"]))) or s.epistellarOrbits > 2):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(star)
            get_info(s)
            raise ValueError("Wrong number of epistellar orbits.")

        if (("Close" in s.companionOrbits and s.innerZoneOrbits > 0)
            or (s.luminosityClass == "M-V" and s.innerZoneOrbits > 4)
            or (s.luminosityClass == "L" and s.innerZoneOrbits > 2)
                or s.innerZoneOrbits > 5):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(star)
            get_info(s)
            raise ValueError("Wrong number of inner zone orbits.")

        if (("Moderate" in s.companionOrbits and s.outerZoneOrbits > 0)
            or (s.luminosityClass in ["M-V", "L"] and s.outerZoneOrbits > 4)
                or s.outerZoneOrbits > 5):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(star)
            get_info(s)
            raise ValueError("Wrong number of outer zone orbits.")

        if s.epistellarOrbits != sum(
                [1 for p in s.planets if p.orbitType == "Epistellar" and p.parentObject == s]):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(star)
            get_info(s)
            raise ValueError("Wrong number of epistellar planets.")

        if s.innerZoneOrbits != sum(
                [1 for p in s.planets if p.orbitType == "Inner Zone" and p.parentObject == s]):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(star)
            get_info(s)
            raise ValueError("Wrong number of inner zone planets.")

        if s.outerZoneOrbits != sum(
                [1 for p in s.planets if p.orbitType == "Outer Zone" and p.parentObject == s]):
            get_info(s.systemHex)
            for st in s.systemHex.stars:
                if st != s:
                    get_info(star)
            get_info(s)
            raise ValueError("Wrong number of outer zone planets.")

    # Planets
    # These validations cannot currently deal with terraforming, so planets that have been
    # terraformed may look invalid here. I think it was thoroughly tested prior to
    # implementing terraforming so we're probably ok.
    for p in planet.allPlanets:
        # if [pl.name for pl in planet.allPlanets].count(p.name) > 1:
        #     get_info(p.systemHex)
        #     for st in s.systemHex.stars:
        #         if star != p.star:
        #             get_info(star)
        #     get_info(p.star)
        #     get_info(p)
        #     raise ValueError("Duplicate name found: " + p.name)

        if p.groupName == "Asteroid Belt" and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 1:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if star != p.star:
                    get_info(star)
            get_info(p.star)
            get_info(p)
            raise ValueError("Asteroid belt has too many satellites.")

        if p.groupName == "Dwarf" and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 1:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if star != p.star:
                    get_info(star)
            get_info(p.star)
            get_info(p)
            raise ValueError("Dwarf has too many satellites.")

        if p.groupName == "Terrestrial" and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 1:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if star != p.star:
                    get_info(star)
            get_info(p.star)
            get_info(p)
            raise ValueError("Terrestrial has too many satellites.")

        if p.groupName == "Helian" and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 3:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if star != p.star:
                    get_info(star)
            get_info(p.star)
            get_info(p)
            raise ValueError("Helian has too many satellites.")

        if p.groupName == "Jovian" and sum(
                [1 for s in p.satellites if s.parentObject == p]) > 6:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if star != p.star:
                    get_info(star)
            get_info(p.star)
            get_info(p)
            raise ValueError("Jovian has too many satellites.")

        if p.star.luminosityClass in [
            "D",
            "K-III",
                "M-III"] and p.order <= p.star.expansionAffectedOrbits:
            if (p.groupName == "Dwarf" and p.category != "Stygian"
                or p.groupName == "Terrestrial" and p.category != "Acheronian"
                or p.groupName == "Helian" and p.category != "Asphodelian"
                or p.groupName == "Jovian" and p.category != "Chthonian"):
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError(
                    "Planet should have category determined by star, but category is wrong.")

        if p.star.luminosityClass not in [
                "D", "K-III", "M-III"] or p.order > p.star.expansionAffectedOrbits:
            if ((p.groupName == "Dwarf" and p.category == "Stygian")
                or (p.groupName == "Terrestrial" and p.category == "Acheronian")
                or (p.groupName == "Helian" and p.orbitType != "Epistellar" and p.category == "Asphodelian")
                or (p.groupName == "Jovian" and p.orbitType != "Epistellar" and p.category == "Chthonian")):
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError(
                    "Planet should NOT have category determined by star, but category is wrong.")

            if p.groupName == "Dwarf":
                if p.orbitType == "Epistellar":
                    if p.parentObject != p.star and p.parentObject.groupName == "Asteroid Belt":
                        if p.category in ["Hebean", "Promethean"]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if star != p.star:
                                    get_info(star)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Epistellar dwarf planet in an asteroid belt has an invalid category.")

                    if p.category not in [
                            "Rockball", "Meltball", "Hebean", "Promethean"]:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if star != p.star:
                                get_info(star)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError(
                            "Epistellar dwarf planet has an invalid category.")
                elif p.orbitType == "Inner Zone":
                    if p.parentObject != p.star and p.parentObject.groupName == "Asteroid Belt":
                        if p.category in ["Hebean", "Promethean"]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if star != p.star:
                                    get_info(star)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Inner zone dwarf planet in an asteroid belt has an invalid category.")

                    if p.category not in [
                        "Rockball",
                        "Meltball",
                        "Hebean",
                        "Promethean",
                        "Arean"]:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if star != p.star:
                                get_info(star)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError(
                            "Inner zone dwarf planet has an invalid category.")
                elif p.orbitType == "Outer Zone":
                    if p.parentObject != p.star and p.parentObject.groupName == "Asteroid Belt":
                        if p.category in [
                                "Hebean", "Promethean", "Arean", "Meltball"]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if star != p.star:
                                    get_info(star)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Outer zone dwarf planet in an asteroid belt has an invalid category.")

                    if p.category not in [
                        "Rockball",
                        "Meltball",
                        "Hebean",
                        "Promethean",
                        "Arean",
                        "Snowball"]:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if star != p.star:
                                get_info(star)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError(
                            "Outer zone dwarf planet has an invalid category.")

            if p.groupName == "Terrestrial":
                if p.orbitType == "Epistellar" and p.category not in [
                        "Jani-Lithic", "Vesperian", "Telluric"]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Epistellar terrestrial planet has an invalid category.")
                if p.orbitType == "Inner Zone" and p.category not in [
                        "Telluric", "Arid", "Tectonic", "Oceanic"]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Inner zone terrestiral planet has an invalid category.")
                if p.orbitType == "Outer Zone":
                    if p.parentObject == p.star:
                        if p.category not in ["Arid", "Tectonic"]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if star != p.star:
                                    get_info(star)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Outer zone terrestrial planet has an invalid category.")
                    else:
                        if p.category not in ["Arid", "Tectonic", "Oceanic"]:
                            get_info(p.systemHex)
                            for st in s.systemHex.stars:
                                if star != p.star:
                                    get_info(star)
                            get_info(p.star)
                            get_info(p)
                            raise ValueError(
                                "Outer zone terrestrial planet has an invalid category.")

            if p.groupName == "Helian":
                if p.orbitType == "Epistellar" and p.category not in [
                        "Helian", "Asphodelian"]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Epistellar helian planet has an invalid category.")
                if p.orbitType == "Inner Zone" and p.category not in [
                        "Helian", "Panthalassic"]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Inner zone helian planet has an invalid category.")
                if p.orbitType == "Outer Zone" and p.category != "Helian":
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Outer zone helian planet has an invalid category.")

            if p.groupName == "Jovian":
                if p.orbitType == "Epistellar" and p.category not in [
                        "Jovian", "Chthonian"]:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Epistellar jovian planet has an invalid category.")
                if p.orbitType == "Inner Zone" and p.category != "Jovian":
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Inner zone jovian planet has an invalid category.")
                if p.orbitType == "Outer Zone" and p.category != "Jovian":
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError(
                        "Outer zone jovian planet has an invalid category.")

        # Animals on planets
        if p.biosphere >= 9 and len(p.animals) == 0:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if star != p.star:
                    get_info(star)
            get_info(p.star)
            get_info(p)
            raise ValueError("Planet should have animals but doesn't.")

        # Aliens on planets
        if p.biosphere == 12 and p.alien is None:
            get_info(p.systemHex)
            for st in s.systemHex.stars:
                if star != p.star:
                    get_info(star)
            get_info(p.star)
            get_info(p)
            raise ValueError("Planet should have alien but doesn't.")

        # Acheronian
        if p.category == "Acheronian":
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 1:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Arean
        elif p.category == "Arean":
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere not in [1, 10] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 4 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.atmosphere == 1 and p.hydrosphere > 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in ["Water", "Ammonia", "Methane"] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.orbitType == "Outer Zone" and p.star.luminosityClass == "L" and p.chemistry == "Water":
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.orbitType != "Outer Zone" and p.star.luminosityClass != "L" and p.chemistry == "Methane":
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.atmosphere == 1 and (p.biosphere < 0 or p.biosphere > 2) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Arid
        elif p.category == "Arid":
            if p.size < 0 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.biosphere >= 3 and p.chemistry == "Water":
                if (p.atmosphere < 2 or p.atmosphere > 9) and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            else:
                if p.atmosphere != 10 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 1 or p.hydrosphere > 3 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in ["Water", "Ammonia", "Methane"] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.chemistry != "Water" and (
                p.orbitType != "Outer Zone" and p.star.luminosityClass not in [
                    "K-V", "M-V", "L"]):
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.chemistry == "Methane" and p.star.luminosityClass not in [
                "M-V",
                "L"] and (
                (p.star.luminosityClass != "K-V" and p.orbitType == "Outer Zone") or (
                    p.star.luminosityClass == "K-V" and p.orbitType != "Outer Zone")) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass == "D":
                if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 12 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Asphodelian
        elif p.category == "Asphodelian":
            if p.size < 10 or p.size > 15:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 1:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Chthonian
        elif p.category == "Chthonian":
            if p.size != 16:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 1:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Hebean
        elif p.category == "Hebean":
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere not in [0, 1, 10] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 6 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Helian
        elif p.category == "Helian":
            if p.size < 10 or p.size > 15:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 13 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if (p.hydrosphere < 0 or p.hydrosphere in [
                    12, 13, 14] or p.hydrosphere > 15) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Jani-Lithic
        elif p.category == "Jani-Lithic":
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere not in [1, 10] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Jovian
        elif p.category == "Jovian":
            if p.size != 16:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 16:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 16:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in ["Water", "Ammonia", None]:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere > 0 and p.chemistry not in ["Water", "Ammonia"]:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere in [0, None] and p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.systemHex.age > 6:
                if p.star.luminosityClass == "D" and (
                        p.biosphere < 0 or p.biosphere > 9):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
                if p.star.luminosityClass != "D" and (
                        p.biosphere < 0 or p.biosphere > 12):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Meltball
        elif p.category == "Meltball":
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 1:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 15:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Oceanic
        elif p.category == "Oceanic":
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.chemistry == "Water":
                if p.atmosphere < 0 or p.atmosphere > 12 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            else:
                if p.atmosphere not in [1, 10, 12] and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 11 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in ["Water", "Ammonia", "Methane"] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass in [
                    "M-V", "L"] and p.orbitType == "Outer Zone" and p.chemistry == "Water" and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass not in [
                    "K-V",
                    "M-V",
                    "L"] and p.orbitType != "Outer Zone" and p.chemistry in [
                    "Ammonia",
                    "Methane"] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.chemistry == "Methane" and (
                p.star.luminosityClass not in [
                    "M-V",
                    "L"] and (
                    p.star.luminosityClass != "K-V" or p.orbitType != "Outer Zone")) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            elif p.star.systemHex.age >= 4 + p.ageModifier:
                if p.star.luminosityClass == "D":
                    if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if star != p.star:
                                get_info(star)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
                else:
                    if "M-Ve" not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if star != p.star:
                                get_info(star)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
        # Panthalassic
        elif p.category == "Panthalassic":
            if p.size < 10 or p.size > 15:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if (p.atmosphere < 9 or p.atmosphere > 13) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 11 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [
                "Water",
                "Ammonia",
                "Methane",
                "Sulfur",
                "Chlorine"]:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass not in [
                    "K-V",
                    "M-V",
                    "L"] and (
                    p.chemistry == "Methane" or p.ageModifier != 0) and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass not in [
                    "M-V", "L"] and p.ageModifier == 3:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.systemHex.age >= 4 + p.ageModifier:
                if "M-Ve" not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Promethean
        elif p.category == "Promethean":
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.biosphere >= 3 and p.chemistry == "Water":
                if p.atmosphere < 2 or p.atmosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            else:
                if p.atmosphere != 10 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 10 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in ["Water", "Ammonia", "Methane"] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass != "L" and p.orbitType == "Epistellar" and p.chemistry != "Water":
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.luminosityClass != "L" and p.orbitType != "Outer Zone" and p.chemistry == "Methane" and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            elif p.star.systemHex.age >= 4 + p.ageModifier:
                if p.star.luminosityClass == "D":
                    if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if star != p.star:
                                get_info(star)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
                else:
                    if "M-Ve" not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if star != p.star:
                                get_info(star)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Rockball
        elif p.category == "Rockball":
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.star.luminosityClass == "L":
                if p.orbitType == "Epistellar" and (
                        p.hydrosphere < 0 or p.hydrosphere > 5):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid hydrosphere.")
                elif p.orbitType == "Outer Zone" and (p.hydrosphere < 0 or p.hydrosphere > 9):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid hydrosphere.")
            else:
                if p.orbitType == "Epistellar" and (
                        p.hydrosphere < 0 or p.hydrosphere > 4):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid hydrosphere.")
                elif p.orbitType == "Outer Zone" and (p.hydrosphere < 0 or p.hydrosphere > 8):
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Snowball
        elif p.category == "Snowball":
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere not in [0, 1] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 10 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in ["Water", "Ammonia", "Methane"] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.orbitType != "Outer Zone" and p.star.luminosityClass != "L" and p.chemistry == "Methane" and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if not p.subsurfaceOceans and p.biosphere > 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.star.systemHex.age >= 6 + p.ageModifier:
                if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
        # Stygian
        elif p.category == "Stygian":
            if p.size < 0 or p.size > 5:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Tectonic
        elif p.category == "Tectonic":
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.biosphere >= 3 and p.chemistry == "Water":
                if p.atmosphere < 2 or p.atmosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            elif p.biosphere >= 3 and p.chemistry in ["Sulfur", "Chlorine"] and p.atmosphere != 11 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            elif (p.biosphere < 3 or p.chemistry != "Water") and (p.biosphere < 3 or p.chemistry not in ["Sulfur", "Chlorine"]) and p.terraformingPointsUsed == 0:
                if p.atmosphere != 10:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 10 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in [
                "Water",
                "Ammonia",
                "Methane",
                "Sulfur",
                "Chlorine"]:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.orbitType == "Outer Zone" and p.star.luminosityClass in [
                    "L", "M-V"] and p.chemistry not in ["Ammonia", "Methane"]:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.systemHex.age >= 4 + p.ageModifier:
                if p.star.luminosityClass == "D":
                    if p.biosphere < 0 or p.biosphere > 9 and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if star != p.star:
                                get_info(star)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
                else:
                    if "M-Ve" not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                        get_info(p.systemHex)
                        for st in s.systemHex.stars:
                            if star != p.star:
                                get_info(star)
                        get_info(p.star)
                        get_info(p)
                        raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Telluric
        elif p.category == "Telluric":
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.atmosphere != 12 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            if p.hydrosphere not in [0, 15] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry is not None and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.biosphere != 0 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid subsurface oceans.")
        # Vesperian
        elif p.category == "Vesperian":
            if p.size < 5 or p.size > 10:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid size.")
            if p.biosphere >= 3 and p.chemistry == "Water":
                if p.atmosphere < 2 or p.atmosphere > 9 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            elif p.biosphere >= 3 and p.chemistry == "Chlorine" and p.atmosphere != 11 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid atmosphere.")
            elif p.biosphere < 3 or p.chemistry not in ["Water", "Chlorine"] and p.terraformingPointsUsed == 0:
                if p.atmosphere != 10:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid atmosphere.")
            if p.hydrosphere < 0 or p.hydrosphere > 10 and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid hydrosphere.")
            if p.chemistry not in ["Water", "Chlorine"] and p.terraformingPointsUsed == 0:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
                get_info(p.star)
                get_info(p)
                raise ValueError("Invalid chemistry.")
            if p.star.systemHex.age >= 4:
                if "M-Ve" not in [s.luminosityClass for s in p.star.systemHex.stars] and p.hydrosphere > 0 and (p.atmosphere > 0 or p.subsurfaceOceans) and (p.biosphere < 2 or p.biosphere > 12) and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            else:
                if p.biosphere < 0 or p.biosphere > 3 and p.terraformingPointsUsed == 0:
                    get_info(p.systemHex)
                    for st in s.systemHex.stars:
                        if star != p.star:
                            get_info(star)
                    get_info(p.star)
                    get_info(p)
                    raise ValueError("Invalid biosphere.")
            if p.subsurfaceOceans:
                get_info(p.systemHex)
                for st in s.systemHex.stars:
                    if star != p.star:
                        get_info(star)
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

        if ("Open Ocean" in a.terrain or "Deep Ocean" in a.terrain) and a.primaryMovement != "Swim":
            get_info(a.planet)
            get_info(a)
            raise ValueError("Non-swimmer in the ocean.")

        # Amphibian
        if a.animalClass == "Amphibian":
            if a.diet == "Carnivore":
                validBehaviors = ["Pouncer", "Trapper", "Hunter", "Chaser"]
                if "These amphibians emit a natural pheromone that other animals find highly attractive." in a.quirks:
                    validBehaviors.append("Siren")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Herbivore":
                validBehaviors = ["Filter", "Intermittent", "Grazer"]
                if "These amphibians emit a natural pheromone that other animals find highly attractive." in a.quirks:
                    validBehaviors.append("Siren")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Omnivore":
                validBehaviors = [
                    "Carrion-Eater",
                    "Gatherer",
                    "Eater",
                    "Hunter",
                    "Intermittent",
                    "Reducer"]
                if "These amphibians emit a natural pheromone that other animals find highly attractive." in a.quirks:
                    validBehaviors.append("Siren")
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
            if "These amphibians emit a natural pheromone that other animals find highly attractive." in a.quirks and "Siren" not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Amphibian Siren behavior missing.")
        # Aquatic
        if a.animalClass == "Aquatic":
            if a.diet == "Carnivore":
                validBehaviors = ["Eater", "Hunter", "Killer", "Chaser"]
                if "Posseses a frail physique and has the ability to engage in extremely swift movement." in a.quirks:
                    validBehaviors.append("Pouncer")
                if not all(
                        b in validBehaviors for b in a.behaviors) and "Posseses a frail physique and has the ability to engage in extremely swift movement." not in a.quirks:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Herbivore":
                validBehaviors = ["Filter", "Intermittent", "Grazer"]
                if "Posseses a frail physique and has the ability to engage in extremely swift movement." in a.quirks:
                    validBehaviors.append("Pouncer")
                if not all(
                        b in validBehaviors for b in a.behaviors) and "Posseses a frail physique and has the ability to engage in extremely swift movement." not in a.quirks:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Omnivore":
                validBehaviors = ["Carrion-Eater", "Eater", "Reducer"]
                if "Posseses a frail physique and has the ability to engage in extremely swift movement." in a.quirks:
                    validBehaviors.append("Pouncer")
                if not all(
                        b in validBehaviors for b in a.behaviors) and "Posseses a frail physique and has the ability to engage in extremely swift movement." not in a.quirks:
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if a.primaryMovement != "Swim":
                get_info(a.planet)
                get_info(a)
                raise ValueError(
                    "Aquatic with a primary movement other than swim.")

            if "This creature is never found alone and will die within 1d6 days of natural causes if it cannot find a pack to join." in a.quirks and a.pack == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Aquatic invalid pack because of quirk.")
            if "Posseses a frail physique and has the ability to engage in extremely swift movement" in a.quirks and (
                    "Pouncer" not in a.behaviors or a.armor > 0):
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
        if a.animalClass == "Avian":
            if a.diet == "Carnivore":
                validBehaviors = ["Hunter", "Chaser", "Killer", "Pouncer"]
                if "These avians have developed a way to emit calls that sound exactly like the cries of wounded prey, using these to lure meals closer." in a.quirks:
                    validBehaviors.append("Siren")
                if "Not just ground bound, this flightless species thrives because of it." in a.quirks:
                    validBehaviors.append("Chaser")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Herbivore":
                validBehaviors = ["Intimidator", "Intermittent", "Grazer"]
                if "These avians have developed a way to emit calls that sound exactly like the cries of wounded prey, using these to lure meals closer." in a.quirks:
                    validBehaviors.append("Siren")
                if "Not just ground bound, this flightless species thrives because of it." in a.quirks:
                    validBehaviors.append("Chaser")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Omnivore":
                validBehaviors = [
                    "Carrion-Eater",
                    "Eater",
                    "Intimidator",
                    "Reducer"]
                if "These avians have developed a way to emit calls that sound exactly like the cries of wounded prey, using these to lure meals closer." in a.quirks:
                    validBehaviors.append("Siren")
                if "Not just ground bound, this flightless species thrives because of it." in a.quirks:
                    validBehaviors.append("Chaser")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if "Extremely social, these animals live in immense flocks." in a.quirks and a.pack < 12:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian pack too low.")
            if ("Quite at home on the ground, this species has evolved away from flight." in a.quirks or "Not just ground bound, this flightless species has no F movement rate and thrives because of it." in a.quirks) and a.primaryMovement != "Walk":
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian that needs to walk.")
            if "These avians have adapted a very unusual way of dealing with enemies." in a.quirks and len(
                    a.exoticWeapons) == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian missing exotic weapon.")
            if "These avians have developed a way to emit calls that sound exactly like the cries of wounded prey." in a.quirks and "Siren" not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian missing Siren.")
            if "Environmental pressures have forced this animal to adapt to a hostile environment." in a.quirks and a.armor == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Avian missing armor.")
        # Fungal
        if a.animalClass == "Fungal":
            if a.diet == "Carnivore":
                validBehaviors = ["Hunter", "Siren", "Killer"]
                if "Though capable of physical movement to attack or defend itself, this Fungal species is stationary and cannot change location. If the base species was herbivorous, it is now specialises in luring other fungals to their doom." in a.quirks:
                    validBehaviors.append("Siren")
                if "Almost liquid in structure, this extremely slimy fungal moves at normal speed and is capable of extremely rapid motion when it hunts." in a.quirks:
                    validBehaviors.append("Pouncer")
                if "The scent and outlandish appearance of this fungal terrifies other animals." in a.quirks:
                    validBehaviors.append("Hijacker")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Herbivore":
                validBehaviors = ["Intermittent", "Grazer"]
                if "Though capable of physical movement to attack or defend itself, this Fungal species is stationary and cannot change location. If the base species was herbivorous, it is now specialises in luring other fungals to their doom." in a.quirks:
                    validBehaviors.append("Siren")
                if "Almost liquid in structure, this extremely slimy fungal moves at normal speed and is capable of extremely rapid motion when it hunts." in a.quirks:
                    validBehaviors.append("Pouncer")
                if "The scent and outlandish appearance of this fungal terrifies other animals." in a.quirks:
                    validBehaviors.append("Hijacker")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Omnivore":
                validBehaviors = ["Carrion-Eater", "Eater", "Reducer"]
                if "Though capable of physical movement to attack or defend itself, this Fungal species is stationary and cannot change location. If the base species was herbivorous, it is now specialises in luring other fungals to their doom." in a.quirks:
                    validBehaviors.append("Siren")
                if "Almost liquid in structure, this extremely slimy fungal moves at normal speed and is capable of extremely rapid motion when it hunts." in a.quirks:
                    validBehaviors.append("Pouncer")
                if "The scent and outlandish appearance of this fungal terrifies other animals." in a.quirks:
                    validBehaviors.append("Hijacker")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if "This Fungal is an absolutely bizarre colour and smells rancid." in a.quirks and len(
                    a.exoticWeapons) == 0:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Funal missing exotic weapon.")
            if "The Fungal can inflate itself with a light gas, allowing for a slow form of flight." in a.quirks and a.primaryMovement != "Fly":
                get_info(a.planet)
                get_info(a)
                raise ValueError("Fungal should fly.")
            if "Though capable of physical movement to attack or defend itself, this Fungal species is stationary and cannot change location." in a.quirks and (
                    "Siren" not in a.behaviors or a.primaryMovement != "Stationary"):
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
            if "Almost liquid in structure, this extremely slimy fungal moves at normal speed and is capable of extremely rapid motion when it hunts." in a.quirks and "Pouncer" not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Fungal missing Pouncer.")
        # Insect
        if a.animalClass == "Insect":
            if a.diet == "Carnivore":
                validBehaviors = [
                    "Pouncer",
                    "Hunter",
                    "Killer",
                    "Trapper",
                    "Chaser"]
                if "The insect can generate a hypnotic drone." in a.quirks:
                    validBehaviors.append("Siren")
                if "Solitary by nature. If the insects are herbivores, they just leave their prey to rot and eat the resulting fungus." in a.quirks:
                    validBehaviors.extend(["Pouncer", "Trapper"])
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Herbivore":
                validBehaviors = [
                    "Eater",
                    "Intermittent",
                    "Filter",
                    "Gatherer",
                    "Grazer"]
                if "The insect can generate a hypnotic drone." in a.quirks:
                    validBehaviors.append("Siren")
                if "Solitary by nature. If the insects are herbivores, they just leave their prey to rot and eat the resulting fungus." in a.quirks:
                    validBehaviors.extend(["Pouncer", "Trapper"])
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Omnivore":
                validBehaviors = ["Carrion-Eater", "Eater", "Reducer"]
                if "The insect can generate a hypnotic drone." in a.quirks:
                    validBehaviors.append("Siren")
                if "Solitary by nature. If the insects are herbivores, they just leave their prey to rot and eat the resulting fungus." in a.quirks:
                    validBehaviors.extend(["Pouncer", "Trapper"])
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
                    (a.primaryMovement == "Walk" and "Trapper" not in a.behaviors) or (
                        a.primaryMovement == "Fly" and "Pouncer" not in a.behaviors))):
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
            if "The insect can generate a hypnotic drone." in a.quirks and "Siren" not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Insect missing Siren.")
        # Mammal
        if a.animalClass == "Mammal":
            if a.diet == "Carnivore":
                validBehaviors = [
                    "Pouncer",
                    "Killer",
                    "Trapper",
                    "Chaser",
                    "Hunter",
                    "Hijacker"]
                if "This mammal has an unusual mode of travel, be it gliding or swinging between trees in its home environment." in a.quirks:
                    validBehaviors.append("Pouncer")
                if "Unusually vicious, these mammals are hostile to any species but their own." in a.quirks:
                    validBehaviors.append("Killer")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Herbivore":
                validBehaviors = [
                    "Eater", "Intermittent", "Grazer", "Gatherer"]
                if "This mammal has an unusual mode of travel, be it gliding or swinging between trees in its home environment." in a.quirks:
                    validBehaviors.append("Pouncer")
                if "Unusually vicious, these mammals are hostile to any species but their own." in a.quirks:
                    validBehaviors.append("Killer")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Omnivore":
                validBehaviors = [
                    "Carrion-Eater",
                    "Gatherer",
                    "Hunter",
                    "Intimidator",
                    "Reducer"]
                if "This mammal has an unusual mode of travel, be it gliding or swinging between trees in its home environment." in a.quirks:
                    validBehaviors.append("Pouncer")
                if "Unusually vicious, these mammals are hostile to any species but their own." in a.quirks:
                    validBehaviors.append("Killer")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")

            if "This mammal has an unusual mode of travel, be it gliding or swinging between trees in its home environment." in a.quirks and a.diet == "Omnivore" and "Pouncer" not in a.behaviors:
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
                    "Horns" not in a.weapons or a.meleeNaturalWeapons == -3):
                get_info(a.planet)
                get_info(a)
                raise ValueError(
                    "Mammal should have horns and a rank in melee natural weapons.")

            if "Unusually vicious, these mammals are hostile to any species but their own." in a.quirks and "Killer" not in a.behaviors:
                get_info(a.planet)
                get_info(a)
                raise ValueError("Mammal missing Killer.")

            if "This animal species is on the verge of evolving into sentience." in a.quirks and (
                    a.intelligence < 2 or a.instinct < 12):
                get_info(a.planet)
                get_info(a)
                raise ValueError("Mammal intelligence or instinct too low.")
        # Reptile
        if a.animalClass == "Reptile":
            if a.diet == "Carnivore":
                validBehaviors = [
                    "Pouncer",
                    "Killer",
                    "Intimidator",
                    "Hunter",
                    "Hijacker"]
                if "This reptile buries itself in its terrain, blending in and waiting for prey to ensnare." in a.quirks:
                    validBehaviors.append("Trapper")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Herbivore":
                validBehaviors = ["Gatherer", "Intermittent", "Grazer"]
                if "This reptile buries itself in its terrain, blending in and waiting for prey to ensnare." in a.quirks:
                    validBehaviors.append("Trapper")
                if not all(b in validBehaviors for b in a.behaviors):
                    get_info(a.planet)
                    get_info(a)
                    raise ValueError("Invalid behavior.")
            elif a.diet == "Omnivore":
                validBehaviors = [
                    "Carrion-Eater",
                    "Gatherer",
                    "Hijacker",
                    "Hunter",
                    "Reducer"]
                if "This reptile buries itself in its terrain, blending in and waiting for prey to ensnare." in a.quirks:
                    validBehaviors.append("Trapper")
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

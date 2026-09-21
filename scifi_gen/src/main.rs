mod system_hex;
mod star;
mod orbital_body;
mod name_generator;
mod dice_roller;
use rand::SeedableRng;
use rand_chacha::ChaCha8Rng;
use crate::name_generator::NameGenerator;
use std::collections::{BTreeMap, BTreeSet, VecDeque};
use crate::dice_roller::roll_xdy;
use crate::system_hex::create_system;
use crate::system_hex::System;
use crate::orbital_body::{Body, OrbitalBody};
use crate::orbital_body::category_group;
use crate::orbital_body::Group;

type Coord = (i16, i16, i16);

pub struct Namer {
    pub astral: NameGenerator,
    pub alien: NameGenerator,
    pub animal: NameGenerator,
}

impl Namer {
    pub fn load() -> std::io::Result<Namer> {
        Ok(Namer {
            astral: NameGenerator::from_file(
                concat!(env!("CARGO_MANIFEST_DIR"), "/namesastral.txt"), false, true)?,
            alien: NameGenerator::from_file(
                concat!(env!("CARGO_MANIFEST_DIR"), "/namesalien.txt"), false, true)?,
            animal: NameGenerator::from_file(
                concat!(env!("CARGO_MANIFEST_DIR"), "/namesanimal.txt"), true, false)?,
        })
    }
    pub fn star(&mut self, rng: &mut ChaCha8Rng) -> String {
        self.astral.generate_name(rng)
    }
    pub fn species(&mut self, rng: &mut ChaCha8Rng) -> String {
        self.alien.generate_name(rng)
    }
    pub fn creature(&mut self, rng: &mut ChaCha8Rng) -> String {
        self.animal.generate_name(rng)
    }
}

fn generate_sector(rng: &mut ChaCha8Rng, namer: &mut Namer, min: i16, max: i16)
    -> BTreeMap<Coord, System>
{
    let mut systems: BTreeMap<Coord, System> = BTreeMap::new();
    let mut queue: VecDeque<(i16, i16, bool)> = VecDeque::new(); // (h, v, forced_cluster)

    for h in min..=max {
        for v in min..=max {
            queue.push_back((h, v, false));
        }
    }

    while let Some((h, v, forced_cluster)) = queue.pop_front() {
        let coord = (h, v, -h - v);
        if systems.contains_key(&coord) {
            continue; // already exists
        }

        // Set open cluster or not
        let seeds_cluster = roll_xdy(rng, 3, 6) == 18;
        let open_cluster = forced_cluster || seeds_cluster;

        systems.insert(coord, create_system(rng, namer, h, v, open_cluster));

        if seeds_cluster {
            let hex_range = roll_xdy(rng, 2, 6) as i16;
            for dx in -hex_range..=hex_range {
                for dy in (-hex_range).max(-dx - hex_range)..=hex_range.min(-dx + hex_range) {
                    let nh = h + dx;
                    let nv = v + dy;
                    if !systems.contains_key(&(nh, nv, -nh - nv)) {
                        queue.push_back((nh, nv, true));
                    }
                }
            }
        }
    }

    systems
}

fn sector_for(seed: u64) -> BTreeMap<Coord, System> {
    let mut namer = Namer::load().unwrap();
    let mut rng = ChaCha8Rng::seed_from_u64(seed);
    generate_sector(&mut rng, &mut namer, -10, 10)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut rng = ChaCha8Rng::seed_from_u64(42);
    let mut namer = Namer::load()?;

    let sector_min: i16 = -10;
    let sector_max: i16 = 10;

    let systems = generate_sector(&mut rng, &mut namer, sector_min, sector_max);
    for (coord, s) in &systems {
        println!("{} ({:?}): {} subsystems{}", s.designation(), coord, s.subsystems.len(), if s.open_cluster { " (open cluster) "} else { "" });
    }

    Ok(())
}

/// Recursively collect designations, asserting each is new.
fn assert_unique_designations(b: &OrbitalBody, seen: &mut BTreeSet<String>, seed: u64, coord: Coord) {
    assert!(
        seen.insert(b.designation.clone()),
        "seed {seed} {coord:?}: duplicate designation {}", b.designation
    );
    for s in &b.satellites {
        assert_unique_designations(s, seen, seed, coord);
    }
}

/// Nesting depth of a body's satellite tree. A childless body is depth 1.
fn max_depth(b: &OrbitalBody) -> usize {
    1 + b.satellites.iter().map(max_depth).max().unwrap_or(0)
}

fn fingerprint_body(out: &mut String, b: &OrbitalBody, depth: usize) {
    let indent = "  ".repeat(depth + 1);
    match &b.body {
        Body::AsteroidBelt => {
            out.push_str(&format!("{indent}{} o{} BELT\n", b.designation, b.order));
        }
        Body::Planet(p) => {
            out.push_str(&format!(
                "{indent}{} o{} {:?} sz={} atm={} hyd={} bio={} chem={:?} rings={:?}\n",
                b.designation, b.order, p.category, p.size,
                p.atmosphere, p.hydrosphere, p.biosphere, p.chemistry, p.rings,
            ));
        }
    }
    for s in &b.satellites {
        fingerprint_body(out, s, depth + 1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // A stable text fingerprint of a whole sector.
    fn fingerprint(systems: &BTreeMap<Coord, System>) -> String {
        let mut out = String::new();
        for (coord, sys) in systems {
            out.push_str(&format!("{coord:?} {} age={}\n", sys.designation(), sys.age));
            for sub in &sys.subsystems {
                for ob in sub.all_bodies() {
                    fingerprint_body(&mut out, ob, 0);
                }
            }
        }
        out
    }

    #[test]
    fn sector_is_reproducible() {
        let mut namer = Namer::load().expect("name files must load");

        let mut rng1 = ChaCha8Rng::seed_from_u64(42);
        let a = generate_sector(&mut rng1, &mut namer, -10, 10);

        let mut namer2 = Namer::load().expect("name files must load");
        let mut rng2 = ChaCha8Rng::seed_from_u64(42);
        let b = generate_sector(&mut rng2, &mut namer2, -10, 10);

        assert_eq!(fingerprint(&a), fingerprint(&b), "same seed produced different sectors");
    }
}

#[cfg(test)]
mod structure_tests {
    use super::*;
    use crate::star::{StarRole, CompanionOrbit};
    use crate::system_hex::Subsystem;

    // Generate one sizeable sector to inspect. A fresh namer + fixed seed.
    fn sample_sector() -> BTreeMap<Coord, System> {
        let mut namer = Namer::load().expect("name files must load");
        let mut rng = ChaCha8Rng::seed_from_u64(42);
        generate_sector(&mut rng, &mut namer, -10, 10)
    }

    #[test]
    fn at_most_one_primary_per_system() {
        for seed in 0..25 {
            for (coord, sys) in sector_for(seed) {
                let primaries = sys.subsystems.iter()
                    .flat_map(|s| s.stars())
                    .filter(|st| matches!(st.role, StarRole::Primary))
                    .count();
                assert!(primaries <= 1, "seed {seed} {coord:?} has {primaries} primaries");
            }
        }
    }

    #[test]
    fn at_most_one_brown_dwarf_per_system() {
        for seed in 0..25 {
            for (coord, sys) in sector_for(seed) {
                let bds = sys.subsystems.iter()
                    .flat_map(|s| s.stars())
                    .filter(|st| matches!(st.role, StarRole::BrownDwarf))
                    .count();
                assert!(bds <= 1, "{coord:?} has {bds} brown dwarfs");
            }
        }
    }

    #[test]
    fn binary_companion_is_never_distant() {
        // Aa Distant companion must be its own Single, never the companion field of a Binary.
        for seed in 0..25 {
            for (coord, sys) in sector_for(seed) {
                for sub in &sys.subsystems {
                    if let Subsystem::Binary { companion, .. } = sub {
                        assert!(
                            !matches!(companion.role, StarRole::Companion(CompanionOrbit::Distant)),
                            "{coord:?}: a Distant companion ended up inside a Binary"
                        );
                    }
                }
            }
        }
    }

    #[test]
    fn binary_companion_is_actually_a_companion() {
        // A Binary's companion field should hold a Companion role, never a
        // Primary or BrownDwarf that slipped into the wrong slot.
        for seed in 0..25 {
            for (coord, sys) in sector_for(seed) {
                for sub in &sys.subsystems {
                    if let Subsystem::Binary { companion, primary, .. } = sub {
                        assert!(matches!(companion.role, StarRole::Companion(_)),
                            "{coord:?}: Binary companion has role {:?}", companion.role);
                        assert!(matches!(primary.role, StarRole::Primary),
                            "{coord:?}: Binary primary has role {:?}", primary.role);
                    }
                }
            }
        }
    }

    #[test]
    fn named_iff_has_subsystems() {
        // A system has a name exactly when it has stars, and is a nameless void otherwise.
        for seed in 0..25 {
            for (coord, sys) in sector_for(seed) {
                assert_eq!(
                    sys.name.is_some(),
                    !sys.subsystems.is_empty(),
                    "{coord:?}: name-presence and subsystem-presence disagree"
                );
            }
        }
    }

    #[test]
    fn star_count_within_bounds() {
        // primary + up to 2 companions + up to 1 brown dwarf = 4 max.
        for seed in 0..25 {
            for (coord, sys) in sector_for(seed) {
                let n = sys.subsystems.iter().flat_map(|s| s.stars()).count();
                assert!(n <= 4, "{coord:?} has {n} stars (max 4)");
            }
        }
    }

    #[test]
    fn designations_are_unique_within_a_system() {
        for seed in 0..25 {
            for (coord, sys) in sector_for(seed) {
                let mut seen = BTreeSet::new();
                for sub in &sys.subsystems {
                    for body in sub.all_bodies() {
                        assert_unique_designations(body, &mut seen, seed, coord);
                    }
                }
            }
        }
    }

    #[test]
    fn satellite_nesting_is_bounded() {
        // Theoretical max chain: Jovian -> Helian -> Terrestrial -> Dwarf -> companion = 5.
        // 6 gives headroom while still catching runaway recursion.
        for seed in 0..25 {
            for (coord, sys) in sector_for(seed) {
                for sub in &sys.subsystems {
                    for body in sub.all_bodies() {
                        let d = max_depth(body);
                        assert!(d <= 6, "seed {seed} {coord:?}: satellite nesting depth {d}");
                    }
                }
            }
        }
    }

    #[test]
    fn satellite_structure_follows_rules() {
        fn check(b: &OrbitalBody, seed: u64, coord: Coord) {
            let n = b.satellites.len();
            let max_allowed = match &b.body {
                Body::AsteroidBelt => 1,                    // 5-6: one embedded dwarf
                Body::Planet(p) => match category_group(p.category) {
                    Group::Dwarf       => 1,                // 6: one binary companion
                    Group::Terrestrial => 1,                // 5-6: one dwarf satellite
                    Group::Helian      => 3,                // 1d6-3
                    Group::Jovian      => 6,                // 1d6
                    Group::AsteroidBelt => 0,               // can't occur for a Planet
                },
            };
            assert!(n <= max_allowed,
                "seed {seed} {coord:?}: {} has {n} satellites (max {max_allowed})", b.designation);

            // The termination invariant: a dwarf binary companion generates nothing.
            if b.designation.ends_with('b') {
                assert!(b.satellites.is_empty(),
                    "seed {seed} {coord:?}: companion {} has satellites", b.designation);
            }

            for s in &b.satellites { check(s, seed, coord); }
        }

        for seed in 0..25 {
            for (coord, sys) in sector_for(seed) {
                for sub in &sys.subsystems {
                    for body in sub.all_bodies() { check(body, seed, coord); }
                }
            }
        }
    }

    // Walks a body and all its satellites recursively, asserting uniqueness.
    fn collect_designations(b: &OrbitalBody, seen: &mut BTreeSet<String>, seed: u64, coord: Coord) {
        assert!(seen.insert(b.designation.clone()),
            "seed {seed} {coord:?}: duplicate designation {}", b.designation);
        for s in &b.satellites {
            collect_designations(s, seen, seed, coord);
        }
    }
}

mod value_tests {
    #[cfg(test)]
    mod planet_values {
        use crate::orbital_body::{category_group, Body, Category, Group, OrbitalBody};
        use crate::sector_for;

        /// Highest legal value for atmosphere, hydrosphere and biosphere.
        ///
        /// Only jovians reach 16, and only for atmosphere and hydrosphere, where it
        /// stands for "no surface, just envelope". Everything else tops out at 15.
        const ABSOLUTE_MAX: u8 = 16;
        const NON_JOVIAN_MAX: u8 = 15;

        /// Every planetary value must be inside the scale the rest of the code
        /// reads it on.
        ///
        /// This is also the test that catches the `99` sentinels left behind by
        /// unimplemented match arms. A 99 is not a value — it is a category that
        /// was never written, and it will silently produce a world with no terrain
        /// rather than an error.
        #[test]
        fn planet_values_are_within_scale() {
            for seed in 0..15 {
                for (coord, system) in sector_for(seed) {
                    for subsystem in &system.subsystems {
                        for body in subsystem.all_bodies() {
                            check_values(body, seed, coord);
                        }
                    }
                }
            }
        }

        fn check_values(body: &OrbitalBody, seed: u64, coord: (i16, i16, i16)) {
            if let Body::Planet(planet) = &body.body {
                let ceiling = if category_group(planet.category) == Group::Jovian {
                    ABSOLUTE_MAX
                } else {
                    NON_JOVIAN_MAX
                };

                for (field, value) in [
                    ("atmosphere", planet.atmosphere),
                    ("hydrosphere", planet.hydrosphere),
                    ("biosphere", planet.biosphere),
                ] {
                    assert!(
                        value <= ceiling,
                        "seed {seed} {coord:?}: {} ({:?}) has {field} {value}, max is {ceiling}",
                        body.designation, planet.category,
                    );
                }

                // Biosphere is on the 0-15 scale for every group, jovians included.
                assert!(
                    planet.biosphere <= NON_JOVIAN_MAX,
                    "seed {seed} {coord:?}: {} ({:?}) has biosphere {}",
                    body.designation, planet.category, planet.biosphere,
                );
            }

            for satellite in &body.satellites {
                check_values(satellite, seed, coord);
            }
        }

        /// Categories that pin a field to a constant, as a guard against a
        /// refactor quietly making one of them variable.
        ///
        /// `None` means "this category varies that field, don't check it" - a
        /// deliberate choice over a sentinel number, since sentinel numbers in
        /// planetary fields are exactly what the test above exists to catch.
        fn fixed_values(category: Category) -> (Option<u8>, Option<u8>, Option<u8>) {
            match category {
                Category::Rockball | Category::Stygian => (Some(0), Some(0), Some(0)),
                Category::Meltball => (Some(1), Some(15), Some(0)),
                Category::Acheronian | Category::Asphodelian | Category::Chthonian => (Some(1), Some(0), Some(0)),
                Category::Telluric => (Some(12), None, Some(0)),
                Category::JaniLithic => (None, Some(0), Some(0)),
                Category::Helian => (Some(13), None, Some(0)),
                Category::Oceanic | Category::Panthalassic => (None, Some(11), None),
                Category::Jovian => (Some(16), Some(16), None),
                Category::Hebean => (None, None, Some(0)),
                _ => (None, None, None),
            }
        }

        #[test]
        fn fixed_category_values_stay_fixed() {
            for seed in 0..10 {
                for (coord, system) in sector_for(seed) {
                    for subsystem in &system.subsystems {
                        for body in subsystem.all_bodies() {
                            check_fixed(body, seed, coord);
                        }
                    }
                }
            }
        }

        fn check_fixed(body: &OrbitalBody, seed: u64, coord: (i16, i16, i16)) {
            if let Body::Planet(p) = &body.body {
                let (atm, hyd, bio) = fixed_values(p.category);
                for (name, expected, actual) in [
                    ("atmosphere", atm, p.atmosphere),
                    ("hydrosphere", hyd, p.hydrosphere),
                    ("biosphere", bio, p.biosphere),
                ] {
                    if let Some(expected) = expected {
                        assert_eq!(actual, expected,
                            "seed {seed} {coord:?}: {} ({:?}) {name}",
                            body.designation, p.category);
                    }
                }
            }
            for s in &body.satellites {
                check_fixed(s, seed, coord);
            }
        }
    }

    #[cfg(test)]
    mod satellite_rates {
        use crate::orbital_body::{category_group, Body, Group, OrbitalBody};
        use crate::sector_for;

        /// How often each kind of parent should end up with at least one satellite.
        ///
        /// The existing `satellite_structure_follows_rules` test only bounds the
        /// count from above, so an implementation that generates satellites far too
        /// rarely — or never — passes it. This bounds the rate from both sides.
        ///
        /// Fixed seeds make this a deterministic computation, not a flaky
        /// statistical one: it either passes or it does not, every run.
        ///
        /// Dwarfs are the awkward case. A dwarf's binary companion is created with
        /// `is_binary_companion`, so it can never have satellites of its own.
        /// Companions are 1/6 as numerous as the dwarfs that spawn them, so they
        /// are 1/7 of all dwarfs, and a naive "1/6 of dwarfs have a satellite"
        /// check fails against a correct implementation. They are excluded below.
        fn expected_rate(group: Group) -> f64 {
            match group {
                Group::AsteroidBelt => 2.0 / 6.0,  // 1d6 > 4
                Group::Dwarf => 1.0 / 6.0,         // 1d6 == 6
                Group::Terrestrial => 2.0 / 6.0,   // 1d6 >= 5
                Group::Helian => 3.0 / 6.0,        // max(0, 1d6 - 3) >= 1
                Group::Jovian => 1.0,              // 1d6 >= 1 always
            }
        }

        const TOLERANCE: f64 = 0.03;

        const GROUPS: [Group; 5] = [
            Group::AsteroidBelt, Group::Dwarf, Group::Terrestrial, Group::Helian, Group::Jovian,
        ];

        /// Index into the tally array. Group has no `Ord`, so a fixed array beats a
        /// map here and avoids adding derives just to support a test.
        fn slot(group: Group) -> usize {
            GROUPS.iter().position(|&g| g == group).expect("every group is listed")
        }

        #[test]
        fn satellites_are_generated_at_the_intended_rate() {
            // (parents with at least one satellite, parents total), per group.
            let mut tally = [(0usize, 0usize); GROUPS.len()];

            for seed in 0..15 {
                for (_, system) in sector_for(seed) {
                    for subsystem in &system.subsystems {
                        for body in subsystem.all_bodies() {
                            tally_body(body, &mut tally);
                        }
                    }
                }
            }

            for (i, &(with_satellites, total)) in tally.iter().enumerate() {
                let group = GROUPS[i];
                assert!(total > 1_000, "{group:?}: only {total} samples, too few to judge");
                let observed = with_satellites as f64 / total as f64;
                let expected = expected_rate(group);
                assert!(
                    (observed - expected).abs() < TOLERANCE,
                    "{group:?}: {with_satellites}/{total} = {observed:.4} have satellites, \
                    expected {expected:.4}",
                );
            }
        }

        fn tally_body(body: &OrbitalBody, tally: &mut [(usize, usize); GROUPS.len()]) {
            let group = match &body.body {
                Body::AsteroidBelt => Group::AsteroidBelt,
                Body::Planet(p) => category_group(p.category),
            };

            // A dwarf binary companion is generated with satellites suppressed, so
            // counting it would drag the dwarf rate down. Identified by the naming
            // convention, which is fragile - an explicit flag on OrbitalBody would
            // be better once there is a reason to add one.
            let is_binary_companion = group == Group::Dwarf && body.designation.ends_with('b');

            if !is_binary_companion {
                let entry = &mut tally[slot(group)];
                entry.1 += 1;
                if !body.satellites.is_empty() {
                    entry.0 += 1;
                }
            }

            for satellite in &body.satellites {
                tally_body(satellite, tally);
            }
        }
    }
}

// Tests for the stellar expansion rule.
//
// A star of luminosity class D, KIII or MIII expanded off the main sequence
// and scorched its inner orbits. Every planet in a direct stellar orbit at or
// below `expansion_affected_orbits` becomes the ruined variant of its group,
// and its satellites go with it.
//
// These will not compile until `Star` carries `expansion_affected_orbits: u8`.

#[cfg(test)]
mod expansion {
    use crate::orbital_body::{category_group, Body, Category, Group, OrbitalBody};
    use crate::sector_for;
    use crate::star::{LuminosityClass, Star};
    use crate::system_hex::Subsystem;

    /// What a group turns into when its orbit is scorched.
    ///
    /// Asteroid belts are exempt: there is nothing left to boil off.
    fn scorched_form(group: Group) -> Option<Category> {
        match group {
            Group::Dwarf => Some(Category::Stygian),
            Group::Terrestrial => Some(Category::Acheronian),
            Group::Helian => Some(Category::Asphodelian),
            Group::Jovian => Some(Category::Chthonian),
            Group::AsteroidBelt => None,
        }
    }

    /// Categories reachable *only* through expansion.
    ///
    /// Asphodelian and Chthonian are deliberately absent: an ordinary
    /// epistellar roll produces them too, so finding one outside the scorched
    /// range proves nothing. Stygian and Acheronian have no other path, which
    /// is what makes them usable as evidence.
    fn expansion_exclusive(category: Category) -> bool {
        matches!(category, Category::Stygian | Category::Acheronian)
    }

    fn expands(lum: LuminosityClass) -> bool {
        matches!(lum, LuminosityClass::D | LuminosityClass::KIII | LuminosityClass::MIII)
    }

    /// (governing star name, scorched range in this group's own numbering, bodies)
    fn orbit_groups(subsystem: &Subsystem) -> Vec<(&str, u8, &Vec<OrbitalBody>)> {
        match subsystem {
            Subsystem::Single { star, bodies } =>
                vec![(star.name.as_str(), star.expansion_affected_orbits, bodies)],
            Subsystem::Binary { primary, companion, primary_bodies, companion_bodies, shared_bodies } => {
                let shared_range = primary.expansion_affected_orbits
                    .saturating_sub(primary_bodies.len() as u8)
                    .max(companion.expansion_affected_orbits
                        .saturating_sub(companion_bodies.len() as u8));
                vec![
                    (primary.name.as_str(), primary.expansion_affected_orbits, primary_bodies),
                    (companion.name.as_str(), companion.expansion_affected_orbits, companion_bodies),
                    ("circumbinary", shared_range, shared_bodies),
                ]
            }
        }
    }

    /// Only post-main-sequence stars scorch anything, and never more than 1d6
    /// orbits.
    #[test]
    fn only_expanded_stars_have_affected_orbits() {
        for seed in 0..15 {
            for (coord, system) in sector_for(seed) {
                for subsystem in &system.subsystems {
                    for star in subsystem.stars() {
                        assert!(
                            star.expansion_affected_orbits <= 6,
                            "seed {seed} {coord:?}: {} claims {} affected orbits",
                            star.name, star.expansion_affected_orbits,
                        );
                        if !expands(star.luminosity_class) {
                            assert_eq!(
                                star.expansion_affected_orbits, 0,
                                "seed {seed} {coord:?}: {} is {:?} but scorched {} orbits",
                                star.name, star.luminosity_class,
                                star.expansion_affected_orbits,
                            );
                        }
                    }
                }
            }
        }
    }

    /// Every stellar orbit inside the scorched range holds the ruined form of
    /// its group, and nothing inside the range escaped.
    #[test]
    fn orbits_inside_the_scorched_range_are_ruined() {
        for seed in 0..15 {
            for (coord, system) in sector_for(seed) {
                for subsystem in &system.subsystems {
                    for (name, range, bodies) in orbit_groups(subsystem) {
                        for body in bodies {
                            if body.order > range {
                                continue;
                            }
                            let Body::Planet(planet) = &body.body else {
                                continue; // belts survive
                            };
                            let group = category_group(planet.category);
                            let expected = scorched_form(group)
                                .expect("a Planet is never in the asteroid belt group");
                            assert_eq!(
                                planet.category, expected,
                                "seed {seed} {coord:?}: {} is in orbit {} of {} \
                                 (scorched range {}) but is {:?}, not {:?}",
                                body.designation, body.order, name,
                                range, planet.category, expected,
                            );
                        }
                    }
                }
            }
        }
    }

    /// A scorched world takes its moons with it, and an intact world has no
    /// scorched moons.
    #[test]
    fn satellites_inherit_the_scorched_state() {
        for seed in 0..15 {
            for (coord, system) in sector_for(seed) {
                for subsystem in &system.subsystems {
                    for (name, range, bodies) in orbit_groups(subsystem) {
                        for body in bodies {
                            let scorched = body.order <= range;
                            for satellite in &body.satellites {
                                check_inheritance(satellite, scorched, seed, coord);
                            }
                        }
                    }
                }
            }
        }
    }

    fn check_inheritance(
        body: &OrbitalBody, parent_scorched: bool, seed: u64, coord: (i16, i16, i16),
    ) {
        if let Body::Planet(planet) = &body.body {
            let group = category_group(planet.category);
            let is_scorched = Some(planet.category) == scorched_form(group);
            if parent_scorched {
                assert!(
                    is_scorched,
                    "seed {seed} {coord:?}: {} orbits a scorched world but is {:?}",
                    body.designation, planet.category,
                );
            } else {
                assert!(
                    !expansion_exclusive(planet.category),
                    "seed {seed} {coord:?}: {} is {:?} but orbits an intact world",
                    body.designation, planet.category,
                );
            }
        }
        for satellite in &body.satellites {
            check_inheritance(satellite, parent_scorched, seed, coord);
        }
    }

    /// Nothing outside a scorched range is a Stygian or an Acheronian.
    ///
    /// This is the one that catches an off-by-one in the `<=` comparison, or a
    /// scorched check that accidentally reads a satellite's index-within-parent
    /// instead of its stellar orbit.
    #[test]
    fn expansion_exclusive_categories_only_appear_when_scorched() {
        for seed in 0..15 {
            for (coord, system) in sector_for(seed) {
                for subsystem in &system.subsystems {
                    for (name, range, bodies) in orbit_groups(subsystem) {
                        for body in bodies {
                            let in_range = body.order <= range;
                            if in_range {
                                continue;
                            }
                            if let Body::Planet(planet) = &body.body {
                                assert!(
                                    !expansion_exclusive(planet.category),
                                    "seed {seed} {coord:?}: {} is {:?} in orbit {} of {}, \
                                     whose scorched range is {}",
                                    body.designation, planet.category, body.order,
                                    name, range,
                                );
                            }
                        }
                    }
                }
            }
        }
    }

    /// Nothing lives on a scorched world.
    #[test]
    fn scorched_worlds_are_dead() {
        for seed in 0..15 {
            for (coord, system) in sector_for(seed) {
                for subsystem in &system.subsystems {
                    for body in subsystem.all_bodies() {
                        check_dead(body, seed, coord);
                    }
                }
            }
        }
    }

    fn check_dead(body: &OrbitalBody, seed: u64, coord: (i16, i16, i16)) {
        if let Body::Planet(planet) = &body.body {
            let group = category_group(planet.category);
            if Some(planet.category) == scorched_form(group) {
                assert_eq!(
                    planet.biosphere, 0,
                    "seed {seed} {coord:?}: scorched world {} ({:?}) has biosphere {}",
                    body.designation, planet.category, planet.biosphere,
                );
                assert_eq!(
                    planet.hydrosphere, 0,
                    "seed {seed} {coord:?}: scorched world {} ({:?}) has hydrosphere {}",
                    body.designation, planet.category, planet.hydrosphere,
                );
                assert!(
                    planet.rings.is_none(),
                    "seed {seed} {coord:?}: scorched world {} ({:?}) has rings {:?}",
                    body.designation, planet.category, planet.rings,
                );
            }
        }
        for satellite in &body.satellites {
            check_dead(satellite, seed, coord);
        }
    }
}

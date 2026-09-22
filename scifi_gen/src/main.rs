mod system_hex;
mod star;
mod orbital_body;
mod name_generator;
mod dice_roller;
mod temperature;
mod terrain;
mod text;
mod animal;
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
                "{indent}{} o{} {:?} sz={} atm={} hyd={} bio={} chem={:?} rings={:?} base_temperature={:?}\n",
                b.designation, b.order, p.category, p.size,
                p.atmosphere, p.hydrosphere, p.biosphere, p.chemistry, p.rings,
                p.base_temperature
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

#[cfg(test)]
mod climate {
    use crate::orbital_body::{Body, Category, Chemistry, OrbitalBody, Planet, solvent};
    use crate::sector_for;
    use crate::temperature::{
        greenhouse, liquid_range, min_max, wet_bounds, zone, ClimateBand, Solvent,
        Temperature,
    };
 
    const SEEDS: std::ops::Range<u64> = 0..15;
 
    const SOLVENTS: [Solvent; 5] = [
        Solvent::Water, Solvent::SulfuricAcid, Solvent::Chlorine,
        Solvent::Ammonia, Solvent::Methane,
    ];
 
    const BANDS: [ClimateBand; 5] = [
        ClimateBand::Frozen, ClimateBand::Cold, ClimateBand::Temperate,
        ClimateBand::Hot, ClimateBand::Scorching,
    ];
 
    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------
 
    fn walk(body: &OrbitalBody, f: &mut dyn FnMut(&OrbitalBody)) {
        f(body);
        for satellite in &body.satellites {
            walk(satellite, f);
        }
    }
 
    /// Call `f` for every planet — satellites included — across a range of seeds.
    fn each_planet(
        seeds: std::ops::Range<u64>,
        mut f: impl FnMut(u64, (i16, i16, i16), &OrbitalBody, &Planet),
    ) {
        for seed in seeds {
            for (coord, system) in sector_for(seed) {
                for subsystem in &system.subsystems {
                    for root in subsystem.all_bodies() {
                        walk(root, &mut |body| {
                            if let Body::Planet(planet) = &body.body {
                                f(seed, coord, body, planet);
                            }
                        });
                    }
                }
            }
        }
    }
 
    /// A hand-built planet for unit tests. The one place to fix if the
    /// `Planet` field list changes.
    fn planet(category: Category, chemistry: Option<Chemistry>, atmosphere: u8,
              hydrosphere: u8, base_temperature: i16) -> Planet {
        Planet {
            order: 1,
            category,
            size: 8,
            chemistry,
            atmosphere,
            hydrosphere,
            subsurface_oceans: false,
            biosphere: 0,
            rings: None,
            proper_name: None,
            base_temperature,
        }
    }
 
    // -----------------------------------------------------------------------
    // Generation invariants
    // -----------------------------------------------------------------------
 
    /// The one-time clamp: every generated world lands inside its category's
    /// bounds for its own solvent, given the atmosphere it was generated with.
    #[test]
    fn generated_worlds_sit_inside_category_bounds() {
        each_planet(SEEDS, |seed, coord, body, p| {
            let s = solvent(p.chemistry);
            let (lo, hi) = min_max(p.category, p.atmosphere, s);
            let mean = p.temperature().mean;
            if let Some(lo) = lo {
                assert!(mean >= lo,
                    "seed {seed} {coord:?}: {} ({:?}, {s:?}, atm {}) mean {mean} below bound {lo}",
                    body.designation, p.category, p.atmosphere);
            }
            if let Some(hi) = hi {
                assert!(mean <= hi,
                    "seed {seed} {coord:?}: {} ({:?}, {s:?}, atm {}) mean {mean} above bound {hi}",
                    body.designation, p.category, p.atmosphere);
            }
        });
    }
 
    /// Any world with surface liquid and enough atmosphere to hold it must
    /// reach its own solvent's liquid range somewhere on its surface.
    ///
    /// Helian is excluded: with no solid surface, its hydrosphere measures
    /// ocean depth against the envelope, and temperature decides whether that
    /// layer is liquid at all.
    #[test]
    fn surface_liquid_worlds_reach_their_liquid_range() {
        each_planet(SEEDS, |seed, coord, body, p| {
            let surface_liquid = p.category != Category::Helian
                && p.atmosphere >= 2
                && (1..=11).contains(&p.hydrosphere);
            if surface_liquid {
                let t = p.temperature();
                let (freeze, boil) = liquid_range(t.solvent);
                assert!(t.min() <= boil && t.max() >= freeze,
                    "seed {seed} {coord:?}: {} ({:?}, {:?}, atm {}, hyd {}) spans {}..{}, \
                     never reaching liquid {freeze}..{boil}",
                    body.designation, p.category, t.solvent, p.atmosphere, p.hydrosphere,
                    t.min(), t.max());
            }
        });
    }
 
    /// Snowballs are ice worlds: below their solvent's freezing point on average.
    #[test]
    fn snowballs_are_below_their_freezing_point() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if p.category == Category::Snowball {
                let t = p.temperature();
                let (freeze, _) = liquid_range(t.solvent);
                assert!(t.mean < freeze,
                    "seed {seed} {coord:?}: {:?} Snowball {} has mean {} (freezes at {freeze})",
                    t.solvent, body.designation, t.mean);
            }
        });
    }
 
    /// A trace-atmosphere Oceanic is an ice shell over its ocean.
    #[test]
    fn airless_ocean_worlds_are_frozen_over() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if p.category == Category::Oceanic && p.atmosphere < 2 {
                let t = p.temperature();
                let (freeze, _) = liquid_range(t.solvent);
                assert!(t.mean < freeze,
                    "seed {seed} {coord:?}: trace-atmosphere {:?} Oceanic {} has mean {} \
                     (freezes at {freeze})",
                    t.solvent, body.designation, t.mean);
            }
        });
    }
 
    /// Molten surfaces and runaway greenhouses are hot in absolute terms,
    /// whatever the solvent. Thresholds are looser than the bounds on purpose.
    #[test]
    fn molten_and_runaway_worlds_are_hot() {
        each_planet(SEEDS, |seed, coord, body, p| {
            let mean = p.temperature().mean;
            match p.category {
                Category::Meltball => assert!(mean >= 600,
                    "seed {seed} {coord:?}: Meltball {} has mean {mean}", body.designation),
                Category::Telluric => assert!(mean >= 200,
                    "seed {seed} {coord:?}: Telluric {} has mean {mean}", body.designation),
                _ => {}
            }
        });
    }
 
    /// Every Vesperian has a terminator that's temperate for its own solvent.
    #[test]
    fn vesperians_have_a_temperate_terminator() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if p.category == Category::Vesperian {
                let t = p.temperature();
                assert!(t.spans(ClimateBand::Temperate),
                    "seed {seed} {coord:?}: {:?} Vesperian {} spans {}..{}, no temperate band",
                    t.solvent, body.designation, t.min(), t.max());
            }
        });
    }
 
    /// Where the clamp doesn't apply, the stored base is exactly the zone's
    /// raw temperature. Satellites share their parent's orbit type, so this
    /// also pins down inheritance.
    #[test]
    fn unbounded_categories_keep_their_zone_temperature() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if min_max(p.category, p.atmosphere, solvent(p.chemistry)) == (None, None) {
                assert_eq!(p.base_temperature, zone(body.orbit_type),
                    "seed {seed} {coord:?}: unbounded {} ({:?}) in {:?} has base {}",
                    body.designation, p.category, body.orbit_type, p.base_temperature);
            }
        });
    }
 
    #[test]
    fn spread_is_always_positive() {
        each_planet(SEEDS, |seed, coord, body, p| {
            let t = p.temperature();
            assert!(t.spread > 0,
                "seed {seed} {coord:?}: {} ({:?}) has spread {}",
                body.designation, p.category, t.spread);
        });
    }
 
    /// A planet's temperature is always read against its own solvent.
    #[test]
    fn temperature_carries_the_planets_solvent() {
        each_planet(SEEDS, |seed, coord, body, p| {
            assert_eq!(p.temperature().solvent, solvent(p.chemistry),
                "seed {seed} {coord:?}: {} ({:?}) has the wrong solvent on its temperature",
                body.designation, p.chemistry);
        });
    }
 
    // -----------------------------------------------------------------------
    // The solvent tables
    // -----------------------------------------------------------------------
 
    #[test]
    fn chemistry_maps_to_the_agreed_solvents() {
        assert_eq!(solvent(None), Solvent::Water, "no chemistry defaults to water");
        assert_eq!(solvent(Some(Chemistry::Water)), Solvent::Water);
        assert_eq!(solvent(Some(Chemistry::Sulfur)), Solvent::SulfuricAcid);
        assert_eq!(solvent(Some(Chemistry::Chlorine)), Solvent::Chlorine);
        assert_eq!(solvent(Some(Chemistry::Ammonia)), Solvent::Ammonia);
        assert_eq!(solvent(Some(Chemistry::Methane)), Solvent::Methane);
    }
 
    /// Each solvent's bands tile the whole number line with no gaps or
    /// overlaps: open at both ends, and each band starts where the last stops.
    #[test]
    fn band_tables_are_contiguous() {
        for s in SOLVENTS {
            assert_eq!(ClimateBand::Frozen.range(s).0, None, "{s:?}: Frozen has a floor");
            assert_eq!(ClimateBand::Scorching.range(s).1, None, "{s:?}: Scorching has a ceiling");
            for pair in BANDS.windows(2) {
                let (_, upper_of_lower) = pair[0].range(s);
                let (lower_of_upper, _) = pair[1].range(s);
                assert_eq!(upper_of_lower, lower_of_upper,
                    "{s:?}: gap or overlap between {:?} and {:?}", pair[0], pair[1]);
            }
        }
    }
 
    /// Temperate means comfortable for the solvent, so it must sit inside
    /// the solvent's liquid range.
    #[test]
    fn temperate_sits_inside_the_liquid_range() {
        for s in SOLVENTS {
            let (freeze, boil) = liquid_range(s);
            let (lo, hi) = ClimateBand::Temperate.range(s);
            let (lo, hi) = (lo.expect("Temperate has a floor"), hi.expect("Temperate has a ceiling"));
            assert!(lo >= freeze && hi <= boil,
                "{s:?}: Temperate {lo}..{hi} outside liquid {freeze}..{boil}");
        }
    }
 
    /// Wet categories are clamped into a range where their solvent is liquid.
    #[test]
    fn wet_bounds_sit_inside_the_liquid_range() {
        for s in SOLVENTS {
            let (freeze, boil) = liquid_range(s);
            let (lo, hi) = wet_bounds(s);
            assert!(lo <= hi, "{s:?}: wet bounds {lo}..{hi} are inverted");
            assert!(lo >= freeze && hi <= boil,
                "{s:?}: wet bounds {lo}..{hi} outside liquid {freeze}..{boil}");
        }
    }
 
    #[test]
    fn bands_are_ordered_cold_to_hot() {
        for pair in BANDS.windows(2) {
            assert!(pair[0] < pair[1], "{:?} should sort before {:?}", pair[0], pair[1]);
        }
    }
 
    // -----------------------------------------------------------------------
    // Unit tests on the model
    // -----------------------------------------------------------------------
 
    /// Band boundaries are half-open, and an Earth-like climate spans
    /// everything short of Scorching.
    #[test]
    fn water_bands_behave_as_specified() {
        let point = Temperature { mean: 15, spread: 0, solvent: Solvent::Water };
        assert!(point.spans(ClimateBand::Temperate));
        for band in [ClimateBand::Frozen, ClimateBand::Cold, ClimateBand::Hot, ClimateBand::Scorching] {
            assert!(!point.spans(band), "15 degrees should not span {band:?}");
        }
 
        let edge = Temperature { mean: 25, spread: 0, solvent: Solvent::Water };
        assert!(edge.spans(ClimateBand::Hot), "25 is Hot");
        assert!(!edge.spans(ClimateBand::Temperate), "25 is not Temperate");
 
        let earth = Temperature { mean: 15, spread: 41, solvent: Solvent::Water };
        for band in [ClimateBand::Frozen, ClimateBand::Cold, ClimateBand::Temperate, ClimateBand::Hot] {
            assert!(earth.spans(band), "Earth-like climate should span {band:?}");
        }
        assert!(!earth.spans(ClimateBand::Scorching));
    }
 
    /// The same temperature reads differently against different solvents.
    #[test]
    fn bands_depend_on_the_solvent() {
        let cold = Temperature { mean: -175, spread: 0, solvent: Solvent::Methane };
        assert!(cold.spans(ClimateBand::Temperate), "-175 is temperate for methane");
        let same_as_water = Temperature { solvent: Solvent::Water, ..cold };
        assert!(same_as_water.spans(ClimateBand::Frozen), "-175 is frozen for water");
    }
 
    /// Earth is the Kelvin anchor: 288 K means a scale factor of exactly 1.
    #[test]
    fn earth_is_unscaled() {
        let t = planet(Category::Tectonic, Some(Chemistry::Water), 6, 7, -15).temperature();
        assert_eq!(t.mean, 15);
        assert_eq!(t.spread, 41, "55 - 2*7 = 41, times 288/288");
    }
 
    /// Cold worlds swing less than warm ones with the same air and water.
    #[test]
    fn cold_worlds_swing_less() {
        let warm = planet(Category::Tectonic, Some(Chemistry::Water), 6, 7, -15).temperature();
        let cold = planet(Category::Tectonic, Some(Chemistry::Methane), 6, 7, -200).temperature();
        assert!(cold.spread < warm.spread,
            "a {}°C world swings {} but a {}°C one swings {}",
            cold.mean, cold.spread, warm.mean, warm.spread);
    }
 
    /// A Meltball's spread times its Kelvin temperature overflows i16. The
    /// multiplication must happen in a wider type. In a debug build the old
    /// code panics here; in release it produces nonsense, which the range
    /// check catches.
    #[test]
    fn hot_worlds_do_not_overflow() {
        let t = planet(Category::Meltball, None, 1, 15, 800).temperature();
        assert!(t.spread > 150 && t.spread < 1000,
            "Meltball at {}°C has spread {}", t.mean, t.spread);
    }
 
    /// Tide-locking doubles the spread exactly. This case is chosen so the
    /// order matters: at 27°C with a damped spread of 45, scaling then
    /// doubling gives 92, while doubling then scaling gives 93.
    #[test]
    fn tide_locking_doubles_exactly() {
        let locked = planet(Category::Vesperian, Some(Chemistry::Water), 6, 5, -3).temperature();
        let free = planet(Category::Tectonic, Some(Chemistry::Water), 6, 5, -3).temperature();
        assert_eq!(locked.mean, 27, "test setup: mean should be 27");
        assert_eq!(locked.spread, free.spread * 2,
            "locked {} is not twice free {}", locked.spread, free.spread);
    }
 
    /// The category clamp is applied once, at generation. Changing the
    /// atmosphere afterward moves the mean by exactly the greenhouse
    /// difference, and can take a world outside its bounds.
    #[test]
    fn changing_atmosphere_is_not_reclamped() {
        let mut p = planet(Category::Tectonic, Some(Chemistry::Water), 6, 7, -15);
        assert_eq!(p.temperature().mean, -15 + greenhouse(6));
 
        p.atmosphere = 12;
        let after = p.temperature().mean;
        assert_eq!(after, -15 + greenhouse(12));
 
        let (_, hi) = min_max(Category::Tectonic, 6, Solvent::Water);
        assert!(after > hi.expect("Tectonic has an upper bound"),
            "a runaway greenhouse should be able to leave its generated bounds");
    }
 
    /// Changing chemistry changes how a world is classified, not how hot it
    /// is — terraforming a methane world to water chemistry doesn't warm it.
    #[test]
    fn changing_chemistry_reclassifies_without_warming() {
        let mut p = planet(Category::Tectonic, Some(Chemistry::Methane), 6, 7, -200);
        let before = p.temperature();
        assert!(before.spans(ClimateBand::Temperate) || before.spans(ClimateBand::Hot),
            "setup: a -170°C methane world should be comfortable for methane");
 
        p.chemistry = Some(Chemistry::Water);
        let after = p.temperature();
        assert_eq!(after.mean, before.mean, "chemistry must not move the mean");
        assert_eq!(after.spread, before.spread, "chemistry must not move the spread");
        assert!(after.spans(ClimateBand::Frozen) && !after.spans(ClimateBand::Temperate),
            "the same world should read as frozen for water");
    }
}

#[cfg(test)]
mod life_rules {
    use crate::orbital_body::{Body, Category, Chemistry, OrbitalBody, Planet};
    use crate::sector_for;
    use crate::star::{LuminosityClass, Star};
    use crate::system_hex::Subsystem;
 
    const SEEDS: std::ops::Range<u64> = 0..15;
 
    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------
 
    fn walk(body: &OrbitalBody, f: &mut dyn FnMut(&OrbitalBody)) {
        f(body);
        for satellite in &body.satellites {
            walk(satellite, f);
        }
    }
 
    fn each_planet(
        seeds: std::ops::Range<u64>,
        mut f: impl FnMut(u64, (i16, i16, i16), &OrbitalBody, &Planet),
    ) {
        for seed in seeds {
            for (coord, system) in sector_for(seed) {
                for subsystem in &system.subsystems {
                    for root in subsystem.all_bodies() {
                        walk(root, &mut |body| {
                            if let Body::Planet(planet) = &body.body {
                                f(seed, coord, body, planet);
                            }
                        });
                    }
                }
            }
        }
    }
 
    /// Each group of stellar orbits, paired with the star whose luminosity
    /// class governed its generation. Shared bodies use the primary's, as
    /// `create_system` does.
    fn governed_groups(subsystem: &Subsystem) -> Vec<(&Star, &Vec<OrbitalBody>)> {
        match subsystem {
            Subsystem::Single { star, bodies } => vec![(star, bodies)],
            Subsystem::Binary { primary, companion, primary_bodies, companion_bodies, shared_bodies } =>
                vec![
                    (primary, primary_bodies),
                    (companion, companion_bodies),
                    (primary, shared_bodies),
                ],
        }
    }
 
    /// The highest biosphere each category can roll before any flare penalty.
    /// A category missing from this table gets a ceiling of 0, so the first
    /// living world of a new category fails the test until it's added here.
    fn natural_max(category: Category) -> u8 {
        match category {
            Category::Arean => 9,       // 1d6 + size(5) - 2
            Category::Promethean => 11, // 1d6 + size(5)
            Category::Arid | Category::Tectonic | Category::Vesperian
                | Category::Jovian => 12, // 2d6
            _ => 0, // no life, or always shielded
        }
    }
 
    // -----------------------------------------------------------------------
    // Subsurface oceans
    // -----------------------------------------------------------------------
 
    #[test]
    fn subsurface_oceans_only_on_oceanic_and_snowball() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if p.subsurface_oceans {
                assert!(matches!(p.category, Category::Oceanic | Category::Snowball),
                    "seed {seed} {coord:?}: {} ({:?}) has subsurface oceans",
                    body.designation, p.category);
            }
        });
    }
 
    /// An Oceanic world's ocean is under ice exactly when its atmosphere is
    /// too thin to hold liquid on the surface, whether or not anything lives
    /// there.
    #[test]
    fn oceanic_subsurface_iff_trace_atmosphere() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if p.category == Category::Oceanic {
                assert_eq!(p.subsurface_oceans, p.atmosphere < 2,
                    "seed {seed} {coord:?}: Oceanic {} has atmosphere {} but subsurface {}",
                    body.designation, p.atmosphere, p.subsurface_oceans);
            }
        });
    }
 
    #[test]
    fn living_snowballs_have_subsurface_oceans() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if p.category == Category::Snowball && p.biosphere > 0 {
                assert!(p.subsurface_oceans,
                    "seed {seed} {coord:?}: frozen-solid Snowball {} has biosphere {}",
                    body.designation, p.biosphere);
            }
        });
    }
 
    // -----------------------------------------------------------------------
    // Flare shielding
    // -----------------------------------------------------------------------
 
    /// Shielding reaches only worlds with an ice shell or a superdense ocean.
    /// A new category reaching this rule should be a deliberate decision.
    #[test]
    fn flare_shielding_only_reaches_ocean_worlds() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if p.flare_shielded() {
                assert!(matches!(p.category,
                        Category::Oceanic | Category::Panthalassic
                        | Category::Snowball | Category::Helian),
                    "seed {seed} {coord:?}: {} ({:?}) is flare-shielded",
                    body.designation, p.category);
            }
        });
    }
 
    /// No unshielded world around a flare star exceeds its category's natural
    /// ceiling minus the two-point penalty.
    #[test]
    fn flare_stars_hold_unshielded_biospheres_down() {
        for seed in SEEDS {
            for (coord, system) in sector_for(seed) {
                for subsystem in &system.subsystems {
                    for (star, bodies) in governed_groups(subsystem) {
                        if star.luminosity_class != LuminosityClass::MVe {
                            continue;
                        }
                        for root in bodies {
                            walk(root, &mut |body| {
                                if let Body::Planet(p) = &body.body {
                                    if !p.flare_shielded() {
                                        let ceiling = natural_max(p.category).saturating_sub(2);
                                        assert!(p.biosphere <= ceiling,
                                            "seed {seed} {coord:?}: {} ({:?}) orbits flare star {} \
                                             unshielded with biosphere {} (ceiling {ceiling})",
                                            body.designation, p.category, star.name, p.biosphere);
                                    }
                                }
                            });
                        }
                    }
                }
            }
        }
    }
 
    // -----------------------------------------------------------------------
    // Biologically produced atmospheres
    // -----------------------------------------------------------------------
 
    /// On these four categories, a water world's breathable atmosphere is made
    /// by its biosphere: atmosphere 2-9 exactly when biosphere is 3 or more.
    #[test]
    fn biologically_produced_atmospheres_match_biosphere() {
        each_planet(SEEDS, |seed, coord, body, p| {
            let life_made = matches!(p.category,
                Category::Arid | Category::Tectonic | Category::Vesperian | Category::Promethean);
            if life_made && p.chemistry == Some(Chemistry::Water) {
                assert_eq!((2..=9).contains(&p.atmosphere), p.biosphere >= 3,
                    "seed {seed} {coord:?}: {} ({:?}) has atmosphere {} with biosphere {}",
                    body.designation, p.category, p.atmosphere, p.biosphere);
            }
        });
    }
}

#[cfg(test)]
mod terrain_rules {
    use crate::orbital_body::{Body, Category, Chemistry, OrbitalBody, Planet};
    use crate::sector_for;
    use crate::temperature::{liquid_range, ClimateBand};
    use crate::terrain::Terrain;
    use crate::terrain::Terrain::*;
 
    const SEEDS: std::ops::Range<u64> = 0..10;
 
    const OCEAN: [Terrain; 3] = [ShallowOcean, OpenOcean, DeepOcean];
    const LIQUID_EDGED: [Terrain; 2] = [BeachShore, Riverbank];
    const VEGETATION: [Terrain; 7] = [Plains, Woods, Forest, Jungle, Rainforest, SwampMarsh, Tundra];
 
    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------
 
    /// A water-chemistry planet with nothing set. Tests override the fields
    /// they care about with struct update syntax:
    ///     Planet { atmosphere: 6, ..blank(Category::Tectonic) }
    fn blank(category: Category) -> Planet {
        Planet {
            order: 1,
            category,
            size: 8,
            chemistry: Some(Chemistry::Water),
            atmosphere: 0,
            hydrosphere: 0,
            subsurface_oceans: false,
            biosphere: 0,
            rings: None,
            proper_name: None,
            base_temperature: 0,
        }
    }
 
    fn reaches_liquid(p: &Planet) -> bool {
        let t = p.temperature();
        let (freeze, boil) = liquid_range(t.solvent);
        t.max() >= freeze && t.min() <= boil
    }
 
    fn walk(body: &OrbitalBody, f: &mut dyn FnMut(&OrbitalBody)) {
        f(body);
        for satellite in &body.satellites {
            walk(satellite, f);
        }
    }
 
    fn each_planet(
        seeds: std::ops::Range<u64>,
        mut f: impl FnMut(u64, (i16, i16, i16), &OrbitalBody, &Planet),
    ) {
        for seed in seeds {
            for (coord, system) in sector_for(seed) {
                for subsystem in &system.subsystems {
                    for root in subsystem.all_bodies() {
                        walk(root, &mut |body| {
                            if let Body::Planet(planet) = &body.body {
                                f(seed, coord, body, planet);
                            }
                        });
                    }
                }
            }
        }
    }
 
    // -----------------------------------------------------------------------
    // Hand-built worlds: each pins down one part of the rules exactly.
    // Worked temperatures are in the comments so a failure can be traced.
    // -----------------------------------------------------------------------
 
    /// Mean 15, spread 41: -26..56, spanning Frozen through Hot. Everything
    /// but Desert, which needs hydrosphere 4 or less.
    #[test]
    fn earth_like_world_has_everything_but_desert() {
        let p = Planet { atmosphere: 6, hydrosphere: 7, biosphere: 10, base_temperature: -15,
                         ..blank(Category::Tectonic) };
        assert_eq!(p.terrains(), vec![
            BeachShore, Clear, DeepOcean, Forest, Hills, IceSheet, Jungle, Mountains,
            OpenOcean, Plains, Rainforest, Riverbank, RoughBroken, ShallowOcean,
            SwampMarsh, Tundra, Woods,
        ]);
    }
 
    /// The same world with no life keeps its landscape and water, and loses
    /// every vegetation type.
    #[test]
    fn lifeless_world_has_no_vegetation() {
        let p = Planet { atmosphere: 6, hydrosphere: 7, biosphere: 0, base_temperature: -15,
                         ..blank(Category::Tectonic) };
        assert_eq!(p.terrains(), vec![
            BeachShore, Clear, DeepOcean, Hills, IceSheet, Mountains, OpenOcean,
            Riverbank, RoughBroken, ShallowOcean,
        ]);
    }
 
    /// Mean -20, spread 23: -43..3. Reaches liquid, spans Frozen and Cold,
    /// never Temperate. Forest, woods, swamp and tundra; no jungle, no plains.
    #[test]
    fn cold_world_has_boreal_terrain_only() {
        let p = Planet { atmosphere: 8, hydrosphere: 9, biosphere: 10, base_temperature: -70,
                         ..blank(Category::Tectonic) };
        assert_eq!(p.terrains(), vec![
            BeachShore, Clear, DeepOcean, Forest, Hills, IceSheet, Mountains, OpenOcean,
            Riverbank, RoughBroken, ShallowOcean, SwampMarsh, Tundra, Woods,
        ]);
    }
 
    /// Mean 55, spread 46: 9..101. Never Cold or Frozen.
    #[test]
    fn hot_world_has_jungle_and_no_ice() {
        let p = Planet { atmosphere: 6, hydrosphere: 7, biosphere: 10, base_temperature: 25,
                         ..blank(Category::Tectonic) };
        let t = p.terrains();
        assert!(t.contains(&Jungle) && t.contains(&Rainforest), "got {t:?}");
        assert!(!t.contains(&IceSheet) && !t.contains(&Tundra), "got {t:?}");
    }
 
    /// Mean -170, spread 14: -184..-156. Temperate-to-hot for methane, so it
    /// gets jungle. Relabelled as water, the same world is frozen and dead.
    #[test]
    fn climate_terrain_follows_the_solvent() {
        let methane = Planet { chemistry: Some(Chemistry::Methane), atmosphere: 6,
                               hydrosphere: 7, biosphere: 10, base_temperature: -200,
                               ..blank(Category::Tectonic) };
        let t = methane.terrains();
        assert!(t.contains(&Jungle) && t.contains(&OpenOcean), "methane world got {t:?}");
        assert!(!t.contains(&IceSheet), "methane world never reaches its Frozen band: {t:?}");
 
        let water = Planet { chemistry: Some(Chemistry::Water), ..methane };
        assert_eq!(water.terrains(), vec![Clear, Hills, IceSheet, Mountains, RoughBroken],
            "at -170 a water world is ice and rock");
    }
 
    /// Hydrosphere 10 is total ice cover: no land, and no ocean without
    /// weather or an ice shell. Just ice.
    #[test]
    fn frozen_solid_snowball_is_only_ice() {
        let p = Planet { atmosphere: 0, hydrosphere: 10, base_temperature: -100,
                         ..blank(Category::Snowball) };
        assert_eq!(p.terrains(), vec![IceSheet]);
    }
 
    /// Oceans under the ice need no weather and no surface liquid.
    #[test]
    fn subsurface_snowball_has_oceans_under_ice() {
        let p = Planet { atmosphere: 0, hydrosphere: 6, subsurface_oceans: true, biosphere: 3,
                         base_temperature: -100, ..blank(Category::Snowball) };
        assert_eq!(p.terrains(), vec![
            Clear, DeepOcean, Hills, IceSheet, Mountains, OpenOcean, RoughBroken, ShallowOcean,
        ]);
    }
 
    /// An ice-shelled global ocean: ice on top, open and deep water beneath,
    /// no shallows at hydrosphere 11.
    #[test]
    fn ice_shelled_ocean_world() {
        let p = Planet { atmosphere: 1, hydrosphere: 11, subsurface_oceans: true, biosphere: 5,
                         base_temperature: -25, ..blank(Category::Oceanic) };
        assert_eq!(p.terrains(), vec![DeepOcean, IceSheet, OpenOcean]);
    }
 
    /// No solid surface: only Open and Deep Ocean, and never ice.
    #[test]
    fn panthalassic_is_only_open_and_deep_ocean() {
        let p = Planet { atmosphere: 9, hydrosphere: 11, biosphere: 10, base_temperature: -30,
                         ..blank(Category::Panthalassic) };
        assert_eq!(p.terrains(), vec![DeepOcean, OpenOcean]);
    }
 
    /// A Helian gets ocean only at hydrosphere 11, and only if it's liquid.
    #[test]
    fn helians_get_ocean_only_when_superdense_and_liquid() {
        let warm = Planet { chemistry: None, atmosphere: 13, hydrosphere: 11,
                            base_temperature: -40, ..blank(Category::Helian) };
        assert_eq!(warm.terrains(), vec![DeepOcean, OpenOcean], "mean 20");
 
        let frozen = Planet { base_temperature: -150, ..warm };
        assert_eq!(frozen.terrains(), Vec::<Terrain>::new(), "mean -90: frozen, and no surface to hold ice");
 
        let shallow = Planet { chemistry: None, atmosphere: 13, hydrosphere: 6,
                               base_temperature: -40, ..blank(Category::Helian) };
        assert_eq!(shallow.terrains(), Vec::<Terrain>::new(), "below 11, hydrosphere is depth, not coverage");
    }
 
    #[test]
    fn jovians_have_no_terrain() {
        let p = Planet { chemistry: None, atmosphere: 16, hydrosphere: 16, biosphere: 10,
                         base_temperature: -150, ..blank(Category::Jovian) };
        assert_eq!(p.terrains(), Vec::<Terrain>::new());
    }
 
    /// Airless and dry: bare landscape only. No desert without weather, no
    /// ice without water.
    #[test]
    fn airless_rock_is_bare_landscape() {
        let p = Planet { chemistry: None, atmosphere: 0, hydrosphere: 0, base_temperature: -15,
                         ..blank(Category::Rockball) };
        assert_eq!(p.terrains(), vec![Clear, Hills, Mountains, RoughBroken]);
    }
 
    /// Mean -30, spread 40: -70..10. A cold desert with polar ice and not
    /// enough water for shores or rivers.
    #[test]
    fn cold_dry_world_is_desert_and_ice() {
        let p = Planet { atmosphere: 10, hydrosphere: 1, base_temperature: -60,
                         ..blank(Category::Arean) };
        assert_eq!(p.terrains(), vec![Clear, Desert, Hills, IceSheet, Mountains, RoughBroken]);
    }
 
    // -----------------------------------------------------------------------
    // Sector-wide invariants
    // -----------------------------------------------------------------------
 
    /// Animal generation walks terrains in order and rolls dice per terrain,
    /// so the order must be fixed: declaration order, no duplicates.
    #[test]
    fn terrains_are_in_declaration_order_without_duplicates() {
        each_planet(SEEDS, |seed, coord, body, p| {
            let t = p.terrains();
            assert!(t.windows(2).all(|w| w[0] < w[1]),
                "seed {seed} {coord:?}: {} has terrains out of order: {t:?}", body.designation);
        });
    }
 
    /// Hydrosphere 11 is a world ocean: nothing but water and its ice.
    #[test]
    fn superdense_worlds_are_only_ocean_and_ice() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if p.hydrosphere == 11 {
                for t in p.terrains() {
                    assert!(matches!(t, OpenOcean | DeepOcean | IceSheet),
                        "seed {seed} {coord:?}: {} ({:?}, hydrosphere 11) has {t:?}",
                        body.designation, p.category);
                }
            }
        });
    }
 
    /// Worlds with no solid surface have no land and no ice, and ocean only
    /// at hydrosphere 11.
    #[test]
    fn worlds_without_ground_have_only_deep_water() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if matches!(p.category, Category::Helian | Category::Panthalassic | Category::Jovian) {
                let t = p.terrains();
                assert!(t.iter().all(|x| matches!(x, OpenOcean | DeepOcean)),
                    "seed {seed} {coord:?}: {} ({:?}) has {t:?}", body.designation, p.category);
                if p.hydrosphere != 11 {
                    assert!(t.is_empty(),
                        "seed {seed} {coord:?}: {} ({:?}, hydrosphere {}) has {t:?}",
                        body.designation, p.category, p.hydrosphere);
                }
            }
        });
    }
 
    /// Vegetation needs complex life and liquid somewhere on the surface.
    #[test]
    fn vegetation_needs_life_and_liquid() {
        each_planet(SEEDS, |seed, coord, body, p| {
            for t in p.terrains() {
                if VEGETATION.contains(&t) {
                    assert!(p.biosphere >= 9,
                        "seed {seed} {coord:?}: {} has {t:?} at biosphere {}",
                        body.designation, p.biosphere);
                    assert!(reaches_liquid(p),
                        "seed {seed} {coord:?}: {} has {t:?} but never reaches liquid",
                        body.designation);
                }
            }
        });
    }
 
    /// Open water needs liquid on the surface, or an ice shell over it.
    #[test]
    fn water_terrain_needs_liquid_or_an_ice_shell() {
        each_planet(SEEDS, |seed, coord, body, p| {
            for t in p.terrains() {
                if OCEAN.contains(&t) {
                    assert!(p.subsurface_oceans || reaches_liquid(p),
                        "seed {seed} {coord:?}: {} ({:?}) has {t:?} with no liquid",
                        body.designation, p.category);
                }
                if LIQUID_EDGED.contains(&t) {
                    assert!(reaches_liquid(p),
                        "seed {seed} {coord:?}: {} ({:?}) has {t:?} with no liquid",
                        body.designation, p.category);
                }
            }
        });
    }
 
    /// Ice needs water to freeze and somewhere cold enough to freeze it.
    #[test]
    fn ice_needs_water_and_frost() {
        each_planet(SEEDS, |seed, coord, body, p| {
            if p.terrains().contains(&IceSheet) {
                assert!((1..=11).contains(&p.hydrosphere),
                    "seed {seed} {coord:?}: {} has ice at hydrosphere {}",
                    body.designation, p.hydrosphere);
                assert!(p.temperature().spans(ClimateBand::Frozen),
                    "seed {seed} {coord:?}: {} has ice but never freezes", body.designation);
            }
        });
    }

    /// Hydrosphere 3 has open water, but not deep ocean.
    #[test]
    fn deep_ocean_needs_real_depth() {
        let p = Planet { atmosphere: 6, hydrosphere: 3, base_temperature: -15,
                        ..blank(Category::Tectonic) };
        let t = p.terrains();
        assert!(t.contains(&OpenOcean) && t.contains(&ShallowOcean), "got {t:?}");
        assert!(!t.contains(&DeepOcean), "hydrosphere 3 is too shallow for deep ocean: {t:?}");
    }
}

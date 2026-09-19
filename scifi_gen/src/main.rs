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
                    match &ob.body {
                        Body::AsteroidBelt => {
                            fingerprint_body(&mut out, ob, 0)
                        }
                        Body::Planet(p) => {
                            fingerprint_body(&mut out, ob, 0)
                        }
                    }
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
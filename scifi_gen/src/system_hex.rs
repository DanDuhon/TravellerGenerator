use crate::dice_roller::roll_xdy;
use crate::star::LuminosityClass;
use rand_chacha::ChaCha8Rng;
use rand::RngExt;
use crate::star::Star;
use crate::star::StarRole;
use crate::star::CompanionOrbit;
use crate::Namer;
use crate::star::create_star;
use crate::star::create_brown_dwarf;
use crate::orbital_body::OrbitalBody;
use crate::orbital_body::OrbitType;
use crate::orbital_body::Group;
use crate::orbital_body::to_roman;
use crate::orbital_body::create_orbital_body;

const ORDINAL: [&str; 4] = [" Alpha", " Beta", " Gamma", " Delta"];

pub enum Subsystem {
    Single {
        star: Star,
        bodies: Vec<OrbitalBody>,
    },
    // A primary plus one Tight/Close/Moderate companion.
    Binary {
        primary: Star,
        companion: Star,                       // role = Companion(Tight|Close|Moderate)
        primary_bodies: Vec<OrbitalBody>,      // orbits the primary
        companion_bodies: Vec<OrbitalBody>,    // orbits the companion
        shared_bodies: Vec<OrbitalBody>,       // orbits both
    },
}

impl Subsystem {
    pub fn all_bodies(&self) -> impl Iterator<Item = &OrbitalBody> {
        let groups: [&[OrbitalBody]; 3] = match self {
            Subsystem::Single { bodies, .. } => [bodies.as_slice(), &[], &[]],
            Subsystem::Binary { primary_bodies, companion_bodies, shared_bodies, .. } =>
                [primary_bodies.as_slice(), companion_bodies.as_slice(), shared_bodies.as_slice()],
        };
        groups.into_iter().flatten()
    }

    pub fn stars(&self) -> impl Iterator<Item = &Star> {
        let group: [Option<&Star>; 2] = match self {
            Subsystem::Single { star, .. } => [Some(star), None],
            Subsystem::Binary { primary, companion, .. } => [Some(primary), Some(companion)],
        };
        group.into_iter().flatten()   // flatten drops the Nones
}
}

pub struct System {
    pub coordinates: (i16, i16, i16),
    pub open_cluster: bool,
    pub age: u8,
    pub name: Option<String>,
    pub subsystems: Vec<Subsystem>,
}

impl System {
    // pub fn has_brown_dwarf(&self) -> bool {
    //     self.stars.iter().any(|s| matches!(s.role, StarRole::BrownDwarf))
    // }
    // pub fn number_of_stars(&self) -> usize {
    //     self.stars.len()
    // }
    // pub fn primary(&self) -> Option<&Star> {
    //     self.stars.iter().find(|s| matches!(s.role, StarRole::Primary))
    // }
    pub fn designation(&self) -> String {
        match &self.name {
            Some(n) => n.clone(),
            None => {
                let (h, v, _) = self.coordinates;
                format!("Void {h:+04}{v:+04}")
            }
        }
    }
    // pub fn unrefined_fuel_available(&self) -> bool {
    //     // look for gas giants and water worlds
    // }
    // pub fn refined_fuel_available(&self) -> bool {
    //     // look for a starport of class C+
    // }
}

fn roll_base_star_count(rng: &mut ChaCha8Rng, open_cluster: bool) -> usize {
    if roll_xdy(rng, 1, 6) + if open_cluster { 2 } else { 0 } < 4 {
        return 0;
    }
    match roll_xdy(rng, 3, 6) + if open_cluster { 3 } else { 0 } {
        ..=10 => 1,
        11..=15 => 2,
        _ => 3,
    }
}

fn lookup_companion_orbit(roll: u8) -> CompanionOrbit {
    match roll {
        ..=2 => CompanionOrbit::Tight,
        3..=4 => CompanionOrbit::Close,
        5 => CompanionOrbit::Moderate,
        _ => CompanionOrbit::Distant
    }
}

fn zone_counts(rng: &mut ChaCha8Rng, lum: &LuminosityClass) -> [u8; 3] {
    let mv = if *lum == LuminosityClass::MV { 1 } else { 0 };
    let mv_or_l = if *lum == LuminosityClass::MV || *lum == LuminosityClass::L { 1 } else { 0 };
    let inner_die = if *lum == LuminosityClass::L { 3 } else { 6 };

    let epistellar = (roll_xdy(rng, 1, 6) as i8 - 3 - mv).clamp(0, 2) as u8;
    let inner      = (roll_xdy(rng, 1, inner_die) as i8 - 1 - mv).clamp(0, 5) as u8;
    let outer      = (roll_xdy(rng, 1, 6) as i8 - 1 - mv_or_l).clamp(0, 5) as u8;
    [epistellar, inner, outer]
}

fn fill_zone(
    rng: &mut ChaCha8Rng,
    zone: OrbitType,
    lum: &LuminosityClass,
    name_base: &str,
    dest: &mut Vec<OrbitalBody>,
    order: &mut u8,
    age: u8,
    count: u8,
) {
    for _ in 0..count {
        let designation = format!("{name_base} {}", to_roman(*order));
        let roll = (roll_xdy(rng, 1, 6) as i8 - if *lum == LuminosityClass::L { 1 } else { 0 }).max(0) as u8;
        let group = match roll {
            ..=1 => Group::AsteroidBelt,
            2 => Group::Dwarf,
            3 => Group::Terrestrial,
            4 => Group::Helian,
            _ => Group::Jovian,
        };
        dest.push(create_orbital_body(
            rng,
            *order,
            zone,
            designation,
            name_base,
            lum,
            age,
            group,
            None,
            false,
        ));
        *order += 1;
    }
}

pub fn create_system(rng: &mut ChaCha8Rng, namer: &mut Namer, h: i16, v: i16, open_cluster: bool) -> System {
    let age = roll_xdy(rng, 3, 6) - 3;
    let has_brown_dwarf = rng.random_bool(0.5);
    let base = roll_base_star_count(rng, open_cluster);
    let mut subsystems: Vec<Subsystem> = Vec::new();
    let mut companion_orbits: Vec<CompanionOrbit> = Vec::new();
    // Set the first companion normally
    if base > 1 {
        companion_orbits.push(lookup_companion_orbit(roll_xdy(rng, 1, 6)));
    }
    // To avoid the three body problem, set the second companion to Distant if the first one isn't Distant
    // Otherwise, set it normally
    if base > 2 {
        companion_orbits.push(lookup_companion_orbit(roll_xdy(rng, 1, 6)));
        if companion_orbits[0] != CompanionOrbit::Distant
            && companion_orbits[1] != CompanionOrbit::Distant
        {
            companion_orbits[1] = CompanionOrbit::Distant;
        }
    }

    let has_stars = base > 0 || has_brown_dwarf;
    let base_name = if has_stars { namer.star(rng) } else { String::new() };
    let mut star_count = 0;

    if base > 0 {
        let primary_roll = roll_xdy(rng, 2, 6);
        let primary = create_star(rng, &StarRole::Primary, &age, &primary_roll, format!("{}{}", base_name, ORDINAL[star_count]));
        star_count += 1;
        let binary_orbit = companion_orbits.iter().copied().find(|o| *o != CompanionOrbit::Distant);

        match binary_orbit {
            Some(orbit) => {
                let companion_roll = primary_roll + roll_xdy(rng, 1, 6) - 1;
                let companion = create_star(rng, &StarRole::Companion(orbit), &age, &companion_roll, format!("{}{}", base_name, ORDINAL[star_count]));
                star_count += 1;
                subsystems.push(Subsystem::Binary {
                    primary, companion,
                    primary_bodies: Vec::new(),
                    companion_bodies: Vec::new(),
                    shared_bodies: Vec::new(),
                });
            }
            None => subsystems.push(Subsystem::Single { star: primary, bodies: Vec::new() }),
        }

        // Each Distant companion is its own Single.
        for orbit in companion_orbits.iter().copied().filter(|o| *o == CompanionOrbit::Distant) {
            let companion_roll = primary_roll + roll_xdy(rng, 1, 6) - 1;
            subsystems.push(Subsystem::Single { star: create_star(rng, &StarRole::Companion(orbit), &age, &companion_roll, format!("{}{}", base_name, ORDINAL[star_count])), bodies: Vec::new() });
            star_count += 1;
        }
    }

    if has_brown_dwarf {
        subsystems.push(Subsystem::Single { star: create_brown_dwarf(format!("{}{}", base_name, ORDINAL[star_count])), bodies: Vec::new() });
    }

    // Fill subsystems with orbital bodies.
    for subsystem in &mut subsystems {
        match subsystem {
            Subsystem::Single { star, bodies } => {
                let [epi, inner, outer] = zone_counts(rng, &star.luminosity_class);
                let mut order: u8 = 1;
                fill_zone(rng, OrbitType::Epistellar, &star.luminosity_class, &star.name, bodies, &mut order, age, epi);
                fill_zone(rng, OrbitType::InnerZone, &star.luminosity_class, &star.name, bodies, &mut order, age, inner);
                fill_zone(rng, OrbitType::OuterZone, &star.luminosity_class, &star.name, bodies, &mut order, age, outer);
            },
            Subsystem::Binary { primary, companion, primary_bodies, companion_bodies, shared_bodies } => {
                let primary_counts = zone_counts(rng, &primary.luminosity_class);
                let p_epi = primary_counts[0];
                let p_inner = primary_counts[1];
                let p_outer = primary_counts[2];
                let companion_counts = zone_counts(rng, &companion.luminosity_class);
                let c_epi = companion_counts[0];
                let c_inner = companion_counts[1];
                let mut primary_order: u8 = 1;
                let mut companion_order: u8 = 1;
                let mut shared_order: u8 = 1;
                let shared_base = format!("{} Alpha-Beta", base_name);
                let companion_orbit = match companion.role {
                    StarRole::Companion(o) => o,
                    _ => unreachable!("Binary companion is always a Companion role"),
                };

                // No epistellar orbits if the Companion is Tight
                // In other configurations each star has its own epistellar orbits
                match companion_orbit {
                    CompanionOrbit::Close | CompanionOrbit::Moderate => {
                        fill_zone(rng, OrbitType::Epistellar, &primary.luminosity_class, &primary.name, primary_bodies, &mut primary_order, age, p_epi);
                        fill_zone(rng, OrbitType::Epistellar, &companion.luminosity_class, &companion.name, companion_bodies, &mut companion_order, age, c_epi);
                    },
                    CompanionOrbit::Tight => {}, // No epistellar orbits here
                    CompanionOrbit::Distant => unreachable!("Distant is a separate Single")
                }

                // No inner zone orbits if the Companion is Close
                // If Tight, inner zone planets orbit both
                // If Moderate, inner zone planets orbit one star
                match companion_orbit {
                    CompanionOrbit::Tight => {
                        fill_zone(rng, OrbitType::InnerZone, &primary.luminosity_class, &shared_base, shared_bodies, &mut shared_order, age, p_inner);
                    }
                    CompanionOrbit::Moderate => {
                        fill_zone(rng, OrbitType::InnerZone, &primary.luminosity_class, &primary.name, primary_bodies, &mut primary_order, age, p_inner);
                        fill_zone(rng, OrbitType::InnerZone, &companion.luminosity_class, &companion.name, companion_bodies, &mut companion_order, age, c_inner);
                    },
                    CompanionOrbit::Close => {} // No inner zone orbits here
                    CompanionOrbit::Distant => unreachable!("Distant is a separate Single")
                }

                // No outer zone orbits if Companion is Moderate
                // If Tight or Close, outer zone planets orbit both
                match companion_orbit {
                    CompanionOrbit::Tight | CompanionOrbit::Close => {
                        fill_zone(rng, OrbitType::OuterZone, &primary.luminosity_class, &shared_base, shared_bodies, &mut shared_order, age, p_outer);
                    },
                    CompanionOrbit::Distant => unreachable!("Distant is a separate Single"),
                    CompanionOrbit::Moderate => {} // No outer zone orbits here
                }
            }
        }
    }
    
    System {
        coordinates: (h, v, -h - v),
        open_cluster: open_cluster,
        age: age,
        name: if has_stars { Some(base_name) } else { None },
        subsystems: subsystems,
    }
}
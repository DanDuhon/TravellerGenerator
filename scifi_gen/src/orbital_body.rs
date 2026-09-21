use rand_chacha::ChaCha8Rng;
use crate::star::LuminosityClass;
use crate::dice_roller::roll_xdy;
use std::cmp::max;
use std::cmp::min;

pub struct OrbitalBody {
    pub order: u8,
    pub orbit_type: OrbitType,
    pub designation: String,
    pub satellites: Vec<OrbitalBody>,
    pub body: Body,
}

impl OrbitalBody {
    pub fn display_name(&self) -> &str {
        match &self.body {
            Body::Planet(p) => p.proper_name.as_deref().unwrap_or(&self.designation),
            Body::AsteroidBelt => &self.designation,
        }
    }
}

pub enum Body {
    AsteroidBelt,
    Planet(Planet),
}

pub struct Planet {
    pub order: u8,
    pub category: Category,
    pub size: u8,
    pub chemistry: Option<Chemistry>,
    pub atmosphere: u8,
    pub hydrosphere: u8,
    pub biosphere: u8,
    pub rings: Option<RingsType>,
    pub proper_name: Option<String>
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Category { Rockball, Snowball, Meltball, Hebean, Promethean, Arean, Stygian,
                    Telluric, Arid, Tectonic, Oceanic, Vesperian, JaniLithic, Acheronian,
                    Helian, Panthalassic, Asphodelian, Jovian, Chthonian, AsteroidBelt }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Group { AsteroidBelt, Dwarf, Terrestrial, Helian, Jovian }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Chemistry { Ammonia, Chlorine, Methane, Sulfur, Water }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OrbitType { Epistellar, InnerZone, OuterZone }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RingsType { Minor, Complex }

pub fn to_roman(n: u8) -> &'static str {
    const NUMERALS: [&str; 21] = [
        "", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
        "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
    ];
    NUMERALS.get(n as usize).copied().unwrap_or("?")
}

pub fn category_group(cat: Category) -> Group {
    match cat {
        Category::AsteroidBelt => Group::AsteroidBelt,
        Category::Rockball | Category::Snowball | Category::Meltball | Category::Hebean
        | Category::Promethean | Category::Arean | Category::Stygian => Group::Dwarf,
        Category::Telluric | Category::Arid | Category::Tectonic | Category::Oceanic
        | Category::Vesperian | Category::JaniLithic | Category::Acheronian => Group::Terrestrial,
        Category::Helian | Category::Panthalassic | Category::Asphodelian => Group::Helian,
        Category::Jovian | Category::Chthonian => Group::Jovian,
    }
}

pub fn describe(cat: Category) -> &'static str {
    match cat {
        Category::Acheronian => { "These are worlds that were directly affected by their primary's transition from the main sequence; the atmosphere and oceans have been boiled away, leaving a scorched, dead planet." },
        Category::Arean => { "These are worlds with little liquid, that move through a slow geological cycle of a gradual build-up, a short wet and clement period, and a long decline." },
        Category::Arid => { "These are worlds with limited amounts of surface liquid, that maintain an equilibrium with the help of their tectonic activity and their biosphere." },
        Category::Asphodelian => { "These are worlds that were directly affected by their primary's transition from the main sequence; their atmosphere has been boiled away, leaving the surface exposed." },
        Category::Chthonian => { "These are worlds that were directly affected by their primary's transition from the main sequence, or that have simply spent too long in a tight epistellar orbit; their atmospheres have been stripped away." },
        Category::Hebean => { "These are highly active worlds, due to tidal flexing, but with some regions of stability; the larger ones may be able to maintain some atmosphere and surface liquid." },
        Category::Helian => { "These are typical helian or subgiant worlds - large enough to retain helium atmospheres." },
        Category::JaniLithic => { "These worlds, tide-locked to the primary, are rocky, dry, and geologically active." },
        Category::Jovian => { "These are huge worlds with helium-hydrogen envelopes and compressed cores; the largest emit more heat than they absorb." },
        Category::Meltball => { "These are dwarfs with molten or semi-molten surfaces, either from extreme tidal flexing, or extreme approach to a star." },
        Category::Oceanic => { "These are worlds with a continuous hydrological cycle and deep oceans, due to either dense greenhouse atmosphere or active plate tectonics." },
        Category::Panthalassic => { "These are massive worlds, aborted gas giants, largely composed of water and hydrogen." },
        Category::Promethean => { "These are worlds that, through tidal-flexing, have a geological cycle similar to plate tectonics, that supports surface liquid and atmosphere." },
        Category::Rockball => { "These are mostly dormant worlds, with surfaces largely unchanged since the early period of planetary formation." },
        Category::Snowball => { "These worlds are composed of mostly ice and some rock. They may have varying degrees of activity, ranging from completely cold and still to cryo-volcanically active with extensive subsurface oceans." },
        Category::Stygian => { "These are worlds that were directly affected by their primary's transition from the main sequence; they are melted and blasted lumps." },
        Category::Tectonic => { "These are worlds with active plate tectonics and large bodies of surface liquid, allowing for stable atmospheres and a high likelihood of life." },
        Category::Telluric => { "These are worlds with geoactivity but no hydrological cycle at all, leading to dense runaway-greenhouse atmospheres." },
        Category::Vesperian => { "These worlds are tide-locked to their primary, but at a distance that permits surface liquid and the development of life." },
        Category::AsteroidBelt => { "" }
    }
}

pub fn create_orbital_body(
    rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, designation: String,
    star_name: &str, luminosity_class: &LuminosityClass, system_age: u8,
    group: Group, parent_group: Option<Group>, is_binary_companion: bool
) -> OrbitalBody {
    let (num_of_sats, body) = match group {
        Group::AsteroidBelt => {
            (if roll_xdy(rng, 1, 6) >= 5 { 1 } else { 0 } as usize,
            Body::AsteroidBelt)
        },
        Group::Dwarf => {
            let planet = create_dwarf_planet(rng, order, orbit_type, luminosity_class, &system_age, parent_group);
            if is_binary_companion == false {
                (if roll_xdy(rng, 1, 6) == 6 { 1 } else { 0 } as usize,
                Body::Planet(planet))
            } else { // Don't let a dwarf binary companion keep generating companions
                (0 as usize,
                Body::Planet(planet))
            }
        },
        Group::Terrestrial => {
            let planet = create_terrestrial_planet(rng, order, orbit_type, luminosity_class, &system_age, parent_group);
            (if roll_xdy(rng, 1, 6) >= 5 { 1 } else { 0 } as usize,
            Body::Planet(planet))
        }
        Group::Helian => {
            let planet = create_helian_planet(rng, order, orbit_type, luminosity_class, &system_age);
            (max(0, roll_xdy(rng, 1, 6) as i8 - 3) as usize,
            Body::Planet(planet))
        }
        Group::Jovian => {
            let planet = create_jovian_planet(rng, order, orbit_type, luminosity_class, &system_age);
            (roll_xdy(rng, 1, 6) as usize,
            Body::Planet(planet))
        }
    };

    let satellites = if num_of_sats > 0 {
        generate_satellites(rng, &body, orbit_type, &designation, star_name, luminosity_class, &system_age, parent_group, num_of_sats)
    } else { Vec::with_capacity(0) };

    OrbitalBody {
        order,
        orbit_type,
        designation: designation,
        satellites: satellites,
        body,
    }
}

fn push_satellite(
    rng: &mut ChaCha8Rng, sats: &mut Vec<OrbitalBody>, orbit_type: OrbitType,
    parent_designation: &str, star_name: &str, lum: &LuminosityClass, age: u8,
    group: Group, parent_group: Option<Group>, is_companion: bool,
) {
    let index = (sats.len() + 1) as u8;
    let desig = format!("{parent_designation}-{index}");
    sats.push(create_orbital_body(rng, index, orbit_type, desig, star_name, lum, age, group, parent_group, is_companion));
}

fn generate_satellites(
    rng: &mut ChaCha8Rng, body: &Body, orbit_type: OrbitType,
    parent_designation: &str, star_name: &str, lum: &LuminosityClass,
    age: &u8, own_parent_group: Option<Group>, num_of_sats: usize
) -> Vec<OrbitalBody> {
    let mut sats = Vec::with_capacity(num_of_sats);

    match body {
        Body::AsteroidBelt => {
            push_satellite(
                rng, &mut sats, orbit_type, parent_designation, star_name,
                lum, *age, Group::Dwarf, Some(Group::AsteroidBelt), false,
            );
        }
        Body::Planet(p) => match category_group(p.category) {
            Group::Dwarf => {
                let desig = format!("{parent_designation}b");
                sats.push(create_orbital_body(
                    rng,
                    1,
                    orbit_type,
                    desig,
                    star_name,
                    lum,
                    *age,
                    Group::Dwarf,
                    own_parent_group,
                    true, // This ensures a companion dwarf can't create more companions
                ));
            },
            Group::Terrestrial => {
                push_satellite(
                rng, &mut sats, orbit_type, parent_designation, star_name,
                lum, *age, Group::Dwarf, Some(Group::Terrestrial), false,
                );
            },
            Group::Helian => {
                for i in 0..num_of_sats {
                    if i == 0 && roll_xdy(rng, 1, 6) == 6 {
                        push_satellite(
                            rng, &mut sats, orbit_type, parent_designation, star_name,
                            lum, *age, Group::Terrestrial, Some(Group::Helian), false,
                        );
                    } else {
                        push_satellite(
                            rng, &mut sats, orbit_type, parent_designation, star_name,
                            lum, *age, Group::Dwarf, Some(Group::Helian), false,
                        );
                    }
                }
            },
            Group::Jovian => {
                for i in 0..num_of_sats {
                    if i == 0 && roll_xdy(rng, 1, 6) == 6 {
                        if roll_xdy(rng, 1, 6) == 6 {
                            push_satellite(
                                rng, &mut sats, orbit_type, parent_designation, star_name,
                                lum, *age, Group::Helian, Some(Group::Jovian), false,
                            );
                        } else {
                            push_satellite(
                                rng, &mut sats, orbit_type, parent_designation, star_name,
                                lum, *age, Group::Terrestrial, Some(Group::Jovian), false,
                            );
                        }
                    } else {
                        push_satellite(
                            rng, &mut sats, orbit_type, parent_designation, star_name,
                            lum, *age, Group::Dwarf, Some(Group::Jovian), false,
                        );
                    }
                }
            },
            Group::AsteroidBelt => {}
        }
    }
    sats
}

fn planet_size(rng: &mut ChaCha8Rng, group: &Group) -> u8 {
    match group {
        Group::AsteroidBelt => { 34 },
        Group::Dwarf => { roll_xdy(rng, 1, 6) - 1 },
        Group::Terrestrial => { roll_xdy(rng, 1, 6) + 4 },
        Group::Helian => { roll_xdy(rng, 1, 6) + 9 },
        Group::Jovian => { 16 }
    }
}

fn dwarf_chem_dm(lum: LuminosityClass, orbit: OrbitType, category: Category) -> i8 {
    let l = if lum == LuminosityClass::L { 2 } else { 0 };
    let outer = if orbit == OrbitType::OuterZone { 2 } else { 0 };
    let epistellar = if orbit == OrbitType::Epistellar && category == Category::Promethean { -2 } else { 0 };
    l + outer + epistellar
}

fn dwarf_chemistry(roll: i8) -> (u8, Option<Chemistry>) {
    match roll {
        ..=4 => { (0, Some(Chemistry::Water)) },
        5..=6 => { (1, Some(Chemistry::Ammonia)) },
        _ => { (3, Some(Chemistry::Methane)) }
    }
}

fn terrestrial_chem_dm(lum: LuminosityClass, orbit: OrbitType) -> i8 {
    let star = match lum {
        LuminosityClass::KV => 2,
        LuminosityClass::MV => 4,
        LuminosityClass::L  => 5,
        _ => 0,
    };
    let outer = if orbit == OrbitType::OuterZone { 2 } else { 0 };
    star + outer
}

fn terrestrial_chemistry(rng: &mut ChaCha8Rng, roll: i8, category: &Category) -> (u8, Option<Chemistry>) {
    match category {
        Category::Vesperian => {
            match roll {
                ..=11 => (0, Some(Chemistry::Water)),
                _ => (0, Some(Chemistry::Chlorine))
            }
        },
        Category::Tectonic => {
            match roll {
                ..=6 => {
                    let roll = roll_xdy(rng, 2, 6);
                    match roll {
                        ..=8 => (0, Some(Chemistry::Water)),
                        9..=11 => (0, Some(Chemistry::Sulfur)),
                        _ => (0, Some(Chemistry::Chlorine))
                    }
                },
                7..=8 => (1, Some(Chemistry::Ammonia)),
                _ => (3, Some(Chemistry::Methane))
            }
        },
        Category::Arid | Category::Oceanic => {
            match roll {
                ..=6 => (0, Some(Chemistry::Water)),
                7..=8 => (1, Some(Chemistry::Ammonia)),
                _ => (3, Some(Chemistry::Methane))
            }
        },
        _ => (0, None)
    }
}

fn helian_chem_dm(lum: LuminosityClass) -> i8 {
    match lum {
        LuminosityClass::KV => 2,
        LuminosityClass::MV => 4,
        LuminosityClass::L  => 5,
        _ => 0,
    }
}

fn jovian_chem_dm(lum: LuminosityClass, orbit: OrbitType) -> i8 {
    let l = if lum == LuminosityClass::L { 1 } else { 0 };
    let zone = match orbit {
        OrbitType::Epistellar => -2,
        OrbitType::OuterZone  => 2,
        OrbitType::InnerZone  => 0,
    };
    l + zone
}

fn dwarf_atmosphere(category: &Category, roll: i8) -> u8 {
    match category {
        Category::Arean => {
            match roll {
                ..=3 => { 1 },
                _ => { 10 }
            }
        }
        Category::Hebean => {
            match roll {
                ..=0 => { 0 },
                1 => { 1 },
                _ => { 10 }
            }
        }
        Category::Snowball => {
            match roll {
                ..=4 => { 0 },
                _ => { 1 }
            }
        },
        _ => unreachable!("dwarf_atmosphere called for {category:?}")
    }
}

fn helian_hydrosphere (rng: &mut ChaCha8Rng, category: &Category, roll: i8) -> u8 {
    match category {
        Category::Helian => {
            match roll {
                ..=2 => 0,
                3..=4 => roll_xdy(rng, 2, 6) - 1,
                _ => 15
            }
        },
        _ => unreachable!("helian_hydrosphere called for {category:?}")
    }
}

fn create_dwarf_planet(rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, luminosity_class: &LuminosityClass, system_age: &u8, parent_group: Option<Group>) -> Planet {
    // Size
    let size = planet_size(rng, &Group::Dwarf);

    // Category
    let category = match orbit_type {
        OrbitType::Epistellar => {
            let cat_roll = max(0, roll_xdy(rng, 1, 6) as i8
                - if parent_group == Some(Group::AsteroidBelt) { 2 } else { 0 });
            match cat_roll {
                ..=3 => { Category::Rockball },
                4..=5 => { Category::Meltball },
                _ => { 
                    let roll2 = roll_xdy(rng, 1, 6);
                    match roll2 {
                        ..=4 => { Category::Hebean },
                        _ => { Category::Promethean }
                    }
                }
            }
        },
        OrbitType::InnerZone => {
            let cat_roll = max(0, roll_xdy(rng, 1, 6) as i8
                - if parent_group == Some(Group::AsteroidBelt) { 2 } else { 0 }
                + if parent_group == Some(Group::Helian) { 1 } else { 0 }
                + if parent_group == Some(Group::Jovian) { 2 } else { 0 });
            match cat_roll {
                ..=4 => { Category::Rockball },
                5..=6 => { Category::Arean },
                7 => { Category::Meltball },
                _ => { 
                    let roll2 = roll_xdy(rng, 1, 6);
                    match roll2 {
                        ..=4 => { Category::Hebean },
                        _ => { Category::Promethean }
                    }
                }
            }
        },
        OrbitType::OuterZone => {
            let cat_roll = max(0, roll_xdy(rng, 1, 6) as i8
                - if parent_group == Some(Group::AsteroidBelt) { 1 } else { 0 }
                + if parent_group == Some(Group::Helian) { 1 } else { 0 }
                + if parent_group == Some(Group::Jovian) { 2 } else { 0 });
            match cat_roll {
                0 => { Category::Rockball },
                1..=4 => { Category::Snowball },
                5..=6 => { Category::Rockball },
                7 => { Category::Meltball },
                _ => { 
                    let roll2 = roll_xdy(rng, 1, 6);
                    match roll2 {
                        ..=3 => { Category::Hebean },
                        4..=5 => { Category::Arean },
                        _ => { Category::Promethean }
                    }
                }
            }
        }
    };
        
    let (age_mod, chemistry) = match category {
        Category::Arean | Category::Promethean | Category::Snowball => {
            let chem_roll: i8 = roll_xdy(rng, 1, 6) as i8 + dwarf_chem_dm(*luminosity_class, orbit_type, category);
            dwarf_chemistry(chem_roll)
        },
        _ => { (0, None) } // Other dwarf planet Categories: Hebean, Meltball, Rockball, Stygian
    };

    let (atmosphere, hydrosphere, biosphere) = match category {
        Category::Arean => {
            let atmo_roll: i8 = roll_xdy(rng, 1, 6) as i8 - if *luminosity_class == LuminosityClass::D { 2 } else { 0 };
            let atmosphere: u8 = dwarf_atmosphere(&category, atmo_roll);
            let hydro_roll: i8 = roll_xdy(rng, 2, 3) as i8 + size as i8 - 7 - if atmosphere == 1 { 4 } else { 0 };
            let hydrosphere: u8 = max(0, hydro_roll) as u8;
            let age_compare: u8 = roll_xdy(rng, 1, 3);
            let biosphere: u8 = if atmosphere == 1 && *system_age >= age_compare + age_mod {
                    max(0, roll_xdy(rng, 1, 6) as i8 - 4) as u8
                } else if atmosphere == 10 && *system_age >= 4 + age_mod {
                    max(0, roll_xdy(rng, 1, 6) as i8 + size as i8 - 2) as u8
                } else if atmosphere == 10 && *system_age >= age_compare + age_mod {
                    roll_xdy(rng, 1, 3)
                } else { 0 };
            (atmosphere, hydrosphere, biosphere)
        }
        Category::Hebean => {
            let atmo_roll: i8 = roll_xdy(rng, 1, 6) as i8 + size as i8 - 6;
            let atmosphere: u8 = dwarf_atmosphere(&category, atmo_roll);
            let hydro_roll: i8 = roll_xdy(rng, 2, 6) as i8 + size as i8 - 11;
            let hydrosphere: u8 = max(0, hydro_roll) as u8;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Meltball => {
            let atmosphere: u8 = 1;
            let hydrosphere: u8 = 15;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Promethean => {
            let hydro_roll: i8 = roll_xdy(rng, 2, 6) as i8 - 2;
            let hydrosphere: u8 = max(0, hydro_roll) as u8;
            let age_compare: u8 = roll_xdy(rng, 1, 3);
            let biosphere_roll: i8 = roll_xdy(rng, 1, 6) as i8;
            let biosphere: u8 = if *system_age >= 4 + age_mod {
                    max(0, biosphere_roll + size as i8 - if *luminosity_class == LuminosityClass::D { 3 } else { 0 }) as u8
                } else if *system_age >= age_compare + age_mod {
                    roll_xdy(rng, 1, 3)
                } else { 0 };
            let atmosphere: u8 = if biosphere >= 3 && chemistry == Some(Chemistry::Water) {
                (roll_xdy(rng, 2, 6) as i8 + size as i8 - 7).clamp(2, 9) as u8
            } else { 0 };
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Rockball => {
            let atmosphere: u8 = 0;
            let hydrosphere: u8 = 0;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Snowball => {
            let atmosphere: u8 = dwarf_atmosphere(&category, roll_xdy(rng, 1, 6) as i8);
            let hydro_roll: i8 = roll_xdy(rng, 1, 6) as i8;
            let hydrosphere: u8 = match hydro_roll {
                ..=3 => 10,
                _ => roll_xdy(rng, 2, 6) - 2
            };
            let age_compare: u8 = roll_xdy(rng, 1, 6);
            let biosphere: u8 = if *system_age >= 6 + age_mod {
                    max(0, roll_xdy(rng, 1, 6) as i8 + size as i8 - 2) as u8
                } else if *system_age >= age_compare {
                    max(0, roll_xdy(rng, 1, 6) as i8 -3) as u8
                } else { 0 };
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Stygian => {
            let atmosphere: u8 = 0;
            let hydrosphere: u8 = 0;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere)
        },
        _ => unreachable!("create_dwarf_planet called for {category:?}")
    };

    Planet {
        order: order,
        category: category,
        size: size,
        chemistry: chemistry,
        atmosphere: atmosphere,
        hydrosphere: hydrosphere,
        biosphere: biosphere,
        rings: None,
        proper_name: None
    }
}

fn create_terrestrial_planet(rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, luminosity_class: &LuminosityClass, system_age: &u8, parent_group: Option<Group>) -> Planet {
    // Size
    let size = planet_size(rng, &Group::Terrestrial);

    // Category
    let category = match orbit_type {
        OrbitType::Epistellar => {
            let cat_roll = roll_xdy(rng, 1, 6);
            match cat_roll {
                ..=3 => { Category::JaniLithic },
                4..=5 => { Category::Vesperian },
                _ => { Category::Telluric }
            }
        },
        OrbitType::InnerZone => {
            let cat_roll = roll_xdy(rng, 2, 6);
            match cat_roll {
                ..=4 => { Category::Telluric },
                5..=6 => { Category::Arid },
                7 => { Category::Tectonic },
                8..=9 => { Category::Oceanic },
                10 => { Category::Tectonic },
                _ => { Category::Telluric }
            }
        },
        OrbitType::OuterZone => {
            let cat_roll = roll_xdy(rng, 1, 6)
                + if parent_group.is_some() { 2 } else { 0 };
            match cat_roll {
                ..=4 => { Category::Arid },
                5..=6 => { Category::Tectonic },
                _ => { Category::Oceanic }
            }
        }
    };
        
    let (age_mod, chemistry) = match category {
        Category::Arid | Category::Oceanic | Category::Tectonic => {
            let chem_roll = roll_xdy(rng, 1, 6) as i8 + terrestrial_chem_dm(*luminosity_class, orbit_type);
            terrestrial_chemistry(rng, chem_roll, &category)
        },
        Category::Vesperian => {
            let roll = roll_xdy(rng, 2, 6) as i8;
            terrestrial_chemistry(rng, roll, &category)
        },
        _ => { (0, None) } // Other terrestrial Categories: Acheronian, JaniLithic, Telluric
    };

    let (atmosphere, hydrosphere, biosphere) = match category {
        Category::Acheronian => {
            let atmosphere = 1;
            let hydrosphere = 0;
            let biosphere = 0;
            (atmosphere, hydrosphere, biosphere)
        }
        Category::Arid => {
            let age_compare = roll_xdy(rng, 1, 3);
            let biosphere: u8 = if *system_age >= 4 + age_mod {
                max(0, roll_xdy(rng, 2, 6) as i8 - if *luminosity_class == LuminosityClass::D { 3 } else { 0 }) as u8
            } else if *system_age >= age_compare + age_mod {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            let hydrosphere = roll_xdy(rng, 1, 3);
            let atmosphere = if biosphere >= 3 && chemistry == Some(Chemistry::Water) {
                (roll_xdy(rng, 2, 6) as i8 - 7 + size as i8).clamp(2, 9) as u8
            } else { 10 };
            (atmosphere, hydrosphere, biosphere)
        },
        Category::JaniLithic => {
            let atmo_roll = roll_xdy(rng, 1, 6) as i8;
            let atmosphere: u8 = match atmo_roll {
                    ..=3 => { 1 },
                    _ => { 10 }
                };
            let hydrosphere: u8 = 0;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Oceanic => {
            let hydrosphere: u8 = 11;
            let age_compare = roll_xdy(rng, 1, 3);
            let biosphere: u8 = if *system_age >= 4 + age_mod {
                max(0, roll_xdy(rng, 2, 6) as i8 - if *luminosity_class == LuminosityClass::D { 3 } else { 0 }) as u8
            } else if *system_age >= age_compare + age_mod {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            let atmosphere = if chemistry == Some(Chemistry::Water) {
                let atmo_roll = roll_xdy(rng, 2, 6) as i8
                    - 6
                    + size as i8
                    - match *luminosity_class {
                        LuminosityClass::L => { 3 },
                        LuminosityClass::MV => { 2 },
                        LuminosityClass::KV => { 1 },
                        LuminosityClass::FIV => { 1 },
                        LuminosityClass::GIV => { 1 },
                        LuminosityClass::KIV => { 1 },
                        _ => { 0 }
                    };
                atmo_roll.clamp(1, 12) as u8
            } else {
                let atmo_roll = roll_xdy(rng, 1, 6);
                match atmo_roll {
                    ..=1 => 1,
                    2..4 => 10,
                    _ => 12
                }
            };
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Tectonic => {
            let age_compare = roll_xdy(rng, 1, 3);
            let biosphere: u8 = if *system_age >= 4 + age_mod {
                max(0, roll_xdy(rng, 2, 6) as i8 - if *luminosity_class == LuminosityClass::D { 3 } else { 0 }) as u8
            } else if *system_age >= age_compare + age_mod {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            let hydrosphere = roll_xdy(rng, 2, 6) - 2;
            let atmosphere = if biosphere >= 3 && chemistry == Some(Chemistry::Water) {
                (roll_xdy(rng, 2, 6) as i8 - 7 + size as i8).clamp(2, 9) as u8
            } else if biosphere >= 3 && (chemistry == Some(Chemistry::Sulfur) || chemistry == Some(Chemistry::Chlorine)) {
                11
            } else { 10 };
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Telluric => {
            let atmosphere: u8 = 12;
            let hydrosphere: u8 = if roll_xdy(rng, 1, 6) <= 4 { 0 } else { 15 };
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Vesperian => {
            let age_compare = roll_xdy(rng, 1, 3);
            let biosphere: u8 = if *system_age >= 4 {
                roll_xdy(rng, 2, 6)
            } else if *system_age >= age_compare {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            let hydrosphere = roll_xdy(rng, 2, 6) - 2;
            let atmosphere = if biosphere >= 3 && chemistry == Some(Chemistry::Water) {
                (roll_xdy(rng, 2, 6) as i8 - 7 + size as i8).clamp(2, 9) as u8
            } else if biosphere >= 3 && chemistry == Some(Chemistry::Chlorine) {
                11
            } else { 10 };
            (atmosphere, hydrosphere, biosphere)
        }
        _ => unreachable!("create_terrestrial_planet called for {category:?}")
    };

    Planet {
        order: order,
        category: category,
        size: size,
        chemistry: chemistry,
        atmosphere: atmosphere,
        hydrosphere: hydrosphere,
        biosphere: biosphere,
        rings: None,
        proper_name: None
    }
}

fn create_helian_planet(rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, luminosity_class: &LuminosityClass, system_age: &u8) -> Planet {
    // Size
    let size = planet_size(rng, &Group::Helian);

    // Category
    let category = match orbit_type {
        OrbitType::Epistellar => {
            let cat_roll = roll_xdy(rng, 1, 6);
            match cat_roll {
                ..=5 => { Category::Helian },
                _ => { Category::Asphodelian }
            }
        },
        OrbitType::InnerZone => {
            let cat_roll = roll_xdy(rng, 1, 6);
            match cat_roll {
                ..=4 => { Category::Helian },
                _ => { Category::Panthalassic }
            }
        },
        OrbitType::OuterZone => { Category::Helian }
    };

    let (age_mod, chemistry) = match category {
        Category::Panthalassic => {
            let chem_roll = roll_xdy(rng, 1, 6) as i8 + helian_chem_dm(*luminosity_class);
            match chem_roll {
                ..=6 => {
                    let roll = roll_xdy(rng, 2, 6);
                    match roll {
                        ..=8 => (0, Some(Chemistry::Water)),
                        9..=11 => (0, Some(Chemistry::Sulfur)),
                        _ => (0, Some(Chemistry::Chlorine))
                    }
                },
                7..=8 => { (1, Some(Chemistry::Methane)) },
                _ => { (3, Some(Chemistry::Methane)) }
            }
        },
        _ => (0, None)
    };

    let (atmosphere, hydrosphere, biosphere) = match category {
        Category::Asphodelian => {
            let atmosphere = 1;
            let hydrosphere = 0;
            let biosphere = 0;
            (atmosphere, hydrosphere, biosphere)
        }
        Category::Helian => {
            let biosphere: u8 = 0;
            let hydro_roll = roll_xdy(rng, 1, 6) as i8;
            let hydrosphere = helian_hydrosphere(rng, &category, hydro_roll);
            let atmosphere = 13;
            (atmosphere, hydrosphere, biosphere)
        },
        Category::Panthalassic => {
            let atmosphere = min(13, roll_xdy(rng, 1, 6) + 8);
            let hydrosphere: u8 = 11;
            let age_compare = roll_xdy(rng, 1, 3);
            let biosphere: u8 = if *system_age >= 4 + age_mod {
                roll_xdy(rng, 2, 6)
            } else if *system_age >= age_compare + age_mod {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            (atmosphere, hydrosphere, biosphere)
        }
        _ => unreachable!("create_helian_planet called for {category:?}")
    };

    Planet {
        order: order,
        category: category,
        size: size,
        chemistry: chemistry,
        atmosphere: atmosphere,
        hydrosphere: hydrosphere,
        biosphere: biosphere,
        rings: None,
        proper_name: None
    }
}

fn create_jovian_planet(rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, luminosity_class: &LuminosityClass, system_age: &u8) -> Planet {
    // Size
    let size = planet_size(rng, &Group::Jovian);

    // Category
    let category = match orbit_type {
        OrbitType::Epistellar => {
            let cat_roll = roll_xdy(rng, 1, 6);
            match cat_roll {
                ..=5 => { Category::Jovian },
                _ => { Category::Chthonian }
            }
        },
        _ => { Category::Jovian }
    };
    
    let atmosphere: u8 = match category { Category::Chthonian => 1, _ => 16 };
    let hydrosphere: u8 = match category { Category::Chthonian => 0, _ => 16 };

    let biosphere: u8 = match category {
        Category::Chthonian => 0,
        _ => {
            let bio_roll = roll_xdy(rng, 1, 6) + if orbit_type == OrbitType::InnerZone { 2 } else { 0 };
            match bio_roll {
                ..=5 => 0,
                _ => {
                    let age_compare = roll_xdy(rng, 1, 6);
                    if *system_age >= 7 {
                        let roll = roll_xdy(rng, 2, 6) as i8 - if *luminosity_class == LuminosityClass::D { 3 } else { 0 };
                        max(0, roll) as u8
                    } else if *system_age >= age_compare { roll_xdy(rng, 1, 3) }
                    else { 0 }
                }
            }
        }
    };

    // Chemistry
    let chemistry = match category {
        Category::Chthonian => { None },
        _ => {
            if biosphere > 0 {
                let chem_roll = roll_xdy(rng, 1, 6) as i8 + jovian_chem_dm(*luminosity_class, orbit_type);
                match chem_roll {
                    ..=3 => Some(Chemistry::Water),
                    _ => Some(Chemistry::Ammonia)
                }
            } else { None }
        }
    };

    let rings = match category {
        Category::Chthonian => { None },
        _ => {
            Some(match roll_xdy(rng, 1, 6) {
                ..=4 => RingsType::Minor,
                _ => RingsType::Complex
            })
        }
    };

    Planet {
        order: order,
        category: category,
        size: size,
        chemistry: chemistry,
        atmosphere: atmosphere,
        hydrosphere: hydrosphere,
        biosphere: biosphere,
        rings: rings,
        proper_name: None
    }
}

#[cfg(test)]
mod chem_dm_tests {
    use super::*;

    #[test]
    fn terrestrial_dms_are_positive_and_stack() {
        assert_eq!(terrestrial_chem_dm(LuminosityClass::L,  OrbitType::InnerZone), 5); // L adds — catches bug #3
        assert_eq!(terrestrial_chem_dm(LuminosityClass::KV, OrbitType::InnerZone), 2);
        assert_eq!(terrestrial_chem_dm(LuminosityClass::MV, OrbitType::OuterZone), 6); // 4 + 2 stack
        assert_eq!(terrestrial_chem_dm(LuminosityClass::GV, OrbitType::InnerZone), 0);
    }

    #[test]
    fn helian_dms_are_positive() {
        assert_eq!(helian_chem_dm(LuminosityClass::L),  5);
        assert_eq!(helian_chem_dm(LuminosityClass::KV), 2);
        assert_eq!(helian_chem_dm(LuminosityClass::MV), 4);
        assert_eq!(helian_chem_dm(LuminosityClass::GV), 0);
    }

    #[test]
    fn jovian_zone_signs_are_opposite() {
        assert_eq!(jovian_chem_dm(LuminosityClass::GV, OrbitType::Epistellar), -2); // epistellar subtracts
        assert_eq!(jovian_chem_dm(LuminosityClass::GV, OrbitType::OuterZone),   2); // outer adds
        assert_eq!(jovian_chem_dm(LuminosityClass::L,  OrbitType::Epistellar), -1); // L+1 nets against -2
        assert_eq!(jovian_chem_dm(LuminosityClass::L,  OrbitType::OuterZone),   3); // L+1 plus +2
    }

    #[test]
    fn dwarf_epistellar_penalty_is_promethean_only() {
        assert_eq!(dwarf_chem_dm(LuminosityClass::GV, OrbitType::Epistellar, Category::Promethean), -2);
        assert_eq!(dwarf_chem_dm(LuminosityClass::GV, OrbitType::Epistellar, Category::Arean),       0);
        assert_eq!(dwarf_chem_dm(LuminosityClass::GV, OrbitType::Epistellar, Category::Snowball),    0);
        assert_eq!(dwarf_chem_dm(LuminosityClass::L,  OrbitType::OuterZone,  Category::Arean),       4); // L +2, outer +2
    }
}
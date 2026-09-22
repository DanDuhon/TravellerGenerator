use std::cmp::max;
use std::cmp::min;
use rand_chacha::ChaCha8Rng;
use crate::star::LuminosityClass;
use crate::temperature::Solvent;
use crate::dice_roller::roll_xdy;
use crate::temperature;
use crate::terrain::Terrain;
use crate::terrain::terrain_present;

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

pub fn solvent(chemistry: Option<Chemistry>) -> Solvent {
    match chemistry {
        Some(Chemistry::Ammonia) => Solvent::Ammonia,
        Some(Chemistry::Chlorine) => Solvent::Chlorine,
        Some(Chemistry::Methane) => Solvent::Methane,
        Some(Chemistry::Sulfur) => Solvent::SulfuricAcid,
        _ => Solvent::Water
    }
}

#[derive(Debug, Clone, Copy)]
pub struct OrbitalData<'a> {
    pub name: &'a str,
    pub luminosity_class: LuminosityClass,
    pub system_age: u8,
    pub expansion_affected_orbits: u8
}

#[derive(Debug, Clone, Copy)]
pub enum Placement {
    Stellar,
    Satellite { parent_scorched: bool },
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
    pub subsurface_oceans: bool,
    pub biosphere: u8,
    pub rings: Option<RingsType>,
    pub proper_name: Option<String>,
    pub base_temperature: i16
}

impl Planet {
    pub fn temperature(&self) -> temperature::Temperature {
        temperature::current(self.base_temperature, self.category, self.atmosphere, self.hydrosphere, solvent(self.chemistry))
    }
    pub fn flare_shielded(&self) -> bool {
        is_flare_shielded(self.hydrosphere, self.subsurface_oceans)
    }
    pub fn terrains(&self) -> Vec<Terrain> {
        let s = solvent(self.chemistry);
        terrain_present(self)
    }
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

pub fn has_solid_surface(category: Category) -> bool {
    match category {
        Category::Helian | Category::Jovian | Category::Panthalassic => false,
        _ => true
    }
}

fn after_flares(biosphere: u8, luminosity_class: LuminosityClass, shielded: bool) -> u8 {
    if luminosity_class == LuminosityClass::MVe && !shielded {
        biosphere.saturating_sub(2)
    } else {
        biosphere
    }
}

fn is_flare_shielded(hydrosphere: u8, subsurface_oceans: bool) -> bool {
    subsurface_oceans || hydrosphere == 11
}

pub fn create_orbital_body(
    rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, designation: String,
    group: Group, parent_group: Option<Group>, is_binary_companion: bool,
    orbital_data: OrbitalData, placement: Placement
) -> OrbitalBody {
    let scorched = match placement {
        Placement::Stellar => order <= orbital_data.expansion_affected_orbits,
        Placement::Satellite { parent_scorched } => parent_scorched,
    };
    let (num_of_sats, body) = match group {
        Group::AsteroidBelt => {
            (if roll_xdy(rng, 1, 6) >= 5 { 1 } else { 0 } as usize,
            Body::AsteroidBelt)
        },
        Group::Dwarf => {
            let planet = if scorched {
                Planet {
                    order: order,
                    category: Category::Stygian,
                    size: planet_size(rng, &Group::Dwarf),
                    chemistry: None,
                    atmosphere: 0,
                    hydrosphere: 0,
                    subsurface_oceans: false,
                    biosphere: 0,
                    rings: None,
                    proper_name: None,
                    base_temperature: temperature::base(orbit_type, Category::Stygian, 0, solvent(None))
                }
            } else {
                create_dwarf_planet(rng, order, orbit_type, orbital_data.luminosity_class, orbital_data.system_age, parent_group)
            };
            if is_binary_companion == false {
                (if roll_xdy(rng, 1, 6) == 6 { 1 } else { 0 } as usize,
                Body::Planet(planet))
            } else { // Don't let a dwarf binary companion keep generating companions
                (0 as usize,
                Body::Planet(planet))
            }
        },
        Group::Terrestrial => {
            let planet = if scorched {
                Planet {
                    order: order,
                    category: Category::Acheronian,
                    size: planet_size(rng, &Group::Terrestrial),
                    chemistry: None,
                    atmosphere: 1,
                    hydrosphere: 0,
                    subsurface_oceans: false,
                    biosphere: 0,
                    rings: None,
                    proper_name: None,
                    base_temperature: temperature::base(orbit_type, Category::Acheronian, 1, solvent(None))
                }
            } else {
                create_terrestrial_planet(rng, order, orbit_type, orbital_data.luminosity_class, orbital_data.system_age, parent_group)
            };
            (if roll_xdy(rng, 1, 6) >= 5 { 1 } else { 0 } as usize,
            Body::Planet(planet))
        }
        Group::Helian => {
            let planet = if scorched {
                Planet {
                    order: order,
                    category: Category::Asphodelian,
                    size: planet_size(rng, &Group::Helian),
                    chemistry: None,
                    atmosphere: 1,
                    hydrosphere: 0,
                    subsurface_oceans: false,
                    biosphere: 0,
                    rings: None,
                    proper_name: None,
                    base_temperature: temperature::base(orbit_type, Category::Asphodelian, 1, solvent(None))
                }
            } else {
                create_helian_planet(rng, order, orbit_type, orbital_data.luminosity_class, orbital_data.system_age)
            };
            (max(0, roll_xdy(rng, 1, 6) as i8 - 3) as usize,
            Body::Planet(planet))
        }
        Group::Jovian => {
            let planet = if scorched {
                Planet {
                    order: order,
                    category: Category::Chthonian,
                    size: planet_size(rng, &Group::Jovian),
                    chemistry: None,
                    atmosphere: 1,
                    hydrosphere: 0,
                    subsurface_oceans: false,
                    biosphere: 0,
                    rings: None,
                    proper_name: None,
                    base_temperature: temperature::base(orbit_type, Category::Chthonian, 1, solvent(None))
                }
            } else {
                create_jovian_planet(rng, order, orbit_type, orbital_data.luminosity_class, orbital_data.system_age)
            };
            (roll_xdy(rng, 1, 6) as usize,
            Body::Planet(planet))
        }
    };

    let satellites = if num_of_sats > 0 {
        generate_satellites(rng, &body, orbit_type, &designation, parent_group, num_of_sats, orbital_data, scorched)
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
    parent_designation: &str, group: Group, parent_group: Option<Group>,
    is_companion: bool, orbital_data: OrbitalData, parent_scorched: bool
) {
    let index = (sats.len() + 1) as u8;
    let desig = format!("{parent_designation}-{index}");
    sats.push(create_orbital_body(rng, index, orbit_type, desig, group, parent_group, is_companion, orbital_data, Placement::Satellite { parent_scorched }));
}

fn generate_satellites(
    rng: &mut ChaCha8Rng, body: &Body, orbit_type: OrbitType,
    parent_designation: &str, own_parent_group: Option<Group>,
    num_of_sats: usize, orbital_data: OrbitalData, scorched: bool
) -> Vec<OrbitalBody> {
    let mut sats = Vec::with_capacity(num_of_sats);

    match body {
        Body::AsteroidBelt => {
            push_satellite(
                rng, &mut sats, orbit_type, parent_designation, Group::Dwarf, Some(Group::AsteroidBelt), false, orbital_data, scorched
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
                    Group::Dwarf,
                    own_parent_group,
                    true, // This ensures a companion dwarf can't create more companions
                    orbital_data,
                    Placement::Satellite { parent_scorched: scorched }
                ));
            },
            Group::Terrestrial => {
                push_satellite(
                rng, &mut sats, orbit_type, parent_designation, Group::Dwarf, Some(Group::Terrestrial),
                false, orbital_data, scorched
                );
            },
            Group::Helian => {
                for i in 0..num_of_sats {
                    if i == 0 && roll_xdy(rng, 1, 6) == 6 {
                        push_satellite(
                            rng, &mut sats, orbit_type, parent_designation, Group::Terrestrial, Some(Group::Helian),
                            false, orbital_data, scorched
                        );
                    } else {
                        push_satellite(
                            rng, &mut sats, orbit_type, parent_designation, Group::Dwarf, Some(Group::Helian),
                            false, orbital_data, scorched
                        );
                    }
                }
            },
            Group::Jovian => {
                for i in 0..num_of_sats {
                    if i == 0 && roll_xdy(rng, 1, 6) == 6 {
                        if roll_xdy(rng, 1, 6) == 6 {
                            push_satellite(
                                rng, &mut sats, orbit_type, parent_designation, Group::Helian, Some(Group::Jovian),
                                false, orbital_data, scorched
                            );
                        } else {
                            push_satellite(
                                rng, &mut sats, orbit_type, parent_designation, Group::Terrestrial, Some(Group::Jovian),
                                false, orbital_data, scorched
                            );
                        }
                    } else {
                        push_satellite(
                            rng, &mut sats, orbit_type, parent_designation, Group::Dwarf, Some(Group::Jovian),
                            false, orbital_data, scorched
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
        LuminosityClass::MVe => 4,
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
        LuminosityClass::MVe => 4,
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

fn create_dwarf_planet(rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, luminosity_class: LuminosityClass, system_age: u8, parent_group: Option<Group>) -> Planet {
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
            let chem_roll: i8 = roll_xdy(rng, 1, 6) as i8 + dwarf_chem_dm(luminosity_class, orbit_type, category);
            dwarf_chemistry(chem_roll)
        },
        _ => { (0, None) } // Other dwarf planet Categories: Hebean, Meltball, Rockball, Stygian
    };

    let (atmosphere, hydrosphere, biosphere, subsurface_oceans) = match category {
        Category::Arean => {
            let atmo_roll: i8 = roll_xdy(rng, 1, 6) as i8 - if luminosity_class == LuminosityClass::D { 2 } else { 0 };
            let atmosphere: u8 = dwarf_atmosphere(&category, atmo_roll);
            let hydro_roll: i8 = roll_xdy(rng, 2, 3) as i8 + size as i8 - 7 - if atmosphere == 1 { 4 } else { 0 };
            let hydrosphere: u8 = max(0, hydro_roll) as u8;
            let subsurface_oceans = false;
            let age_compare: u8 = roll_xdy(rng, 1, 3);
            let biosphere: u8 = if atmosphere == 1 && system_age >= age_compare + age_mod {
                    max(0, roll_xdy(rng, 1, 6) as i8 - 4) as u8
                } else if atmosphere == 10 && system_age >= 4 + age_mod {
                    max(0, roll_xdy(rng, 1, 6) as i8 + size as i8 - 2) as u8
                } else if atmosphere == 10 && system_age >= age_compare + age_mod {
                    roll_xdy(rng, 1, 3)
                } else { 0 };
            let biosphere = after_flares(biosphere, luminosity_class, is_flare_shielded(hydrosphere, subsurface_oceans));
            (atmosphere, hydrosphere, biosphere, false)
        }
        Category::Hebean => {
            let atmo_roll: i8 = roll_xdy(rng, 1, 6) as i8 + size as i8 - 6;
            let atmosphere: u8 = dwarf_atmosphere(&category, atmo_roll);
            let hydro_roll: i8 = roll_xdy(rng, 2, 6) as i8 + size as i8 - 11;
            let hydrosphere: u8 = max(0, hydro_roll) as u8;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere, false)
        },
        Category::Meltball => {
            let atmosphere: u8 = 1;
            let hydrosphere: u8 = 15;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere, false)
        },
        Category::Promethean => {
            let hydro_roll: i8 = roll_xdy(rng, 2, 6) as i8 - 2;
            let hydrosphere: u8 = max(0, hydro_roll) as u8;
            let subsurface_oceans = false;
            let age_compare: u8 = roll_xdy(rng, 1, 3);
            let biosphere_roll: i8 = roll_xdy(rng, 1, 6) as i8;
            let biosphere: u8 = if system_age >= 4 + age_mod {
                    max(0, biosphere_roll + size as i8 - if luminosity_class == LuminosityClass::D { 3 } else { 0 }) as u8
                } else if system_age >= age_compare + age_mod {
                    roll_xdy(rng, 1, 3)
                } else { 0 };
            let biosphere = after_flares(biosphere, luminosity_class, is_flare_shielded(hydrosphere, subsurface_oceans));
            let atmosphere: u8 = if biosphere >= 3 && chemistry == Some(Chemistry::Water) {
                (roll_xdy(rng, 2, 6) as i8 + size as i8 - 7).clamp(2, 9) as u8
            } else { 0 };
            (atmosphere, hydrosphere, biosphere, false)
        },
        Category::Rockball => {
            let atmosphere: u8 = 0;
            let hydrosphere: u8 = 0;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere, false)
        },
        Category::Snowball => {
            let atmosphere: u8 = dwarf_atmosphere(&category, roll_xdy(rng, 1, 6) as i8);
            let hydro_roll: i8 = roll_xdy(rng, 1, 6) as i8;
            let (hydrosphere, subsurface_oceans) = match hydro_roll {
                ..=3 => (10, false),
                _ => (roll_xdy(rng, 2, 6) - 2, true)
            };
            let age_compare: u8 = roll_xdy(rng, 1, 6);
            let biosphere: u8 = if system_age >= 6 + age_mod && subsurface_oceans {
                    max(0, roll_xdy(rng, 1, 6) as i8 + size as i8 - 2) as u8
                } else if system_age >= age_compare && subsurface_oceans {
                    max(0, roll_xdy(rng, 1, 6) as i8 -3) as u8
                } else { 0 };
            let biosphere = after_flares(biosphere, luminosity_class, is_flare_shielded(hydrosphere, subsurface_oceans));
            (atmosphere, hydrosphere, biosphere, subsurface_oceans)
        },
        Category::Stygian => {
            let atmosphere: u8 = 0;
            let hydrosphere: u8 = 0;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere, false)
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
        subsurface_oceans: subsurface_oceans,
        biosphere: biosphere,
        rings: None,
        proper_name: None,
        base_temperature: temperature::base(orbit_type, category, atmosphere, solvent(chemistry))
    }
}

fn create_terrestrial_planet(rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, luminosity_class: LuminosityClass, system_age: u8, parent_group: Option<Group>) -> Planet {
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
            let chem_roll = roll_xdy(rng, 1, 6) as i8 + terrestrial_chem_dm(luminosity_class, orbit_type);
            terrestrial_chemistry(rng, chem_roll, &category)
        },
        Category::Vesperian => {
            let roll = roll_xdy(rng, 2, 6) as i8;
            terrestrial_chemistry(rng, roll, &category)
        },
        _ => { (0, None) } // Other terrestrial Categories: Acheronian, JaniLithic, Telluric
    };

    let (atmosphere, hydrosphere, biosphere, subsurface_oceans) = match category {
        Category::Acheronian => {
            let atmosphere = 1;
            let hydrosphere = 0;
            let biosphere = 0;
            (atmosphere, hydrosphere, biosphere, false)
        }
        Category::Arid => {
            let age_compare = roll_xdy(rng, 1, 3);
            let hydrosphere = roll_xdy(rng, 1, 3);
            let subsurface_oceans = false;
            let biosphere: u8 = if system_age >= 4 + age_mod {
                max(0, roll_xdy(rng, 2, 6) as i8 - if luminosity_class == LuminosityClass::D { 3 } else { 0 }) as u8
            } else if system_age >= age_compare + age_mod {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            let biosphere = after_flares(biosphere, luminosity_class, is_flare_shielded(hydrosphere, subsurface_oceans));
            let atmosphere = if biosphere >= 3 && chemistry == Some(Chemistry::Water) {
                (roll_xdy(rng, 2, 6) as i8 - 7 + size as i8).clamp(2, 9) as u8
            } else { 10 };
            (atmosphere, hydrosphere, biosphere, false)
        },
        Category::JaniLithic => {
            let atmo_roll = roll_xdy(rng, 1, 6) as i8;
            let atmosphere: u8 = match atmo_roll {
                    ..=3 => { 1 },
                    _ => { 10 }
                };
            let hydrosphere: u8 = 0;
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere, false)
        },
        Category::Oceanic => {
            let hydrosphere: u8 = 11;
            let age_compare = roll_xdy(rng, 1, 3);
            let atmosphere = if chemistry == Some(Chemistry::Water) {
                let atmo_roll = roll_xdy(rng, 2, 6) as i8
                    - 6
                    + size as i8
                    - match luminosity_class {
                        LuminosityClass::L => { 3 },
                        LuminosityClass::MV => { 2 },
                        LuminosityClass::MVe => { 2 },
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
            let subsurface_oceans = atmosphere < 2;
            let biosphere: u8 = if system_age >= 4 + age_mod {
                max(0, roll_xdy(rng, 2, 6) as i8 - if luminosity_class == LuminosityClass::D { 3 } else { 0 }) as u8
            } else if system_age >= age_compare + age_mod {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            let biosphere = after_flares(biosphere, luminosity_class, is_flare_shielded(hydrosphere, subsurface_oceans));
            (atmosphere, hydrosphere, biosphere, subsurface_oceans)
        },
        Category::Tectonic => {
            let age_compare = roll_xdy(rng, 1, 3);
            let hydrosphere = roll_xdy(rng, 2, 6) - 2;
            let subsurface_oceans = false;
            let biosphere: u8 = if system_age >= 4 + age_mod {
                max(0, roll_xdy(rng, 2, 6) as i8 - if luminosity_class == LuminosityClass::D { 3 } else { 0 }) as u8
            } else if system_age >= age_compare + age_mod {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            let biosphere = after_flares(biosphere, luminosity_class, is_flare_shielded(hydrosphere, subsurface_oceans));
            let atmosphere = if biosphere >= 3 && chemistry == Some(Chemistry::Water) {
                (roll_xdy(rng, 2, 6) as i8 - 7 + size as i8).clamp(2, 9) as u8
            } else if biosphere >= 3 && (chemistry == Some(Chemistry::Sulfur) || chemistry == Some(Chemistry::Chlorine)) {
                11
            } else { 10 };
            (atmosphere, hydrosphere, biosphere, false)
        },
        Category::Telluric => {
            let atmosphere: u8 = 12;
            let hydrosphere: u8 = if roll_xdy(rng, 1, 6) <= 4 { 0 } else { 15 };
            let biosphere: u8 = 0;
            (atmosphere, hydrosphere, biosphere, false)
        },
        Category::Vesperian => {
            let age_compare = roll_xdy(rng, 1, 3);
            let biosphere: u8 = if system_age >= 4 {
                roll_xdy(rng, 2, 6)
            } else if system_age >= age_compare {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            let hydrosphere = roll_xdy(rng, 2, 6) - 2;
            let subsurface_oceans = false;
            let biosphere = after_flares(biosphere, luminosity_class, is_flare_shielded(hydrosphere, subsurface_oceans));
            let atmosphere = if biosphere >= 3 && chemistry == Some(Chemistry::Water) {
                (roll_xdy(rng, 2, 6) as i8 - 7 + size as i8).clamp(2, 9) as u8
            } else if biosphere >= 3 && chemistry == Some(Chemistry::Chlorine) {
                11
            } else { 10 };
            (atmosphere, hydrosphere, biosphere, false)
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
        subsurface_oceans: subsurface_oceans,
        biosphere: biosphere,
        rings: None,
        proper_name: None,
        base_temperature: temperature::base(orbit_type, category, atmosphere, solvent(chemistry))
    }
}

fn create_helian_planet(rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, luminosity_class: LuminosityClass, system_age: u8) -> Planet {
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
            let chem_roll = roll_xdy(rng, 1, 6) as i8 + helian_chem_dm(luminosity_class);
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
            let subsurface_oceans = false;
            let age_compare = roll_xdy(rng, 1, 3);
            let biosphere: u8 = if system_age >= 4 + age_mod {
                roll_xdy(rng, 2, 6)
            } else if system_age >= age_compare + age_mod {
                roll_xdy(rng, 1, 3)
            } else { 0 };
            let biosphere = after_flares(biosphere, luminosity_class, is_flare_shielded(hydrosphere, subsurface_oceans));
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
        subsurface_oceans: false,
        biosphere: biosphere,
        rings: None,
        proper_name: None,
        base_temperature: temperature::base(orbit_type, category, atmosphere, solvent(chemistry))
    }
}

fn create_jovian_planet(rng: &mut ChaCha8Rng, order: u8, orbit_type: OrbitType, luminosity_class: LuminosityClass, system_age: u8) -> Planet {
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
                    if system_age >= 7 {
                        let roll = roll_xdy(rng, 2, 6) as i8 - if luminosity_class == LuminosityClass::D { 3 } else { 0 };
                        max(0, roll) as u8
                    } else if system_age >= age_compare { roll_xdy(rng, 1, 3) }
                    else { 0 }
                }
            }
        }
    };
    let subsurface_oceans = false;
    let biosphere = after_flares(biosphere, luminosity_class, is_flare_shielded(hydrosphere, subsurface_oceans));

    // Chemistry
    let chemistry = match category {
        Category::Chthonian => { None },
        _ => {
            if biosphere > 0 {
                let chem_roll = roll_xdy(rng, 1, 6) as i8 + jovian_chem_dm(luminosity_class, orbit_type);
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
        subsurface_oceans: false,
        biosphere: biosphere,
        rings: rings,
        proper_name: None,
        base_temperature: temperature::base(orbit_type, category, atmosphere, solvent(chemistry))
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
        assert_eq!(terrestrial_chem_dm(LuminosityClass::MVe, OrbitType::OuterZone), 6); // 4 + 2 stack
        assert_eq!(terrestrial_chem_dm(LuminosityClass::GV, OrbitType::InnerZone), 0);
    }

    #[test]
    fn helian_dms_are_positive() {
        assert_eq!(helian_chem_dm(LuminosityClass::L),  5);
        assert_eq!(helian_chem_dm(LuminosityClass::KV), 2);
        assert_eq!(helian_chem_dm(LuminosityClass::MV), 4);
        assert_eq!(helian_chem_dm(LuminosityClass::MVe), 4);
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

#[cfg(test)]
mod flare_tests {
    use super::*;
 
    #[test]
    fn flares_cost_unshielded_worlds_two_points() {
        assert_eq!(after_flares(10, LuminosityClass::MVe, false), 8);
        assert_eq!(after_flares(3, LuminosityClass::MVe, false), 1);
        // Floors at zero rather than wrapping.
        assert_eq!(after_flares(2, LuminosityClass::MVe, false), 0);
        assert_eq!(after_flares(1, LuminosityClass::MVe, false), 0);
        assert_eq!(after_flares(0, LuminosityClass::MVe, false), 0);
    }
 
    #[test]
    fn shielded_worlds_and_quiet_stars_are_untouched() {
        assert_eq!(after_flares(10, LuminosityClass::MVe, true), 10);
        for lum in [LuminosityClass::MV, LuminosityClass::GV, LuminosityClass::KV,
                    LuminosityClass::D, LuminosityClass::L] {
            assert_eq!(after_flares(10, lum, false), 10, "{lum:?} should not flare");
        }
    }
 
    #[test]
    fn shielding_comes_from_deep_oceans_or_ice() {
        assert!(is_flare_shielded(11, false), "a superdense ocean shields");
        assert!(is_flare_shielded(0, true), "an ice shell shields");
        assert!(is_flare_shielded(5, true), "an ice shell shields at any hydrosphere");
        // 15 and 16 aren't oceans; 10 is a normal ocean, not a superdense one.
        for hydrosphere in [0, 5, 10, 15, 16] {
            assert!(!is_flare_shielded(hydrosphere, false),
                "hydrosphere {hydrosphere} with no ice shell should not shield");
        }
    }
}
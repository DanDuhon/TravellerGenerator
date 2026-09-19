use crate::dice_roller::roll_xdy;
use rand_chacha::ChaCha8Rng;
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StarRole {
    Primary,
    Companion(CompanionOrbit),
    BrownDwarf, // automatic, non-companion brown dwarf
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SpectralType {
    A,
    F,
    G,
    K,
    M,
    L
}

impl fmt::Display for SpectralType {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
       match self {
           SpectralType::A => write!(f, "A"),
           SpectralType::F => write!(f, "F"),
           SpectralType::G => write!(f, "G"),
           SpectralType::K => write!(f, "K"),
           SpectralType::M => write!(f, "M"),
           SpectralType::L => write!(f, "L"),
       }
    }
}

fn spectral_type_lookup(roll: u8) -> SpectralType {
    match roll {
        2 => SpectralType::A,
        3 => SpectralType::F,
        4 => SpectralType::G,
        5 => SpectralType::K,
        6..=13 => SpectralType::M,
        _ => SpectralType::L
    }
}

fn luminosity_class_lookup(rng: &mut ChaCha8Rng, role: StarRole, spectral_type: SpectralType, age: &u8) -> LuminosityClass {
    if spectral_type == SpectralType::A {
        if *age <= 2 {
            return LuminosityClass::AV
        }
        else if *age == 3 {
            let roll = roll_xdy(rng, 1, 6);
            return match roll {
                ..=2 => LuminosityClass::FIV,
                3 => LuminosityClass::KIII,
                _ => LuminosityClass::D
            }
        }
        else {
            return LuminosityClass::D
        }
    }
    else if spectral_type == SpectralType::F {
        if *age <= 5 {
            return LuminosityClass::FV
        }
        else if *age == 6 {
            let roll = roll_xdy(rng, 1, 6);
            return match roll {
                ..=4 => LuminosityClass::GIV,
                _ => LuminosityClass::MIII
            }
        }
        else {
            return LuminosityClass::D
        }
    }
    else if spectral_type == SpectralType::G {
        if *age <= 11 {
            return LuminosityClass::GV
        }
        else if *age <= 13 {
            let roll = roll_xdy(rng, 1, 6);
            return match roll {
                ..=3 => LuminosityClass::KIV,
                _ => LuminosityClass::MIII
            }
        }
        else {
            return LuminosityClass::D
        }
    }
    else if spectral_type == SpectralType::K {
        return LuminosityClass::KV
    }
    else if spectral_type == SpectralType::M {
        let roll = roll_xdy(rng, 2, 6) + if matches!(role, StarRole::Companion(_)) { 2 } else { 0 };
        return match roll {
            ..=9 => LuminosityClass::MV,
            10..=12 => LuminosityClass::MVe,
            _ => LuminosityClass::L
        }
    }
    else {
        return LuminosityClass::L
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LuminosityClass {
    AV,
    D,
    FIV,
    FV,
    GIV,
    GV,
    KIII,
    KIV,
    KV,
    L,
    MIII,
    MV,
    MVe,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CompanionOrbit {
    Tight,
    Close,
    Moderate,
    Distant
}

pub struct Star {
    pub role: StarRole,
    pub spectral_type: SpectralType,
    pub luminosity_class: LuminosityClass,
    pub name: String
}

pub fn create_star(rng: &mut ChaCha8Rng, role: &StarRole, age: &u8, roll: &u8, name: String) -> Star {
    let spectral_type = spectral_type_lookup(*roll);
    let luminosity_class = luminosity_class_lookup(rng, *role, spectral_type, age);
    let s = Star {
        role: *role,
        spectral_type: spectral_type,
        luminosity_class: luminosity_class,
        name: name
    };

    return s
}

pub fn create_brown_dwarf(name: String) -> Star {
    let s = Star {
        role: StarRole::BrownDwarf,
        spectral_type: SpectralType::L,
        luminosity_class: LuminosityClass::L,
        name: name
    };

    return s
}
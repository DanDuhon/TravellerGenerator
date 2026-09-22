use crate::orbital_body::OrbitType;
use crate::orbital_body::Category;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Temperature { pub mean: i16, pub spread: i16, pub solvent: Solvent }

impl Temperature {
    pub fn min(&self) -> i16 { self.mean - self.spread }
    pub fn max(&self) -> i16 { self.mean + self.spread }
    pub fn spans(&self, band: ClimateBand) -> bool {
        let (lo, hi) = band.range(self.solvent);
        lo.is_none_or(|lo| self.max() >= lo) && hi.is_none_or(|hi| self.min() < hi)
    }
    pub fn reaches_liquid(&self) -> bool {
        let (freeze, boil) = liquid_range(self.solvent);
        self.max() >= freeze && self.min() <= boil
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ClimateBand {
    Frozen,
    Cold,
    Temperate,
    Hot,
    Scorching
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Solvent {
    Water,
    SulfuricAcid,
    Chlorine,
    Ammonia,
    Methane
}

impl ClimateBand {
    pub fn range(self, solvent: Solvent) -> (Option<i16>, Option<i16>) {
        match solvent {
            Solvent::Water => match self {
                ClimateBand::Frozen => (None, Some(-15)),
                ClimateBand::Cold => (Some(-15), Some(5)),
                ClimateBand::Temperate => (Some(5), Some(25)),
                ClimateBand::Hot => (Some(25), Some(60)),
                ClimateBand::Scorching => (Some(60), None),
            },
            Solvent::SulfuricAcid => match self {
                ClimateBand::Frozen => (None, Some(-5)),
                ClimateBand::Cold => (Some(-5), Some(15)),
                ClimateBand::Temperate => (Some(15), Some(35)),
                ClimateBand::Hot => (Some(35), Some(70)),
                ClimateBand::Scorching => (Some(70), None),
            },
            Solvent::Chlorine => match self {
                ClimateBand::Frozen => (None, Some(-116)),
                ClimateBand::Cold => (Some(-116), Some(-96)),
                ClimateBand::Temperate => (Some(-96), Some(-76)),
                ClimateBand::Hot => (Some(-76), Some(-41)),
                ClimateBand::Scorching => (Some(-41), None),
            },
            Solvent::Ammonia => match self {
                ClimateBand::Frozen => (None, Some(-90)),
                ClimateBand::Cold => (Some(-90), Some(-72)),
                ClimateBand::Temperate => (Some(-72), Some(-58)),
                ClimateBand::Hot => (Some(-58), Some(-40)),
                ClimateBand::Scorching => (Some(-40), None),
            },
            Solvent::Methane => match self {
                ClimateBand::Frozen => (None, Some(-190)),
                ClimateBand::Cold => (Some(-190), Some(-180)),
                ClimateBand::Temperate => (Some(-180), Some(-172)),
                ClimateBand::Hot => (Some(-172), Some(-164)),
                ClimateBand::Scorching => (Some(-164), None),
            },
        }
        
    }
}

pub fn liquid_range(solvent: Solvent) -> (i16, i16) {
    match solvent {
            Solvent::Water => (0, 100),
            Solvent::SulfuricAcid => (10, 337),
            Solvent::Chlorine => (-101, -34),
            Solvent::Ammonia => (-78, -33),
            Solvent::Methane => (-182, -161),
    }
}

pub fn wet_bounds(solvent: Solvent) -> (i16, i16) {
    match solvent {
            Solvent::Water => (0, 40),
            Solvent::SulfuricAcid => (10, 50),
            Solvent::Chlorine => (-101, -61),
            Solvent::Ammonia => (-75, -50),
            Solvent::Methane => (-180, -168),
    }
}

pub fn zone(orbit_type: OrbitType) -> i16 {
    match orbit_type {
        OrbitType::Epistellar => 300,
        OrbitType::InnerZone => -15,
        OrbitType::OuterZone => -150
    }
}

pub fn greenhouse(atmosphere: u8) -> i16 {
    match atmosphere {
        ..=1 => 0,
        2..=3 => 5,
        4..=5 => 15,
        6..=7 => 30,
        8..=9 => 50,
        10 => 30,
        11 => 80,
        12 => 450,
        13 => 60,
        16 => 0,
        _ => unreachable!("greenhouse called for {atmosphere:?}")
    }
}

pub fn atmospheric_spread(atmosphere: u8) -> i16 {
    match atmosphere {
        ..=1 => 150,
        2..=3 => 90,
        4..=5 => 70,
        6..=7 => 55,
        8..=9 => 45,
        10 => 50,
        11 => 40,
        12 => 10,
        13 => 40,
        16 => 15,
        _ => unreachable!("atmospheric_spread called for {atmosphere:?}")
    }
}

pub fn min_max(category: Category, atmosphere: u8, solvent: Solvent) -> (Option<i16>, Option<i16>) {
    let freeze = liquid_range(solvent).0;
    match category {
        Category::Snowball => (None, Some(freeze - 20)),
        Category::Arean => (Some(freeze - 10), Some(freeze + 20)),
        Category::Hebean if atmosphere >= 2 => (Some(-20), Some(80)),
        Category::Hebean => (Some(-20), None),
        Category::Oceanic if atmosphere < 2 => (None, Some(freeze - 10)),
        Category::Arid | Category::Tectonic | Category::Promethean | Category::Panthalassic | Category::Oceanic => {
            let bounds = wet_bounds(solvent);
            (Some(bounds.0), Some(bounds.1))
        },
        Category::Vesperian => (Some(freeze - 10), Some(freeze + 30)),
        Category::Meltball => (Some(800), None),
        Category::Telluric => (Some(300), None),
        _ => (None, None),
    }
}

pub fn base(orbit_type: OrbitType, category: Category, atmosphere: u8, solvent: Solvent) -> i16 {
    let raw = zone(orbit_type);
    let g = greenhouse(atmosphere);
    let (lo, hi) = min_max(category, atmosphere, solvent);
    let mut mean = raw + g;
    if let Some(lo) = lo { mean = mean.max(lo); }
    if let Some(hi) = hi { mean = mean.min(hi); }
    mean - g
}

pub fn current(base: i16, category: Category, atmosphere: u8, hydrosphere: u8, solvent: Solvent) -> Temperature {
    let mean = base + greenhouse(atmosphere);

    // 1. Damp: oceans even out the climate.
    let damping = if hydrosphere <= 11 { 2 * hydrosphere as i16 } else { 0 };
    let damped = (atmospheric_spread(atmosphere) - damping).max(5);

    // 2. Scale by absolute temperature, anchored so Earth would be unchanged.
    let kelvin = (mean as i32 + 273).max(10);
    let scaled = (damped as i32 * kelvin / 288).max(1) as i16;

    // 3. Tide-locking doubles it.
    let tide_locked = matches!(category, Category::JaniLithic | Category::Vesperian);
    let spread = if tide_locked { scaled * 2 } else { scaled };

    Temperature { mean, spread, solvent }
}
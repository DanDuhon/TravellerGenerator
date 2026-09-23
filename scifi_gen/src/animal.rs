use crate::terrain::Terrain;

mod amphibian;
mod aquatic;
mod avian;
mod fungal;
mod insect;
mod mammal;
mod reptile;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum AnimalClass {
    Amphibian,
    Aquatic,
    Avian,
    Fungal,
    Insect,
    Mammal,
    Reptile
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Diet {
    Carnivore,
    Herbivore,
    Omnivore
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Behavior {
    CarrionEater,
    Chaser,
    Eater,
    Filter,
    Gatherer,
    Grazer,
    Hijacker,
    Hunter,
    Intermittent,
    Intimidator,
    Killer,
    Pouncer,
    Reducer,
    Siren,
    Trapper
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Movement {
    Burrow,
    Fly,
    Swim,
    Walk
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Skill {
    Athletics,
    Deception,
    MeleeNaturalWeapons,
    Persuade,
    Recon,
    Stealth,
    Survival
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Weapon {
    Standard(WeaponStandard),
    Exotic(WeaponExotic)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum WeaponStandard {
    Antlers,
    Beak,
    BodySlam,
    Claws,
    Constriction,
    DartingTongue,
    Fins,
    Headbutt,
    Hooves,
    Horns,
    Mandibles,
    SharpScales,
    Stinger,
    Stomp,
    Suckers,
    Talons,
    Teeth,
    Thrasher,
    Trample,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum WeaponExotic {
    Bioelectric,
    Bleed,
    ConcealingMist,
    Diseased,
    Poison,
    Ranged
}

pub struct Animal {
    pub class: AnimalClass,
    pub diet: Diet,
    pub strength_mod: u8,
    pub dexterity_mod: u8,
    pub endurance_mod: u8,
    pub instinct_mod: u8,
    pub intelligence_mod: u8,
    pub number_encountered_dice: u8,
    pub size: u8,
    pub armor: u8,
    // pub quirks: Vec<Quirk>,
    pub behaviors: [Option<Behavior>; 2],
    pub reaction_modifier: i8,
    pub weapons: Vec<Option<Weapon>>,
    pub damage_dice: u8,
    pub damage_mod: i8,
    pub initiative: i8,
    pub movement: [Option<Movement>; 2],
}

pub struct Builder {
    pub class: AnimalClass,
    pub diet: Diet,
    pub strength: u8,
    pub dexterity: u8,
    pub endurance: u8,
    pub instinct: u8,
    pub pack: u8,
    pub intelligence: u8,
    pub strength_mod: u8,
    pub dexterity_mod: u8,
    pub endurance_mod: u8,
    pub instinct_mod: u8,
    pub intelligence_mod: u8,
    pub number_encountered_dice: u8,
    pub size: u8,
    pub armor: u8,
    // pub quirks: Vec<Quirk>,
    pub behaviors: [Option<Behavior>; 2],
    pub reaction_modifier: i8,
    pub weapons: Vec<Option<Weapon>>,
    pub damage_dice: u8,
    pub damage_mod: i8,
    pub initiative: i8,
    pub movement: [Option<Movement>; 2],
    pub size_roll: u8,
    pub size_roll_mod: i8,
    pub exotic_weapon_rolls: u8,
    pub evolution_physical_rolls: u8,
    pub evolution_social_rolls: u8,
    pub quirk_rolls: u8,
    pub weight: u16,
    pub movement_primary_mod: i8,
    pub movement_secondary_mod: i8,
}

pub fn terrain_mods(terrain: Terrain, roll: u8) -> (i8, Movement, i8) {
    match terrain {
        Terrain::BeachShore => {
            let size_mod = 2;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Swim,  1) },
                2 => { (Movement::Swim,  1) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  0) },
                5 => { (Movement::Fly,  -4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Clear => {
            let size_mod = 0;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk,  0) },
                2 => { (Movement::Walk,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  0) },
                5 => { (Movement::Walk,  2) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::DeepOcean => {
            let size_mod = 2;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Swim,  8) },
                2 => { (Movement::Swim,  6) },
                3 => { (Movement::Swim,  4) },
                4 => { (Movement::Swim,  2) },
                5 => { (Movement::Swim,  0) },
                6 => { (Movement::Swim, -2) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Desert => {
            let size_mod = -3;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk,  0) },
                2 => { (Movement::Walk,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  0) },
                5 => { (Movement::Fly, -4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Forest => {
            let size_mod = -4;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk,  0) },
                2 => { (Movement::Walk,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  0) },
                5 => { (Movement::Fly,  -4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Hills => {
            let size_mod = 0;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk,  0) },
                2 => { (Movement::Walk,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  2) },
                5 => { (Movement::Fly,  -4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::IceSheet => {
            let size_mod = 2;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Swim,  4) },
                2 => { (Movement::Swim,  2) },
                3 => { (Movement::Walk,  2) },
                4 => { (Movement::Walk,  0) },
                5 => { (Movement::Walk, -4) },
                6 => { (Movement::Fly,  -4) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Jungle => {
            let size_mod = -3;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk,  0) },
                2 => { (Movement::Walk,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  0) },
                5 => { (Movement::Walk,  2) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Mountains => {
            let size_mod = 0;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk,  0) },
                2 => { (Movement::Walk,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Fly,  -2) },
                5 => { (Movement::Fly,  -4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::OpenOcean => {
            let size_mod = -4;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Swim,  6) },
                2 => { (Movement::Swim,  4) },
                3 => { (Movement::Swim,  2) },
                4 => { (Movement::Swim,  0) },
                5 => { (Movement::Fly,  -4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Plains => {
            let size_mod = 0;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk,  0) },
                2 => { (Movement::Walk,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  2) },
                5 => { (Movement::Walk,  4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Rainforest => {
            let size_mod = -2;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk,  0) },
                2 => { (Movement::Walk,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  2) },
                5 => { (Movement::Walk,  4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Riverbank => {
            let size_mod = 1;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Swim,  -4) },
                2 => { (Movement::Swim,   2) },
                3 => { (Movement::Walk,   0) },
                4 => { (Movement::Walk,   0) },
                5 => { (Movement::Walk,   0) },
                6 => { (Movement::Fly,   -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::RoughBroken => {
            let size_mod = -3;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk,  0) },
                2 => { (Movement::Walk,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  2) },
                5 => { (Movement::Fly,  -4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::ShallowOcean => {
            let size_mod = 1;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Swim,   4) },
                2 => { (Movement::Swim,   2) },
                3 => { (Movement::Swim,   0) },
                4 => { (Movement::Swim,   0) },
                5 => { (Movement::Fly,   -4) },
                6 => { (Movement::Fly,   -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::SwampMarsh => {
            let size_mod = 4;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Swim, -6) },
                2 => { (Movement::Swim,  0) },
                3 => { (Movement::Walk,  0) },
                4 => { (Movement::Walk,  0) },
                5 => { (Movement::Fly,  -4) },
                6 => { (Movement::Fly,  -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Tundra => {
            let size_mod = 1;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk, 0) },
                2 => { (Movement::Walk, 0) },
                3 => { (Movement::Walk, 0) },
                4 => { (Movement::Walk, 0) },
                5 => { (Movement::Walk, 2) },
                6 => { (Movement::Fly, -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
        Terrain::Woods => {
            let size_mod = -1;
            let (movement, move_mod) = match roll {
                1 => { (Movement::Walk, 0) },
                2 => { (Movement::Walk, 0) },
                3 => { (Movement::Walk, 0) },
                4 => { (Movement::Walk, 0) },
                5 => { (Movement::Walk, 0) },
                6 => { (Movement::Fly, -6) },
                _ => unreachable!("terrain_mods {terrain:?} called for {roll:?}")
            };
            (size_mod, movement, move_mod)
        },
    }
}
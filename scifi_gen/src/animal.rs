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

pub struct Animal {
    pub class: AnimalClass,
    pub diet: Diet,
    pub strength: u8,
    pub dexterity: u8,
    pub endurance: u8,
    pub instinct: u8,
    pub pack: u8,
    pub intelligence: u8,
    pub size: u8,
    pub armor: u8,
    // pub quirks: Vec<Quirk>,
    pub behaviors: Vec<Behavior>,
    pub reaction_modifier: i8,
    // pub weapons: Vec<Weapon>,
    pub weapon_dice: u8,
    pub weapon_damage_mod: i8,
    pub initiative: i8,
    pub movement_primary: Movement,
    pub movement_secondary: Movement,
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
    pub size: u8,
    pub armor: u8,
    // pub quirks: Vec<Quirk>,
    pub behaviors: Vec<Behavior>,
    pub reaction_modifier: i8,
    // pub weapons: Vec<Weapon>,
    pub weapon_dice: u8,
    pub weapon_damage_mod: i8,
    pub initiative: i8,
    pub movement_primary: Movement,
    pub movement_secondary: Movement,
    pub size_roll: u8,
    pub size_roll_mod: i8
}
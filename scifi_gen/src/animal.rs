use std::cmp::max;
use crate::dice_roller::roll_xdy;
use crate::terrain::Terrain;
use rand_chacha::ChaCha8Rng;
use std::collections::BTreeSet;
pub(crate) use amphibian::Quirk as AmphibianQuirk;

mod amphibian;
mod aquatic;
mod avian;
mod fungal;
mod insect;
mod mammal;
mod reptile;

/// Classes with a `ClassRules` impl. Add each class here as `rules()` stops
/// being `todo!()` for it, and every test that iterates it starts covering it.
#[cfg(test)]
pub(crate) const IMPLEMENTED: [AnimalClass; 1] = [AnimalClass::Amphibian];

pub(crate) trait ClassRules {
    fn diet(&self, roll: u8) -> Diet;
    fn starting_stats_skills(&self, b: &mut Builder);
    fn evolutionary_additional_skills(&self, rng: &mut ChaCha8Rng, b: &mut Builder);
    fn evolutionary_other_benefits(&self, rng: &mut ChaCha8Rng, b: &mut Builder);
    fn evolution_skill(&self, rng: &mut ChaCha8Rng, b: &mut Builder);
    fn social_skill(&self, rng: &mut ChaCha8Rng, b: &mut Builder);
    fn physical_skill(&self, rng: &mut ChaCha8Rng, b: &mut Builder);
    fn quirk_for(&self, roll: u8) -> Quirk;
    fn behavior(&self, rng: &mut ChaCha8Rng, b: &mut Builder) -> (Behavior, i8) ;
    fn also_viable_terrain_mods(&self, b: &mut Builder, roll: u8);
    /// Exotic weapons only this class can roll, after the shared six.
    fn extra_exotics(&self) -> &'static [WeaponExotic] { &[] }
    /// Size DM and movement from the terrain chart.
    fn size_and_movement(&self, rng: &mut ChaCha8Rng, b: &mut Builder) { terrain_size_movement(rng, b); }
}

fn rules(class: AnimalClass) -> &'static dyn ClassRules {
    match class {
        AnimalClass::Amphibian => &amphibian::Rules,
        _ => todo!()
        // AnimalClass::Aquatic   => &aquatic::Rules,
        // AnimalClass::Avian     => &avian::Rules,
        // AnimalClass::Fungal    => &fungal::Rules,
        // AnimalClass::Insect    => &insect::Rules,
        // AnimalClass::Mammal    => &mammal::Rules,
        // AnimalClass::Reptile   => &reptile::Rules,
    }
}

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
    Immobile,
    Swim,
    Walk
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Skill {
    Athletics,
    Deception,
    Melee,
    Persuade,
    Recon,
    Stealth,
    Survival
}

impl Skill {
    pub const COUNT: usize = 7;
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Default)]
pub struct SkillLevel(Option<i8>);

impl SkillLevel {
    pub const UNTRAINED_DM: i8 = -3;

    /// Untrained becomes level 0; trained goes up by one.
    pub fn raise(&mut self) {
        self.0 = Some(self.0.map_or(0, |level| level + 1));
    }

    /// Trained skills decrease by one, stopping at the untrained modifier.
    pub fn lower(&mut self) {
        if let Some(level) = self.0.as_mut() {
            *level = (*level - 1).max(Self::UNTRAINED_DM);
        }
    }

    pub fn train_at(&mut self, level: i8) { self.0 = Some(level); }
    pub fn is_trained(&self) -> bool { self.0.is_some() }

    /// The modifier this skill contributes to a check.
    pub fn dm(&self) -> i8 { self.0.unwrap_or(Self::UNTRAINED_DM) }
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
    Ranged,
    Stench
}

impl WeaponExotic {
    /// The shared exotic weapons, in 1d6 table order.
    pub(crate) const SHARED: [WeaponExotic; 6] = [
        WeaponExotic::Diseased, WeaponExotic::Poison, WeaponExotic::Bleed,
        WeaponExotic::Bioelectric, WeaponExotic::ConcealingMist, WeaponExotic::Ranged,
    ];
}


#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum AttackThreshold {
    Heavier,
    Outnumbers,
    Roll(u8),
    Surprise
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum FleeThreshold {
    Immobile,
    Roll(u8),
    Surprise
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Quirk {
    Amphibian(AmphibianQuirk),
}

impl Quirk {
    fn apply(self, b: &mut Builder) {
        match self {
            Quirk::Amphibian(q) => q.apply(b),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Animal {
    pub terrain: Terrain,
    pub class: AnimalClass,
    pub diet: Diet,
    pub strength: u8,
    pub dexterity: u8,
    pub endurance: u8,
    pub instinct: u8,
    pub intelligence: u8,
    pub pack: u8,
    pub weight_kg: u16,
    pub armor: u8,
    pub quirks: BTreeSet<Quirk>,
    pub behaviors: BTreeSet<Behavior>,
    pub reaction_modifier: i8,
    pub weapons: Vec<Weapon>,
    pub damage_dice: u8,
    pub initiative: i8,
    pub movement: Option<Movement>,
    pub skills: [SkillLevel; Skill::COUNT],
    pub attack_threshold: AttackThreshold,
    pub flee_threshold: FleeThreshold
}

pub struct Builder {
    pub terrain: Terrain,
    pub class: AnimalClass,
    pub diet: Diet,
    pub strength: i8,
    pub dexterity: i8,
    pub endurance: i8,
    pub instinct: i8,
    pub pack: i8,
    pub intelligence: i8,
    pub size: i8,
    pub armor: i8,
    pub quirks: BTreeSet<Quirk>,
    pub behaviors: BTreeSet<Behavior>,
    pub reaction_modifier: i8,
    pub weapons: Vec<Weapon>,
    pub damage_dice: u8,
    pub initiative: i8,
    pub movement: Option<Movement>,
    pub exotic_weapon_rolls: u8,
    pub evolution_additional_skill_rolls: u8,
    pub evolution_other_benefits_rolls: u8,
    pub evolution_mod: u8,
    pub physical_skill_rolls: u8,
    pub social_skill_rolls: u8,
    pub evolution_skill_rolls: u8,
    pub quirk_rolls: u8,
    pub weight_kg: u16,
    pub skills: [SkillLevel; Skill::COUNT],
    pub attack_threshold: AttackThreshold,
    pub flee_threshold: FleeThreshold,
    pub roll_mod: i8,
    pub size_halved: bool
}

impl Builder {
    pub fn skill(&mut self, skill: Skill) -> &mut SkillLevel {
        &mut self.skills[skill as usize]
    }
    pub fn add_weapon(&mut self, weapon: Weapon) {
        if !self.weapons.contains(&weapon) {
            self.weapons.push(weapon);
        }
    }
}

pub fn create_animal(rng: &mut ChaCha8Rng, class: AnimalClass, terrain: Terrain) -> Animal {
    debug_assert!(
        prefers(terrain).contains(&class) || also_viable(terrain).contains(&class),
        "{class:?} cannot live in {terrain:?}"
    );

    let class_rules = rules(class);

    let diet_roll = roll_xdy(rng, 1, 6);
    let diet = roll_diet(class_rules, diet_roll);
    
    let mut b = Builder {
        terrain: terrain,
        class: class,
        diet: diet,
        strength: 0,
        dexterity: 0,
        endurance: 0,
        instinct: 0,
        pack:0,
        intelligence: 0,
        size: 0,
        armor: 0,
        quirks: BTreeSet::new(),
        behaviors: BTreeSet::new(),
        reaction_modifier: 0,
        weapons: Vec::new(),
        damage_dice: 0,
        initiative: 0,
        movement: None,
        exotic_weapon_rolls: 0,
        evolution_additional_skill_rolls: 1,
        evolution_other_benefits_rolls: 1,
        evolution_mod: 0,
        physical_skill_rolls: 0,
        social_skill_rolls: 0,
        evolution_skill_rolls: 0,
        quirk_rolls: 0,
        weight_kg: 0,
        skills: [SkillLevel::default(); Skill::COUNT],
        attack_threshold: AttackThreshold::Roll(0),
        flee_threshold: FleeThreshold::Roll(0),
        roll_mod: 0,
        size_halved: false
    };

    apply_starting_stats_skills(class_rules, &mut b);

    b.initiative += match b.diet {
        Diet::Carnivore => 1,
        Diet::Herbivore => -1,
        Diet::Omnivore => 0
    };
    
    class_rules.size_and_movement(rng, &mut b);
    if b.movement == Some(Movement::Burrow) { b.instinct += 2; b.skill(Skill::Stealth).raise(); }
    let viable_roll = roll_xdy(rng, 1, 6);
    if also_viable(terrain).contains(&class) { apply_also_viable_terrain_mods(class_rules, &mut b, viable_roll) };
    b.instinct += roll_xdy(rng, 2, 6) as i8 + b.roll_mod;
    b.pack += roll_xdy(rng, 2, 6) as i8 + b.roll_mod;
    b.intelligence += if roll_xdy(rng, 1, 6) as i8 + b.roll_mod < 5 { 0 } else { 1 };
    armor(rng, &mut b);
    roll_evolutionary_other_benefits(rng, class_rules, &mut b);
    roll_evolutionary_additional_skills(rng, class_rules, &mut b); // These grant phy/soc/evo skill rolls
    roll_evolution_skills(rng, class_rules, &mut b); // These can grant phy/soc skill rolls
    roll_physical_skills(rng, class_rules, &mut b);
    roll_social_skills(rng, class_rules, &mut b);
    let (behavior, reaction_mod): (Behavior, i8) = roll_behavior(rng, class_rules, &mut b);
    let primary_behavior = behavior;
    b.behaviors.insert(behavior);
    b.reaction_modifier += reaction_mod;
    roll_quirks(rng, class_rules, &mut b); // Get quirks before behavior effects in case a quirk adds a behavior
    behavior_effects(rng, &mut b, primary_behavior);
    size_stats(rng, &mut b);

    roll_exotic_weapons(rng, class_rules, &mut b);

    let weapon_roll_mod = if b.weapons
        .iter()
        .any(|weapon| matches!(weapon, Weapon::Exotic(_))) { 0 }
        else {
            match b.diet {
                Diet::Carnivore => 8,
                Diet::Herbivore => -6,
                Diet::Omnivore => 4
            }
        };

    weapon_and_damage_modifier(rng, &mut b, weapon_roll_mod);

    Animal {
        terrain: terrain,
        class: class,
        diet: b.diet,
        strength: max(0, b.strength) as u8,
        dexterity: max(0, b.dexterity) as u8,
        endurance: max(0, b.endurance) as u8,
        instinct: max(0, b.instinct) as u8,
        pack: max(0, b.pack) as u8,
        intelligence: b.intelligence as u8,
        armor: max(0, b.armor) as u8,
        quirks: b.quirks,
        behaviors: b.behaviors,
        reaction_modifier: b.reaction_modifier,
        weapons: b.weapons,
        damage_dice: b.damage_dice,
        initiative: b.initiative,
        movement: b.movement,
        weight_kg: b.weight_kg,
        skills: b.skills,
        attack_threshold: b.attack_threshold,
        flee_threshold: b.flee_threshold
    }
}

pub fn characteristic_dm(score: u8) -> i8 {
    match score {
        0 => -3,
        1..=2 => -2,
        3..=5 => -1,
        6..=8 => 0,
        9..=11 => 1,
        12..=14 => 2,
        _ => 3,
    }
}

pub fn apply_starting_stats_skills(rules: &dyn ClassRules, b: &mut Builder) {
    rules.starting_stats_skills(b);
}

pub fn armor(rng: &mut ChaCha8Rng, b: &mut Builder) {
    let roll = roll_xdy(rng, 2, 6) as i8 + b.roll_mod;
    b.armor += match roll {
        ..=3 => 0,
        4..=5 => 1,
        6..=7 => 2,
        8..=9 => 3,
        10..=11 => 4,
        12..=13 => 5,
        14..=15 => 6,
        _ => 7,
    }
}

fn weapon_and_damage_modifier(rng: &mut ChaCha8Rng, b: &mut Builder, weapon_roll_mod: i8) {
    let roll = roll_xdy(rng, 2, 6) as i8 + b.roll_mod + weapon_roll_mod;
    let (weapons, damage_mod): (Vec<Weapon>, u8) = match roll {
        ..=1 => { (vec![], 0) },
        2 => {
            let w: Vec<Weapon> = match roll_xdy(rng, 1, 3) {
                1 => vec![Weapon::Standard(WeaponStandard::Teeth)],
                2 => vec![Weapon::Standard(WeaponStandard::Mandibles)],
                _ => vec![Weapon::Standard(WeaponStandard::Suckers)],
            };
            (w, 0)
        },
        3 => {
            let w = match roll_xdy(rng, 1, 4) {
                1 => vec![Weapon::Standard(WeaponStandard::Horns)],
                2 => vec![Weapon::Standard(WeaponStandard::Antlers)],
                3 => vec![Weapon::Standard(WeaponStandard::Beak)],
                _ => vec![Weapon::Standard(WeaponStandard::Headbutt)],
            };
            (w, 0)
        },
        4 => {
            let w = match roll_xdy(rng, 1, 6) {
                1 => vec![Weapon::Standard(WeaponStandard::Hooves)],
                2 => vec![Weapon::Standard(WeaponStandard::Stomp)],
                3 => vec![Weapon::Standard(WeaponStandard::BodySlam)],
                4 => vec![Weapon::Standard(WeaponStandard::Thrasher)],
                5 => vec![Weapon::Standard(WeaponStandard::Constriction)],
                _ => vec![Weapon::Standard(WeaponStandard::Trample)],
            };
            (w, 0)
        },
        5 => {
            let w = match roll_xdy(rng, 1, 18) {
                1 => vec![Weapon::Standard(WeaponStandard::Hooves), Weapon::Standard(WeaponStandard::Teeth)],
                2 => vec![Weapon::Standard(WeaponStandard::Hooves), Weapon::Standard(WeaponStandard::Mandibles)],
                3 => vec![Weapon::Standard(WeaponStandard::Hooves), Weapon::Standard(WeaponStandard::Suckers)],
                4 => vec![Weapon::Standard(WeaponStandard::Stomp), Weapon::Standard(WeaponStandard::Teeth)],
                5 => vec![Weapon::Standard(WeaponStandard::Stomp), Weapon::Standard(WeaponStandard::Mandibles)],
                6 => vec![Weapon::Standard(WeaponStandard::Stomp), Weapon::Standard(WeaponStandard::Suckers)],
                7 => vec![Weapon::Standard(WeaponStandard::BodySlam), Weapon::Standard(WeaponStandard::Teeth)],
                8 => vec![Weapon::Standard(WeaponStandard::BodySlam), Weapon::Standard(WeaponStandard::Mandibles)],
                9 => vec![Weapon::Standard(WeaponStandard::BodySlam), Weapon::Standard(WeaponStandard::Suckers)],
                10 => vec![Weapon::Standard(WeaponStandard::Thrasher), Weapon::Standard(WeaponStandard::Teeth)],
                11 => vec![Weapon::Standard(WeaponStandard::Thrasher), Weapon::Standard(WeaponStandard::Mandibles)],
                12 => vec![Weapon::Standard(WeaponStandard::Thrasher), Weapon::Standard(WeaponStandard::Suckers)],
                13 => vec![Weapon::Standard(WeaponStandard::Constriction), Weapon::Standard(WeaponStandard::Teeth)],
                14 => vec![Weapon::Standard(WeaponStandard::Constriction), Weapon::Standard(WeaponStandard::Mandibles)],
                15 => vec![Weapon::Standard(WeaponStandard::Constriction), Weapon::Standard(WeaponStandard::Suckers)],
                16 => vec![Weapon::Standard(WeaponStandard::Trample), Weapon::Standard(WeaponStandard::Teeth)],
                17 => vec![Weapon::Standard(WeaponStandard::Trample), Weapon::Standard(WeaponStandard::Mandibles)],
                _ => vec![Weapon::Standard(WeaponStandard::Trample), Weapon::Standard(WeaponStandard::Suckers)],
            };
            (w, 0)
        },
        6 => {
            let w = match roll_xdy(rng, 1, 3) {
                1 => vec![Weapon::Standard(WeaponStandard::Teeth)],
                2 => vec![Weapon::Standard(WeaponStandard::Mandibles)],
                _ => vec![Weapon::Standard(WeaponStandard::Suckers)],
            };
            (w, 0)
        },
        7 => {
            let w = match roll_xdy(rng, 1, 4) {
                1 => vec![Weapon::Standard(WeaponStandard::Claws)],
                2 => vec![Weapon::Standard(WeaponStandard::Fins)],
                3 => vec![Weapon::Standard(WeaponStandard::SharpScales)],
                _ => vec![Weapon::Standard(WeaponStandard::Talons)],
            };
            (w, 1)
        },
        8 => {
            let w = match roll_xdy(rng, 1, 2) {
                1 => vec![Weapon::Standard(WeaponStandard::Stinger)],
                _ => vec![Weapon::Standard(WeaponStandard::DartingTongue)],
            };
            (w, 1)
        },
        9 => {
            let w = match roll_xdy(rng, 1, 3) {
                1 => vec![Weapon::Standard(WeaponStandard::Thrasher)],
                2 => vec![Weapon::Standard(WeaponStandard::Constriction)],
                _ => vec![Weapon::Standard(WeaponStandard::Trample)],
            };
            (w, 1)
        },
        10 => {
            let w = match roll_xdy(rng, 1, 12) {
                1 => vec![Weapon::Standard(WeaponStandard::Claws), Weapon::Standard(WeaponStandard::Teeth)],
                2 => vec![Weapon::Standard(WeaponStandard::Claws), Weapon::Standard(WeaponStandard::Mandibles)],
                3 => vec![Weapon::Standard(WeaponStandard::Claws), Weapon::Standard(WeaponStandard::Suckers)],
                4 => vec![Weapon::Standard(WeaponStandard::Fins), Weapon::Standard(WeaponStandard::Teeth)],
                5 => vec![Weapon::Standard(WeaponStandard::Fins), Weapon::Standard(WeaponStandard::Mandibles)],
                6 => vec![Weapon::Standard(WeaponStandard::Fins), Weapon::Standard(WeaponStandard::Suckers)],
                7 => vec![Weapon::Standard(WeaponStandard::SharpScales), Weapon::Standard(WeaponStandard::Teeth)],
                8 => vec![Weapon::Standard(WeaponStandard::SharpScales), Weapon::Standard(WeaponStandard::Mandibles)],
                9 => vec![Weapon::Standard(WeaponStandard::SharpScales), Weapon::Standard(WeaponStandard::Suckers)],
                10 => vec![Weapon::Standard(WeaponStandard::Talons), Weapon::Standard(WeaponStandard::Teeth)],
                11 => vec![Weapon::Standard(WeaponStandard::Talons), Weapon::Standard(WeaponStandard::Mandibles)],
                _ => vec![Weapon::Standard(WeaponStandard::Talons), Weapon::Standard(WeaponStandard::Suckers)],
            };
            (w, 2)
        },
        11 => {
            let w = match roll_xdy(rng, 1, 4) {
                1 => vec![Weapon::Standard(WeaponStandard::Claws)],
                2 => vec![Weapon::Standard(WeaponStandard::Fins)],
                3 => vec![Weapon::Standard(WeaponStandard::SharpScales)],
                _ => vec![Weapon::Standard(WeaponStandard::Talons)],
            };
            (w, 2)
        },
        12 => {
            let w = match roll_xdy(rng, 1, 3) {
                1 => vec![Weapon::Standard(WeaponStandard::Teeth)],
                2 => vec![Weapon::Standard(WeaponStandard::Mandibles)],
                _ => vec![Weapon::Standard(WeaponStandard::Suckers)],
            };
            (w, 2)
        },
        13 => {
            let w = match roll_xdy(rng, 1, 3) {
                1 => vec![Weapon::Standard(WeaponStandard::Thrasher)],
                2 => vec![Weapon::Standard(WeaponStandard::Constriction)],
                _ => vec![Weapon::Standard(WeaponStandard::Trample)],
            };
            (w, 2)
        },
        14 => {
            let w = match roll_xdy(rng, 1, 12) {
                1 => vec![Weapon::Standard(WeaponStandard::Claws), Weapon::Standard(WeaponStandard::Teeth)],
                2 => vec![Weapon::Standard(WeaponStandard::Claws), Weapon::Standard(WeaponStandard::Mandibles)],
                3 => vec![Weapon::Standard(WeaponStandard::Claws), Weapon::Standard(WeaponStandard::Suckers)],
                4 => vec![Weapon::Standard(WeaponStandard::Fins), Weapon::Standard(WeaponStandard::Teeth)],
                5 => vec![Weapon::Standard(WeaponStandard::Fins), Weapon::Standard(WeaponStandard::Mandibles)],
                6 => vec![Weapon::Standard(WeaponStandard::Fins), Weapon::Standard(WeaponStandard::Suckers)],
                7 => vec![Weapon::Standard(WeaponStandard::SharpScales), Weapon::Standard(WeaponStandard::Teeth)],
                8 => vec![Weapon::Standard(WeaponStandard::SharpScales), Weapon::Standard(WeaponStandard::Mandibles)],
                9 => vec![Weapon::Standard(WeaponStandard::SharpScales), Weapon::Standard(WeaponStandard::Suckers)],
                10 => vec![Weapon::Standard(WeaponStandard::Talons), Weapon::Standard(WeaponStandard::Teeth)],
                11 => vec![Weapon::Standard(WeaponStandard::Talons), Weapon::Standard(WeaponStandard::Mandibles)],
                _ => vec![Weapon::Standard(WeaponStandard::Talons), Weapon::Standard(WeaponStandard::Suckers)],
            };
            (w, 2)
        },
        15 => {
            let w = match roll_xdy(rng, 1, 4) {
                1 => vec![Weapon::Standard(WeaponStandard::Claws)],
                2 => vec![Weapon::Standard(WeaponStandard::Fins)],
                3 => vec![Weapon::Standard(WeaponStandard::SharpScales)],
                _ => vec![Weapon::Standard(WeaponStandard::Talons)],
            };
            (w, 2)
        },
        16 => {
            let w = match roll_xdy(rng, 1, 2) {
                1 => vec![Weapon::Standard(WeaponStandard::Stinger)],
                _ => vec![Weapon::Standard(WeaponStandard::DartingTongue)],
            };
            (w, 2)
        },
        17 => {
            let w = match roll_xdy(rng, 1, 3) {
                1 => vec![Weapon::Standard(WeaponStandard::Thrasher)],
                2 => vec![Weapon::Standard(WeaponStandard::Constriction)],
                _ => vec![Weapon::Standard(WeaponStandard::Trample)],
            };
            (w, 2)
        },
        18 => {
            let w = match roll_xdy(rng, 1, 3) {
                1 => vec![Weapon::Standard(WeaponStandard::Teeth)],
                2 => vec![Weapon::Standard(WeaponStandard::Mandibles)],
                _ => vec![Weapon::Standard(WeaponStandard::Suckers)],
            };
            (w, 3)
        },
        19 => {
            let w = match roll_xdy(rng, 1, 12) {
                1 => vec![Weapon::Standard(WeaponStandard::Claws), Weapon::Standard(WeaponStandard::Teeth)],
                2 => vec![Weapon::Standard(WeaponStandard::Claws), Weapon::Standard(WeaponStandard::Mandibles)],
                3 => vec![Weapon::Standard(WeaponStandard::Claws), Weapon::Standard(WeaponStandard::Suckers)],
                4 => vec![Weapon::Standard(WeaponStandard::Fins), Weapon::Standard(WeaponStandard::Teeth)],
                5 => vec![Weapon::Standard(WeaponStandard::Fins), Weapon::Standard(WeaponStandard::Mandibles)],
                6 => vec![Weapon::Standard(WeaponStandard::Fins), Weapon::Standard(WeaponStandard::Suckers)],
                7 => vec![Weapon::Standard(WeaponStandard::SharpScales), Weapon::Standard(WeaponStandard::Teeth)],
                8 => vec![Weapon::Standard(WeaponStandard::SharpScales), Weapon::Standard(WeaponStandard::Mandibles)],
                9 => vec![Weapon::Standard(WeaponStandard::SharpScales), Weapon::Standard(WeaponStandard::Suckers)],
                10 => vec![Weapon::Standard(WeaponStandard::Talons), Weapon::Standard(WeaponStandard::Teeth)],
                11 => vec![Weapon::Standard(WeaponStandard::Talons), Weapon::Standard(WeaponStandard::Mandibles)],
                _ => vec![Weapon::Standard(WeaponStandard::Talons), Weapon::Standard(WeaponStandard::Suckers)],
            };
            (w, 3)
        },
        _ => {
            let w = match roll_xdy(rng, 1, 3) {
                1 => vec![Weapon::Standard(WeaponStandard::Thrasher)],
                2 => vec![Weapon::Standard(WeaponStandard::Constriction)],
                _ => vec![Weapon::Standard(WeaponStandard::Trample)],
            };
            (w, 3)
        },
    };
    b.weapons.extend(weapons);
    b.damage_dice += damage_mod;
}

fn behavior_effects(rng: &mut ChaCha8Rng, b: &mut Builder, primary_behavior: Behavior) {
    for behavior in b.behaviors.iter().copied().collect::<Vec<_>>() {
        match behavior {
            Behavior::CarrionEater => { b.instinct += 2; b.size -= 2; b.initiative -= 1; }
            Behavior::Chaser => { b.dexterity += 4; b.instinct += 2; b.pack += 2; b.initiative += 2; }
            Behavior::Eater => { b.endurance += 4; b.pack += 4; b.initiative += 1; }
            Behavior::Filter => { b.endurance += 4; b.pack -= 2; b.initiative -= 4; }
            Behavior::Gatherer => { b.pack += 2; b.instinct += 1; b.skill(Skill::Stealth).raise(); }
            Behavior::Grazer => { b.instinct += 2; b.pack += 4; b.initiative -= 1; }
            Behavior::Hijacker => { b.strength += 2; b.pack += 2; b.initiative += 1; }
            Behavior::Hunter => { b.instinct += 2; b.skill(Skill::Survival).raise(); b.skill(Skill::Recon).raise(); b.initiative += 1; }
            Behavior::Intermittent => { b.pack += 4; b.size += 2; b.skill(Skill::Survival).raise(); b.initiative -= 2; }
            Behavior::Intimidator => { b.instinct += 2; b.skill(Skill::Persuade).raise(); }
            Behavior::Killer => { b.instinct += 4; b.pack -= 2; if roll_xdy(rng, 1, 6) < 4 { b.strength += 4 } else { b.dexterity += 4 }; b.skill(Skill::Melee).raise(); }
            Behavior::Pouncer => { b.dexterity += 2; b.instinct += 2; b.skill(Skill::Athletics).raise(); b.skill(Skill::Recon).raise(); b.skill(Skill::Stealth).raise(); b.initiative += 3; }
            Behavior::Reducer => { b.endurance += 2; b.pack += 4; b.initiative -= 2; }
            Behavior::Siren => { b.pack -= 4; b.skill(Skill::Deception).raise(); }
            Behavior::Trapper => { b.endurance += 1; b.pack -= 2; b.skill(Skill::Stealth).raise(); b.initiative += 2; }
        }
    }

    match primary_behavior {
        Behavior::CarrionEater => { b.attack_threshold = AttackThreshold::Roll(11); b.flee_threshold = FleeThreshold::Roll(7); }
        Behavior::Chaser => { b.attack_threshold = AttackThreshold::Outnumbers; b.flee_threshold = FleeThreshold::Roll(5); }
        Behavior::Eater => { b.attack_threshold = AttackThreshold::Roll(5); b.flee_threshold = FleeThreshold::Roll(4); }
        Behavior::Filter => { b.attack_threshold = AttackThreshold::Roll(10); b.flee_threshold = FleeThreshold::Roll(5); }
        Behavior::Gatherer => { b.attack_threshold = AttackThreshold::Roll(9); b.flee_threshold = FleeThreshold::Roll(7); }
        Behavior::Grazer => { b.attack_threshold = AttackThreshold::Roll(8); b.flee_threshold = FleeThreshold::Roll(6); }
        Behavior::Hijacker => { b.attack_threshold = AttackThreshold::Roll(7); b.flee_threshold = FleeThreshold::Roll(6); }
        Behavior::Hunter => { b.attack_threshold = AttackThreshold::Heavier; b.flee_threshold = FleeThreshold::Roll(5); }
        Behavior::Intermittent => { b.attack_threshold = AttackThreshold::Roll(10); b.flee_threshold = FleeThreshold::Roll(4); }
        Behavior::Intimidator => { b.attack_threshold = AttackThreshold::Roll(8); b.flee_threshold = FleeThreshold::Roll(7); }
        Behavior::Killer => { b.attack_threshold = AttackThreshold::Roll(6); b.flee_threshold = FleeThreshold::Roll(3); }
        Behavior::Pouncer => { b.attack_threshold = AttackThreshold::Surprise; b.flee_threshold = FleeThreshold::Surprise; }
        Behavior::Reducer => { b.attack_threshold = AttackThreshold::Roll(10); b.flee_threshold = FleeThreshold::Roll(7); }
        Behavior::Siren => { b.attack_threshold = AttackThreshold::Surprise; b.flee_threshold = FleeThreshold::Roll(4); }
        Behavior::Trapper => { b.attack_threshold = AttackThreshold::Surprise; b.flee_threshold = FleeThreshold::Roll(5); }
    }
}

fn roll_diet(rules: &dyn ClassRules, roll: u8) -> Diet {
    rules.diet(roll)
}

fn roll_quirks(rng: &mut ChaCha8Rng, rules: &dyn ClassRules, b: &mut Builder) {
    while b.quirk_rolls > 0 {
        b.quirk_rolls -= 1;
        let roll = roll_xdy(rng, 2, 6);
        if roll == 12 {
            b.quirk_rolls += 2;   // "roll twice"
            continue;
        }
        let quirk = rules.quirk_for(roll);
        if b.quirks.insert(quirk) {
            quirk.apply(b);       // only a newly gained quirk takes effect
        }
    }
}

fn roll_exotic_weapons(rng: &mut ChaCha8Rng, rules: &dyn ClassRules, b: &mut Builder) {
    let shared = &WeaponExotic::SHARED;
    let extras = rules.extra_exotics();
    let sides = (shared.len() + extras.len()) as u8;
    while b.exotic_weapon_rolls > 0 {
        b.exotic_weapon_rolls -= 1;
        let i = roll_xdy(rng, 1, sides) as usize - 1;
        let exotic = if i < shared.len() { shared[i] } else { extras[i - shared.len()] };
        b.add_weapon(Weapon::Exotic(exotic));
    }
}

fn roll_physical_skills(rng: &mut ChaCha8Rng, rules: &dyn ClassRules, b: &mut Builder) {
    while b.physical_skill_rolls > 0 {
        b.physical_skill_rolls -= 1;
        rules.physical_skill(rng, b);
    }
}

fn roll_social_skills(rng: &mut ChaCha8Rng, rules: &dyn ClassRules, b: &mut Builder) {
    while b.social_skill_rolls > 0 {
        b.social_skill_rolls -= 1;
        rules.social_skill(rng, b);
    }
}

fn roll_evolution_skills(rng: &mut ChaCha8Rng, rules: &dyn ClassRules, b: &mut Builder) {
    while b.evolution_skill_rolls > 0 {
        b.evolution_skill_rolls -= 1;
        rules.evolution_skill(rng, b);
    }
}

fn roll_evolutionary_additional_skills(rng: &mut ChaCha8Rng, rules: &dyn ClassRules, b: &mut Builder) {
    while b.evolution_additional_skill_rolls > 0 {
        b.evolution_additional_skill_rolls -= 1;
        rules.evolutionary_additional_skills(rng, b);
    }
}

fn roll_evolutionary_other_benefits(rng: &mut ChaCha8Rng, rules: &dyn ClassRules, b: &mut Builder) {
    while b.evolution_other_benefits_rolls > 0 {
        b.evolution_other_benefits_rolls -= 1;
        rules.evolutionary_other_benefits(rng, b);
    }
}

fn roll_behavior(rng: &mut ChaCha8Rng, rules: &dyn ClassRules, b: &mut Builder) -> (Behavior, i8) {
    rules.behavior(rng, b)
}

fn apply_also_viable_terrain_mods(rules: &dyn ClassRules, b: &mut Builder, roll: u8) {
    rules.also_viable_terrain_mods(b, roll);
}

pub fn size_stats(rng: &mut ChaCha8Rng, b: &mut Builder) {
    let mut roll = roll_xdy(rng, 2, 6) as i8 + b.size + b.roll_mod;
    if b.size_halved { roll /= 2; }
    match roll {
        ..=1 => { b.weight_kg = 1;     b.strength += 1;                                                   b.dexterity += roll_xdy(rng, 1, 6) as i8; b.endurance += 1; },
        2 =>    { b.weight_kg = 3;     b.strength += 2;                                                   b.dexterity += roll_xdy(rng, 1, 6) as i8; b.endurance += 2; },
        3 =>    { b.weight_kg = 6;     b.strength += roll_xdy(rng, 1, 6) as i8; b.dexterity += roll_xdy(rng, 2, 6) as i8;       b.endurance += roll_xdy(rng, 1, 6) as i8; },
        4 =>    { b.weight_kg = 12;    b.strength += roll_xdy(rng, 1, 6) as i8; b.dexterity += roll_xdy(rng, 2, 6) as i8;       b.endurance += roll_xdy(rng, 1, 6) as i8; },
        5 =>    { b.weight_kg = 25;    b.strength += roll_xdy(rng, 2, 6) as i8; b.dexterity += roll_xdy(rng, 3, 6) as i8;       b.endurance += roll_xdy(rng, 2, 6) as i8; },
        6 =>    { b.weight_kg = 50;    b.strength += roll_xdy(rng, 2, 6) as i8; b.dexterity += roll_xdy(rng, 4, 6) as i8;       b.endurance += roll_xdy(rng, 2, 6) as i8; },
        7 =>    { b.weight_kg = 100;   b.strength += roll_xdy(rng, 3, 6) as i8; b.dexterity += roll_xdy(rng, 3, 6) as i8;       b.endurance += roll_xdy(rng, 3, 6) as i8; },
        8 =>    { b.weight_kg = 200;   b.strength += roll_xdy(rng, 3, 6) as i8; b.dexterity += roll_xdy(rng, 3, 6) as i8;       b.endurance += roll_xdy(rng, 3, 6) as i8; },
        9 =>    { b.weight_kg = 400;   b.strength += roll_xdy(rng, 4, 6) as i8; b.dexterity += roll_xdy(rng, 2, 6) as i8;       b.endurance += roll_xdy(rng, 4, 6) as i8; },
        10 =>   { b.weight_kg = 800;   b.strength += roll_xdy(rng, 4, 6) as i8; b.dexterity += roll_xdy(rng, 2, 6) as i8;       b.endurance += roll_xdy(rng, 4, 6) as i8; },
        11 =>   { b.weight_kg = 1600;  b.strength += roll_xdy(rng, 5, 6) as i8; b.dexterity += roll_xdy(rng, 2, 6) as i8;       b.endurance += roll_xdy(rng, 5, 6) as i8; },
        12 =>   { b.weight_kg = 3200;  b.strength += roll_xdy(rng, 6, 6) as i8; b.dexterity += roll_xdy(rng, 1, 6) as i8;       b.endurance += roll_xdy(rng, 6, 6) as i8; },
        13 =>   { b.weight_kg = 5000;  b.strength += roll_xdy(rng, 7, 6) as i8; b.dexterity += roll_xdy(rng, 1, 6) as i8;       b.endurance += roll_xdy(rng, 7, 6) as i8; },
        14 =>   { b.weight_kg = 8000;  b.strength += roll_xdy(rng, 8, 6) as i8; b.dexterity += 2;                                                   b.endurance += roll_xdy(rng, 8, 6) as i8; },
        _ =>    { b.weight_kg = 10000; b.strength += roll_xdy(rng, 9, 6) as i8; b.dexterity += 1;                                                   b.endurance += roll_xdy(rng, 9, 6) as i8; },
    };
}

pub fn prefers(terrain: Terrain) -> &'static [AnimalClass] {
    match terrain {
        Terrain::BeachShore => { &[AnimalClass::Amphibian, AnimalClass::Aquatic, AnimalClass::Avian, AnimalClass::Insect] },
        Terrain::Clear => { &[AnimalClass::Avian, AnimalClass::Insect, AnimalClass::Mammal] },
        Terrain::DeepOcean => { &[AnimalClass::Aquatic] },
        Terrain::Desert => { &[AnimalClass::Avian, AnimalClass::Insect, AnimalClass::Reptile] },
        Terrain::Forest => { &[AnimalClass::Avian, AnimalClass::Fungal, AnimalClass::Insect, AnimalClass::Mammal] },
        Terrain::Hills => { &[AnimalClass::Avian, AnimalClass::Insect, AnimalClass::Mammal, AnimalClass::Reptile] },
        Terrain::IceSheet => { &[] },
        Terrain::Jungle => { &[AnimalClass::Amphibian, AnimalClass::Avian, AnimalClass::Fungal, AnimalClass::Insect, AnimalClass::Reptile] },
        Terrain::Mountains => { &[AnimalClass::Avian, AnimalClass::Insect] },
        Terrain::OpenOcean => { &[AnimalClass::Aquatic] },
        Terrain::Plains => { &[AnimalClass::Avian, AnimalClass::Insect, AnimalClass::Mammal, AnimalClass::Reptile] },
        Terrain::Rainforest => { &[AnimalClass::Avian, AnimalClass::Fungal, AnimalClass::Insect, AnimalClass::Reptile] },
        Terrain::Riverbank => { &[AnimalClass::Amphibian, AnimalClass::Aquatic, AnimalClass::Avian, AnimalClass::Insect, AnimalClass::Mammal, AnimalClass::Reptile] },
        Terrain::RoughBroken => { &[AnimalClass::Avian, AnimalClass::Insect, AnimalClass::Reptile] },
        Terrain::ShallowOcean => { &[AnimalClass::Amphibian, AnimalClass::Aquatic, AnimalClass::Avian] },
        Terrain::SwampMarsh => { &[AnimalClass::Amphibian, AnimalClass::Aquatic, AnimalClass::Avian, AnimalClass::Fungal, AnimalClass::Insect, AnimalClass::Reptile] },
        Terrain::Tundra => { &[] },
        Terrain::Woods => { &[AnimalClass::Avian, AnimalClass::Fungal, AnimalClass::Insect, AnimalClass::Mammal] },
    }
}

pub fn also_viable(terrain: Terrain) -> &'static [AnimalClass] {
    match terrain {
        Terrain::BeachShore => { &[AnimalClass::Fungal, AnimalClass::Mammal, AnimalClass::Reptile] },
        Terrain::Clear => { &[AnimalClass::Fungal, AnimalClass::Reptile] },
        Terrain::DeepOcean => { &[] },
        Terrain::Desert => { &[AnimalClass::Fungal, AnimalClass::Mammal] },
        Terrain::Forest => { &[AnimalClass::Reptile] },
        Terrain::Hills => { &[AnimalClass::Fungal] },
        Terrain::IceSheet => { &[AnimalClass::Avian, AnimalClass::Mammal] },
        Terrain::Jungle => { &[AnimalClass::Mammal] },
        Terrain::Mountains => { &[AnimalClass::Fungal, AnimalClass::Mammal, AnimalClass::Reptile] },
        Terrain::OpenOcean => { &[] },
        Terrain::Plains => { &[AnimalClass::Fungal] },
        Terrain::Rainforest => { &[AnimalClass::Amphibian, AnimalClass::Mammal] },
        Terrain::Riverbank => { &[AnimalClass::Fungal] },
        Terrain::RoughBroken => { &[AnimalClass::Fungal, AnimalClass::Mammal] },
        Terrain::ShallowOcean => { &[AnimalClass::Insect] },
        Terrain::SwampMarsh => { &[AnimalClass::Mammal] },
        Terrain::Tundra => { &[AnimalClass::Avian, AnimalClass::Insect, AnimalClass::Mammal] },
        Terrain::Woods => { &[AnimalClass::Reptile] },
    }
}

fn terrain_table(terrain: Terrain) -> (i8, [(Movement, i8); 6]) {
    use Movement::*;
    match terrain {
        Terrain::BeachShore   => (2,  [(Swim, 1),  (Swim, 1), (Walk, 0), (Walk, 0), (Fly, -4), (Fly, -6)]),
        Terrain::Clear        => (0,  [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -6)]),
        Terrain::DeepOcean    => (2,  [(Swim, 8),  (Swim, 6), (Swim, 4), (Swim, 2), (Swim, 0), (Swim, -2)]),
        Terrain::Desert       => (-3, [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 0), (Fly, -4), (Fly, -6)]),
        Terrain::Forest       => (-4, [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 0), (Fly, -4), (Fly, -6)]),
        Terrain::Hills        => (0,  [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -4), (Fly, -6)]),
        Terrain::IceSheet     => (2,  [(Swim, 4),  (Swim, 2), (Walk, 2), (Walk, 0), (Walk, 0), (Fly, -4)]),
        Terrain::Jungle       => (-3, [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -6)]),
        Terrain::Mountains    => (0,  [(Walk, 0),  (Walk, 0), (Walk, 0), (Fly, -2), (Fly, -4), (Fly, -6)]),
        Terrain::OpenOcean    => (-4, [(Swim, 6),  (Swim, 4), (Swim, 2), (Swim, 0), (Fly, -4), (Fly, -6)]),
        Terrain::Plains       => (0,  [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 2), (Walk, 4), (Fly, -6)]),
        Terrain::Rainforest   => (-2, [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 2), (Walk, 4), (Fly, -6)]),
        Terrain::Riverbank    => (1,  [(Swim, -4), (Swim, 2), (Walk, 0), (Walk, 0), (Walk, 0), (Fly, -6)]),
        Terrain::RoughBroken  => (-3, [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -4), (Fly, -6)]),
        Terrain::ShallowOcean => (1,  [(Swim, 4),  (Swim, 2), (Swim, 0), (Swim, 0), (Fly, -4), (Fly, -6)]),
        Terrain::SwampMarsh   => (4,  [(Swim, -6), (Swim, 0), (Walk, 0), (Walk, 0), (Fly, -4), (Fly, -6)]),
        Terrain::Tundra       => (1,  [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -6)]),
        Terrain::Woods        => (-1, [(Walk, 0),  (Walk, 0), (Walk, 0), (Walk, 0), (Walk, 0), (Fly, -6)])
    }
}

fn burrows_instead(class: AnimalClass, terrain: Terrain, roll_2d6: u8) -> bool {
    class != AnimalClass::Avian
        && !matches!(terrain, Terrain::ShallowOcean | Terrain::OpenOcean | Terrain::DeepOcean)
        && roll_2d6 >= 10
}

/// The terrain chart's base size DM, without any movement row's DM.
pub(crate) fn terrain_base_size(terrain: Terrain) -> i8 {
    terrain_table(terrain).0
}

/// Sets the rolled movement, swapping Fly for Burrow when the burrow roll allows.
pub(crate) fn set_movement(rng: &mut ChaCha8Rng, b: &mut Builder, mut movement: Movement) {
    if movement == Movement::Fly && burrows_instead(b.class, b.terrain, roll_xdy(rng, 2, 6)) {
        movement = Movement::Burrow;
    }
    b.movement = Some(movement);
}

pub fn terrain_size_movement(rng: &mut ChaCha8Rng, b: &mut Builder) {
    let (base, rows) = terrain_table(b.terrain);
    let (movement, size_mod) = rows[roll_xdy(rng, 1, 6) as usize - 1];
    set_movement(rng, b, movement);
    b.size += base + size_mod;
}

#[cfg(test)]
mod shared_table_tests {
    use super::*;
    use rand::SeedableRng;
 
    const CLASSES: [AnimalClass; 7] = [
        AnimalClass::Amphibian, AnimalClass::Aquatic, AnimalClass::Avian, AnimalClass::Fungal,
        AnimalClass::Insect, AnimalClass::Mammal, AnimalClass::Reptile,
    ];
 
 
    fn rng() -> ChaCha8Rng {
        ChaCha8Rng::seed_from_u64(1)
    }
 
    // -----------------------------------------------------------------------
    // Terrain movement table
    // -----------------------------------------------------------------------
 
    /// The terrain chart straight from the supplement: base size DM, then
    /// (movement, size DM) for each 1d6 row. An em dash in the book means
    /// zero. Burrowing isn't in the chart; it substitutes for flying.
    #[test]
    fn terrain_table_matches_the_supplement() {
        use Movement::*;
        use Terrain::*;
        let expected: [(Terrain, i8, [(Movement, i8); 6]); 18] = [
            (BeachShore,    2, [(Swim,  1), (Swim, 1), (Walk, 0), (Walk, 0), (Fly, -4), (Fly, -6)]),
            (Clear,         0, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -6)]),
            (DeepOcean,     2, [(Swim,  8), (Swim, 6), (Swim, 4), (Swim, 2), (Swim, 0), (Swim, -2)]),
            (Desert,       -3, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 0), (Fly, -4), (Fly, -6)]),
            (Forest,       -4, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 0), (Fly, -4), (Fly, -6)]),
            (Hills,         0, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -4), (Fly, -6)]),
            (Jungle,       -3, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -6)]),
            (Mountains,     0, [(Walk,  0), (Walk, 0), (Walk, 0), (Fly, -2), (Fly, -4), (Fly, -6)]),
            (OpenOcean,    -4, [(Swim,  6), (Swim, 4), (Swim, 2), (Swim, 0), (Fly, -4), (Fly, -6)]),
            (Plains,        0, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 2), (Walk, 4), (Fly, -6)]),
            (Rainforest,   -2, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 2), (Walk, 4), (Fly, -6)]),
            (Riverbank,     1, [(Swim, -4), (Swim, 2), (Walk, 0), (Walk, 0), (Walk, 0), (Fly, -6)]),
            (RoughBroken,  -3, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -4), (Fly, -6)]),
            (ShallowOcean,  1, [(Swim,  4), (Swim, 2), (Swim, 0), (Swim, 0), (Fly, -4), (Fly, -6)]),
            (SwampMarsh,    4, [(Swim, -6), (Swim, 0), (Walk, 0), (Walk, 0), (Fly, -4), (Fly, -6)]),
            (Woods,        -1, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 0), (Walk, 0), (Fly, -6)]),
            // Ours, not the supplement's.
            (IceSheet,      2, [(Swim,  4), (Swim, 2), (Walk, 2), (Walk, 0), (Walk, 0), (Fly, -4)]),
            (Tundra,        1, [(Walk,  0), (Walk, 0), (Walk, 0), (Walk, 0), (Walk, 2), (Fly, -6)]),
        ];
        for (terrain, base, rows) in expected {
            assert_eq!(terrain_table(terrain), (base, rows), "{terrain:?} terrain chart");
        }
    }

    /// Burrow is only ever a substitution, never a chart entry.
    #[test]
    fn the_table_never_lists_burrow() {
        for terrain in Terrain::ALL {
            let (_, rows) = terrain_table(terrain);
            assert!(rows.iter().all(|(m, _)| *m != Movement::Burrow), "{terrain:?} lists Burrow");
        }
    }

    /// Deep ocean is the one terrain with no escape upward: every row swims.
    #[test]
    fn deep_ocean_is_always_swimming() {
        let (_, rows) = terrain_table(Terrain::DeepOcean);
        assert!(rows.iter().all(|(m, _)| *m == Movement::Swim));
    }

    /// Non-avian fliers burrow instead on 10+.
    #[test]
    fn burrowing_needs_ten_or_more() {
        for roll in 2..=12 {
            assert_eq!(burrows_instead(AnimalClass::Mammal, Terrain::Clear, roll), roll >= 10, "roll {roll}");
        }
    }

    /// Birds fly; the burrow substitution is for everyone else.
    #[test]
    fn avians_never_burrow() {
        for terrain in Terrain::ALL {
            for roll in 2..=12 {
                assert!(!burrows_instead(AnimalClass::Avian, terrain, roll), "{terrain:?} roll {roll}");
            }
        }
    }

    /// There's nothing to burrow into over open water.
    #[test]
    fn nobody_burrows_at_sea() {
        for terrain in [Terrain::ShallowOcean, Terrain::OpenOcean, Terrain::DeepOcean] {
            for class in CLASSES {
                assert!(!burrows_instead(class, terrain, 12), "{class:?} burrowed in {terrain:?}");
            }
        }
    }

    /// The glue: whatever gets rolled is a row of the chart (with fly possibly
    /// swapped for burrow), and the builder gets base plus row size DM.
    #[test]
    fn rolling_applies_a_chart_row() {
        for terrain in Terrain::ALL {
            let (base, rows) = terrain_table(terrain);
            for seed in 0..32 {
                let mut b = baseline();
                b.terrain = terrain;
                b.class = AnimalClass::Mammal;
                terrain_size_movement(&mut ChaCha8Rng::seed_from_u64(seed), &mut b);
                let movement = b.movement.expect("terrain roll sets movement");
                let as_charted = if movement == Movement::Burrow { Movement::Fly } else { movement };
                assert!(rows.iter().any(|&(m, s)| m == as_charted && base + s == b.size),
                    "{terrain:?} seed {seed}: {movement:?} at size {} isn't a chart row", b.size);
            }
        }
    }

    #[test]
    fn fungals_only_get_the_base_size_dm() {
        for terrain in Terrain::ALL {
            let mut seen = BTreeSet::new();
            for seed in 0..64 {
                let mut b = baseline();
                b.terrain = terrain;
                b.class = AnimalClass::Fungal;
                fungal::size_and_movement(&mut ChaCha8Rng::seed_from_u64(seed), &mut b);
                assert_eq!(b.size, terrain_base_size(terrain), "{terrain:?} seed {seed}");
                seen.insert(b.movement.expect("fungal roll sets movement"));
            }
            assert!(seen.contains(&Movement::Immobile), "{terrain:?} never rolled Immobile");
            assert!(!seen.contains(&Movement::Swim), "{terrain:?} fungal swims");
        }
    }

    #[test]
    fn halving_size_halves_the_size_roll() {
        // Whole, 2d6+12 is 14..=24 (8000 kg or more); halved it's 7..=12.
        for seed in 0..32 {
            let mut b = baseline();
            b.size = 12;
            b.size_halved = true;
            size_stats(&mut ChaCha8Rng::seed_from_u64(seed), &mut b);
            assert!((100..=3200).contains(&b.weight_kg), "seed {seed}: {} kg", b.weight_kg);
        }
    }
 
    // -----------------------------------------------------------------------
    // Class preferences
    // -----------------------------------------------------------------------
 
    /// Terrains where a class is listed as preferring to live.
    fn preferred_terrains(class: AnimalClass) -> Vec<Terrain> {
        Terrain::ALL.into_iter().filter(|&t| prefers(t).contains(&class)).collect()
    }
 
    fn viable_terrains(class: AnimalClass) -> Vec<Terrain> {
        Terrain::ALL.into_iter()
            .filter(|&t| prefers(t).contains(&class) || also_viable(t).contains(&class))
            .collect()
    }
 
    /// Each class's preferred terrains, from the supplement's per-class
    /// Terrain Preferences lines. Two deliberate divergences are marked.
    #[test]
    fn preferred_terrains_match_the_supplement() {
        use AnimalClass::*;
        use Terrain::*;
 
        let expected: [(AnimalClass, Vec<Terrain>); 7] = [
            (Amphibian, vec![BeachShore, Jungle, Riverbank, ShallowOcean, SwampMarsh]),
            // Supplement lists only the four coastal terrains; open and deep
            // ocean are ours, since the movement chart has rows for them.
            (Aquatic, vec![BeachShore, DeepOcean, OpenOcean, Riverbank, ShallowOcean, SwampMarsh]),
            // "Any terrain except open ocean and deep ocean" - minus the two
            // cold terrains, which by our rule nobody prefers.
            (Avian, vec![BeachShore, Clear, Desert, Forest, Hills, Jungle, Mountains, Plains,
                         Rainforest, Riverbank, RoughBroken, ShallowOcean, SwampMarsh, Woods]),
            (Fungal, vec![Forest, Jungle, Rainforest, SwampMarsh, Woods]),
            // "All terrains and habitats, though not ocean environs" - again
            // minus the cold terrains.
            (Insect, vec![BeachShore, Clear, Desert, Forest, Hills, Jungle, Mountains, Plains,
                          Rainforest, Riverbank, RoughBroken, SwampMarsh, Woods]),
            (Mammal, vec![Clear, Forest, Hills, Plains, Riverbank, Woods]),
            (Reptile, vec![Desert, Hills, Jungle, Plains, Rainforest, Riverbank, RoughBroken,
                           SwampMarsh]),
        ];
 
        for (class, terrains) in expected {
            assert_eq!(preferred_terrains(class), terrains, "{class:?} preferred terrains");
        }
    }
 
    /// A class is either preferred or additionally viable in a terrain, never
    /// both - otherwise the out-of-terrain penalties would be ambiguous.
    #[test]
    fn preferred_and_viable_never_overlap() {
        for terrain in Terrain::ALL {
            for class in prefers(terrain) {
                assert!(!also_viable(terrain).contains(class),
                    "{terrain:?}: {class:?} is both preferred and additionally viable");
            }
        }
    }
 
    /// Both lists are sorted and free of duplicates. Generation walks them in
    /// order, so a stable order is what keeps a seed reproducible.
    #[test]
    fn class_lists_are_sorted_and_unique() {
        for terrain in Terrain::ALL {
            for (label, list) in [("preferred", prefers(terrain)), ("viable", also_viable(terrain))] {
                assert!(list.windows(2).all(|w| w[0] < w[1]),
                    "{terrain:?} {label} list is unsorted or has duplicates: {list:?}");
            }
        }
    }
 
    /// No class is homeless, and no class is everywhere-preferred by accident.
    #[test]
    fn every_class_has_somewhere_to_live() {
        for class in CLASSES {
            assert!(!preferred_terrains(class).is_empty(), "{class:?} prefers nowhere");
            assert!(viable_terrains(class).len() < Terrain::ALL.len(),
                "{class:?} lives everywhere - is that intended?");
        }
    }
 
    /// Aquatics need water. This is the one hard exclusion in the supplement.
    #[test]
    fn aquatics_only_live_in_water() {
        use Terrain::*;
        let watery = [BeachShore, DeepOcean, OpenOcean, Riverbank, ShallowOcean, SwampMarsh];
        for terrain in viable_terrains(AnimalClass::Aquatic) {
            assert!(watery.contains(&terrain), "aquatics listed for {terrain:?}");
        }
    }
 
    /// The cold terrains are outside every class's preferences, which is what
    /// gives their fauna the out-of-terrain modifiers.
    #[test]
    fn nobody_prefers_the_cold() {
        for terrain in [Terrain::IceSheet, Terrain::Tundra] {
            assert!(prefers(terrain).is_empty(), "{terrain:?} has preferred classes");
            assert!(!also_viable(terrain).is_empty(), "{terrain:?} has no fauna at all");
        }
    }
 
    // -----------------------------------------------------------------------
    // Skills
    // -----------------------------------------------------------------------
 
    /// Untrained is -3, and the first increase jumps to 0 rather than -2.
    #[test]
    fn raising_an_untrained_skill_reaches_zero() {
        let mut s = SkillLevel::default();
        assert!(!s.is_trained());
        assert_eq!(s.dm(), -3);
 
        s.raise();
        assert!(s.is_trained());
        assert_eq!(s.dm(), 0, "untrained raises to 0, never to -2");
 
        s.raise();
        assert_eq!(s.dm(), 1);
    }
 
    #[test]
    fn training_sets_a_level_directly() {
        let mut s = SkillLevel::default();
        s.train_at(0);
        assert_eq!(s.dm(), 0);
        s.raise();
        assert_eq!(s.dm(), 1);
    }

    #[test]
    fn lowering_a_skill_stops_at_untrained() {
        let mut s = SkillLevel::default();
        s.train_at(1);
        s.lower();
        assert_eq!(s.dm(), 0);
        s.lower();
        assert_eq!(s.dm(), -1);
        s.lower();
        assert_eq!(s.dm(), -2);
        s.lower();
        assert_eq!(s.dm(), -3);
        assert!(s.is_trained());
        s.lower();
        assert_eq!(s.dm(), -3);
    }

    #[test]
    fn lowering_an_untrained_skill_does_nothing() {
        let mut s = SkillLevel::default();
        s.lower();
        assert_eq!(s.dm(), -3);
        assert!(!s.is_trained());
    }
 
    /// `skill as usize` indexes the array, so the enum's declaration order is
    /// load-bearing. This fails if a variant is added without bumping COUNT,
    /// or inserted ahead of Survival.
    #[test]
    fn skill_count_matches_the_enum() {
        assert_eq!(Skill::Survival as usize, Skill::COUNT - 1);
    }

    #[test]
    fn quirks_are_unique_within_a_class() {
        let mut b = baseline();
        b.quirk_rolls = 3;
        roll_quirks(&mut rng(), rules(b.class), &mut b);
        assert_eq!(b.quirk_rolls, 0);
        assert!(b.quirks.iter().all(|q| matches!(q, Quirk::Amphibian(_))));
    }
 
    // -----------------------------------------------------------------------
    // Exotic weapons
    // -----------------------------------------------------------------------

    /// Every exotic weapon a class's builder ends up with after many rolls.
    fn exotics_after_many_rolls(class: AnimalClass) -> Vec<WeaponExotic> {
        let mut b = baseline();
        b.class = class;
        b.exotic_weapon_rolls = 200;
        roll_exotic_weapons(&mut rng(), rules(class), &mut b);
        b.weapons.iter().filter_map(|w| match w { Weapon::Exotic(e) => Some(*e), _ => None }).collect()
    }

    #[test]
    fn shared_exotics_are_unique() {
        let shared = WeaponExotic::SHARED;
        for (i, e) in shared.iter().enumerate() {
            assert!(!shared[i + 1..].contains(e), "{e:?} appears twice in SHARED");
        }
    }

    /// A class extra that's already shared would just double its odds.
    #[test]
    fn class_exotics_are_unique_and_not_shared() {
        for class in IMPLEMENTED {
            let extras = rules(class).extra_exotics();
            for (i, e) in extras.iter().enumerate() {
                assert!(!WeaponExotic::SHARED.contains(e), "{class:?} extra {e:?} is already shared");
                assert!(!extras[i + 1..].contains(e), "{class:?} lists {e:?} twice");
            }
        }
    }

    /// Given enough rolls, a class gets exactly its pool: the shared six plus
    /// its own extras, and nothing belonging to another class.
    #[test]
    fn each_class_rolls_exactly_its_pool() {
        for class in IMPLEMENTED {
            let mut expected: Vec<WeaponExotic> = WeaponExotic::SHARED.iter()
                .chain(rules(class).extra_exotics())
                .copied()
                .collect();
            expected.sort();
            let mut got = exotics_after_many_rolls(class);
            got.sort();
            assert_eq!(got, expected, "{class:?} exotic pool");
        }
    }

    /// Stench is amphibian-only: in their pool, not in the shared six.
    // TODO: once mammal rules exist, also assert mammals never roll it.
    #[test]
    fn stench_is_amphibian_only() {
        assert!(exotics_after_many_rolls(AnimalClass::Amphibian).contains(&WeaponExotic::Stench));
        assert!(!WeaponExotic::SHARED.contains(&WeaponExotic::Stench));
    }

    /// A repeat roll doesn't add a second copy, and every roll is spent.
    #[test]
    fn exotic_rolls_never_duplicate_weapons() {
        let mut b = baseline();
        b.exotic_weapon_rolls = 50;
        roll_exotic_weapons(&mut rng(), rules(b.class), &mut b);
        assert_eq!(b.exotic_weapon_rolls, 0);
        for (i, w) in b.weapons.iter().enumerate() {
            assert!(!b.weapons[i + 1..].contains(w), "{w:?} added twice");
        }
    }

    /// Foul Skin grants Stench, but not a second copy if it was already rolled.
    #[test]
    fn foul_skin_does_not_duplicate_stench() {
        let mut b = baseline();
        b.add_weapon(Weapon::Exotic(WeaponExotic::Stench));
        Quirk::Amphibian(amphibian::Quirk::FoulSkin).apply(&mut b);
        let stench = b.weapons.iter().filter(|w| **w == Weapon::Exotic(WeaponExotic::Stench)).count();
        assert_eq!(stench, 1);
    }
 
    // -----------------------------------------------------------------------
    // Behavior effects
    // -----------------------------------------------------------------------
 
    /// A builder with every tracked value at a known baseline. Pack starts at
    /// 10 so the behaviors that subtract from it have room to.
    fn baseline() -> Builder {
        Builder {
            terrain: Terrain::Riverbank,
            class: AnimalClass::Amphibian,
            diet: Diet::Omnivore,
            strength: 0, dexterity: 0, endurance: 0,
            instinct: 0, pack: 10, intelligence: 0,
            size: 0,
            armor: 0,
            quirks: BTreeSet::new(),
            behaviors: BTreeSet::new(),
            reaction_modifier: 0,
            weapons: Vec::new(),
            damage_dice: 0,
            initiative: 0,
            movement: None,
            exotic_weapon_rolls: 0, evolution_additional_skill_rolls: 0,
            evolution_other_benefits_rolls: 0, evolution_mod: 0,
            physical_skill_rolls: 0, social_skill_rolls: 0, evolution_skill_rolls: 0,
            quirk_rolls: 0,
            weight_kg: 0,
            skills: [SkillLevel::default(); Skill::COUNT],
            attack_threshold: AttackThreshold::Roll(0),
            flee_threshold: FleeThreshold::Roll(0),
            roll_mod: 0,
            size_halved: false
        }
    }
 
    fn after(behavior: Behavior) -> Builder {
        let mut b = baseline();
        b.behaviors.insert(behavior);
        behavior_effects(&mut rng(), &mut b, behavior);
        b
    }
 
    /// Every behavior's stat changes, from the supplement's behavior
    /// descriptions. Skills are checked separately below.
    #[test]
    fn behavior_stat_changes_match_the_supplement() {
        use Behavior::*;
        // (behavior, strength, dexterity, endurance, instinct, pack, size)
        let expected = [
            (CarrionEater, 0, 0, 0, 2, 10, -2),
            (Chaser,       0, 4, 0, 2, 12,  0),
            (Eater,        0, 0, 4, 0, 14,  0),
            (Filter,       0, 0, 4, 0,  8,  0),
            (Gatherer,     0, 0, 0, 1, 12,  0),
            (Grazer,       0, 0, 0, 2, 14,  0),
            (Hijacker,     2, 0, 0, 0, 12,  0),
            (Hunter,       0, 0, 0, 2, 10,  0),
            (Intermittent, 0, 0, 0, 0, 14,  2),
            (Intimidator,  0, 0, 0, 2, 10,  0),
            (Pouncer,      0, 2, 0, 2, 10,  0),
            (Reducer,      0, 0, 2, 0, 14,  0),
            (Siren,        0, 0, 0, 0,  6,  0),
            (Trapper,      0, 0, 1, 0,  8,  0),
        ];
        for (behavior, str_, dex, end, inst, pack, size) in expected {
            let b = after(behavior);
            assert_eq!(b.strength, str_, "{behavior:?} strength");
            assert_eq!(b.dexterity, dex, "{behavior:?} dexterity");
            assert_eq!(b.endurance, end, "{behavior:?} endurance");
            assert_eq!(b.instinct, inst, "{behavior:?} instinct");
            assert_eq!(b.pack, pack, "{behavior:?} pack");
            assert_eq!(b.size, size, "{behavior:?} size");
        }
    }
 
    /// Killer splits its bonus on a die roll, so it can't go in the table
    /// above: instinct and pack are fixed, and exactly four points land on
    /// either strength or dexterity.
    #[test]
    fn killers_put_four_points_into_strength_or_dexterity() {
        let b = after(Behavior::Killer);
        assert_eq!(b.instinct, 4);
        assert_eq!(b.pack, 8);
        assert_eq!(b.strength + b.dexterity, 4, "one stat gets +4, not both");
        assert!(b.strength == 0 || b.dexterity == 0);
        assert!(b.skills[Skill::Melee as usize].is_trained());
    }
 
    /// Which skills each behavior grants.
    #[test]
    fn behaviors_grant_the_right_skills() {
        use Behavior::*;
        use Skill::*;
        let expected: [(Behavior, &[Skill]); 15] = [
            (CarrionEater, &[]),
            (Chaser,       &[]),
            (Eater,        &[]),
            (Filter,       &[]),
            (Gatherer,     &[Stealth]),
            (Grazer,       &[]),
            (Hijacker,     &[]),
            (Hunter,       &[Survival, Recon]),
            (Intermittent, &[Survival]),
            (Intimidator,  &[Persuade]),
            (Killer,       &[Melee]),
            (Pouncer,      &[Stealth, Recon, Athletics]),
            (Reducer,      &[]),
            (Siren,        &[Deception]),
            (Trapper,      &[Stealth]),
        ];
        for (behavior, granted) in expected {
            let b = after(behavior);
            for skill in [Athletics, Deception, Melee, Persuade, Recon, Stealth, Survival] {
                assert_eq!(b.skills[skill as usize].is_trained(), granted.contains(&skill),
                    "{behavior:?} and {skill:?}");
            }
        }
    }
 
    /// Two behaviors apply both sets of effects, in a fixed order.
    #[test]
    fn multiple_behaviors_stack() {
        let mut b = baseline();
        b.behaviors.insert(Behavior::Eater);     // endurance +4, pack +4
        b.behaviors.insert(Behavior::Trapper);   // endurance +1, pack -2
        behavior_effects(&mut rng(), &mut b, Behavior::Eater);
        assert_eq!(b.endurance, 5);
        assert_eq!(b.pack, 12);
    }
}

#[cfg(test)]
mod pipeline_tests {
    use super::*;
    use rand::SeedableRng;
 
 
    /// Every weight the size table can produce.
    const WEIGHTS: [u16; 15] = [1, 3, 6, 12, 25, 50, 100, 200, 400, 800, 1600, 3200, 5000, 8000, 10000];
 
    const SEEDS: std::ops::Range<u64> = 0..200;
 
    fn can_live(class: AnimalClass, terrain: Terrain) -> bool {
        prefers(terrain).contains(&class) || also_viable(terrain).contains(&class)
    }
 
    fn animal(class: AnimalClass, terrain: Terrain, seed: u64) -> Animal {
        create_animal(&mut ChaCha8Rng::seed_from_u64(seed), class, terrain)
    }
 
    /// Call `f` for an animal of every implemented class, in every terrain it
    /// can live in, across the seed range.
    fn each_animal(mut f: impl FnMut(AnimalClass, Terrain, u64, &Animal)) {
        for class in IMPLEMENTED {
            for terrain in Terrain::ALL.into_iter().filter(|&t| can_live(class, t)) {
                for seed in SEEDS {
                    f(class, terrain, seed, &animal(class, terrain, seed));
                }
            }
        }
    }
 
    // -----------------------------------------------------------------------
    // Determinism
    // -----------------------------------------------------------------------
 
    #[test]
    fn same_seed_same_animal() {
        for class in IMPLEMENTED {
            for terrain in Terrain::ALL.into_iter().filter(|&t| can_live(class, t)) {
                assert_eq!(animal(class, terrain, 7), animal(class, terrain, 7),
                    "{class:?} in {terrain:?} is not reproducible");
            }
        }
    }
 
    /// A sanity check that the dice are actually used: different seeds give
    /// different animals.
    #[test]
    fn different_seeds_give_variety() {
        for class in IMPLEMENTED {
            let first = animal(class, Terrain::Riverbank, 0);
            assert!((1..20).any(|seed| animal(class, Terrain::Riverbank, seed) != first),
                "{class:?}: twenty seeds all produced the same animal");
        }
    }
 
    // -----------------------------------------------------------------------
    // Every animal, every terrain
    // -----------------------------------------------------------------------
 
    /// Runs the whole pipeline across every viable terrain, including the
    /// out-of-terrain ones where the roll DM can push table rolls below 1.
    /// Any table without a floor panics here.
    #[test]
    fn generation_never_panics() {
        let mut count = 0;
        each_animal(|_, _, _, _| count += 1);
        assert!(count > 0, "no animals were generated");
    }
 
    #[test]
    fn every_animal_has_a_diet_movement_and_behavior() {
        each_animal(|class, terrain, seed, a| {
            assert!(a.movement.is_some(), "{class:?} {terrain:?} seed {seed}: no movement");
            assert!(!a.behaviors.is_empty(), "{class:?} {terrain:?} seed {seed}: no behavior");
        });
    }
 
    /// Weight only ever comes from the size table.
    #[test]
    fn weight_is_a_size_table_value() {
        each_animal(|class, terrain, seed, a| {
            assert!(WEIGHTS.contains(&a.weight_kg),
                "{class:?} {terrain:?} seed {seed}: weight {} isn't on the size table", a.weight_kg);
        });
    }
 
    /// Loose ceilings. Nothing legitimate comes near them; a value past one
    /// means something is adding repeatedly or an i8 was misread.
    #[test]
    fn characteristics_stay_in_a_sane_range() {
        each_animal(|class, terrain, seed, a| {
            for (name, value, ceiling) in [
                ("strength", a.strength, 100),
                ("dexterity", a.dexterity, 100),
                ("endurance", a.endurance, 100),
                ("instinct", a.instinct, 60),
                ("pack", a.pack, 60),
                ("intelligence", a.intelligence, 6),
            ] {
                assert!(value <= ceiling,
                    "{class:?} {terrain:?} seed {seed}: {name} {value} exceeds {ceiling}");
            }
        });
    }
 
    /// Exotic weapons are rolled with duplicates discarded.
    #[test]
    fn exotic_weapons_are_never_duplicated() {
        each_animal(|class, terrain, seed, a| {
            let exotics: Vec<_> = a.weapons.iter()
                .filter(|w| matches!(w, Weapon::Exotic(_)))
                .collect();
            let unique: BTreeSet<_> = exotics.iter().collect();
            assert_eq!(exotics.len(), unique.len(),
                "{class:?} {terrain:?} seed {seed}: duplicate exotic weapons {:?}", a.weapons);
        });
    }
 
    /// Burrowers gain Stealth from the burrow rule.
    #[test]
    fn burrowers_are_stealthy() {
        each_animal(|class, terrain, seed, a| {
            if a.movement == Some(Movement::Burrow) {
                assert!(a.skills[Skill::Stealth as usize].is_trained(),
                    "{class:?} {terrain:?} seed {seed}: burrower without Stealth");
            }
        });
    }
 
    // -----------------------------------------------------------------------
    // Amphibians specifically
    // -----------------------------------------------------------------------
 
    /// Athletics, Recon and Survival start at 0. Later effects can raise them,
    /// and Blind can lower Recon to -1, but none of them can un-train a skill.
    #[test]
    fn amphibians_keep_their_starting_skills() {
        for terrain in Terrain::ALL.into_iter().filter(|&t| can_live(AnimalClass::Amphibian, t)) {
            for seed in SEEDS {
                let a = animal(AnimalClass::Amphibian, terrain, seed);
                for skill in [Skill::Athletics, Skill::Recon, Skill::Survival] {
                    assert!(a.skills[skill as usize].is_trained(),
                        "{terrain:?} seed {seed}: amphibian lost starting {skill:?}");
                }
            }
        }
    }
 
    /// Carnivorous amphibians start with Melee 0. This is the test that
    /// catches the diet and its starting bonuses coming from different rolls.
    #[test]
    fn carnivorous_amphibians_start_with_melee() {
        for terrain in Terrain::ALL.into_iter().filter(|&t| can_live(AnimalClass::Amphibian, t)) {
            for seed in SEEDS {
                let a = animal(AnimalClass::Amphibian, terrain, seed);
                if a.diet == Diet::Carnivore {
                    assert!(a.skills[Skill::Melee as usize].is_trained(),
                        "{terrain:?} seed {seed}: carnivorous amphibian without Melee");
                }
            }
        }
    }
 
    /// All three diets actually occur. A diet table that can't reach one of
    /// them - like the fungal table that briefly had an unreachable arm -
    /// fails here.
    #[test]
    fn amphibians_eat_everything() {
        let mut seen = BTreeSet::new();
        for seed in SEEDS {
            seen.insert(animal(AnimalClass::Amphibian, Terrain::Riverbank, seed).diet);
        }
        assert_eq!(seen.len(), 3, "only saw diets {seen:?}");
    }
 
    // -----------------------------------------------------------------------
    // Primary behavior
    // -----------------------------------------------------------------------
 
    /// Thresholds come from the primary behavior, even when a quirk adds a
    /// second behavior that would sort after it.
    #[test]
    fn thresholds_come_from_the_primary_behavior() {
        let mut b = Builder {
            terrain: Terrain::Riverbank,
            class: AnimalClass::Amphibian,
            diet: Diet::Carnivore,
            strength: 0, dexterity: 0, endurance: 0,
            instinct: 0, pack: 10, intelligence: 0,
            size: 0,
            armor: 0,
            quirks: BTreeSet::new(),
            behaviors: BTreeSet::new(),
            reaction_modifier: 0,
            weapons: Vec::new(),
            damage_dice: 0,
            initiative: 0,
            movement: None,
            exotic_weapon_rolls: 0, evolution_additional_skill_rolls: 0,
            evolution_other_benefits_rolls: 0, evolution_mod: 0,
            physical_skill_rolls: 0, social_skill_rolls: 0, evolution_skill_rolls: 0,
            quirk_rolls: 0,
            weight_kg: 0,
            skills: [SkillLevel::default(); Skill::COUNT],
            attack_threshold: AttackThreshold::Roll(0),
            flee_threshold: FleeThreshold::Roll(0),
            roll_mod: 0,
            size_halved: false
        };
        // Hunter was rolled; Siren came from the Pheromone quirk and sorts later.
        b.behaviors.insert(Behavior::Hunter);
        b.behaviors.insert(Behavior::Siren);
        behavior_effects(&mut ChaCha8Rng::seed_from_u64(1), &mut b, Behavior::Hunter);
 
        assert_eq!(b.attack_threshold, AttackThreshold::Heavier, "should be Hunter's, not Siren's");
        assert_eq!(b.flee_threshold, FleeThreshold::Roll(5), "should be Hunter's, not Siren's");
    }
}

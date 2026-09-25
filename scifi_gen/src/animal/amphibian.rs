use crate::animal::Behavior;
use crate::animal::ClassRules;
use crate::animal::Skill;
use crate::animal::Weapon;
use crate::animal::WeaponExotic;
use crate::animal::Builder;
use crate::animal::Diet;
use crate::animal::Quirk as AnimalQuirk;
use crate::dice_roller::roll_xdy;
use rand_chacha::ChaCha8Rng;

pub(crate) struct Rules;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum Quirk {
    PackNoise,
    Blind,
    Silent,
    ReverseCamouflage,
    Everywhere,
    Pheromone,
    Scream,
    Swarm,
    FoulSkin,
    Shell,
}

impl Quirk {
    pub(crate) fn from_roll(roll: u8) -> Option<Self> {
        match roll {
            2 => Some(Self::PackNoise),
            3 => Some(Self::Blind),
            4 => Some(Self::Silent),
            5 => Some(Self::ReverseCamouflage),
            6 => Some(Self::Everywhere),
            7 => Some(Self::Pheromone),
            8 => Some(Self::Scream),
            9 => Some(Self::Swarm),
            10 => Some(Self::FoulSkin),
            11 => Some(Self::Shell),
            _ => None,
        }
    }

    pub(super) fn apply(self, b: &mut Builder) {
        match self {
            Self::PackNoise => {}
            Self::Blind => b.skill(Skill::Recon).lower(),
            Self::Silent => {
                if b.skill(Skill::Stealth).dm() < 0 {
                    b.skill(Skill::Stealth).train_at(0);
                }
            }
            Self::ReverseCamouflage => {}
            Self::Everywhere => { b.skill(Skill::Survival).raise(); b.skill(Skill::Survival).raise(); },
            Self::Pheromone => {
                b.behaviors.insert(Behavior::Siren);
            }
            Self::Scream => {}
            Self::Swarm => {}
            Self::FoulSkin => b.add_weapon(Weapon::Exotic(WeaponExotic::Stench)),
            Self::Shell => b.armor += 2,
        }
    }
}

impl ClassRules for Rules {
    fn diet(&self, roll: u8) -> Diet {
        match roll {
            1..=2 => { Diet::Carnivore }
            3 => { Diet::Herbivore }
            _ => { Diet::Omnivore }
        }
    }

    fn also_viable_terrain_mods(&self, b: &mut Builder, roll: u8) {
        b.roll_mod = -2;
    }

    fn starting_stats_skills(&self, b: &mut Builder) {
        b.skill(Skill::Athletics).train_at(0);
        b.skill(Skill::Recon).train_at(0);
        b.skill(Skill::Survival).train_at(0);
        
        match b.diet {
            Diet::Carnivore => {
                b.strength += 1;
                b.evolution_mod += 1;
                b.physical_skill_rolls += 1;
                b.skill(Skill::Melee).train_at(0);
            }
            Diet::Herbivore => {
                b.endurance += 1;
                b.instinct += 1;
                b.social_skill_rolls += 1;
            }
            Diet::Omnivore => {
                b.pack += 4;
                b.instinct += 1;
                b.physical_skill_rolls += 1;
                b.social_skill_rolls += 1;
            }
        }
    }

    fn evolutionary_additional_skills(&self, rng: &mut ChaCha8Rng, b: &mut Builder) {
        let roll = (roll_xdy(rng, 1, 6) as i8 + b.evolution_mod as i8 + b.roll_mod).min(7);
        match roll {
            ..=1 => { b.social_skill_rolls += 1; },
            2 => { b.social_skill_rolls += 1; },
            3 => { b.social_skill_rolls += 1; b.evolution_skill_rolls += 1; },
            4 => { b.social_skill_rolls += 1; b.evolution_skill_rolls += 1; },
            5 => { b.physical_skill_rolls += 1; b.evolution_skill_rolls += 1; },
            6 => { b.social_skill_rolls += 1; b.physical_skill_rolls += 1; b.evolution_skill_rolls += 1; },
            7 => { b.social_skill_rolls += 2; b.physical_skill_rolls += 1; b.evolution_skill_rolls += 1; },
            _ => unreachable!("evolutionary_additional_skills called for {roll:?}")
        }
    }

    fn extra_exotics(&self) -> &'static [WeaponExotic] { &[WeaponExotic::Stench] }

    fn evolutionary_other_benefits(&self, rng: &mut ChaCha8Rng, b: &mut Builder) {
        let roll = (roll_xdy(rng, 1, 6) as i8 + b.evolution_mod as i8 + b.roll_mod).min(7);
        match roll {
            ..=1 => { b.instinct += 2 },
            2 => { b.pack += 2 },
            3 => { b.intelligence += 1 },
            4 => { b.dexterity += roll_xdy(rng, 1, 6) as i8 },
            5 => { b.endurance += roll_xdy(rng, 1, 6) as i8 },
            6 => { b.quirk_rolls += 2 },
            7 => { b.evolution_other_benefits_rolls += 2 },
            _ => unreachable!("evolutionary_other_benefits called for {roll:?}")
        }
    }

    fn evolution_skill(&self, rng: &mut ChaCha8Rng, b: &mut Builder) {
        let roll = roll_xdy(rng, 1, 6) as i8 + b.roll_mod;
        match roll {
            ..=1 => b.damage_dice += 1,
            2 => b.armor += 1,
            3 => b.intelligence += 1,
            4 => b.physical_skill_rolls += 1,
            5 => b.social_skill_rolls += 1,
            6 => b.exotic_weapon_rolls += 1,
            _ => unreachable!("evolution_skill called for {roll:?}")
        }
    }

    fn social_skill(&self, rng: &mut ChaCha8Rng, b: &mut Builder) {
        let roll = roll_xdy(rng, 1, 6) as i8 + b.roll_mod;
        match roll {
            ..=1 => b.pack += 4,
            2 => b.instinct += 1,
            3 => b.skill(Skill::Deception).raise(),
            4 => b.instinct += 1,
            5 => b.skill(Skill::Deception).raise(),
            6 => b.skill(Skill::Recon).raise(),
            _ => unreachable!("social_skill called for {roll:?}")
        }
    }

    fn physical_skill(&self, rng: &mut ChaCha8Rng, b: &mut Builder) {
        let roll = roll_xdy(rng, 1, 6) as i8 + b.roll_mod;
        match roll {
            ..=1 => b.dexterity += 1,
            2 => b.strength += 2,
            3 => b.endurance += 1,
            4 => b.endurance += 2,
            5 => b.dexterity += roll_xdy(rng, 1, 6) as i8,
            6 => b.skill(Skill::Melee).raise(),
            _ => unreachable!("physical_skill called for {roll:?}")
        }
    }

    fn quirk_for(&self, roll: u8) -> AnimalQuirk {
        AnimalQuirk::Amphibian(Quirk::from_roll(roll).expect("quirk rolls are 2..=11"))
    }

    fn behavior(&self, rng: &mut ChaCha8Rng, b: &mut Builder) -> (Behavior, i8) {
        let roll = roll_xdy(rng, 1, 6);
        match b.diet {
            Diet::Carnivore => {
                match roll {
                    1 => { (Behavior::Pouncer, -1) },
                    2 => { (Behavior::Trapper, -2) },
                    3 => { (Behavior::Hunter, -2) },
                    4 => { (Behavior::Hunter, -1) },
                    5 => { (Behavior::Hunter, 0) },
                    6 => { (Behavior::Chaser, -2) },
                    _ => unreachable!("behavior called for {roll:?}")
                }
            },
            Diet::Herbivore => {
                match roll {
                    1 => { (Behavior::Filter, -1) },
                    2 => { (Behavior::Filter, 0) },
                    3 => { (Behavior::Intermittent, -2) },
                    4 => { (Behavior::Intermittent, -1) },
                    5 => { (Behavior::Intermittent, 0) },
                    6 => { (Behavior::Grazer, -2) },
                    _ => unreachable!("behavior called for {roll:?}")
                }
            },
            Diet::Omnivore => {
                match roll {
                    1 => { (Behavior::CarrionEater, -1) },
                    2 => { (Behavior::Gatherer, -1) },
                    3 => { (Behavior::Eater, -1) },
                    4 => { (Behavior::Hunter, 0) },
                    5 => { (Behavior::Intermittent, -1) },
                    6 => { (Behavior::Reducer, -2) },
                    _ => unreachable!("behavior called for {roll:?}")
                }
            },
        }
    }
}

use crate::animal::{set_movement, terrain_base_size, Builder, Movement};
use crate::dice_roller::roll_xdy;
use rand_chacha::ChaCha8Rng;

pub(crate) struct Rules;

/// Fungal override for `ClassRules::size_and_movement`: fungals ignore the
/// terrain chart's movement rows (and their size DMs), keeping only the
/// terrain's base size DM. 1-4 Immobile, 5 Walk, 6 Fly.
#[allow(dead_code)] // Called from fungal::Rules once it implements ClassRules.
pub(super) fn size_and_movement(rng: &mut ChaCha8Rng, b: &mut Builder) {
    let movement = match roll_xdy(rng, 1, 6) {
        1..=4 => Movement::Immobile,
        5 => Movement::Walk,
        _ => Movement::Fly
    };
    set_movement(rng, b, movement);
    b.size += terrain_base_size(b.terrain);
}

use rand::{Rng, RngExt};

pub fn roll_xdy<R: Rng>(rng: &mut R, number_to_roll: u8, die_sides: u8) -> u8 {
    let mut total: u8 = 0;
    for _ in 0..number_to_roll {
        total += rng.random_range(1..=die_sides);
    }
    total
}
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::io;
use rand::RngExt;
use rand_chacha::ChaCha8Rng;

// Uniformly pick one element from a set. None if the set is empty
// (or absent, handled at the call site). Sets aren't indexable, so we
// walk to the nth element — in sorted order, which is what makes it reproducible.
fn pick_random<'a, T>(set: &'a BTreeSet<T>, rng: &mut ChaCha8Rng) -> Option<&'a T> {
    if set.is_empty() {
        return None;
    }
    let idx = rng.random_range(0..set.len());
    set.iter().nth(idx)
}

pub struct NameGenerator {
    double: bool,
    track: bool,
    existing_names: Vec<String>,
    first_grams: BTreeMap<String, BTreeSet<char>>,
    middle_grams: BTreeMap<String, BTreeSet<char>>,
    last_grams: BTreeMap<String, BTreeSet<String>>,
    name_lengths: BTreeMap<usize, u32>,
}

impl NameGenerator {
    pub fn from_file(path: &str, double: bool, track: bool) -> io::Result<NameGenerator> {
        let mut ng = NameGenerator {
            double,
            track,
            existing_names: vec![
                "Terra".to_string(),
                "Luna".to_string(),
                "Terran".to_string(),
            ],
            first_grams: BTreeMap::new(),
            middle_grams: BTreeMap::new(),
            last_grams: BTreeMap::new(),
            name_lengths: BTreeMap::new(),
        };

        let contents = fs::read_to_string(path)?;
        for raw in contents.lines() {
            let name = raw.replace('_', " ");
            let chars: Vec<char> = name.chars().collect();
            let len = chars.len();
            if len < 4 {
                continue; // your Python would have crashed on these; skipping is safer
            }

            // firstGrams: prefixes of length 0..=3 -> the next char
            for letter in 0..4 {
                let lookup: String = chars[..letter].iter().collect();
                ng.first_grams.entry(lookup).or_default().insert(chars[letter]);
            }

            // middleGrams: each trigram -> the char after it
            for letter in 1..len.saturating_sub(5) {
                let lookup: String = chars[letter..letter + 3].iter().collect();
                ng.middle_grams.entry(lookup).or_default().insert(chars[letter + 3]);
            }

            // lastGrams: the 2 chars before the end -> the final 2 chars
            let key: String = chars[len - 4..len - 2].iter().collect();
            let ending: String = chars[len - 2..].iter().collect();
            ng.last_grams.entry(key).or_default().insert(ending);

            *ng.name_lengths.entry(len).or_insert(0) += 1;
        }

        Ok(ng)
    }

    fn get_length(&self, rng: &mut ChaCha8Rng, minlength: usize) -> usize {
        let total: u32 = self
            .name_lengths
            .iter()
            .filter(|&(&length, _)| length >= minlength)
            .map(|(_, &cnt)| cnt)
            .sum();

        let selection = rng.random_range(0..total);
        let mut cumulative = 0u32;
        for (&length, &cnt) in &self.name_lengths {
            if length >= minlength {
                cumulative += cnt;
                if cumulative > selection {
                    return length;
                }
            }
        }
        unreachable!("cumulative always exceeds selection when total > 0")
    }

    fn try_build(&self, rng: &mut ChaCha8Rng, length: usize) -> Option<String> {
        let mut name: Vec<char> = Vec::new();
        for letter in 0..length.saturating_sub(2) {
            let next = if letter < 4 {
                let key: String = name.iter().collect();
                *pick_random(self.first_grams.get(&key)?, rng)?
            } else {
                let key: String = name[name.len() - 3..].iter().collect();
                *pick_random(self.middle_grams.get(&key)?, rng)?
            };
            name.push(next);
        }
        let key: String = name[name.len() - 2..].iter().collect();
        let ending = pick_random(self.last_grams.get(&key)?, rng)?;
        name.extend(ending.chars());
        Some(name.into_iter().collect())
    }

    fn generate_name_attempt(&self, rng: &mut ChaCha8Rng, minlength: usize) -> String {
        let length = self.get_length(rng, minlength);
        loop {
            if let Some(name) = self.try_build(rng, length) {
                return name;
            }
            // dead end at this length — retry, same length, exactly like the Python
        }
    }

    pub fn generate_name(&mut self, rng: &mut ChaCha8Rng) -> String {
        loop {
            let mut name = self.generate_name_attempt(rng, 0);

            if self.double {
                let maxlen = *self.name_lengths.keys().next_back().unwrap();
                let minlength = maxlen.saturating_sub(name.chars().count());
                let name2 = self.generate_name_attempt(rng, minlength);
                name = if rng.random_bool(0.5) {
                    format!("{name} {name2}")
                } else {
                    format!("{name2} {name}")
                };
            }

            if !self.track {
                return name;
            }
            if !self.existing_names.contains(&name) {
                self.existing_names.push(name.clone());
                return name;
            }
        }
    }
}
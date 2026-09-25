use crate::orbital_body::Planet;
use crate::orbital_body::has_solid_surface;
use crate::temperature::Temperature;
use crate::temperature::ClimateBand;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Terrain {
    BeachShore,
    Clear,
    DeepOcean,
    Desert,
    Forest,
    Hills,
    IceSheet,
    Jungle,
    Mountains,
    OpenOcean,
    Plains,
    Rainforest,
    Riverbank,
    RoughBroken,
    ShallowOcean,
    SwampMarsh,
    Tundra,
    Woods
}

impl Terrain {
    pub const ALL: [Terrain; 18] = [
        Terrain::BeachShore,
        Terrain::Clear,
        Terrain::DeepOcean,
        Terrain::Desert,
        Terrain::Forest,
        Terrain::Hills,
        Terrain::IceSheet,
        Terrain::Jungle,
        Terrain::Mountains,
        Terrain::OpenOcean,
        Terrain::Plains,
        Terrain::Rainforest,
        Terrain::Riverbank,
        Terrain::RoughBroken,
        Terrain::ShallowOcean,
        Terrain::SwampMarsh,
        Terrain::Tundra,
        Terrain::Woods
    ];
}

pub fn terrain_present(planet: &Planet) -> Vec<Terrain> {
    let solid = has_solid_surface(planet.category);
    let land = solid && planet.hydrosphere <= 9;
    let weather = planet.atmosphere >= 2;
    let canopy = planet.atmosphere >= 4;
    let life = planet.biosphere >= 9;
    let temp = planet.temperature();
    let liquid = temp.reaches_liquid();
    let cold = temp.spans(ClimateBand::Cold);
    let temperate = temp.spans(ClimateBand::Temperate);
    let hot = temp.spans(ClimateBand::Hot);
    let frozen = temp.spans(ClimateBand::Frozen);

    Terrain::ALL.into_iter()
    .filter(|t| match t {
        Terrain::BeachShore => land && weather && liquid && planet.hydrosphere >= 2,
        Terrain::Clear | Terrain::Hills | Terrain::Mountains | Terrain::RoughBroken => land,
        Terrain::DeepOcean => planet.subsurface_oceans
            || (weather && liquid && (5..=11).contains(&planet.hydrosphere) && (solid || planet.hydrosphere == 11)),
        Terrain::Desert => land && weather && planet.hydrosphere <= 4,
        Terrain::Forest => life && land && canopy && liquid && planet.hydrosphere >= 3 && (cold || temperate),
        Terrain::IceSheet => solid && (1..=11).contains(&planet.hydrosphere) && frozen,
        Terrain::Jungle => life && land && canopy && liquid && planet.hydrosphere >= 4 && hot,
        Terrain::OpenOcean => planet.subsurface_oceans
        || (weather && liquid && (3..=11).contains(&planet.hydrosphere) && (solid || planet.hydrosphere == 11)),
        Terrain::Plains => life && land && weather && liquid && (2..=7).contains(&planet.hydrosphere) && (temperate || hot),
        Terrain::Rainforest => life && land && canopy && liquid && planet.hydrosphere >= 6 && hot,
        Terrain::Riverbank => land && weather && liquid && planet.hydrosphere >= 3,
        Terrain::ShallowOcean => solid && ((weather && liquid && (2..=10).contains(&planet.hydrosphere))
            || (planet.subsurface_oceans && planet.hydrosphere <= 10)),
        Terrain::SwampMarsh => life && land && weather && liquid && planet.hydrosphere >= 4 && (cold || temperate || hot),
        Terrain::Tundra => life && land && weather && liquid && planet.hydrosphere >= 1 && cold,
        Terrain::Woods => life && land && weather && liquid && planet.hydrosphere >= 2 && (cold || temperate || hot)
    })
    .collect()
}
use crate::orbital_body::Category;

pub fn describe(category: Category) -> &'static str {
    match category {
        Category::Acheronian => { "These are worlds that were directly affected by their primary's transition from the main sequence; the atmosphere and oceans have been boiled away, leaving a scorched, dead planet." },
        Category::Arean => { "These are worlds with little liquid, that move through a slow geological cycle of a gradual build-up, a short wet and clement period, and a long decline." },
        Category::Arid => { "These are worlds with limited amounts of surface liquid, that maintain an equilibrium with the help of their tectonic activity and their biosphere." },
        Category::Asphodelian => { "These are worlds that were directly affected by their primary's transition from the main sequence; their atmosphere has been boiled away, leaving the surface exposed." },
        Category::Chthonian => { "These are worlds that were directly affected by their primary's transition from the main sequence, or that have simply spent too long in a tight epistellar orbit; their atmospheres have been stripped away." },
        Category::Hebean => { "These are highly active worlds, due to tidal flexing, but with some regions of stability; the larger ones may be able to maintain some atmosphere and surface liquid." },
        Category::Helian => { "These are typical helian or subgiant worlds - large enough to retain helium atmospheres." },
        Category::JaniLithic => { "These worlds, tide-locked to the primary, are rocky, dry, and geologically active." },
        Category::Jovian => { "These are huge worlds with helium-hydrogen envelopes and compressed cores; the largest emit more heat than they absorb." },
        Category::Meltball => { "These are dwarfs with molten or semi-molten surfaces, either from extreme tidal flexing, or extreme approach to a star." },
        Category::Oceanic => { "These are worlds with a continuous hydrological cycle and deep oceans, due to either dense greenhouse atmosphere or active plate tectonics." },
        Category::Panthalassic => { "These are massive worlds, aborted gas giants, largely composed of water and hydrogen." },
        Category::Promethean => { "These are worlds that, through tidal-flexing, have a geological cycle similar to plate tectonics, that supports surface liquid and atmosphere." },
        Category::Rockball => { "These are mostly dormant worlds, with surfaces largely unchanged since the early period of planetary formation." },
        Category::Snowball => { "These worlds are composed of mostly ice and some rock. They may have varying degrees of activity, ranging from completely cold and still to cryo-volcanically active with extensive subsurface oceans." },
        Category::Stygian => { "These are worlds that were directly affected by their primary's transition from the main sequence; they are melted and blasted lumps." },
        Category::Tectonic => { "These are worlds with active plate tectonics and large bodies of surface liquid, allowing for stable atmospheres and a high likelihood of life." },
        Category::Telluric => { "These are worlds with geoactivity but no hydrological cycle at all, leading to dense runaway-greenhouse atmospheres." },
        Category::Vesperian => { "These worlds are tide-locked to their primary, but at a distance that permits surface liquid and the development of life." },
        Category::AsteroidBelt => { "" }
    }
}
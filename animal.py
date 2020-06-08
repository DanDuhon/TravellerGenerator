from diceroller import roll_xdy
import namegenerator

allAnimals = []

behaviorDescriptions = {"Carrion-Eater": "Scavengers that eat the prey and leavings of other animals. Carrion-Eaters are usually quite resilient to disease and often carry it in their flesh, transmitting contagion in their attacks on other creatures. Often small and almost always voracious, these scavengers should never be underestimated. Terran Examples: Vultures, Jackals, Crows",
                        "Chaser": "Typically predators, these animals chase down and overbear prey to survive. Chasers are seldom as large as the prey they hunt, often working in packs to bring down much larger and stronger animals. When Chasers are larger than their prey, they tend to stalk herds of animals, using brute force to down several at once. Both sorts of Chaser have a tendency to gorge on its meals, feasting when it can in preparation for famine later. Terran Examples: Wolves, Cheetahs, Falcons",
                        "Eater": "Voracious animals that will consume anything in their path, Eaters can be extremely dangerous to encounter because any such meeting is an opportunity for the animals to feed. Eaters usually have very high metabolisms, requiring them to eat far more often than other animals of their size and class. Terran Examples: Army Ants, Piranhas, Locusts",
                        "Filter": "These animals pass their environment through themselves as they move, feeding from absorbed nutrients. The most common forms of Filters are burrowers and swimmers, creatures that move through environments rich in minerals and suspended nutrients. Filters are very rarely hostile in any capacity, fighting only to defend themselves and then only infrequently. Terran Examples: Earthworms, Sponges, Whales",
                        "Gatherer": "Usually omnivores, these animals collect sustenance and hide it within their habitats for later consumption. Gatherers are often very intelligent creatures, having developed this method of behaviour as a survival trait to overcome diminishing food supplies or inefficiencies in their own digestive systems. Gatherers are not commonly hostile but can be provoked if their food stockpiles are threatened. Terran Examples: Squirrels, Chimpanzees, Leafcutter Ants",
                        "Grazer": "Almost always herbivores, these animals feed off growth in their terrain across very large territories. Grazers typically form large herds and travel constantly to maintain themselves and their food supply. In a healthy environment, the ecosystem is in balance with its Grazers. They feed and grow while simultaneously keeping vegetation in their territory from becoming rampant. Terran Examples: Antelope, Bison, Horses",
                        "Hijacker": "These animals seize and steal the sustenance of other, weaker animals. They use force or cunning to clear a kill, usually preferring fresh meat, and then either glut on the carcass where it lies or pull it a safe distance away before doing so. Hijackers develop from species suited to fight or outwit other predators but not their chosen prey. This forces them to adapt to a behaviour of interfering with other hunts for their own gain. Terran Examples: Lions, Bears, Harrier Hawks",
                        "Hunter": "Hunters stalk and kill their prey, tending toward easily killed animals in quantity over harder, larger kills. They are by definition at least primarily carnivores but do occasionally include omnivores able to supplement their diets through either need or capability. Hunters prefer speed over strength and can maintain a hunt for very long periods of time, striking only when the odds are in their favour. Terran Examples: Baboons, Tigers, Gar",
                        "Intermittent": "These animals are typically peaceful herbivores and spend most of their time wandering their territories caring for their families. Intermittent animals are pack-oriented and often slow moving, unhurried and large enough not to be concerned by predators except on rare occasions. Intermittent animals always have some method of driving off attack; this is why they do not fear predation. Terran Examples: Elephants, Brontosaurs",
                        "Intimidator": "Using guile and fear, these creatures dominate their territories without direct force. Much like Hijackers, Intimidators steal kills but their dominant behaviour goes far deeper. Intimidators maintain control over their habitats at all times, not just while they feed. Intimidators rule their territory, driving out rivals and subjugating other species as they can. Terran Examples: Coyotes, Wasps, Jays",
                        "Killer": "Aggressive at all times and physically capable of great violence, these creatures are a danger to any in their path. Killer animals are similar to Eaters but are not as constant in their attacks. Killers usually stake out a small territory and ruthlessly patrol it, fighting anything it comes in contact with and devouring whatever it kills. Killers have, on average, small family units and rarely shelter their young. Terran Examples: Sharks, Badgers, Vipers",
                        "Pouncer": "Deadly by design, these creatures ambush their meals. Usually hunting through speed and stealth, Pouncers are not built to fight for long periods of time and will often break off attack if their first strikes do not result in a kill or significant damage. Pouncers are usually swift, cautious and only attack if it seems apparent that they will be victorious. Terran Examples: Panthers, Asps, Wolf Spiders",
                        "Reducer": "Opportunistic omnivores, these animals feed on the waste from all other forms of life. Also called vermin or ‘bottom feeders’, Reducers are a vital part of the food chain. They ensure that nothing is lost during the hunting process of other animals. Reducers differ from Carrion-Eaters in that they rarely wait for meals and often begin eating as soon as sustenance becomes available. Some Reducers are parasitic in nature, feeding from living hosts instead of waste products. Terran Examples: Rats, Scarab Beetles, Remoras",
                        "Siren": "Creatures like these often remain stationary for long periods of time. They bring their prey to them through some kind of lure or attractive bait. Some use pheromones and other chemicals while others hide in trafficked areas or seem completely harmless until they strike. Siren creatures can be extremely insidious, remaining motionless and inoffensive until their prey is so far gone that there is no chance of escape. Terran Examples: Anglerfish, Trapdoor Spiders, Venus Flytraps",
                        "Trapper": "Animals of this nature imprison and immobilise prey, generally by surprise. Trappers differ from Sirens in that they rarely use a lure or convenient placement and instead just subsist on whatever they catch over long periods of time. Trappers are patient animals and, like Sirens, often remain in one place and let their prey come to them. When possible, Trappers blend into their surroundings and can be quite difficult to find. Terran Examples: Web-weaving Spiders, Ant Lions, Octopi"}


class Animal():
    """
    Defines an animal.

    Parameters:
        planet: Class instance
            The planet object the animal lives on. Valid classes are
            DwarfPlanet, TerrestrialPlanet, HelianPlanet.
        terrain: String
            The type of terrain that this animal calls home.
    """

    def __init__(self, planet, terrain):
        allAnimals.append(self)
        self.name = None#namegenerator.animalNGrams.generate_name()
        self.planet = planet
        self.terrain = terrain
        self.animalClass = None
        self.diet = None
        self.strength = 0
        self.dexterity = 0
        self.endurance = 0
        self.instinct = roll_xdy(2, 6)
        self.pack = roll_xdy(2, 6)
        if roll_xdy(1, 6) >= 5:
            self.intelligence = 1
        else:
            self.intelligence = 0
        self.size = 0
        self.sizeRoll = roll_xdy(2, 6)
        self.sizeRollModifier = 0
        self.armor = 0
        self.athletics = -3
        self.deception = -3
        self.meleeNaturalWeapons = -3
        self.persuade = -3
        self.recon = -3
        self.stealth = -3
        self.survival = -3
        self.exoticWeapons = set()
        self.quirks = []
        self.behaviors = set()
        self.reactionModifier = 0
        self.weapons = set()
        self.weaponDice = 0
        self.weaponDamageModifier = 0
        self.initiative = 0

        # The type of terrain the animal lives in helps determine how
        # large the animal is.
        if terrain == "Desert":
            self.sizeRollModifier -= 3
        elif terrain == "Forest":
            self.sizeRollModifier -= 4
        elif terrain == "Woods":
            self.sizeRollModifier -= 1
        elif terrain == "Jungle":
            self.sizeRollModifier -= 3
        elif terrain == "Rainforest":
            self.sizeRollModifier -= 2
        elif terrain == "Rough/Broken":
            self.sizeRollModifier -= 3
        elif terrain == "Swamp/Marsh":
            self.sizeRollModifier += 4
        elif terrain == "Beach/Shore":
            self.sizeRollModifier += 2
        elif terrain == "Riverbank":
            self.sizeRollModifier += 1
        elif terrain == "Shallow Ocean":
            self.sizeRollModifier += 1
        elif terrain == "Open Ocean":
            self.sizeRollModifier -= 4
        elif terrain == "Deep Ocean":
            self.sizeRollModifier += 2

        # The type of terrain also helps determine the type of movement
        # favored by the animal. This may be overridden by the child class.
        self.primaryMovement = None
        roll = roll_xdy(1, 6)
        burrowRoll = roll_xdy(2, 6)
        if terrain == "Clear":
            if roll <= 5:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Plains":
            if roll <= 5:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Desert":
            if roll <= 4:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Hills":
            if roll <= 4:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Mountains":
            if roll <= 3:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Forest":
            if roll <= 4:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Woods":
            if roll <= 5:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Jungle":
            if roll <= 5:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Rainforest":
            if roll <= 5:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Rough/Broken":
            if roll <= 4:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Swamp/Marsh":
            if roll <= 2:
                self.primaryMovement = "Swim"
            elif roll <= 4:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Beach/Shore":
            if roll <= 2:
                self.primaryMovement = "Swim"
            elif roll <= 4:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Riverbank":
            if roll <= 2:
                self.primaryMovement = "Swim"
            elif roll <= 5:
                self.primaryMovement = "Walk"
            else:
                if burrowRoll >= 10:
                    self.primaryMovement = "Burrow"
                    self.stealth += 1
                    self.instinct += 2
                else:
                    self.primaryMovement = "Fly"
        elif terrain == "Shallow Ocean":
            if roll <= 4:
                self.primaryMovmement = "Swim"
            else:
                self.primaryMovement = "Fly"
        elif terrain == "Open Ocean":
            if roll <= 4:
                self.primaryMovmement = "Swim"
            else:
                self.primaryMovement = "Fly"
        elif terrain == "Deep Ocean":
            self.primaryMovmement = "Swim"

    def raise_skill_level(self, skill, points):
        """
        Raises the skill level of the given skill by one rank.
        Skills start at -3. When the skill is raised, it goes from
        -3 to 0. After that, it goes up in increments of 1.

        Parameters:
            skill: String
                The name of the skill to be raised.
            points: Integer
                The number of ranks by which to raise the skill.
        """
        while points > 0:
            if getattr(self, skill) == -3:
                setattr(self, skill, 0)
            else:
                setattr(self, skill, getattr(self, skill) + 1)
            points -= 1

    def behavior_effects(self):
        """
        Modifies certain attributes of an animal based on the behaviors
        that animal exhibits.
        """
        for behavior in self.behaviors:
            if behavior == "Carrion-Eater":
                self.instinct += 2
                self.sizeRollModifier -= 2
            elif behavior == "Chaser":
                self.dexterity += 4
                self.instinct += 2
                self.pack += 2
            elif behavior == "Eater":
                self.endurance += 4
                self.pack += 4
            elif behavior == "Filter":
                self.endurance += 4
                if self.pack - 2 < 0:
                    self.pack = 0
                else:
                    self.pack -= 2
            elif behavior == "Gatherer":
                self.stealth += 1
                self.pack += 2
                self.instinct += 1
            elif behavior == "Grazer":
                self.instinct += 2
                self.pack += 4
            elif behavior == "Hunter":
                self.instinct += 2
                self.survival += 1
                self.recon += 1
            elif behavior == "Hijacker":
                self.strength += 2
                self.pack += 2
            elif behavior == "Intimidator":
                self.instinct += 1
                self.persuade += 1
            elif behavior == "Killer":
                self.meleeNaturalWeapons += 1
                self.instinct += 4
                if self.pack - 2 < 0:
                    self.pack = 0
                else:
                    self.pack -= 2
                if roll_xdy(1, 6) <= 3:
                    self.strength += 4
                else:
                    self.dexterity += 4
            elif behavior == "Intermittent":
                self.survival += 1
                self.pack += 4
                self.sizeRollModifier += 2
            elif behavior == "Pouncer":
                self.stealth += 1
                self.recon += 1
                self.athletics += 1
                self.dexterity += 2
                self.instinct += 2
            elif behavior == "Reducer":
                self.endurance += 2
                self.pack += 4
            elif behavior == "Siren":
                self.deception += 1
                if self.pack - 4 < 0:
                    self.pack = 0
                else:
                    self.pack -= 4
            elif behavior == "Trapper":
                self.stealth += 1
                self.endurance += 1
                if self.pack - 2 < 0:
                    self.pack = 0
                else:
                    self.pack -= 2

    def set_size(self, sizeRoll, sizeRollModifier):
        """
        Sets the weight of the animal based on 2d6 and any modifiers
        to that dice roll.

        Parameters:
            sizeRoll: Integer
                The result of a 2d6 roll.
            sizeRollModifier: Integer
                The sum of all roll modifiers to the size roll.
        """
        self.size = self.sizeRoll + self.sizeRollModifier
        if self.size <= 1:
            self.weight = "1 kg"
        elif self.size == 2:
            self.weight = "3 kg"
        elif self.size == 3:
            self.weight = "6 kg"
        elif self.size == 4:
            self.weight = "12 kg"
        elif self.size == 5:
            self.weight = "25 kg"
        elif self.size == 6:
            self.weight = "50 kg"
        elif self.size == 7:
            self.weight = "100 kg"
        elif self.size == 8:
            self.weight = "200 kg"
        elif self.size == 9:
            self.weight = "400 kg"
        elif self.size == 10:
            self.weight = "800 kg"
        elif self.size == 11:
            self.weight = "1,600 kg"
        elif self.size == 12:
            self.weight = "3,200 kg"
        elif self.size == 13:
            self.weight = "5,000 kg"
        elif self.size == 14:
            self.weight = "8,000 kg"
        else:  # 15+
            self.weight = "10,000 kg"

    def set_strength(self, sizeRoll):
        """
        Sets the strength of the animal based on the size roll
        and any strength modifiers the animal has already gotten.

        Parameters:
            sizeRoll: Integer
                The result of the 2d6 roll for size.
        """
        if self.sizeRoll <= 1:
            self.strength += 1
        elif self.sizeRoll == 2:
            self.strength += 2
        elif self.sizeRoll == 3:
            self.strength += roll_xdy(1, 6)
        elif self.sizeRoll == 4:
            self.strength += roll_xdy(1, 6)
        elif self.sizeRoll == 5:
            self.strength += roll_xdy(2, 6)
        elif self.sizeRoll == 6:
            self.strength += roll_xdy(2, 6)
        elif self.sizeRoll == 7:
            self.strength += roll_xdy(3, 6)
        elif self.sizeRoll == 8:
            self.strength += roll_xdy(3, 6)
        elif self.sizeRoll == 9:
            self.strength += roll_xdy(4, 6)
        elif self.sizeRoll == 10:
            self.strength += roll_xdy(4, 6)
        elif self.sizeRoll == 11:
            self.strength += roll_xdy(5, 6)
        elif self.sizeRoll == 12:
            self.strength += roll_xdy(6, 6)
        elif self.sizeRoll == 13:
            self.strength += roll_xdy(7, 6)
        elif self.sizeRoll == 14:
            self.strength += roll_xdy(8, 6)
        else:  # 15+
            self.strength += roll_xdy(9, 6)

    def set_endurance(self, sizeRoll):
        """
        Sets the endurance of the animal based on the size roll
        and any endurance modifiers the animal has already gotten.

        Parameters:
            sizeRoll: Integer
                The result of the 2d6 roll for size.
        """
        if self.sizeRoll <= 1:
            self.endurance += 1
        elif self.sizeRoll == 2:
            self.endurance += 2
        elif self.sizeRoll == 3:
            self.endurance += roll_xdy(1, 6)
        elif self.sizeRoll == 4:
            self.endurance += roll_xdy(1, 6)
        elif self.sizeRoll == 5:
            self.endurance += roll_xdy(2, 6)
        elif self.sizeRoll == 6:
            self.endurance += roll_xdy(2, 6)
        elif self.sizeRoll == 7:
            self.endurance += roll_xdy(3, 6)
        elif self.sizeRoll == 8:
            self.endurance += roll_xdy(3, 6)
        elif self.sizeRoll == 9:
            self.endurance += roll_xdy(4, 6)
        elif self.sizeRoll == 10:
            self.endurance += roll_xdy(4, 6)
        elif self.sizeRoll == 11:
            self.endurance += roll_xdy(5, 6)
        elif self.sizeRoll == 12:
            self.endurance += roll_xdy(6, 6)
        elif self.sizeRoll == 13:
            self.endurance += roll_xdy(7, 6)
        elif self.sizeRoll == 14:
            self.endurance += roll_xdy(8, 6)
        else:  # 15+
            self.endurance += roll_xdy(9, 6)

    def set_dexterity(self, sizeRoll):
        """
        Sets the dexterity of the animal based on the size roll
        and any dexterity modifiers the animal has already gotten.

        Parameters:
            sizeRoll: Integer
                The result of the 2d6 roll for size.
        """
        if self.sizeRoll <= 1:
            self.dexterity += roll_xdy(1, 6)
        elif self.sizeRoll == 2:
            self.dexterity += roll_xdy(1, 6)
        elif self.sizeRoll == 3:
            self.dexterity += roll_xdy(2, 6)
        elif self.sizeRoll == 4:
            self.dexterity += roll_xdy(2, 6)
        elif self.sizeRoll == 5:
            self.dexterity += roll_xdy(3, 6)
        elif self.sizeRoll == 6:
            self.dexterity += roll_xdy(4, 6)
        elif self.sizeRoll == 7:
            self.dexterity += roll_xdy(3, 6)
        elif self.sizeRoll == 8:
            self.dexterity += roll_xdy(3, 6)
        elif self.sizeRoll == 9:
            self.dexterity += roll_xdy(2, 6)
        elif self.sizeRoll == 10:
            self.dexterity += roll_xdy(2, 6)
        elif self.sizeRoll == 11:
            self.dexterity += roll_xdy(2, 6)
        elif self.sizeRoll == 12:
            self.dexterity += roll_xdy(1, 6)
        elif self.sizeRoll == 13:
            self.dexterity += roll_xdy(1, 6)
        elif self.sizeRoll == 14:
            self.dexterity += 2
        else:  # 15+
            self.dexterity += 1

    def set_exotic_weapons(self, exoticWeaponRolls):
        """
        Gives the animal up to one exotic weapon per roll.

        Parameters:
            exoticWeaponRolls: Integer
                The number of rolls for exotic weapons to make.
        """
        if exoticWeaponRolls >= 6:
            self.exoticWeapons = set(
                ["Diseased", "Poison", "Bleed", "Bioelectric", "Concealing Mist", "Ranged"])
            exoticWeaponRolls = 0

        if exoticWeaponRolls > 0 and "Carrion-Eater" in self.behaviors:
            self.exoticWeapons.add("Diseased")

        while exoticWeaponRolls > len(self.exoticWeapons):
            roll = roll_xdy(1, 6)
            if roll == 1:
                self.exoticWeapons.add("Diseased")
            elif roll == 2:
                self.exoticWeapons.add("Poison")
            elif roll == 3:
                self.exoticWeapons.add("Bleed")
            elif roll == 4:
                self.exoticWeapons.add("Bioelectric")
            elif roll == 5:
                self.exoticWeapons.add("Concealing Mist")
            else:
                self.exoticWeapons.add("Ranged")

    def set_weapon_and_damage_modifier(self):
        """
        Sets both the type of natural weapon this animal possesses and
        the damage modifier for damage rolls.
        Animals with a meleeNaturalWeapons skill of -3 that ends up with
        a weapon from this method will have that skill raised to 0.
        """
        roll = roll_xdy(2, 6)
        if len(self.exoticWeapons) == 0:
            if self.diet == "Carnivore":
                roll += 8
            elif self.diet == "Herbivore":
                roll -= 6
            elif self.diet == "Omnivore":
                roll += 4

        if (self.meleeNaturalWeapons == -3 and
                (roll >= 2 or len(self.exoticWeapons) > 0)):
            self.meleeNaturalWeapons = 0

        if 7 <= roll <= 9:
            self.weaponDamageModifier += 1
        elif 10 <= roll <= 17:
            self.weaponDamageModifier += 2
        elif roll >= 18:
            self.weaponDamageModifier += 3

        if roll == 2 or (roll < 2 and len(self.exoticWeapons) > 0):
            roll2 = roll_xdy(1, 3)
            if roll2 == 1:
                self.weapons.add("Teeth")
            elif roll2 == 2:
                self.weapons.add("Mandibles")
            else:
                self.weapons.add("Suckers")
        elif roll == 3:
            roll2 = roll_xdy(1, 4)
            if roll2 == 1:
                self.weapons.add("Horns")
            elif roll2 == 2:
                self.weapons.add("Antlers")
            elif roll2 == 3:
                self.weapons.add("Beak")
            else:
                self.weapons.add("Headbutt")
        elif roll == 4:
            roll2 = roll_xdy(1, 6)
            if roll2 == 1:
                self.weapons.add("Hooves")
            if roll2 == 2:
                self.weapons.add("Stomp")
            if roll2 == 3:
                self.weapons.add("Body Slam")
            if roll2 == 4:
                self.weapons.add("Thrasher")
            if roll2 == 5:
                self.weapons.add("Constriction")
            else:
                self.weapons.add("Trample")
        elif roll == 5:
            roll2 = roll_xdy(1, 8)
            if roll2 == 1:
                self.weapons.add("Hooves")
            if roll2 == 2:
                self.weapons.add("Stomp")
            if roll2 == 3:
                self.weapons.add("Body Slam")
            if roll2 == 4:
                self.weapons.add("Thrasher")
            if roll2 == 5:
                self.weapons.add("Constriction")
            if roll2 == 6:
                self.weapons.add("Trample and Teeth")
            if roll2 == 7:
                self.weapons.add("Mandibles")
            else:
                self.weapons.add("Suckers")
        elif roll == 6:
            roll2 = roll_xdy(1, 3)
            if roll2 == 1:
                self.weapons.add("Teeth")
            if roll2 == 2:
                self.weapons.add("Mandibles")
            else:
                self.weapons.add("Suckers")
        elif roll == 7:
            roll2 = roll_xdy(1, 4)
            if roll2 == 1:
                self.weapons.add("Claws")
            if roll2 == 2:
                self.weapons.add("Fins")
            if roll2 == 3:
                self.weapons.add("Sharp Scales")
            else:
                self.weapons.add("Talons")
        elif roll == 8:
            roll2 = roll_xdy(1, 2)
            if roll2 == 1:
                self.weapons.add("Stinger")
            else:
                self.weapons.add("Darting Tongue")
        elif roll == 9:
            roll2 = roll_xdy(1, 3)
            if roll2 == 1:
                self.weapons.add("Thrasher")
            if roll2 == 2:
                self.weapons.add("Constriction")
            else:
                self.weapons.add("Trample")
        elif roll == 10:
            roll2 = roll_xdy(1, 6)
            if roll2 == 1:
                self.weapons.add("Claws")
            if roll2 == 2:
                self.weapons.add("Fins")
            if roll2 == 3:
                self.weapons.add("Sharp Scales")
            if roll2 == 4:
                self.weapons.add("Talons and Teeth")
            if roll2 == 5:
                self.weapons.add("Mandibles")
            else:
                self.weapons.add("Suckers")
        elif roll == 11:
            roll2 = roll_xdy(1, 4)
            if roll2 == 1:
                self.weapons.add("Claws")
            if roll2 == 2:
                self.weapons.add("Fins")
            if roll2 == 3:
                self.weapons.add("Sharp Scales")
            else:
                self.weapons.add("Talons")
        elif roll == 12:
            roll2 = roll_xdy(1, 3)
            if roll2 == 1:
                self.weapons.add("Teeth")
            if roll2 == 2:
                self.weapons.add("Mandibles")
            else:
                self.weapons.add("Suckers")
        elif roll == 13:
            roll2 = roll_xdy(1, 3)
            if roll2 == 1:
                self.weapons.add("Thrasher")
            if roll2 == 2:
                self.weapons.add("Constriction")
            else:
                self.weapons.add("Trample")
        elif roll == 14:
            roll2 = roll_xdy(1, 6)
            if roll2 == 1:
                self.weapons.add("Claws")
            if roll2 == 2:
                self.weapons.add("Fins")
            if roll2 == 3:
                self.weapons.add("Sharp Scales")
            if roll2 == 4:
                self.weapons.add("Talons and Teeth")
            if roll2 == 5:
                self.weapons.add("Mandibles")
            else:
                self.weapons.add("Suckers")
        elif roll == 15:
            roll2 = roll_xdy(1, 4)
            if roll2 == 1:
                self.weapons.add("Claws")
            if roll2 == 2:
                self.weapons.add("Fins")
            if roll2 == 3:
                self.weapons.add("Sharp Scales")
            else:
                self.weapons.add("Talons")
        elif roll == 16:
            roll2 = roll_xdy(1, 2)
            if roll2 == 1:
                self.weapons.add("Stinger")
            else:
                self.weapons.add("Darting Tongue")
        elif roll == 17:
            roll2 = roll_xdy(1, 3)
            if roll2 == 1:
                self.weapons.add("Thrasher")
            if roll2 == 2:
                self.weapons.add("Constriction")
            else:
                self.weapons.add("Trample")
        elif roll == 18:
            roll2 = roll_xdy(1, 3)
            if roll2 == 1:
                self.weapons.add("Teeth")
            if roll2 == 2:
                self.weapons.add("Mandibles")
            else:
                self.weapons.add("Suckers")
        elif roll == 19:
            roll2 = roll_xdy(1, 6)
            if roll2 == 1:
                self.weapons.add("Claws")
            if roll2 == 2:
                self.weapons.add("Fins")
            if roll2 == 3:
                self.weapons.add("Sharp Scales")
            if roll2 == 4:
                self.weapons.add("Talons and Teeth")
            if roll2 == 5:
                self.weapons.add("Mandibles")
            else:
                self.weapons.add("Suckers")
        elif roll == 20:
            roll2 = roll_xdy(1, 3)
            if roll2 == 1:
                self.weapons.add("Thrasher")
            if roll2 == 2:
                self.weapons.add("Constriction")
            else:
                self.weapons.add("Trample")
        else:  # 1 or less
            self.weapons.add("None")

    def set_weapon_damage(self):
        """
        Sets the number of dice to be rolled when this animal hits
        with an attack.
        """
        if self.strength <= 10:
            self.weaponDice += 1
        elif self.strength <= 20:
            self.weaponDice += 2
        elif self.strength <= 30:
            self.weaponDice += 3
        elif self.strength <= 40:
            self.weaponDice += 4
        elif self.strength <= 50:
            self.weaponDice += 5
        elif self.strength <= 60:
            self.weaponDice += 6
        else:
            self.weaponDice += 7

    def set_armor(self):
        """
        Sets the armor value for this animal.
        """
        roll = roll_xdy(2, 6)
        if roll <= 3:
            self.armor += 0
        elif roll <= 5:
            self.armor += 1
        elif roll <= 7:
            self.armor += 2
        elif roll <= 9:
            self.armor += 3
        elif roll <= 11:
            self.armor += 4
        elif roll <= 13:
            self.armor += 5
        elif roll <= 15:
            self.armor += 6
        else:
            self.armor += 7

    def set_number_encountered(self):
        """
        Tells the GM how many of these animals are encountered at a time.
        """
        if self.pack == 0:
            self.numberEncountered = "1"
        elif self.pack <= 2:
            self.numberEncountered = "1d3"
        elif self.pack <= 5:
            self.numberEncountered = "1d6"
        elif self.pack <= 8:
            self.numberEncountered = "2d6"
        elif self.pack <= 11:
            self.numberEncountered = "3d6"
        elif self.pack <= 15:
            self.numberEncountered = "4d6"
        else:
            self.numberEncountered = "5d6"

        if self.animalClass == "Insect" and self.pack > 2 and "Acutely self-aware" not in self.quirks:
            if "These insects form veritable swarms." in self.quirks:
                self.numberEncountered += " * 4"
            else:
                self.numberEncountered += " * 3"

    def set_initiative(self):
        """
        Modifies the initiative of the animal based on diet,
        behaviors, and terrain.
        """
        if self.diet == "Carnivore":
            self.initiative += 1
        elif self.diet == "Herbivore":
            self.initiative -= 1

        if "Filter" in self.behaviors:
            self.initiative -= 4

        if "Intermittent" in self.behaviors:
            self.initiative -= 2

        if "Reducer" in self.behaviors:
            self.initiative -= 2

        if "Grazer" in self.behaviors:
            self.initiative -= 1

        if "Carrion-Eater" in self.behaviors:
            self.initiative -= 1

        if "Hunter" in self.behaviors:
            self.initiative += 1

        if "Hijacker" in self.behaviors:
            self.initiative += 1

        if "Eater" in self.behaviors:
            self.initiative += 1

        if "Chaser" in self.behaviors:
            self.initiative += 2

        if "Trapper" in self.behaviors:
            self.initiative += 2

        if "Killer" in self.behaviors:
            self.initiative += 2

        if "Pouncer" in self.behaviors:
            self.initiative += 3

        if self.terrain == "Rainforest":
            self.initiative -= 2
        elif self.terrain == "Deep Ocean":
            self.initiative -= 2
        elif self.terrain == "Forest":
            self.initiative -= 1
        elif self.terrain == "Jungle":
            self.initiative -= 1
        elif self.terrain == "Beach/Shore":
            self.initiative += 1
        elif self.terrain == "Riverbank":
            self.initiative += 1
        elif self.terrain == "Hills":
            self.initiative += 2
        elif self.terrain == "Swamp/Marsh":
            self.initiative += 2
        elif self.terrain == "Shallow Ocean":
            self.initiative += 2
        elif self.terrain == "Clear":
            self.initiative += 3
        elif self.terrain == "Plains":
            self.initiative += 3
        elif self.terrain == "Mountain":
            self.initiative += 3

    def set_reactions(self):
        """
        Sets the thresholds or conditions needed for the animal to
        flee and attack.
        """
        if "Filter" in self.behaviors:
            self.attackTrigger = "10+"
            self.fleeTrigger = "5-"
        elif "Intermittent" in self.behaviors:
            self.attackTrigger = "10+"
            self.fleeTrigger = "4-"
        elif "Grazer" in self.behaviors:
            self.attackTrigger = "8+"
            self.fleeTrigger = "6-"
        elif "Gatherer" in self.behaviors:
            self.attackTrigger = "9+"
            self.fleeTrigger = "7-"
        elif "Hunter" in self.behaviors:
            self.attackTrigger = "If the Hunter is heavier than at least one foe, it attacks on a 6+. Otherwise, it attacks on a 10+."
            self.fleeTrigger = "5-"
        elif "Eater" in self.behaviors:
            self.attackTrigger = "5+"
            self.fleeTrigger = "4-"
        elif "Pouncer" in self.behaviors:
            self.attackTrigger = "If the Pouncer has surprise, it attacks."
            self.fleeTrigger = "If the Pouncer is surprised, it flees. If it cannot flee, it attacks."
        elif "Chaser" in self.behaviors:
            self.attackTrigger = "If the Chasers outnumber the foes, they attack."
            self.fleeTrigger = "5-"
        elif "Trapper" in self.behaviors:
            self.attackTrigger = "If the Trapper has surprise, it attacks."
            self.fleeTrigger = "5-"
        elif "Siren" in self.behaviors:
            self.attackTrigger = "If the Siren has surprise, it attacks."
            self.fleeTrigger = "4-"
        elif "Killer" in self.behaviors:
            self.attackTrigger = "6+"
            self.fleeTrigger = "3-"
        elif "Hijacker" in self.behaviors:
            self.attackTrigger = "7+"
            self.fleeTrigger = "6-"
        elif "Intimidator" in self.behaviors:
            self.attackTrigger = "8+"
            self.fleeTrigger = "7-"
        elif "Carrion-Eater" in self.behaviors:
            self.attackTrigger = "11+"
            self.fleeTrigger = "7-"
        elif "Reducer" in self.behaviors:
            self.attackTrigger = "10+"
            self.fleeTrigger = "7-"


class Amphibian(Animal):
    """
    Defines an amphibian.

    Parameters:
        planet: Class instance
            The planet object the animal lives on. Valid classes are
            DwarfPlanet, TerrestrialPlanet, HelianPlanet.
        terrain: String
            The type of terrain that this animal calls home.
    """

    def __init__(self, planet, terrain):
        super(Amphibian, self).__init__(planet, terrain)
        self.animalClass = "Amphibian"

        # Skills this class innately has.
        self.athletics = 0
        self.recon = 0
        self.survival = 0

        evolutionRollModifier = 0
        physicalSkillRolls = 0
        socialSkillRolls = 0
        evolutionSkillRolls = 0
        quirkRolls = 0
        exoticWeaponRolls = 0

        # Determine the diet and modify attributes.
        dietRoll = roll_xdy(1, 6)
        if dietRoll <= 2:
            self.diet = "Carnivore"
            self.dietDescription = "Carnivorous amphibians usually feed off the young of other amphibious species or smaller aquatic life. Insects may also comprise a large part of their diet."
            self.strength += 1
            self.meleeNaturalWeapons = 0
            evolutionRollModifier += 1
            physicalSkillRolls += 1
        elif dietRoll == 3:
            self.diet = "Herbivore"
            self.dietDescription = "Rare among amphibians, these herbivores are most likely plankton and algae eaters, remaining close to water sources for their nutrition. Larger herbivorous amphibians may be nut and fruit eaters but this is even rarer as their digestive systems are not usually complex enough to handle such a diet."
            self.endurance += 1
            self.instinct += 1
            socialSkillRolls += 1
        else:
            self.diet = "Omnivore"
            self.dietDescription = "Most amphibians are omnivorous, eating in an opportunistic fashion as their environment allows. By design, amphibians are adaptive and therefore make the most of any sustenance in their ecosystem."
            self.pack += 4
            self.instinct += 1
            physicalSkillRolls += 1
            socialSkillRolls += 1

        # Determine how many of each type of skill roll will be made.
        evoRollSkills = roll_xdy(1, 6) + evolutionRollModifier
        socialSkillRolls += 1
        if evoRollSkills == 7:
            socialSkillRolls += 1
        if evoRollSkills >= 3:
            evolutionSkillRolls += 1
        if evoRollSkills >= 5:
            physicalSkillRolls += 1

        # Roll for "other" evolutionary benefits.
        evoOtherRolls = 1
        while evoOtherRolls > 0:
            evoRollOther = roll_xdy(1, 6) + evolutionRollModifier
            if evoRollOther == 1:
                self.instinct += 2
            elif evoRollOther == 2:
                self.pack += 2
            elif evoRollOther == 3:
                self.intelligence += 1
            elif evoRollOther == 4:
                self.dexterity += roll_xdy(1, 6)
            elif evoRollOther == 5:
                self.endurance += roll_xdy(1, 6)
            elif evoRollOther == 6:
                quirkRolls += 2
            else:
                evoOtherRolls += 1
                continue

            evoOtherRolls -= 1

        # Roll for quirks.
        quirk2 = False
        quirk3 = False
        quirk4 = False
        quirk5 = False
        quirk7 = False
        quirk8 = False
        quirk9 = False
        quirk10 = False
        while quirkRolls > len(self.quirks):
            quirkRoll = roll_xdy(2, 6)
            if quirkRoll == 2 and not quirk2:
                quirk2 = True
                self.quirks.append(
                    "Whenever packs of these animals make any noise at all, they all make the exact same sound simultaneously several times in a row.")
            if quirkRoll == 3 and not quirk3:
                quirk3 = True
                self.quirks.append(
                    "Apparently blind, these amphibians have no visible eyes or means of sight.")
                self.recon -= 1
            if quirkRoll == 4 and not quirk4:
                quirk4 = True
                self.quirks.append(
                    "These animals make no sound at all, even when they move in natural surroundings.")
                if self.stealth < 1:
                    self.stealth = 1
            if quirkRoll == 5 and not quirk5:
                quirk5 = True
                self.quirks.append(
                    "The colours of this amphibian’s hide are vivid and clashing, a sort of natural reverse camouflage. Natural predators dislike this display and leave it alone.")
            if quirkRoll == 6:
                self.quirks.append(
                    "Seemingly everywhere, forms of this animal can be found in virtually every habitat type on their world.")
                self.raise_skill_level("survival", 1)
            if quirkRoll == 7 and not quirk7:
                quirk7 = True
                self.quirks.append(
                    "These amphibians emit a natural pheromone that other animals find highly attractive.")
                self.behaviors.add("Siren")
            if quirkRoll == 8 and not quirk8:
                quirk8 = True
                self.quirks.append(
                    "When threatened, these amphibians emit a piercing scream that sounds like a sentient creature in terrible pain.")
            if quirkRoll == 9 and not quirk9:
                quirk9 = True
                self.quirks.append(
                    "On rare occasions, these amphibians swarm viciously.")
            if quirkRoll == 10 and not quirk10:
                quirk10 = True
                self.quirks.append(
                    "The skin of these animals is naturally coated in a thick, foul-smelling emulsion.")
                self.exoticWeapons.add("Stench")
            if quirkRoll == 11:
                self.quirks.append(
                    "Unusually for its kind, these amphibians have developed a rigid shell over their forelimbs and torsos.")
                self.armor += 2
            if quirkRoll == 12:
                quirkRolls += 1

        # Roll for evolutionary skills.
        while evolutionSkillRolls > 0:
            evoSkillRoll = roll_xdy(1, 6)
            if evoSkillRoll == 1:
                self.weaponDice += 1
            elif evoSkillRoll == 2:
                self.armor += 1
            elif evoSkillRoll == 3:
                self.intelligence += 1
            elif evoSkillRoll == 4:
                physicalSkillRolls += 1
            elif evoSkillRoll == 5:
                socialSkillRolls += 1
            else:
                exoticWeaponRolls += 1

            evolutionSkillRolls -= 1

        # Roll for social skills.
        while socialSkillRolls > 0:
            socialSkillRoll = roll_xdy(1, 6)
            if socialSkillRoll == 1:
                self.pack += 4
            elif socialSkillRoll == 2:
                self.instinct += 1
            elif socialSkillRoll == 3:
                self.raise_skill_level("deception", 1)
            elif socialSkillRoll == 4:
                self.instinct += 1
            elif socialSkillRoll == 5:
                self.raise_skill_level("deception", 1)
            else:
                self.raise_skill_level("recon", 1)

            socialSkillRolls -= 1

        # Roll for physical skills.
        while physicalSkillRolls > 0:
            physicalSkillRoll = roll_xdy(1, 6)
            if physicalSkillRoll == 1:
                self.dexterity += 1
            elif physicalSkillRoll == 2:
                self.strength += 2
            elif physicalSkillRoll == 3:
                self.endurance += 1
            elif physicalSkillRoll == 4:
                self.endurance += 2
            elif physicalSkillRoll == 5:
                self.dexterity += roll_xdy(1, 6)
            else:
                self.raise_skill_level("meleeNaturalWeapons", 1)

            physicalSkillRolls -= 1

        # Roll for a behavior.
        behaviorRoll = roll_xdy(1, 6)
        if self.diet == "Carnivore":
            if behaviorRoll == 1:
                self.behaviors.add("Pouncer")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Trapper")
                self.reactionModifier -= 2
            elif behaviorRoll == 3:
                self.behaviors.add("Hunter")
                self.reactionModifier -= 2
            elif behaviorRoll == 4:
                self.behaviors.add("Hunter")
                self.reactionModifier -= 1
            elif behaviorRoll == 5:
                self.behaviors.add("Hunter")
            else:
                self.behaviors.add("Chaser")
                self.reactionModifier -= 2
        elif self.diet == "Herbivore":
            if behaviorRoll == 1:
                self.behaviors.add("Filter")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Filter")
            elif behaviorRoll == 3:
                self.behaviors.add("Intermittent")
                self.reactionModifier -= 2
            elif behaviorRoll == 4:
                self.behaviors.add("Intermittent")
                self.reactionModifier -= 1
            elif behaviorRoll == 5:
                self.behaviors.add("Intermittent")
            else:
                self.behaviors.add("Grazer")
                self.reactionModifier -= 2
        else:
            if behaviorRoll == 1:
                self.behaviors.add("Carrion-Eater")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Gatherer")
                self.reactionModifier -= 1
            elif behaviorRoll == 3:
                self.behaviors.add("Eater")
                self.reactionModifier -= 1
            elif behaviorRoll == 4:
                self.behaviors.add("Hunter")
            elif behaviorRoll == 5:
                self.behaviors.add("Intermittent")
                self.reactionModifier -= 1
            else:
                self.behaviors.add("Reducer")
                self.reactionModifier -= 2

        self.behavior_effects()
        self.set_size(self.sizeRoll, self.sizeRollModifier)
        self.set_strength(self.sizeRoll)
        self.set_endurance(self.sizeRoll)
        self.set_dexterity(self.sizeRoll)
        self.set_exotic_weapons(exoticWeaponRolls)
        self.set_weapon_and_damage_modifier()
        self.set_weapon_damage()
        self.set_armor()
        self.set_number_encountered()
        self.set_initiative()
        self.set_reactions()

        if self.intelligence > 2:
            self.intelligence = 2


class Aquatic(Animal):
    """
    Defines an aquatic.

    Parameters:
        planet: Class instance
            The planet object the animal lives on. Valid classes are
            DwarfPlanet, TerrestrialPlanet, HelianPlanet.
        terrain: String
            The type of terrain that this animal calls home.
    """

    def __init__(self, planet, terrain):
        super(Aquatic, self).__init__(planet, terrain)
        self.animalClass = "Aquatic"

        # Skills this class innately has.
        self.athletics = 0
        self.recon = 0
        self.survival = 0

        self.primaryMovement = "Swim"
        evolutionRollModifier = 0
        physicalSkillRolls = 0
        socialSkillRolls = 0
        evolutionSkillRolls = 0
        evoSkillRollModifier = 0
        quirkRolls = 0
        exoticWeaponRolls = 0

        # Determine the diet and modify attributes.
        dietRoll = roll_xdy(1, 6)
        if dietRoll <= 3:
            self.diet = "Carnivore"
            self.dietDescription = "Carnivorous aquatics usually have large teeth, comparative to their size, and hunt by the scent of blood released into the water. They are very commonly opportunistic feeders, hunting and killing anything they come across."
            self.meleeNaturalWeapons = 0
            self.dexterity += 1
            self.pack += 4
            physicalSkillRolls = 1
        elif dietRoll <= 5:
            self.diet = "Herbivore"
            self.dietDescription = " Like amphibians of this variety, herbivore aquatics typically feast on plankton, water-rotted plants and algae. Larger herbivorous aquatics have the same diet but commonly strain their sustenance from the same medium they breathe."
            self.endurance += roll_xdy(1, 6)
            socialSkillRolls += 1
        else:
            self.diet = "Omnivore"
            self.dietDescription = "Rare among aquatic life, omnivorous water dwellers are almost always scavengers and eat whatever they can find. It is a common adaptation of these life forms to be extremely foul tasting as a result of their diet and they are rarely considered prey by other aquatics."
            self.meleeNaturalWeapons = 0
            self.pack += 2
            self.instinct += 1
            physicalSkillRolls += 1
            socialSkillRolls += 1

        # Determine how many of each type of skill roll will be made.
        evoRollSkills = roll_xdy(1, 6) + evolutionRollModifier
        if evoRollSkills == 1 or 2 <= evoRollSkills <= 3 or evoRollSkills >= 6:
            socialSkillRolls += 1
        if evoRollSkills == 7:
            socialSkillRolls += 1
        if evoRollSkills == 2 or evoRollSkills >= 5:
            physicalSkillRolls += 1
        if evoRollSkills >= 4:
            evolutionSkillRolls += 1

        # Roll for "other" evolutionary benefits.
        evoOtherRolls = 1
        while evoOtherRolls > 0:
            evoRollOther = roll_xdy(1, 6) + evolutionRollModifier
            if evoRollOther == 1:
                self.instinct += 2
            elif evoRollOther == 2:
                self.pack += 2
            elif evoRollOther == 3:
                self.intelligence += 1
            elif evoRollOther == 4:
                self.dexterity += roll_xdy(1, 6)
            elif evoRollOther == 5:
                self.endurance += roll_xdy(1, 6)
            elif evoRollOther == 6:
                quirkRolls += 2
            else:
                evoOtherRolls += 1
                continue

            evoOtherRolls -= 1

        # Roll for quirks.
        quirk2 = False
        quirk3 = False
        quirk4 = False
        quirk5 = False
        quirk7 = False
        quirk9 = False
        quirk10 = 0
        quirk11 = False
        while quirkRolls > len(self.quirks):
            quirkRoll = roll_xdy(2, 6)
            if quirkRoll == 2 and not quirk2:
                self.quirks.append(
                    "This aquatic is found in the darkest parts of its habitat and sees through bioluminescent eyes.")
            if quirkRoll == 3 and not quirk3 and not quirk9:
                quirk3 = True
                self.quirks.append(
                    "This creature is never found alone and will die within 1d6 days of natural causes if it cannot find a pack to join.")
            if quirkRoll == 4 and not quirk4:
                quirk4 = True
                self.quirks.append(
                    "Posseses a frail physique and has the ability to engage in extremely swift movement.")
                self.behaviors.add("Pouncer")
                self.armor = 0
            if quirkRoll == 5 and not quirk5:
                quirk5 = True
                self.quirks.append(
                    "Possessed of a unique biology, this aquatic can survive for 1d6 hours on dry land and can walk in addition to its ability to swim.")
            if quirkRoll == 6:
                self.quirks.append("Unnaturally large for the local ecology.")
                self.sizeRollModifier += 1
            if quirkRoll == 7 and not quirk7:
                quirk7 = True
                self.quirks.append(
                    "Capable of surviving for long periods of time without any nourishment, this aquatic goes dormant for long periods of time, awaking for 3d6 days at a time to feed and breed.")
            if quirkRoll == 8:
                self.quirks.append(
                    "This aquatic breed has volatile genetics and is prone to mutation.")
                evoSkillRollModifier += 1
            if quirkRoll == 9 and not quirk9 and not quirk3:
                quirk9 = True
                self.quirks.append(
                    "Unlike most aquatics, this species reproduces asexually and is never encountered with others of its kind.")
                self.pack = 0
                self.endurance += roll_xdy(1, 6)
            if quirkRoll == 10:
                quirk10 += 1
                self.quirks.append(
                    "Extremely vicious, this animal gains a +1 DM to all Melee (natural weapons) and damage rolls after it or its opponent suffers damage in combat.")
            if quirkRoll == 11 and not quirk11:
                quirk11 = True
                self.quirks.append("Unusually bright and clever.")
            if quirkRoll == 12:
                quirkRolls += 1

        # Roll for evolutionary skills.
        while evolutionSkillRolls > 0:
            evoSkillRoll = roll_xdy(1, 6) + evoSkillRollModifier
            if evoSkillRoll == 1:
                self.weaponDice += 1
            elif evoSkillRoll == 2:
                self.raise_skill_level("meleeNaturalWeapons", 1)
            elif evoSkillRoll == 3:
                self.instinct += 1
            elif evoSkillRoll == 4:
                physicalSkillRolls += 1
            elif evoSkillRoll == 5:
                socialSkillRolls += 1
            else:
                exoticWeaponRolls += 1

            evolutionSkillRolls -= 1

        # Roll for social skills.
        while socialSkillRolls > 0:
            socialSkillRoll = roll_xdy(1, 6)
            if socialSkillRoll == 1:
                self.pack += 2
            elif socialSkillRoll == 2:
                self.instinct += 1
            elif socialSkillRoll == 3:
                self.raise_skill_level("deception", 1)
            elif socialSkillRoll == 4:
                self.instinct += 1
            elif socialSkillRoll == 5:
                self.pack += 5
            else:
                self.raise_skill_level("recon", 1)

            socialSkillRolls -= 1

        # Roll for physical skills.
        while physicalSkillRolls > 0:
            physicalSkillRoll = roll_xdy(1, 6)
            if physicalSkillRoll == 1:
                self.dexterity += 1
            elif physicalSkillRoll == 2:
                self.dexterity += 2
            elif physicalSkillRoll == 3:
                self.endurance += 2
            elif physicalSkillRoll == 4:
                self.endurance += 4
            elif physicalSkillRoll == 5:
                self.dexterity += roll_xdy(1, 6)
            else:
                self.raise_skill_level("meleeNaturalWeapons", 1)

            physicalSkillRolls -= 1

        # Roll for a behavior.
        behaviorRoll = roll_xdy(1, 6)
        if self.diet == "Carnivore":
            if behaviorRoll == 1:
                self.behaviors.add("Eater")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Hunter")
                self.reactionModifier -= 2
            elif behaviorRoll == 3:
                self.behaviors.add("Killer")
                self.reactionModifier -= 1
            elif behaviorRoll == 4:
                self.behaviors.add("Killer")
            elif behaviorRoll == 5:
                self.behaviors.add("Killer")
                self.reactionModifier += 1
            else:
                self.behaviors.add("Chaser")
                self.reactionModifier -= 2
        elif self.diet == "Herbivore":
            if behaviorRoll == 1:
                self.behaviors.add("Filter")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Filter")
            elif behaviorRoll == 3:
                self.behaviors.add("Filter")
                self.reactionModifier += 1
            elif behaviorRoll == 4:
                self.behaviors.add("Intermittent")
                self.reactionModifier -= 1
            elif behaviorRoll == 5:
                self.behaviors.add("Intermittent")
            else:
                self.behaviors.add("Grazer")
                self.reactionModifier -= 2
        else:
            if behaviorRoll == 1:
                self.behaviors.add("Carrion-Eater")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Eater")
                self.reactionModifier -= 1
            elif behaviorRoll == 3:
                self.behaviors.add("Eater")
            elif behaviorRoll == 4:
                self.behaviors.add("Eater")
                self.reactionModifier += 1
            elif behaviorRoll == 5:
                self.behaviors.add("Reducer")
                self.reactionModifier -= 1
            else:
                self.behaviors.add("Reducer")
                self.reactionModifier -= 2

        self.behavior_effects()

        if quirk3 and self.pack < 1:
            self.pack = 1

        self.set_size(self.sizeRoll, self.sizeRollModifier)
        self.set_strength(self.sizeRoll)
        self.set_endurance(self.sizeRoll)
        self.set_dexterity(self.sizeRoll)
        self.set_exotic_weapons(exoticWeaponRolls)
        self.set_weapon_and_damage_modifier()
        self.set_weapon_damage()
        self.set_armor()
        self.set_number_encountered()
        self.set_initiative()
        self.set_reactions()

        if quirk4:
            self.armor = 0
        if quirk9:
            self.pack = 0
        if quirk10 > 0:
            self.quirks = list(
                filter(
                    ("Extremely vicious, this animal gains a +1 DM to all Melee (natural weapons) and damage rolls after it or its opponent suffers damage in combat.").__ne__,
                    self.quirks))
            self.quirks.append(
                "Extremely vicious, this animal gains a +" +
                str(quirk10) +
                " DM to all Melee (natural weapons) and damage rolls after it or its opponent suffers damage in combat.")
        if quirk11:
            if self.instinct < 9:
                self.instinct = 9
            if self.intelligence < 2:
                self.intelligence = 2

        if self.intelligence > 2:
            self.intelligence = 2


class Avian(Animal):
    """
    Defines an avian.

    Parameters:
        planet: Class instance
            The planet object the animal lives on. Valid classes are
            DwarfPlanet, TerrestrialPlanet, HelianPlanet.
        terrain: String
            The type of terrain that this animal calls home.
    """

    def __init__(self, planet, terrain):
        super(Avian, self).__init__(planet, terrain)
        self.animalClass = "Avian"

        # Skills this class innately has.
        self.athletics = 0
        self.recon = 1
        self.survival = 0

        self.primaryMovement = "Fly"
        evolutionRollModifier = 0
        physicalSkillRolls = 0
        socialSkillRolls = 0
        evolutionSkillRolls = 0
        quirkRolls = 0
        exoticWeaponRolls = 0

        # Determine the diet and modify attributes.
        dietRoll = roll_xdy(1, 6)
        if dietRoll <= 2:
            self.diet = "Carnivore"
            self.dietDescription = "Carnivorous avians tend to be larger than other avian species and have a tendency toward cannibalism. Those avians that do not eat others of their kind prefer small, easily caught game and may even be suited to hunting for shallow water aquatic animals."
            self.meleeNaturalWeapons = 0
            self.dexterity += 2
            evolutionRollModifier += 1
            physicalSkillRolls += 1
        elif dietRoll <= 4:
            self.diet = "Herbivore"
            self.dietDescription = "Herbivorous avians typically survive on seeds and fruit, soft palate fare that can be easily crushed or swallowed and digested before excretion. Very few herbivores of this class are hostile."
            self.endurance += 2
            self.pack += 2
            socialSkillRolls += 1
        else:
            self.diet = "Omnivore"
            self.dietDescription = "The most common form of omnivorous avian is the seed eating variety that has extended its diet to worms and insects. Scavengers are also common, eating stray fruit and picking clean the kills of other, larger creatures."
            self.meleeNaturalWeapons = 0
            self.pack += 2
            evolutionSkillRolls += 1
            physicalSkillRolls += 1
            socialSkillRolls += 1

        # Determine how many of each type of skill roll will be made.
        evoRollSkills = roll_xdy(1, 6) + evolutionRollModifier
        if evoRollSkills != 5:
            socialSkillRolls += 1
        if evoRollSkills == 7:
            socialSkillRolls += 1
        if evoRollSkills == 3 or evoRollSkills >= 5:
            physicalSkillRolls += 1
        if evoRollSkills >= 4:
            evolutionSkillRolls += 1

        # Roll for "other" evolutionary benefits.
        evoOtherRolls = 1
        while evoOtherRolls > 0:
            evoRollOther = roll_xdy(1, 6) + evolutionRollModifier
            if evoRollOther == 1:
                self.instinct += 2
            elif evoRollOther == 2:
                self.pack += 2
            elif evoRollOther == 3:
                self.instinct += 1
                self.pack += 2
            elif evoRollOther == 4:
                self.dexterity += roll_xdy(1, 6)
                self.pack += 2
            elif evoRollOther == 5:
                self.endurance += 2
                self.pack += roll_xdy(1, 6)
            elif evoRollOther == 6:
                quirkRolls += 2
            else:
                evoOtherRolls += 1
                continue

            evoOtherRolls -= 1

        # Roll for quirks.
        quirk2 = False
        quirk3 = False
        quirk4 = False
        quirk7 = False
        quirk9 = False
        quirk10 = False
        quirk11 = False
        while quirkRolls > len(self.quirks):
            quirkRoll = roll_xdy(2, 6)
            if quirkRoll == 2 and not quirk2:
                quirk2 = True
                self.quirks.append(
                    "The plumage of this animal is highly exotic and valuable, exhibiting colours rarely found within its habitat.")
            if quirkRoll == 3 and not quirk3:
                quirk3 = True
                self.quirks.append(
                    "Extremely social, these animals live in immense flocks.")
            if quirkRoll == 4 and not quirk4:
                quirk4 = True
                self.quirks.append(
                    "Quite at home on the ground, this species has evolved away from flight.")
            if quirkRoll == 5:
                self.quirks.append(
                    "Far smaller than their evolutionary niche would suggest.")
                self.sizeRollModifier = -4
            if quirkRoll == 6:
                self.quirks.append(
                    "These avians have adapted a very unusual way of dealing with enemies.")
                exoticWeaponRolls += 1
            if quirkRoll == 7 and not quirk7:
                quirk7 = True
                self.quirks.append(
                    "These avians have developed a way to emit calls that sound exactly like the cries of wounded prey, using these to lure meals closer.")
                self.behaviors.add("Siren")
            if quirkRoll == 8:
                self.quirks.append(
                    "Environmental pressures have forced this animal to adapt to a hostile environment.")
                self.endurance += 1
                self.armor += 1
            if quirkRoll == 9 and not quirk9:
                quirk9 = True
                self.quirks.append(
                    "Not just ground bound, this flightless species thrives because of it.")
                self.behaviors.add("Chaser")
                self.endurance += 1
            if quirkRoll == 10 and not quirk10:
                quirk10 = True
                self.quirks.append(
                    "Possessed of a deadly main attack, these avians are truly vicious and always press their attack once they wound an enemy.")
            if quirkRoll == 11 and not quirk11:
                quirk11 = True
                self.quirks.append(
                    "These avians mate for life, are never encountered in packs larger than a pair of adults. If one is killed the other will automatically flee if possible.")
            if quirkRoll == 12:
                quirkRolls += 1

        # Roll for evolutionary skills.
        while evolutionSkillRolls > 0:
            evoSkillRoll = roll_xdy(1, 6)
            if evoSkillRoll == 1:
                self.weaponDice += 1
            elif evoSkillRoll == 2:
                self.raise_skill_level("meleeNaturalWeapons", 1)
            elif evoSkillRoll == 3:
                self.instinct += 1
            elif evoSkillRoll == 4:
                physicalSkillRolls += 1
            elif evoSkillRoll == 5:
                socialSkillRolls += 1
            else:
                self.raise_skill_level("meleeNaturalWeapons", 1)

            evolutionSkillRolls -= 1

        # Roll for social skills.
        while socialSkillRolls > 0:
            socialSkillRoll = roll_xdy(1, 6)
            if socialSkillRoll == 1:
                self.pack += 2
            elif socialSkillRoll == 2:
                self.instinct += 1
            elif socialSkillRoll == 3:
                self.raise_skill_level("deception", 1)
            elif socialSkillRoll == 4:
                self.instinct += 2
            elif socialSkillRoll == 5:
                self.pack += roll_xdy(1, 6)
            else:
                self.raise_skill_level("recon", 1)

            socialSkillRolls -= 1

        # Roll for physical skills.
        while physicalSkillRolls > 0:
            physicalSkillRoll = roll_xdy(1, 6)
            if physicalSkillRoll == 1:
                self.dexterity += 1
            elif physicalSkillRoll == 2:
                self.dexterity += 2
            elif physicalSkillRoll == 3:
                self.endurance += 2
            elif physicalSkillRoll == 4:
                self.endurance += 4
            elif physicalSkillRoll == 5:
                self.dexterity += roll_xdy(1, 6)
            else:
                self.raise_skill_level("meleeNaturalWeapons", 1)

            physicalSkillRolls -= 1

        # Roll for a behavior.
        behaviorRoll = roll_xdy(1, 6)
        if self.diet == "Carnivore":
            if behaviorRoll == 1:
                self.behaviors.add("Hunter")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Hunter")
            elif behaviorRoll == 3:
                self.behaviors.add("Hunter")
            elif behaviorRoll == 4:
                self.behaviors.add("Chaser")
            elif behaviorRoll == 5:
                self.behaviors.add("Killer")
                self.reactionModifier += 1
            else:
                self.behaviors.add("Pouncer")
                self.reactionModifier -= 2
        elif self.diet == "Herbivore":
            if behaviorRoll == 1:
                self.behaviors.add("Intimidator")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Intermittent")
            elif behaviorRoll == 3:
                self.behaviors.add("Intermittent")
            elif behaviorRoll == 4:
                self.behaviors.add("Intermittent")
                self.reactionModifier += 1
            elif behaviorRoll == 5:
                self.behaviors.add("Intermittent")
                self.reactionModifier += 2
            else:
                self.behaviors.add("Grazer")
                self.reactionModifier -= 2
        else:
            if behaviorRoll == 1:
                self.behaviors.add("Carrion-Eater")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Eater")
                self.reactionModifier -= 1
            elif behaviorRoll == 3:
                self.behaviors.add("Eater")
            elif behaviorRoll == 4:
                self.behaviors.add("Intimidator")
                self.reactionModifier += 1
            elif behaviorRoll == 5:
                self.behaviors.add("Reducer")
                self.reactionModifier -= 1
            else:
                self.behaviors.add("Reducer")
                self.reactionModifier -= 2

        self.behavior_effects()
        self.set_size(self.sizeRoll, self.sizeRollModifier)
        self.set_strength(self.sizeRoll)
        self.set_endurance(self.sizeRoll)
        self.set_dexterity(self.sizeRoll)
        self.set_exotic_weapons(exoticWeaponRolls)
        self.set_weapon_and_damage_modifier()
        self.set_weapon_damage()
        self.set_armor()
        self.set_number_encountered()
        self.set_initiative()
        self.set_reactions()

        if quirk3:
            if self.pack <= 6:
                self.pack = 12
            else:
                self.pack = self.pack * 2
        if quirk4 or quirk9:
            self.primaryMovement = "Walk"
        if quirk11:
            self.numberEncountered = 2

        if self.intelligence > 2:
            self.intelligence = 2


class Fungal(Animal):
    """
    Defines a fungal.

    Parameters:
        planet: Class instance
            The planet object the animal lives on. Valid classes are
            DwarfPlanet, TerrestrialPlanet, HelianPlanet.
        terrain: String
            The type of terrain that this animal calls home.
    """

    def __init__(self, planet, terrain):
        super(Fungal, self).__init__(planet, terrain)
        self.animalClass = "Fungal"

        # Skills this class innately has.
        self.athletics = 0
        self.stealth = 0
        self.recon = 0
        self.survival = 0

        evolutionRollModifier = 0
        physicalSkillRolls = 0
        socialSkillRolls = 0
        evolutionSkillRolls = 0
        quirkRolls = 0
        exoticWeaponRolls = 0

        # Determine the diet and modify attributes.
        dietRoll = roll_xdy(1, 6)
        if dietRoll == 1:
            self.diet = "Carnivore"
            self.dietDescription = "Carnivorous fungals usually lure food to them, engulfing their prey and dissolving them. Fungal creatures are rarely dense or resilient enough to be combative."
            self.meleeNaturalWeapons = 0
            self.strength += 2
            evolutionRollModifier += 1
            physicalSkillRolls += 1
        elif dietRoll == 2:
            self.diet = "Herbivore"
            self.dietDescription = "Very few fungal life forms subsist solely on other play matter but those few that do tend to be very small so as not to need much nourishment or extremely large and located in heavily vegetated areas."
            self.endurance += 2
            self.pack += 2
            socialSkillRolls += 1
        else:
            self.diet = "Omnivore"
            self.dietDescription = "The most common form of fungal life is omnivorous, eating whatever and whenever opportunity affords. They also tend to be the most mobile, often travelling great distances to remain where they can have access to nourishment."
            evolutionRollModifier += 1
            physicalSkillRolls += 1

        # Determine how many of each type of skill roll will be made.
        evoRollSkills = roll_xdy(1, 6) + evolutionRollModifier
        if evoRollSkills <= 4 or evoRollSkills == 7:
            socialSkillRolls += 1
        if evoRollSkills == 3 or evoRollSkills >= 5:
            physicalSkillRolls += 1
        if evoRollSkills == 6:
            physicalSkillRolls += 1
        if evoRollSkills >= 4:
            evolutionSkillRolls += 1

        # Roll for "other" evolutionary benefits.
        evoOtherRolls = 1
        while evoOtherRolls > 0:
            evoRollOther = roll_xdy(1, 6) + evolutionRollModifier
            if evoRollOther == 1:
                self.instinct += 2
            elif evoRollOther == 2:
                self.endurance += 2
            elif evoRollOther == 3:
                exoticWeaponRolls += 1
            elif evoRollOther == 4:
                self.endurance += roll_xdy(1, 6)
            elif evoRollOther == 5:
                self.endurance += 2
                self.pack += roll_xdy(1, 6)
            elif evoRollOther == 6:
                quirkRolls += 2
            else:
                evoOtherRolls += 1
                continue

            evoOtherRolls -= 1

        # Roll for quirks.
        quirk2 = False
        quirk3 = False
        quirk4 = False
        quirk5 = False
        quirk7 = False
        quirk8 = False
        quirk9 = False
        quirk10 = False
        quirk11 = False
        while quirkRolls > len(self.quirks):
            quirkRoll = roll_xdy(2, 6)
            if quirkRoll == 2:
                quirk2 = True
                self.quirks.append(
                    "This Fungal is an absolutely bizarre colour and smells rancid. It cannot succeed at Stealth rolls.")
                exoticWeaponRolls += 1
            if quirkRoll == 3 and not quirk3:
                quirk3 = True
                self.quirks.append(
                    "Unlike other fungus-based life, this species has developed a rudimentary vocal structure. The sounds it can make may be extremely strange, similar to nothing else found in nature.")
            if quirkRoll == 4 and not quirk4 and not quirk5:
                quirk4 = True
                self.quirks.append(
                    "The Fungal can inflate itself with a light gas, allowing for a slow form of flight.")
                self.primaryMovement = "Fly"
            if quirkRoll == 5 and not quirk5 and not quirk4 and not quirk11:
                quirk5 = True
                self.quirks.append(
                    "Though capable of physical movement to attack or defend itself, this Fungal species is stationary and cannot change location. If the base species was herbivorous, it is now specialises in luring other fungals to their doom.")
                self.behaviors.add("Siren")
                self.primaryMovement = "Stationary"
                self.endurance += roll_xdy(1, 6)
            if quirkRoll == 6:
                self.quirks.append(
                    "This species propagates very quickly and easily, dwelling in large family structures with its progeny. It is never encountered alone.")
                self.pack += roll_xdy(1, 6)
            if quirkRoll == 7:
                quirk7 = True
                self.quirks.append("Very soft in bodily structure.")
                self.endurance += roll_xdy(1, 6)
            if quirkRoll == 8 and not quirk8:
                quirk8 = True
                self.quirks.append(
                    "The scent and outlandish appearance of this fungal terrifies other animals.")
                self.behaviors.add("Hijacker")
            if quirkRoll == 9 and not quirk9:
                quirk9 = True
                self.quirks.append("Unfortunately for this fungal, its biological structure is extremely nutritious, capable of feeding even carnivores in its environment. When encountered, there is a 50% chance that a predator of another species is also in the area.")
            if quirkRoll == 10 and not quirk10:
                quirk10 = True
                self.quirks.append(
                    "Capable of rapid regrowth from even very small samples, this species must be completely destroyed or it will regenerate completely in 1d6 days.")
            if quirkRoll == 11 and not quirk11 and not quirk5:
                quirk11 = True
                self.quirks.append(
                    "Almost liquid in structure, this extremely slimy fungal moves at normal speed and is capable of extremely rapid motion when it hunts.")
                self.behaviors.add("Pouncer")
                self.dexterity += 2
            if quirkRoll == 12:
                quirkRolls += 1

        # Roll for evolutionary skills.
        while evolutionSkillRolls > 0:
            evoSkillRoll = roll_xdy(1, 6)
            if evoSkillRoll == 1:
                self.weaponDice += 1
            elif evoSkillRoll == 2:
                self.raise_skill_level("meleeNaturalWeapons", 1)
            elif evoSkillRoll == 3:
                self.instinct += 1
            elif evoSkillRoll == 4:
                physicalSkillRolls += 1
            elif evoSkillRoll == 5:
                socialSkillRolls += 1
            else:
                exoticWeaponRolls += 1

            evolutionSkillRolls -= 1

        # Roll for social skills.
        while socialSkillRolls > 0:
            socialSkillRoll = roll_xdy(1, 6)
            if socialSkillRoll == 1:
                self.pack += 2
            elif socialSkillRoll == 2:
                self.instinct += 1
            elif socialSkillRoll == 3:
                self.raise_skill_level("stealth", 1)
            elif socialSkillRoll == 4:
                self.instinct += 2
            elif socialSkillRoll == 5:
                self.pack += roll_xdy(1, 6)
            else:
                self.raise_skill_level("recon", 1)

            socialSkillRolls -= 1

        # Roll for physical skills.
        while physicalSkillRolls > 0:
            physicalSkillRoll = roll_xdy(1, 6)
            if physicalSkillRoll == 1:
                self.endurance += 1
            elif physicalSkillRoll == 2:
                self.endurance += 2
            elif physicalSkillRoll == 3:
                self.endurance += 4
            elif physicalSkillRoll == 4:
                self.endurance += roll_xdy(2, 6)
            elif physicalSkillRoll == 5:
                self.endurance += roll_xdy(1, 6)
                self.strength += roll_xdy(1, 6)
            else:
                self.raise_skill_level("meleeNaturalWeapons", 1)

            physicalSkillRolls -= 1

        # Roll for a behavior.
        if not quirk5:
            behaviorRoll = roll_xdy(1, 6)
            if self.diet == "Carnivore":
                if behaviorRoll == 1:
                    self.behaviors.add("Hunter")
                    self.reactionModifier -= 2
                elif behaviorRoll == 2:
                    self.behaviors.add("Hunter")
                    self.reactionModifier -= 1
                elif behaviorRoll == 3:
                    self.behaviors.add("Hunter")
                elif behaviorRoll == 4:
                    self.behaviors.add("Siren")
                elif behaviorRoll == 5:
                    self.behaviors.add("Siren")
                    self.reactionModifier += 1
                else:
                    self.behaviors.add("Killer")
            elif self.diet == "Herbivore":
                if behaviorRoll == 1:
                    self.behaviors.add("Intermittent")
                    self.reactionModifier -= 2
                elif behaviorRoll == 2:
                    self.behaviors.add("Intermittent")
                    self.reactionModifier -= 1
                elif behaviorRoll == 3:
                    self.behaviors.add("Intermittent")
                    self.reactionModifier -= 1
                elif behaviorRoll == 4:
                    self.behaviors.add("Intermittent")
                elif behaviorRoll == 5:
                    self.behaviors.add("Grazer")
                    self.reactionModifier -= 1
                else:
                    self.behaviors.add("Grazer")
                    self.reactionModifier -= 2
            else:
                if behaviorRoll == 1:
                    self.behaviors.add("Carrion-Eater")
                    self.reactionModifier -= 1
                elif behaviorRoll == 2:
                    self.behaviors.add("Carrion-Eater")
                elif behaviorRoll == 3:
                    self.behaviors.add("Eater")
                elif behaviorRoll == 4:
                    self.behaviors.add("Reducer")
                elif behaviorRoll == 5:
                    self.behaviors.add("Reducer")
                    self.reactionModifier -= 1
                else:
                    self.behaviors.add("Reducer")
                    self.reactionModifier -= 2

        if quirk2:
            self.stealth = -99

        self.behavior_effects()
        self.set_size(self.sizeRoll, self.sizeRollModifier)
        self.set_strength(self.sizeRoll)
        self.set_endurance(self.sizeRoll)
        self.set_dexterity(self.sizeRoll)
        self.set_exotic_weapons(exoticWeaponRolls)
        self.set_weapon_and_damage_modifier()
        self.set_weapon_damage()
        self.set_armor()
        self.set_number_encountered()
        self.set_initiative()
        self.set_reactions()

        if quirk7:
            self.armor = 0

        if self.intelligence > 2:
            self.intelligence = 2


class Insect(Animal):
    """
    Defines an insect.

    Parameters:
        planet: Class instance
            The planet object the animal lives on. Valid classes are
            DwarfPlanet, TerrestrialPlanet, HelianPlanet.
        terrain: String
            The type of terrain that this animal calls home.
    """

    def __init__(self, planet, terrain):
        super(Insect, self).__init__(planet, terrain)
        self.animalClass = "Insect"

        # Skills this class innately has.
        self.athletics = 0
        self.meleeNaturalWeapons = 0
        self.recon = 0
        self.survival = 0

        evolutionRollModifier = 0
        physicalSkillRolls = 0
        socialSkillRolls = 0
        evolutionSkillRolls = 0
        quirkRolls = 0
        exoticWeaponRolls = 0

        # Determine the diet and modify attributes.
        dietRoll = roll_xdy(1, 6)
        if dietRoll <= 3:
            self.diet = "Carnivore"
            self.dietDescription = " Most insects are carnivorous by the strictest definition of the term, with weaker insects normally being their food, and many are also cannibalistic. Insects often have a modified diet, consuming liquids from their prey as opposed to devouring flesh."
            self.meleeNaturalWeapons += 1
            self.strength += roll_xdy(1, 6)
            physicalSkillRolls += 1
        elif dietRoll == 4:
            self.diet = "Herbivore"
            self.dietDescription = "Herbivorous forms often dominate their ecosystems through a mix of physical strength, tenacity and sheer numbers."
            self.endurance += 2
            self.pack += 2
            socialSkillRolls += 1
        else:
            self.diet = "Omnivore"
            self.dietDescription = "Most insects are carnivorous by the strictest definition of the term, with weaker insects normally being their food, and many are also cannibalistic. Insects often have a modified diet, consuming liquids from their prey as opposed to devouring flesh."
            self.meleeNaturalWeapons += 1
            evolutionRollModifier += 1
            self.pack += 1
            physicalSkillRolls += 1
            socialSkillRolls += 1

        # Determine how many of each type of skill roll will be made.
        evoRollSkills = roll_xdy(1, 6) + evolutionRollModifier
        physicalSkillRolls += 1
        if evoRollSkills == 6:
            physicalSkillRolls += 1
        if 3 <= evoRollSkills <= 4 or evoRollSkills == 7:
            socialSkillRolls += 1
        if evoRollSkills >= 5:
            evolutionSkillRolls += 1

        # Roll for "other" evolutionary benefits.
        evoOtherRolls = 1
        while evoOtherRolls > 0:
            evoRollOther = roll_xdy(1, 6) + evolutionRollModifier
            if evoRollOther == 1:
                self.instinct += 2
            elif evoRollOther == 2:
                evolutionSkillRolls += 1
            elif evoRollOther == 3:
                exoticWeaponRolls += 1
            elif evoRollOther == 4:
                self.endurance += roll_xdy(1, 6)
            elif evoRollOther == 5:
                self.endurance += 2
                self.strength = roll_xdy(1, 6)
            elif evoRollOther == 6:
                quirkRolls += 2
            else:
                evoOtherRolls += 1
                continue

            evoOtherRolls -= 1

        # Roll for quirks.
        quirk2 = False
        quirk5 = False
        quirk6 = False
        quirk7 = False
        quirk8 = False
        quirk10 = False
        quirk11 = False
        armorQuirkCount = 0
        while quirkRolls > len(self.quirks):
            quirkRoll = roll_xdy(2, 6)
            if quirkRoll == 2 and not quirk2:
                quirk2 = True
                self.quirks.append(
                    "Extremely unusual in appearance, these insects have apparently useless and garish physical structures and barely fit in their own ecosystems.")
            if quirkRoll == 3:
                self.quirks.append(
                    "Slow moving because of heavy exoskeleton plating, these insects travel at half speed.")
                armorQuirkCount += 1
            if quirkRoll == 4:
                self.quirks.append(
                    "This perk granted flying if the insect didn't have it, or takes it away to add strength.")
                if self.primaryMovement == "Fly":
                    self.primaryMovement = "Walk"
                    self.strength += roll_xdy(1, 6)
                else:
                    self.primaryMovement = "Fly"
                    if self.strength - 1 < 0:
                        self.strength = 0
                    else:
                        self.strength -= 1
                    if self.armor - 1 < 0:
                        self.armor = 0
                    else:
                        self.armor -= 1
            if quirkRoll == 5 and not quirk5 and not quirk6:
                quirk5 = True
                self.quirks.append("These insects form veritable swarms.")
            if quirkRoll == 6 and not quirk6 and not quirk5:
                quirk6 = True
                self.quirks.append(
                    "Solitary by nature. If the insects are herbivores, they just leave their prey to rot and eat the resulting fungus.")
                if self.primaryMovement != "Fly":
                    self.behaviors.add("Trapper")
                else:
                    self.behaviors.add("Pouncer")
            if quirkRoll == 7 and not quirk7:
                quirk7 = True
                self.quirks.append("Acutely self-aware.")
            if quirkRoll == 8 and not quirk8:
                quirk8 = True
                self.quirks.append(
                    "These insects have a hive mind and a minimum Pack score of 6. One of their number has an Intelligence of 2, all the rest are 0 and serve its will without question.")
            if quirkRoll == 9:
                self.quirks.append(
                    "Evolved in a particularly dangerous habitat, these insects developed an unusual defence.")
                exoticWeaponRolls += 1
            if quirkRoll == 10 and not quirk10:
                quirk10 = True
                self.quirks.append("These insects have a decentralised nervous system and can be hacked apart into smaller creatures. In combat, any attack that inflicts Endurance damage has a 50% chance of splitting the insect in half. The resulting insects have their attack damage dice halved and divide their remaining Endurance between them. If this would result in an insect with a starting End of 3 or less, the insect dies instead of splitting.")
            if quirkRoll == 11 and not quirk11:
                quirk11 = True
                self.quirks.append("The insect can generate a hypnotic drone.")
                self.behaviors.add("Siren")
            if quirkRoll == 12:
                quirkRolls += 1

        # Roll for evolutionary skills.
        while evolutionSkillRolls > 0:
            evoSkillRoll = roll_xdy(1, 6)
            if evoSkillRoll == 1:
                self.weaponDice += 1
            elif evoSkillRoll == 2:
                self.raise_skill_level("meleeNaturalWeapons", 1)
            elif evoSkillRoll == 3:
                self.pack += 1
                self.instinct += roll_xdy(1, 6)
            elif evoSkillRoll == 4:
                physicalSkillRolls += 1
            elif evoSkillRoll == 5:
                socialSkillRolls += 1
            else:
                exoticWeaponRolls += 1

            evolutionSkillRolls -= 1

        # Roll for social skills.
        while socialSkillRolls > 0:
            socialSkillRoll = roll_xdy(1, 6)
            if socialSkillRoll == 1:
                self.pack += 2
            elif socialSkillRoll == 2:
                self.instinct += 1
            elif socialSkillRoll == 3:
                self.raise_skill_level("stealth", 1)
            elif socialSkillRoll == 4:
                self.instinct += 2
            elif socialSkillRoll == 5:
                self.pack += roll_xdy(1, 6)
            else:
                self.raise_skill_level("recon", 1)

            socialSkillRolls -= 1

        # Roll for physical skills.
        while physicalSkillRolls > 0:
            physicalSkillRoll = roll_xdy(1, 6)
            if physicalSkillRoll == 1:
                self.endurance += 1
            elif physicalSkillRoll == 2:
                self.endurance += 2
            elif physicalSkillRoll == 3:
                self.armor += 1
            elif physicalSkillRoll == 4:
                self.endurance += roll_xdy(1, 6)
                self.armor += 1
            elif physicalSkillRoll == 5:
                self.strength += roll_xdy(1, 6)
                self.armor += 1
            else:
                self.raise_skill_level("meleeNaturalWeapons", 1)

            physicalSkillRolls -= 1

        # Roll for a behavior.
        behaviorRoll = roll_xdy(1, 6)
        if self.diet == "Carnivore":
            if behaviorRoll == 1:
                self.behaviors.add("Pouncer")
            elif behaviorRoll == 2:
                self.behaviors.add("Hunter")
                self.reactionModifier += 1
            elif behaviorRoll == 3:
                self.behaviors.add("Hunter")
                self.reactionModifier += 2
            elif behaviorRoll == 4:
                self.behaviors.add("Killer")
            elif behaviorRoll == 5:
                self.behaviors.add("Trapper")
                self.reactionModifier -= 1
            else:
                self.behaviors.add("Chaser")
        elif self.diet == "Herbivore":
            if behaviorRoll == 1:
                self.behaviors.add("Eater")
                self.reactionModifier -= 2
            elif behaviorRoll == 2:
                self.behaviors.add("Intermittent")
                self.reactionModifier -= 1
            elif behaviorRoll == 3:
                self.behaviors.add("Filter")
            elif behaviorRoll == 4:
                self.behaviors.add("Intermittent")
            elif behaviorRoll == 5:
                self.behaviors.add("Grazer")
                self.reactionModifier -= 1
            else:
                self.behaviors.add("Gatherer")
        else:
            if behaviorRoll == 1:
                self.behaviors.add("Carrion-Eater")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Eater")
            elif behaviorRoll == 3:
                self.behaviors.add("Eater")
                self.reactionModifier += 2
            elif behaviorRoll == 4:
                self.behaviors.add("Reducer")
            elif behaviorRoll == 5:
                self.behaviors.add("Reducer")
                self.reactionModifier -= 1
            else:
                self.behaviors.add("Reducer")
                self.reactionModifier -= 2

        self.behavior_effects()
        self.set_size(self.sizeRoll, self.sizeRollModifier)
        self.set_strength(self.sizeRoll)
        self.set_endurance(self.sizeRoll)
        self.set_dexterity(self.sizeRoll)
        self.set_exotic_weapons(exoticWeaponRolls)
        self.set_weapon_and_damage_modifier()
        self.set_weapon_damage()
        self.set_armor()
        self.set_number_encountered()
        self.set_initiative()
        self.set_reactions()

        self.armor += armorQuirkCount

        if quirk5 and self.pack < 2:
            self.pack = 2
        if quirk6:
            self.pack = 0
        if quirk7:
            self.intelligence = 2
        if quirk8 and self.pack < 6:
            self.pack = 6

        if self.intelligence > 2:
            self.intelligence = 2


class Mammal(Animal):
    """
    Defines a mammal.

    Parameters:
        planet: Class instance
            The planet object the animal lives on. Valid classes are
            DwarfPlanet, TerrestrialPlanet, HelianPlanet.
        terrain: String
            The type of terrain that this animal calls home.
    """

    def __init__(self, planet, terrain):
        super(Mammal, self).__init__(planet, terrain)
        self.animalClass = "Mammal"

        # Skills this class innately has.
        self.athletics = 0
        self.meleeNaturalWeapons = 0
        self.recon = 0
        self.survival = 0

        evolutionRollModifier = 0
        physicalSkillRolls = 0
        socialSkillRolls = 0
        evolutionSkillRolls = 0
        quirkRolls = 0
        exoticWeaponRolls = 0

        # Determine the diet and modify attributes.
        dietRoll = roll_xdy(1, 6)
        if dietRoll <= 2:
            self.diet = "Carnivore"
            self.dietDescription = "Predatory mammals are generally the strongest of their kind and occupy a middle strata between their prey (often herbivorous mammals) and more intelligent omnivorous mammals above them."
            self.strength += 1
            self.dexterity += 1
            physicalSkillRolls += 1
        elif dietRoll <= 4:
            self.diet = "Herbivore"
            self.dietDescription = "Pack oriented and capable of reaching impressive sizes, herbivorous mammals can be quite fierce in defence of their territories and family units but are otherwise very docile. On worlds with intelligent life, these animals are the ones most often domesticated."
            self.endurance += 2
            self.pack += 2
            socialSkillRolls += 1
        else:
            self.diet = "Omnivore"
            self.dietDescription = "Their varied diet, survival ability and dedication to pack structures all lend themselves to elevate omnivorous mammals to a position of evolutionary dominance on many worlds. Sentient races often come from this stock, though some show a tendency toward carnivorous appetites."
            evolutionRollModifier += 1
            self.intelligence += 1
            physicalSkillRolls += 1
            socialSkillRolls += 1

        # Determine how many of each type of skill roll will be made.
        evoRollSkills = roll_xdy(1, 6) + evolutionRollModifier
        if evoRollSkills == 1 or 3 <= evoRollSkills <= 4 or evoRollSkills >= 6:
            physicalSkillRolls += 1
        if evoRollSkills >= 2:
            socialSkillRolls += 1
        if evoRollSkills == 7:
            socialSkillRolls += 1
        if evoRollSkills >= 5:
            evolutionSkillRolls += 1

        # Roll for "other" evolutionary benefits.
        evoOtherRolls = 1
        while evoOtherRolls > 0:
            evoRollOther = roll_xdy(1, 6) + evolutionRollModifier
            if evoRollOther == 1:
                self.instinct += 2
            elif evoRollOther == 2:
                evolutionSkillRolls += 1
            elif evoRollOther == 3:
                self.strength += 1
                self.endurance += 1
                self.pack += 1
            elif evoRollOther == 4:
                self.endurance += roll_xdy(1, 6)
            elif evoRollOther == 5:
                self.sizeRollModifier += 1
            elif evoRollOther == 6:
                quirkRolls += 2
            else:
                evoOtherRolls += 1
                continue

            evoOtherRolls -= 1

        # Roll for quirks.
        quirk2 = False
        quirk3 = 0
        quirk4 = 0
        quirk8 = False
        quirk10 = False
        quirk11 = False
        while quirkRolls > len(self.quirks):
            quirkRoll = roll_xdy(2, 6)
            if quirkRoll == 2 and not quirk2:
                quirk2 = True
                self.quirks.append(
                    "This mammal has an unusual mode of travel, be it gliding or swinging between trees in its home environment.")
                self.behaviors.add("Pouncer")
            if quirkRoll == 3:
                quirk3 += 1
                self.quirks.append("Extremely swift.")
            if quirkRoll == 4:
                quirk4 += 1
                self.quirks.append(
                    "These animals have remarkably fast metabolisms, enabling them to recover quickly from injuries. They regain one lost Endurance point every other round of combat starting at the beginning of the second round.")
            if quirkRoll == 5:
                self.quirks.append(
                    "Bright even for its class, these mammals show a devious cunning that borders on compulsive mischief.")
                self.raise_skill_level("stealth", 1)
                self.raise_skill_level("deception", 1)
            if quirkRoll == 6:
                self.quirks.append(
                    "Profuse body hair marks this species as a sign of its innate adaptability.")
                self.raise_skill_level("survival", 1)
            if quirkRoll == 7:
                self.quirks.append(
                    "Herd-oriented and nomadic, these are mostly peaceful mammals.")
                self.pack += roll_xdy(1, 6)
            if quirkRoll == 8 and not quirk8:
                quirk8 = True
                self.quirks.append(
                    "These animals have prodigious horns and know how to use them in combat.")
                self.weapons.add("Horns")
            if quirkRoll == 9:
                self.quirks.append(
                    "Unusually vicious, these mammals are hostile to any species but their own.")
                if "Killer" in self.behaviors:
                    self.reactionModifier += 2
                    self.strength += 2
                else:
                    self.behaviors.add("Killer")
            if quirkRoll == 10 and not quirk10:
                quirk10 = True
                self.quirks.append(
                    "Adapted to an aquatic environment even if they do not normally live near one.")
                self.primaryMovement = "Swim"
            if quirkRoll == 11 and not quirk11:
                quirk11 = True
                self.quirks.append(
                    "This animal species is on the verge of evolving into sentience.")
            if quirkRoll == 12:
                quirkRolls += 1

        extraBehaviorRoll = False

        # Roll for evolutionary skills.
        while evolutionSkillRolls > 0:
            evoSkillRoll = roll_xdy(1, 6)
            if evoSkillRoll == 1:
                extraBehaviorRoll = True
            elif evoSkillRoll == 2:
                self.raise_skill_level("meleeNaturalWeapons", 1)
            elif evoSkillRoll == 3:
                self.pack += 1
                self.instinct += 1
            elif evoSkillRoll == 4:
                physicalSkillRolls += 1
            elif evoSkillRoll == 5:
                socialSkillRolls += 1
            else:
                exoticWeaponRolls += 1

            evolutionSkillRolls -= 1

        # Roll for social skills.
        while socialSkillRolls > 0:
            socialSkillRoll = roll_xdy(1, 6)
            if socialSkillRoll == 1:
                self.pack += 2
            elif socialSkillRoll == 2:
                self.instinct += 1
            elif socialSkillRoll == 3:
                self.raise_skill_level("stealth", 1)
            elif socialSkillRoll == 4:
                self.intelligence += 1
            elif socialSkillRoll == 5:
                self.pack += 1
                self.raise_skill_level("survival", 1)
            else:
                self.raise_skill_level("recon", 1)

            socialSkillRolls -= 1

        # Roll for physical skills.
        while physicalSkillRolls > 0:
            physicalSkillRoll = roll_xdy(1, 6)
            if physicalSkillRoll == 1:
                self.strength += 1
            elif physicalSkillRoll == 2:
                self.endurance += 2
            elif physicalSkillRoll == 3:
                self.dexterity += 1
            elif physicalSkillRoll == 4:
                self.sizeRollModifier += 1
            elif physicalSkillRoll == 5:
                self.strength += 2
                self.endurance += 1
            else:
                self.raise_skill_level("meleeNaturalWeapons", 1)

            physicalSkillRolls -= 1

        # Roll for a behavior.
        behaviorRoll = roll_xdy(1, 6)
        if self.diet == "Carnivore":
            if behaviorRoll == 1:
                self.behaviors.add("Pouncer")
            elif behaviorRoll == 2:
                self.behaviors.add("Killer")
                self.reactionModifier += 1
            elif behaviorRoll == 3:
                self.behaviors.add("Trapper")
            elif behaviorRoll == 4:
                self.behaviors.add("Chaser")
            elif behaviorRoll == 5:
                self.behaviors.add("Hunter")
                self.reactionModifier -= 1
            else:
                self.behaviors.add("Hijacker")
        elif self.diet == "Herbivore":
            if behaviorRoll == 1:
                self.behaviors.add("Eater")
                self.reactionModifier -= 2
            elif behaviorRoll == 2:
                self.behaviors.add("Intermittent")
                self.reactionModifier -= 1
            elif behaviorRoll == 3:
                self.behaviors.add("Intermittent")
            elif behaviorRoll == 4:
                self.behaviors.add("Intermittent")
            elif behaviorRoll == 5:
                self.behaviors.add("Grazer")
                self.reactionModifier -= 1
            else:
                self.behaviors.add("Gatherer")
        else:
            if behaviorRoll == 1:
                self.behaviors.add("Carrion-Eater")
                self.reactionModifier -= 1
            elif behaviorRoll == 2:
                self.behaviors.add("Gatherer")
            elif behaviorRoll == 3:
                self.behaviors.add("Gatherer")
                self.reactionModifier += 1
            elif behaviorRoll == 4:
                self.behaviors.add("Hunter")
            elif behaviorRoll == 5:
                self.behaviors.add("Intimidator")
                self.reactionModifier -= 1
            else:
                self.behaviors.add("Reducer")

        if extraBehaviorRoll:
            behaviorRoll = roll_xdy(1, 6)
            if self.diet == "Carnivore":
                if behaviorRoll == 1:
                    self.behaviors.add("Pouncer")
                elif behaviorRoll == 2:
                    self.behaviors.add("Killer")
                elif behaviorRoll == 3:
                    self.behaviors.add("Trapper")
                elif behaviorRoll == 4:
                    self.behaviors.add("Chaser")
                elif behaviorRoll == 5:
                    self.behaviors.add("Hunter")
                else:
                    self.behaviors.add("Hijacker")
            elif self.diet == "Herbivore":
                if behaviorRoll == 1:
                    self.behaviors.add("Eater")
                elif behaviorRoll == 2:
                    self.behaviors.add("Intermittent")
                elif behaviorRoll == 3:
                    self.behaviors.add("Intermittent")
                elif behaviorRoll == 4:
                    self.behaviors.add("Intermittent")
                elif behaviorRoll == 5:
                    self.behaviors.add("Grazer")
                else:
                    self.behaviors.add("Gatherer")
            else:
                if behaviorRoll == 1:
                    self.behaviors.add("Carrion-Eater")
                elif behaviorRoll == 2:
                    self.behaviors.add("Gatherer")
                elif behaviorRoll == 3:
                    self.behaviors.add("Gatherer")
                elif behaviorRoll == 4:
                    self.behaviors.add("Hunter")
                elif behaviorRoll == 5:
                    self.behaviors.add("Intimidator")
                else:
                    self.behaviors.add("Reducer")

            self.reactionModifier = 0

        self.behavior_effects()

        if "Herd-oriented and nomadic, these are mostly peaceful mammals." in self.quirks and self.pack < 2:
            self.pack = 2

        self.set_size(self.sizeRoll, self.sizeRollModifier)
        self.set_strength(self.sizeRoll)
        self.set_endurance(self.sizeRoll)
        self.set_dexterity(self.sizeRoll)
        self.set_exotic_weapons(exoticWeaponRolls)
        self.set_weapon_and_damage_modifier()
        self.set_weapon_damage()
        self.set_armor()
        self.set_number_encountered()
        self.set_initiative()
        self.set_reactions()

        while quirk3 > 0:
            self.size = self.size / 2
            self.dexterity += roll_xdy(1, 6)
            quirk3 -= 1
        if quirk4 > 0:
            self.quirks = list(
                filter(
                    ("These animals have remarkably fast metabolisms, enabling them to recover quickly from injuries. They regain one lost Endurance point every other round of combat starting at the beginning of the second round.").__ne__,
                    self.quirks))
            self.quirks.append(
                "These animals have remarkably fast metabolisms, enabling them to recover quickly from injuries. They regain " +
                str(quirk4) +
                " lost Endurance point every other round of combat starting at the beginning of the second round.")
        if quirk11:
            if self.intelligence < 2:
                self.intelligence = 2
            if self.instinct < 12:
                self.instinct = 12

        if self.intelligence > 2:
            self.intelligence = 2


class Reptile(Animal):
    """
    Defines a reptile.

    Parameters:
        planet: Class instance
            The planet object the animal lives on. Valid classes are
            DwarfPlanet, TerrestrialPlanet, HelianPlanet.
        terrain: String
            The type of terrain that this animal calls home.
    """

    def __init__(self, planet, terrain):
        super(Reptile, self).__init__(planet, terrain)
        self.animalClass = "Reptile"
        self.armor += 1

        # Skills this class innately has.
        self.meleeNaturalWeapons = 0
        self.recon = 0
        self.survival = 0

        evolutionRollModifier = 0
        physicalSkillRolls = 0
        socialSkillRolls = 0
        evolutionSkillRolls = 0
        quirkRolls = 0
        exoticWeaponRolls = 0

        # Determine the diet and modify attributes.
        dietRoll = roll_xdy(1, 6)
        if dietRoll <= 4:
            self.diet = "Carnivore"
            self.dietDescription = "Deadly and merciless, carnivorous reptiles almost always bring their prey down through superior strength or speed and exhibit some of the most advanced venoms of the animal world. A bite from a reptile can be fatal due to their common use of poison."
            self.strength += 1
            self.dexterity += 1
            self.athletics = 0
            physicalSkillRolls += 1
        elif dietRoll == 5:
            self.diet = "Herbivore"
            self.dietDescription = "Typically slow and ponderous, plant-eating reptiles survive primarily through their size and resilience."
            self.endurance += 2
            self.pack += 1
            socialSkillRolls += 1
        else:
            self.diet = "Omnivore"
            self.dietDescription = "These animals have an uncommon trait for their kind – a complex digestive system. While this makes them more adaptive than most of their class, it also has a tendency to limit their size and strength."
            evolutionRollModifier += 1
            self.endurance += 1
            physicalSkillRolls += 1
            socialSkillRolls += 1

        # Determine how many of each type of skill roll will be made.
        evoRollSkills = roll_xdy(1, 6) + evolutionRollModifier
        physicalSkillRolls += 1
        if evoRollSkills == 4 or evoRollSkills == 6:
            physicalSkillRolls += 1
        if evoRollSkills == 3 or evoRollSkills == 5 or evoRollSkills == 7:
            socialSkillRolls += 1
        if evoRollSkills >= 5:
            evolutionSkillRolls += 1

        # Roll for "other" evolutionary benefits.
        evoOtherRolls = 1
        while evoOtherRolls > 0:
            evoRollOther = roll_xdy(1, 6) + evolutionRollModifier
            if evoRollOther == 1:
                self.endurance += 2
                self.dexterity += 1
            elif evoRollOther == 2:
                self.strength += 2
            elif evoRollOther == 3:
                self.dexterity += 1
                self.pack += 1
            elif evoRollOther == 4:
                self.endurance += roll_xdy(1, 6)
            elif evoRollOther == 5:
                self.sizeRollModifier += 1
            elif evoRollOther == 6:
                quirkRolls += 2
            else:
                evoOtherRolls += 1
                continue

            evoOtherRolls -= 1

        # Roll for quirks.
        quirk2 = False
        quirk4 = 0
        quirk6 = False
        quirk7 = False
        quirk8 = False
        quirk9 = 0
        while quirkRolls > len(self.quirks):
            quirkRoll = roll_xdy(2, 6)
            if quirkRoll == 2 and not quirk2:
                quirk2 = True
                self.quirks.append(
                    "Outlandish colours and adaptations make this reptile a bizarre sight and remarkably intimidating to other non-sentient species.")
            if quirkRoll == 3:
                self.quirks.append(
                    "Mottled in appearance and adapted to its surroundings.")
                self.raise_skill_level("stealth", 1)
            if quirkRoll == 4:
                quirk4 += 1
                self.quirks.append(
                    "Several of the scales on this reptile are jagged and sharp, letting it inflict 4 + the Effect in damage when it grapples. This becomes its main way to hunt if the animal eats live prey.")
            if quirkRoll == 5:
                self.quirks.append(
                    "Able to go dormant for long periods of time, these reptiles may go for weeks or even months between meals.")
                self.raise_skill_level("survival", 1)
            if quirkRoll == 6 and not quirk6:
                quirk6 = True
                self.quirks.append(
                    "This reptile buries itself in its terrain, blending in and waiting for prey to ensnare.")
                dietRoll = roll_xdy(1, 5)
                if dietRoll == 5:
                    self.diet = "Carnivore"
                    self.dietDescription = "Deadly and merciless, carnivorous reptiles almost always bring their prey down through superior strength or speed and exhibit some of the most advanced venoms of the animal world. A bite from a reptile can be fatal due to their common use of poison."
                else:
                    self.diet = "Omnivore"
                    self.dietDescription = "These animals have an uncommon trait for their kind – a complex digestive system. While this makes them more adaptive than most of their class, it also has a tendency to limit their size and strength."
                self.behaviors.add("Trapper")
                self.raise_skill_level("stealth", 1)
            if quirkRoll == 7 and not quirk7:
                quirk7 = True
                self.quirks.append(
                    "These reptiles see heat, allowing them to have normal vision even in total darkness.")
            if quirkRoll == 8 and not quirk8:
                quirk8 = True
                self.quirks.append("Capable of flying, these reptiles have adapted body structures that generate heat through wind friction, allowing them to stay warm during flight. They do not sleep, they never land intentionally and will die within 1d6 hours if grounded.")
                self.primaryMovement = "Fly"
            if quirkRoll == 9:
                quirk9 += 1
                self.quirks.append(
                    "Unlike other reptiles, these animals have no scales and rely on a dense hide for defence.")
            if quirkRoll == 10:
                self.quirks.append(
                    "An oddity even within an evolutionarily diverse class, this reptile has a very complex genetic history.")
                exoticWeaponRolls += 2
            if quirkRoll == 11:
                self.quirks.append(
                    "Relative safety in its environment has allowed this species to evolve mentally.")
                self.intelligence += 1
            if quirkRoll == 12:
                quirkRolls += 1

        # Roll for evolutionary skills.
        while evolutionSkillRolls > 0:
            evoSkillRoll = roll_xdy(1, 6)
            if evoSkillRoll == 1:
                exoticWeaponRolls += 1
            elif evoSkillRoll == 2:
                self.raise_skill_level("meleeNaturalWeapons", 1)
            elif evoSkillRoll == 3:
                self.pack += 1
                self.dexterity += 1
            elif evoSkillRoll == 4:
                physicalSkillRolls += 1
            elif evoSkillRoll == 5:
                socialSkillRolls += 1
            else:
                exoticWeaponRolls += 1

            evolutionSkillRolls -= 1

        # Roll for social skills.
        while socialSkillRolls > 0:
            socialSkillRoll = roll_xdy(1, 6)
            if socialSkillRoll == 1:
                self.pack += 2
            elif socialSkillRoll == 2:
                self.instinct += 1
            elif socialSkillRoll == 3:
                self.raise_skill_level("stealth", 1)
            elif socialSkillRoll == 4:
                self.raise_skill_level("survival", 1)
            elif socialSkillRoll == 5:
                self.pack += 1
                self.instinct += 1
            else:
                self.raise_skill_level("recon", 1)

            socialSkillRolls -= 1

        # Roll for physical skills.
        while physicalSkillRolls > 0:
            physicalSkillRoll = roll_xdy(1, 6)
            if physicalSkillRoll == 1:
                self.strength += 1
            elif physicalSkillRoll == 2:
                self.endurance += 2
            elif physicalSkillRoll == 3:
                self.dexterity += 2
            elif physicalSkillRoll == 4:
                self.sizeRollModifier += 1
            elif physicalSkillRoll == 5:
                self.strength += 2
                self.endurance += 1
            else:
                self.raise_skill_level("meleeNaturalWeapons", 1)

            physicalSkillRolls -= 1

        # Roll for a behavior.
        if not quirk6:
            behaviorRoll = roll_xdy(1, 6)
            if self.diet == "Carnivore":
                if behaviorRoll == 1:
                    self.behaviors.add("Pouncer")
                elif behaviorRoll == 2:
                    self.behaviors.add("Killer")
                    self.reactionModifier += 1
                elif behaviorRoll == 3:
                    self.behaviors.add("Killer")
                    self.reactionModifier += 2
                elif behaviorRoll == 4:
                    self.behaviors.add("Intimidator")
                elif behaviorRoll == 5:
                    self.behaviors.add("Hunter")
                    self.reactionModifier += 1
                else:
                    self.behaviors.add("Hijacker")
            elif self.diet == "Herbivore":
                if behaviorRoll == 1:
                    self.behaviors.add("Gatherer")
                    self.reactionModifier -= 1
                elif behaviorRoll == 2:
                    self.behaviors.add("Intermittent")
                    self.reactionModifier -= 1
                elif behaviorRoll == 3:
                    self.behaviors.add("Intermittent")
                elif behaviorRoll == 4:
                    self.behaviors.add("Intermittent")
                    self.reactionModifier += 1
                elif behaviorRoll == 5:
                    self.behaviors.add("Grazer")
                    self.reactionModifier -= 1
                else:
                    self.behaviors.add("Grazer")
            else:
                if behaviorRoll == 1:
                    self.behaviors.add("Carrion-Eater")
                    self.reactionModifier -= 1
                elif behaviorRoll == 2:
                    self.behaviors.add("Gatherer")
                elif behaviorRoll == 3:
                    self.behaviors.add("Hijacker")
                    self.reactionModifier += 1
                elif behaviorRoll == 4:
                    self.behaviors.add("Hunter")
                elif behaviorRoll == 5:
                    self.behaviors.add("Hunter")
                    self.reactionModifier += 1
                else:
                    self.behaviors.add("Reducer")

        self.behavior_effects()
        self.set_size(self.sizeRoll, self.sizeRollModifier)
        self.set_strength(self.sizeRoll)
        self.set_endurance(self.sizeRoll)
        self.set_dexterity(self.sizeRoll)
        self.set_exotic_weapons(exoticWeaponRolls)
        self.set_weapon_and_damage_modifier()
        self.set_weapon_damage()
        self.set_armor()
        self.set_number_encountered()
        self.set_initiative()
        self.set_reactions()

        if quirk4 > 0:
            self.quirks = list(
                filter(
                    ("Several of the scales on this reptile are jagged and sharp, letting it inflict 4 + the Effect in damage when it grapples. This becomes its main way to hunt if the animal eats live prey.").__ne__,
                    self.quirks))
            self.quirks.append(
                "Several of the scales on this reptile are jagged and sharp, letting it inflict " +
                str(4 * quirk4) +
                    " + the Effect in damage when it grapples. This becomes its main way to hunt if the animal eats live prey.")
        while quirk9 > 0:
            self.dexterity += roll_xdy(1, 6)
            self.armor = self.armor / 2
            quirk9 -= 1

        if self.intelligence > 2:
            self.intelligence = 2

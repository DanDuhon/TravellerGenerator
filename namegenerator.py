import collections

from random import choice, sample, randint


class NameGenerator:
    def __init__(self, filename, double=False, track=True):
        """
        Generates the lists of the various n-grams that are used to generate
        names.

        Parameters:
            filename: Location of name list with one name per line
            double: provide a double name for use by animals
            track: check for name uniqueness
        """

        self.double = double
        self.track = track
        self.existingNames = ["Terra", "Luna", "Terran"]

        self.firstGrams = collections.defaultdict(set)
        self.middleGrams = collections.defaultdict(set)
        self.lastGrams = collections.defaultdict(set)
        self.namelengths = collections.defaultdict(int)

        with open(filename) as f:
            for rawName in f:
                name = rawName[:-1].replace("_", " ")
                for letter in range(4):
                    lookup = name[:letter]
                    self.firstGrams[lookup].add(name[letter])
                for letter in range(1, len(name) - 5):
                    lookup = name[letter:letter + 3]
                    self.middleGrams[lookup].add(name[letter + 3])
                self.lastGrams[name[-4:-2]].add(name[-2:])
                self.namelengths[len(name)] += 1

    def _get_length(self, minlength=0):
        """
        Gets a random length from the input set
        This provides a target length for the generating process

        Parameters:
            minlength: Specificies a minimum length

        Errors:
            raises ValueError if minlength is higher than all available words
        """
        totalwords = 0
        for length, cnt in self.namelengths.items():
            if length >= minlength:
                totalwords += cnt

        if totalwords == 0:
            raise ValueError("Minlength too high")

        wordselection = randint(0, totalwords - 1)
        cumulativewords = 0
        for length, cnt in self.namelengths.items():
            if length >= minlength:
                cumulativewords += cnt
                if cumulativewords > wordselection:
                    return length

    def _generate_name_attempt(self, minlength=0):
        """
        Generates a name based on lists of n-grams.
        """
        length = self._get_length(minlength)
        while True:
            try:
                name = ""
                for letter in range(length - 2):
                    if letter < 4:
                        name += choice(list(self.firstGrams[name]))
                    else:
                        name += choice(list(self.middleGrams[name[-3:]]))
                name += choice(list(self.lastGrams[name[-2:]]))
                return name
            except IndexError:
                # This fails if there are 0 options available for a choice function.
                # In this case, we simply try again with the same length.
                pass

    def generate_name(self):
        """
        Generates a name based on lists of n-grams. If double is set
        this function creates two names, like a scientific name for an organism.
        To help prevent duplicate names, if a short length is chosen for the
        first name, a longer name must be chosen for the second name. Because
        there are so many animals generated, animals do not check for duplicate
        names. You'll just have to hope you don't run into one.
        """
        while True:
            name = self._generate_name_attempt()
            if self.double:
                name2 = self._generate_name_attempt(
                    max(self.namelengths) - len(name))
                # Randomly swaps the names
                name = " ".join(sample([name, name2], 2))
            if not self.track:
                return name
            if name not in self.existingNames:
                self.existingNames.append(name)
                return name


astralNGrams = NameGenerator("namesastral.txt")

alienNGrams = NameGenerator("namesalien.txt")

animalNGrams = NameGenerator("namesanimal.txt", double=True, track=False)

if __name__ == "__main__":
    print("Astral Name Sample".center(30, "="))
    for x in range(10):
        print(astralNGrams.generate_name())
    print("Alien Name Sample".center(30, "="))
    for x in range(10):
        print(alienNGrams.generate_name())
    print("Animal Name Sample".center(30, "="))
    for x in range(10):
        print(animalNGrams.generate_name())

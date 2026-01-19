from numpy import double

# Base Island class


class Island:
    def __init__(self, temperature: float, size: float, isolation: bool):
        self.temperature = temperature
        self.size = size
        self.isolation = isolation

# Ecosystem and its lifeforms


class Ecosystem():

    area = 50
    # each spaces is measured with unit
    # def init(self):


class Lifeforms(Ecosystem):
    def init(self, starting_population: int, minsize: int, maxsize: int, growrate: float, reproducerate: float, island=None):
        self.population = starting_population
        self.age = 0
        self.minsize = minsize
        self.currentsize = minsize
        self.maxsize = maxsize
        self.growrate = growrate
        self.reproducerate = reproducerate
        self.island = island

    def grow(self):
        pass

    def reproduce(self):
        pass

# Flora base class


class Flora(Lifeforms):
    def init(self, starting_population, minsize, maxsize, growrate, reproducerate, needSunlight: bool, expandRate: float, maxIndividualArea: int):
        super().init(starting_population, minsize, maxsize, growrate, reproducerate)
        self.needSunlight = needSunlight
        self.expandRate = expandRate
        self.maxIndividualArea = maxIndividualArea

    def expand(self):
        pass

# Species of flora


class MangoTree(Flora):
    def init(self, starting_population=10, minsize=1, maxsize=10, growrate=0.1, reproducerate=0.05, needSunlight=True, expandRate=0.02, maxIndividualArea=5,
             isFruiting: bool = False, fruitRate: float = 0.1, fruitYield: int = 20):
        super().init(starting_population, minsize, maxsize, growrate,
                     reproducerate, needSunlight, expandRate, maxIndividualArea)
        self.isFruiting = isFruiting
        self.fruitRate = fruitRate
        self.fruitYield = fruitYield

    def fruiting(self):
        if self.isFruiting:
            self.fruitYield += int(self.population * self.fruitRate)


class Elderberry(Flora):
    def init(self, starting_population=15, minsize=1, maxsize=8, growrate=0.15, reproducerate=0.07, needSunlight=True, expandRate=0.03, maxIndividualArea=4,
             isFruiting: bool = False, fruitRate: float = 0.12, berryYield: int = 25):
        super().init(starting_population, minsize, maxsize, growrate,
                     reproducerate, needSunlight, expandRate, maxIndividualArea)
        self.isFruiting = isFruiting
        self.fruitRate = fruitRate
        self.berryYield = berryYield

    def fruiting(self):
        if self.isFruiting:
            self.berryYield += int(self.population * self.fruitRate)


class Grass(Flora):
    def init(self, starting_population=100, minsize=0.1, maxsize=1, growrate=0.2, reproducerate=0.1, needSunlight=True, expandRate=0.05, maxIndividualArea=1):
        super().init(starting_population, minsize, maxsize, growrate,
                     reproducerate, needSunlight, expandRate, maxIndividualArea)


# Fauna base class
class Fauna(Lifeforms):
    def init(self, starting_population, minsize, maxsize, growrate, reproducerate, nutrientNeed: str, starveRate: float, health: float, selfHarmEffect: float,
             healEffect: float):
        super().init(starting_population, minsize, maxsize, growrate, reproducerate)
        self.nutrientNeed = nutrientNeed
        self.starveRate = starveRate
        self.health = health
        self.selfHarmEffect = selfHarmEffect
        self.healEffect = healEffect

    def consume(self):
        pass

    def starvation(self):
        pass

# Classes of fauna


class Carnivore(Fauna):
    def init(self, starting_population, minsize, maxsize, growrate, reproducerate, nutrientNeed, starveRate,
             health, selfHarmEffect, healEffect, eatMeat: bool, huntSuccessRate: float, selfHarmRate: float):
        super().init(starting_population, minsize, maxsize, growrate, reproducerate,
                     nutrientNeed, starveRate, health, selfHarmEffect, healEffect)
        self.eatMeat = eatMeat
        self.huntSuccessRate = huntSuccessRate
        self.selfHarmRate = selfHarmRate

    def hunt(self):
        pass


class Herbivore(Fauna):
    def init(self, starting_population, minsize, maxsize, growrate, reproducerate, nutrientNeed, starveRate,
             health, selfHarmEffect, healEffect, eatPlants: bool):
        super().init(starting_population, minsize, maxsize, growrate, reproducerate,
                     nutrientNeed, starveRate, health, selfHarmEffect, healEffect)
        self.eatPlants = eatPlants


class Omnivore(Fauna):
    def init(self, starting_population, minsize, maxsize, growrate, reproducerate, nutrientNeed, starveRate,
             health, selfHarmEffect, healEffect, eatAll: bool, huntSuccessRate: float, selfHarmRate: float):
        super().init(starting_population, minsize, maxsize, growrate, reproducerate,
                     nutrientNeed, starveRate, health, selfHarmEffect, healEffect)

    def hunt(self):
        pass

# Species of fauna


class Leopard(Carnivore):
    def init(self, starting_population=5, minsize=1, maxsize=3, growrate=0.1, reproducerate=0.05, nutrientNeed="meat", starveRate=0.1,
             health=100, selfHarmEffect=5, healEffect=10, eatMeat=True, huntSuccessRate=0.6, selfHarmRate=0.05):
        super().init(starting_population, minsize, maxsize, growrate, reproducerate, nutrientNeed, starveRate,
                     health, selfHarmEffect, healEffect, eatMeat, huntSuccessRate, selfHarmRate)


class Rabbit(Herbivore):
    def init(self, starting_population=30, minsize=0.2, maxsize=0.5, growrate=0.2, reproducerate=0.1, nutrientNeed="plants", starveRate=0.15,
             health=80, selfHarmEffect=3, healEffect=8, eatPlants=True):
        super().init(starting_population, minsize, maxsize, growrate, reproducerate, nutrientNeed, starveRate,
                     health, selfHarmEffect, healEffect, eatPlants)


class Fox(Omnivore):
    def init(self, starting_population=15, minsize=0.5, maxsize=1.5, growrate=0.15, reproducerate=0.07, nutrientNeed="all", starveRate=0.12,
             health=90, selfHarmEffect=4, healEffect=9, eatAll=True, huntSuccessRate=0.5, selfHarmRate=0.04):
        super().init(starting_population, minsize, maxsize, growrate, reproducerate, nutrientNeed, starveRate,
                     health, selfHarmEffect, healEffect, eatAll, huntSuccessRate, selfHarmRate)

__author__ = "8407548, Winata, 8655943, Quan"
import random

# Ecosystem and its lifeforms


class Ecosystem():

    def __init__(self, size: float, days: int, temperature: int):
        self.size = size
        self.day = 0
        self.weathercon = None
        self.temperature = temperature
        self.flora = []
        self.fauna = []

    def add_organism(self, organism):
        """
        Test 1: Adding a plant places it in flora
        >>> eco = Ecosystem(100, 10, 25)
        >>> g = Grass()
        >>> eco.add_organism(g)
        >>> len(eco.flora)
        1
        >>> len(eco.fauna)
        0

        Test 2: Adding an animal places it in fauna
        >>> r = Rabbit()
        >>> eco.add_organism(r)
        >>> len(eco.fauna)
        1

        Test 3: Organism receives correct island reference
        >>> eco2 = Ecosystem(50, 5, 20)
        >>> e = Eucalyptus()
        >>> eco2.add_organism(e)
        >>> e.island is eco2
        True
        """
        organism.island = self
        if isinstance(organism, Flora):
            self.flora.append(organism)
        elif isinstance(organism, Fauna):
            self.fauna.append(organism)

    def available_area(self) -> float:
        """
        Test 1: Empty ecosystem → full area
        >>> eco = Ecosystem(size=100, days=10, temperature=25)
        >>> eco.available_area()
        100

        Test 2: Adding one plant took area
        >>> g = Grass()
        >>> eco.add_organism(g)
        >>> eco.available_area() <= 100
        True

        Test 3: Area available never be negative
        >>> eco.size = 0
        >>> eco.available_area()
        0
        """
        used_area = sum(p.maxIndividualArea for p
                        in self.flora if p.is_alive())
        return max(0, self.size - used_area)

    def environment(self):
        self.temperature = random.randrange(22, 40)
        r = random.random()
        if r < 0.3:
            self.weathercon = "windy"
        elif r < 0.4:
            self.weathercon = "storm"
        else:
            self.weathercon = "normal"

    def apply_environment_effects(self):
        # --- WINDY ---
        if self.weathercon == "windy":
            for plant in self.flora:
                plant.current_expand_modifier = 1.5

        # --- STORM ---
        if self.weathercon == "storm":
            if self.flora:
                random.choice(self.flora).die()
            if self.fauna:
                random.choice(self.fauna).die()

        # --- HIGH TEMPERATURE ---
        if self.temperature >= 36:
            for animal in self.fauna:
                if hasattr(animal, "huntSuccessRate"):
                    animal.current_hunt_modifier = 0.5

    def simulate_step(self):
        self.day += 1
        new_organisms = []

        # Age all organisms
        for plant in self.flora:
            plant.age += 1
        for animal in self.fauna:
            animal.age += 1

        # Reset daily modifiers
        for plant in self.flora:
            plant.current_expand_modifier = 1.0
        for animal in self.fauna:
            animal.current_hunt_modifier = 1.0

        self.environment()

        self.apply_environment_effects()

        # Plants grow and reproduce
        total_free_area = self.available_area()

        # Collect requests
        requests = []
        for plant in self.flora:
            requested = plant.expansion_request()
            if requested > 0:
                requests.append((plant, requested))

        random.shuffle(requests)  # fairness

        for plant, requested in requests:
            max_possible = int(total_free_area // plant.maxIndividualArea)
            granted = min(requested, max_possible)

            for _ in range(granted):
                new_plant = plant.__class__()
                new_plant.island = self
                self.flora.append(new_plant)

            total_free_area -= granted * plant.maxIndividualArea
            if total_free_area <= 0:
                break
        for plant in self.flora:
            plant.grow()

        for plant in self.flora:
            plant.fruiting()
        # Animals eat
        for animal in self.fauna:
            if isinstance(animal, Herbivore):
                animal.forage(self.flora)
            elif isinstance(animal, Carnivore):
                animal.hunt(self.fauna)
            elif isinstance(animal, Omnivore):
                if random.random() < 0.5:
                    animal.forage(self.flora)
                else:
                    animal.hunt(self.fauna)

            # make the animals starve
            animal.starvation()

            # Animal reproduces
            offspring = animal.reproduce()
            new_organisms.extend(offspring)

        # Add all newborns
        for organism in new_organisms:
            self.add_organism(organism)

        # Remove dead
        self.flora = [p for p in self.flora if p.is_alive()]
        self.fauna = [a for a in self.fauna if a.is_alive()]

        # Print stats
        # print(f"Day {self.day}: {len(self.flora)} plants,
        # {len(self.fauna)} animals")

    def message(self):
        # Count each organism type
        eucalyptus_num = sum(1 for plant in self.flora
                             if isinstance(plant, Eucalyptus))

        mango_num = sum(1 for plant in self.flora
                        if isinstance(plant, MangoTree))

        elderberry_num = sum(1 for plant in self.flora
                             if isinstance(plant, Elderberry))

        grass_num = sum(1 for plant in self.flora
                        if isinstance(plant, Grass))

        rabbit_num = sum(1 for animal in self.fauna
                         if isinstance(animal, Rabbit))

        koala_num = sum(1 for animal in self.fauna
                        if isinstance(animal, Koala))

        fox_num = sum(1 for animal in self.fauna
                      if isinstance(animal, Fox))

        leopard_num = sum(1 for animal in self.fauna
                          if isinstance(animal, Leopard))

        print(f"Day {self.day}:")
        print(f"Weather = {self.weathercon},"
              f" Temperature = {self.temperature}")
        print(f"  Plants: Eucalyptus={eucalyptus_num},"
              f" Mango={mango_num}, Elderberry={elderberry_num},"
              f" Grass={grass_num}")
        print(f"  Animals: Rabbit={rabbit_num}, Koala={koala_num},"
              f" Fox={fox_num}, Leopard={leopard_num}")
        print(f"  Total: {len(self.flora)} plants,"
              f" {len(self.fauna)} animals\n")


class Lifeforms():
    def __init__(self, minsize: int, maxsize: int, growrate: float,
                 reproducerate: float, island=None):
        self.age = 0
        self.minsize = minsize
        self.currentsize = minsize
        self.maxsize = maxsize
        self.growrate = growrate
        self.reproducerate = reproducerate
        self.island = island
        self.alive = True

    def grow(self):
        """
        Individual organism grows

        Test 1: normal growth
        >>> lf = Lifeforms(1, 10, 0.5, 0.1)
        >>> lf.currentsize
        1
        >>> lf.grow()
        1.5
        >>> lf.grow()
        2.25

        Test 2: maxsize cap
        >>> lf.currentsize = 9
        >>> lf.grow()
        10

        Test 3: dead organism does not grow
        >>> lf2 = Lifeforms(1, 10, 0.5, 0.1)
        >>> lf2.die()
        >>> lf2.grow()
        1
        """
        if self.is_alive():
            self.currentsize = min(self.currentsize * (1 + self.growrate),
                                   self.maxsize)
        return self.currentsize

    def is_alive(self):
        """
        Test 1:
        >>> lf = Lifeforms(1, 5, 0.1, 0.1)
        >>> lf.is_alive()
        True

        Test 2:
        >>> lf.die()
        >>> lf.is_alive()
        False

        Test 3:
        >>> lf2 = Lifeforms(1, 5, 0.1, 0.1)
        >>> lf2.alive = False
        >>> lf2.is_alive()
        False
        """
        return self.alive

    def die(self):
        """
        Kill the organism

        Test 1: 
        >>> lf = Lifeforms(1, 5, 0.1, 0.1)
        >>> lf.is_alive()
        True
        >>> lf.die()
        >>> lf.is_alive()
        False

        Test 2: 
        >>> lf.die()
        >>> lf.is_alive()
        False

        Test 3: 
        >>> lf2 = Lifeforms(1, 5, 0.1, 0.1)
        >>> lf2.die()
        >>> lf2.is_alive()
        False
        """
        self.alive = False


# Flora base class


class Flora(Lifeforms):
    def __init__(self, minsize, maxsize, growrate, reproducerate,
                 expandRate: float, maxIndividualArea: int):
        super().__init__(minsize, maxsize, growrate, reproducerate)
        self.expandRate = expandRate
        self.maxIndividualArea = maxIndividualArea
        self.current_expand_modifier = 1.0
        self.fruitYield = 0
        self.berryYield = 0
        self.isFruiting = False
        self.isBerrying = False

    def expansion_request(self):
        """ 
        Adds new individuals based on expandRate

        Test 1: Cannot expand when too small:
        >>> f = Flora(1, 10, 0.1, 0.1, expandRate=1.0, maxIndividualArea=2) 
        >>> f.currentsize = 4 
        >>> f.expansion_request() 
        0

        Test 2: Can expand when mature enough:
        >>> f.currentsize = 6 
        >>> isinstance(f.expansion_request(), int) 
        True

        Test 3: Cannot expand when expandRate is 0: 
        >>> f.expandRate = 0 
        >>> f.expansion_request() 
        0
        """
        # Only expand if mature enough

        total_new_plants = 0
        if self.currentsize >= self.maxsize * 0.5:
            # Calculate exact number (can be fractional)
            exact_new_plants = (1 * self.expandRate *
                                self.current_expand_modifier)
            # Each plant can spawn based on expandRate

            # Guaranteed new plants (integer part)
            guaranteed_plants = int(exact_new_plants)

            # Fractional part (0.0 to 0.99...)
            fractional_part = exact_new_plants - guaranteed_plants

            # Probabilistically add one more based on fraction
            bonus_plant = 1 if random.random() < fractional_part else 0

            total_new_plants = guaranteed_plants + bonus_plant

        return total_new_plants

    def is_alive(self):
        """
        Test 1:
        >>> f = Flora(2, 10, 0.1, 0.1, 0.2, 3)
        >>> f.currentsize = 3
        >>> f.is_alive()
        True

        Test 2:
        >>> f.currentsize = 1
        >>> f.is_alive()
        False

        Test 3:
        >>> f.alive = False
        >>> f.is_alive()
        False
        """
        return self.alive and self.currentsize >= self.minsize

    def die(self):
        self.alive = False

    def fruiting(self):
        # Default: do nothing
        pass

    def beEaten(self, amount, eater=None):
        """ 
        Harvest fruits or berries without reducing plant height.
        amount: how many units of edible part to eat
        eater: optional, for special logic like Koala

        Test 1: Normal eating
        >>> f = Flora(2, 10, 0.1, 0.1, 0.2, 3) 
        >>> f.currentsize = 5 
        >>> f.beEaten(2) 
        2
        >>> f.currentsize
        3

        Test 2: Too much eating could kills plant: 
        >>> f.beEaten(5) 
        3
        >>> f.is_alive() 
        False

        Test 3: No eating
        >>> f2 = Flora(2, 10, 0.1, 0.1, 0.2, 3) 
        >>> f2.beEaten(0) 
        0
        """
        eaten = 0

        # Check type of plant to decide what to reduce
        if self.__class__.__name__ == "MangoTree" and self.fruitYield > 0:
            eaten = min(amount, self.fruitYield)
            self.fruitYield -= eaten

        elif self.__class__.__name__ == "Elderberry" and self.berryYield > 0:
            eaten = min(amount, self.berryYield)
            self.berryYield -= eaten

        else:
            # Default: reduce plant size if edible
            eaten = min(amount, self.currentsize)
            self.currentsize -= eaten
            if self.currentsize < self.minsize:
                self.die()

        return eaten

# Species of flora


class Eucalyptus(Flora):
    def __init__(self, minsize=2, maxsize=15, growrate=0.2, reproducerate=0.1,
                 expandRate=0.4, maxIndividualArea=6):
        super().__init__(minsize, maxsize, growrate,
                         reproducerate, expandRate, maxIndividualArea)

    def beEaten(self, amount, eater=None):
        """
        Override: Only Koalas can eat Eucalyptus.

        Test 1: Non‑koala cannot eat:
        >>> e = Eucalyptus()
        >>> e.currentsize = 5
        >>> e.beEaten(2)
        0

        Test 2: only Koala can eat:
        >>> k = Koala()
        >>> eaten = e.beEaten(1, eater=k)
        >>> eaten in (0, 1)
        True

        Test 3: Eating cannot kill eucalyptus unless size < minsize:
        >>> e.currentsize = 2
        >>> e.beEaten(1, eater=k) in (0, 1)
        True
        """
        if eater is None or eater.__class__.__name__ != "Koala":
            return 0
        return super().beEaten(amount, eater)


class MangoTree(Flora):
    def __init__(self, minsize=1, maxsize=10, growrate=0.1, reproducerate=0.05,
                 expandRate=0.2, maxIndividualArea=5, isFruiting: bool = True,
                 fruitRate: float = 0.1, maxFruit: int = 30):
        super().__init__(minsize, maxsize, growrate,
                         reproducerate, expandRate, maxIndividualArea)
        self.isFruiting = isFruiting
        self.fruitRate = fruitRate
        self.fruitYield = 0
        self.maxFruit = maxFruit

    def fruiting(self):
        """
        Test 1: Normal fruiting
        >>> m = MangoTree()
        >>> m.currentsize = 10
        >>> m.fruitYield = 0
        >>> m.fruiting()
        0
        >>> m.fruitYield > 0
        True

        Test 2: Max fruit cap
        >>> m.fruitYield = m.maxFruit
        >>> m.fruiting()
        0
        >>> m.fruitYield == m.maxFruit
        True

        Test 3: fruiting not possible
        >>> m = MangoTree(isFruiting=False)
        >>> m.currentsize = 10
        >>> m.berryYield = 0
        >>> m.fruiting()
        0
        >>> m.berryYield
        0
        """
        if self.isFruiting:
            # make fruits propotional to it's size
            self.fruitYield = min(self.fruitYield + int(
                self.currentsize * self.fruitRate), self.maxFruit)
        return 0


class Elderberry(Flora):
    def __init__(self, minsize=1, maxsize=8, growrate=0.15, reproducerate=0.07,
                 expandRate=0.3, maxIndividualArea=4, isBerrying: bool = True,
                 berryRate: float = 0.12, maxBerry: int = 75):
        super().__init__(minsize, maxsize, growrate,
                         reproducerate, expandRate, maxIndividualArea)
        self.isBerrying = isBerrying
        self.berryRate = berryRate
        self.berryYield = 0
        self.maxBerry = maxBerry

    def fruiting(self):
        """
        Test 1: normal fruiting 
        >>> e = Elderberry()
        >>> e.currentsize = 10
        >>> e.berryYield = 0
        >>> e.fruiting()
        0
        >>> e.berryYield > 0
        True

        Test 2: max berry cap
        >>> e.berryYield = e.maxBerry
        >>> e.fruiting()
        0
        >>> e.berryYield == e.maxBerry
        True

        Test 3: fruiting not possible
        >>> e2 = Elderberry(isBerrying=False)
        >>> e2.currentsize = 10
        >>> e2.berryYield = 0
        >>> e2.fruiting()
        0
        >>> e2.berryYield
        0
        """
        if self.isBerrying:
            # make berries propotional to it's size
            self.berryYield = min(self.berryYield + int(
                self.currentsize * self.berryRate), self.maxBerry)
        return 0


class Grass(Flora):
    def __init__(self, minsize=0.1, maxsize=1, growrate=0.2,
                 reproducerate=0.1, expandRate=0.5, maxIndividualArea=1):
        super().__init__(minsize, maxsize, growrate,
                         reproducerate, expandRate, maxIndividualArea)


# Fauna base class


class Fauna(Lifeforms):
    def __init__(self, minsize, maxsize, growrate, reproducerate,
                 starveRate: float, health: float, selfHarmEffect: float,
                 healEffect: float):
        super().__init__(minsize, maxsize, growrate, reproducerate)
        self.starveRate = starveRate
        self.hunger = 0
        self.health = health
        self.selfHarmEffect = selfHarmEffect
        self.healEffect = healEffect
        self.current_hunt_modifier = 1.0

    def is_alive(self):
        """Override: fauna dies if health <= 0 or size <= 0

        Test 1:
        >>> a = Fauna(1, 5, 0.1, 0.1, 0.1, 50, 1, 1)
        >>> a.is_alive()
        True

        Test 2:
        >>> a.health = 0
        >>> a.is_alive()
        False

        Test 3:
        >>> a.health = 50
        >>> a.currentsize = 0
        >>> a.is_alive()
        False
        """
        return self.alive and self.health > 0 and self.currentsize > 0

    def starvation(self):
        """Check if animal is starving

        Test 1: Hunger increases
        >>> a = Fauna(1, 5, 0.1, 0.1, starveRate=1, health=50, selfHarmEffect=1, healEffect=1)
        >>> a.hunger = 3
        >>> a.starvation()
        >>> a.health < 50
        True

        Test 2: Death due to starvation 
        >>> a2 = Fauna(1, 5, 0.1, 0.1, 1, 1, 1, 1)
        >>> a2.hunger = 4
        >>> a2.starvation()
        >>> a2.is_alive()
        False

        Test 3: No starvation if hunger low:
        >>> a3 = Fauna(1, 5, 0.1, 0.1, 1, 100, 1, 1)
        >>> a3.hunger = 0
        >>> a3.starvation()
        >>> a3.health == 100
        True

        """
        self.hunger += 1
        if self.hunger > 3:  # Hasn't eaten in 3 days
            self.health -= self.starveRate * 10
            if self.health <= 0:
                self.die()

    def reproduce(self):
        """
        Test 1: Too unhealthy → no offspring
        >>> a = Fauna(1, 10, 0.1, reproducerate=0.5, starveRate=1, health=30, selfHarmEffect=1, healEffect=1)
        >>> a.reproduce()
        []

        Test 2: Too small → no offspring
        >>> a.health = 100
        >>> a.currentsize = 1
        >>> a.reproduce()
        []

        Test 3: 
        >>> a.currentsize = 5
        >>> a.reproduce()
        []
        """
        # Fauna is an abstract base class for animals.
        # It cannot create babies because it requires many arguments.
        # Therefore only subclasses (Rabbit, Fox, Koala, Leopard) can reproduce.

        offspring = []

        # Only reproduce if healthy and mature
        if self.health > 60 and self.currentsize >= self.maxsize * 0.7:
            # Calculate exact number (can be fractional)
            exact_new_animals = 1 * self.reproducerate

            # Guaranteed new animals (integer part)
            guaranteed_animals = int(exact_new_animals)

            # Fractional part
            fractional_part = exact_new_animals - guaranteed_animals

            # Probabilistically add one more
            bonus_animal = 1 if random.random() < fractional_part else 0

            total_new_animals = guaranteed_animals + bonus_animal

            # Create the new animals
            for _ in range(total_new_animals):
                baby = self.__class__()
                baby.currentsize = self.minsize
                baby.health = 50  # Babies start with lower health
                offspring.append(baby)

        return offspring

# Classes of fauna


class Carnivore(Fauna):
    def __init__(self, minsize, maxsize, growrate, reproducerate,
                 starveRate, health, selfHarmEffect, healEffect,
                 huntSuccessRate: float, selfHarmRate: float):
        super().__init__(minsize, maxsize, growrate, reproducerate,
                         starveRate, health, selfHarmEffect, healEffect)
        self.huntSuccessRate = huntSuccessRate
        self.selfHarmRate = selfHarmRate

    def hunt(self, fauna_list):
        """Hunt other animals"""
        if not self.is_alive():
            return

        # Find potential prey (smaller animals)
        prey_list = [animal for animal in fauna_list
                     if animal.is_alive()
                     and animal != self
                     and animal.currentsize < self.currentsize]

        if prey_list:
            target = random.choice(prey_list)
            if random.random() < (self.huntSuccessRate *
                                  self.current_hunt_modifier):
                # Successful hunt
                self.health = min(100, self.health + self.healEffect)
                self.hunger = 0
                target.die()

            # Failed hunt - self harm
            if random.random() < self.selfHarmRate:
                self.health -= self.selfHarmEffect


class Herbivore(Fauna):
    def __init__(self, minsize, maxsize, growrate, reproducerate, starveRate,
                 health, selfHarmEffect, healEffect):
        super().__init__(minsize, maxsize, growrate, reproducerate,
                         starveRate, health, selfHarmEffect, healEffect)

    def forage(self, flora_list):
        """Eat plants"""
        if not self.is_alive():
            return

        # Find edible plants
        edible_plants = [plant for plant in flora_list if plant.is_alive()]

        if edible_plants:
            target = random.choice(edible_plants)
            amount_eaten = target.beEaten(1, eater=self)
            if amount_eaten > 0:
                self.health = min(100, self.health + self.healEffect)
                self.hunger = 0


class Omnivore(Fauna):
    def __init__(self, minsize, maxsize, growrate, reproducerate, starveRate,
                 health, selfHarmEffect, healEffect,
                 huntSuccessRate: float, selfHarmRate: float):
        super().__init__(minsize, maxsize, growrate, reproducerate,
                         starveRate, health, selfHarmEffect, healEffect)
        self.huntSuccessRate = huntSuccessRate
        self.selfHarmRate = selfHarmRate

    def hunt(self, fauna_list):
        """Hunt other animals (same as Carnivore)"""
        if not self.is_alive():
            return

        prey_list = [animal for animal in fauna_list
                     if animal.is_alive()
                     and animal != self
                     and animal.currentsize < self.currentsize]

        if prey_list:
            target = random.choice(prey_list)
            if random.random() < (self.huntSuccessRate *
                                  self.current_hunt_modifier):
                # Successful hunt - prey dies immediately
                self.health = min(100, self.health + self.healEffect)
                self.hunger = 0
                target.die()
            if random.random() < self.selfHarmRate:
                self.health -= self.selfHarmEffect

    def forage(self, flora_list):
        """Eat plants (same as Herbivore)"""
        if not self.is_alive():
            return

        edible_plants = [plant for plant in flora_list if plant.is_alive()]

        if edible_plants:
            target = random.choice(edible_plants)
            amount_eaten = target.beEaten(1, eater=self)
            if amount_eaten > 0:
                self.health = min(100, self.health + self.healEffect)
                self.hunger = 0

# Species of fauna


class Leopard(Carnivore):
    def __init__(self, minsize=1, maxsize=3, growrate=0.1, reproducerate=0.05,
                 starveRate=0.1, health=100, selfHarmEffect=5, healEffect=10,
                 huntSuccessRate=0.6, selfHarmRate=0.05):
        super().__init__(minsize, maxsize, growrate, reproducerate,
                         starveRate, health, selfHarmEffect, healEffect,
                         huntSuccessRate, selfHarmRate)


class Rabbit(Herbivore):
    def __init__(self, minsize=0.2, maxsize=0.5, growrate=0.2,
                 reproducerate=0.1, starveRate=0.15, health=80,
                 selfHarmEffect=3, healEffect=8):
        super().__init__(minsize, maxsize, growrate, reproducerate, starveRate,
                         health, selfHarmEffect, healEffect)


class Koala(Herbivore):
    def __init__(self, minsize=0.5, maxsize=1.2, growrate=0.15,
                 reproducerate=0.07, starveRate=0.12, health=70,
                 selfHarmEffect=4, healEffect=9):
        super().__init__(minsize, maxsize, growrate, reproducerate, starveRate,
                         health, selfHarmEffect, healEffect)


class Fox(Omnivore):
    def __init__(self, minsize=0.5, maxsize=1.5, growrate=0.15,
                 reproducerate=0.07, starveRate=0.12, health=90,
                 selfHarmEffect=4, healEffect=9, huntSuccessRate=0.5,
                 selfHarmRate=0.04):
        super().__init__(minsize, maxsize, growrate, reproducerate, starveRate,
                         health, selfHarmEffect, healEffect, huntSuccessRate,
                         selfHarmRate)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

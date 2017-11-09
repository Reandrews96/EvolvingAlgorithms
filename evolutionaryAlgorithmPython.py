'''Practice using python and design a basic evolutionary algorithm'''
'''Idea: Evolve a dog so that the best balance of protective and friendly happen'''
import random
import math

class EvolvingDog():
    def __init__(self, g):
        self.genome = g
        self.name = self.createName()

    def createName(self):
        names = ("Phillip", "Russ", "Spot", "Umami", "Ellie", "Buster", "Checkers", "Tom", "'Tom'", "Captain Morgan")
        return random.choice(names)

    def printTraits(self):
        str1 = self.name + " has scores of " + str(self.genome.size) + " for size, "
        str2 = str(self.genome.friendly) + " for friendliness, and "
        str3 = str(self.genome.protective) + " for protectiveness"
        print(str1 + str2 + str3)


class Genome():
    def __init__(self, size, friend, prot):
        self.size = round(size, 1)
        self.friendly = round(friend, 1)
        self.protective = round(prot, 1)

    def getSize(self):
        return self.size

    def getFriendly(self):
        return self.friendly

    def getProtective(self):
        return self.protective

    def duplicate(self):
        return Genome(self.size, self.friendly, self.protective)

    def mutate(self):
        chance = random.random()
        value = random.randrange(1,10,1)/10
        if chance < .33:
            self.size = self.size + value
            if self.size >= 10:
                self.size = 10
            if self.size <= 0:
                self.size = .1
        elif chance < .67:
            self.friendly = self.friendly + value
            if self.friendly >= 10:
                self.friendly = 10
            if self.friendly <= 0:
                self.friendly = .1
        else:
            self.protective = self.protective + value
            if self.protective >= 10:
                self.protective = 10
            if self.protective <= 0:
                self.protective = .1

    def crossover(g1, g2):
        chance = random.random()
        g1 = g1.duplicate()
        g2 = g2.duplicate()
        if chance < .5:
            chanceFlip = random.random()
            if chanceFlip < .33:
                temp = g1.size
                g1.size = g2.size
                g2.size = temp
            elif chanceFlip < .67:
                temp = g1.friendly
                g1.friendly = g2.friendly
                g2.friendly = temp
            else:
                temp = g1.protective
                g1.protective = g2.protective
                g2.protective = temp
        return g1, g2


class Evolution():
    def __init__(self, trials):
        self.trials = trials
        self.population = self.generatePopulation()

    def generatePopulation(self):
        dog1 = EvolvingDog(Genome(random.randrange(1,10,1), random.randrange(1,10,1), random.randrange(1,10,1)))
        dog2 = EvolvingDog(Genome(random.randrange(1,10,1), random.randrange(1,10,1), random.randrange(1,10,1)))
        dog3 = EvolvingDog(Genome(random.randrange(1,10,1), random.randrange(1,10,1), random.randrange(1,10,1)))
        dog4 = EvolvingDog(Genome(random.randrange(1,10,1), random.randrange(1,10,1), random.randrange(1,10,1)))
        return (dog1, dog2, dog3, dog4)

    def printPopulation(self):
        for d in self.population:
            d.printTraits()

    def calculateFitness(d):
        family_pet = math.e/(d.genome.size + .1) + 1.1**d.genome.friendly**-.5*d.genome.size - d.genome.protective**.5*-1*d.genome.size - 14
        protect_fam = 1.5**d.genome.protective + d.genome.protective**-1*d.genome.friendly + 1.1**d.genome.size - d.genome.friendly**.5 - 10
        return math.sqrt(abs(family_pet + protect_fam))

    def evolveGen(self):
        currentBest = 0
        currentSbest = 0
        bestD = None
        sBestD = None
        for d in self.population:
            fitness = Evolution.calculateFitness(d)
            if fitness > currentSbest:
                if fitness > currentBest:
                    currentSbest = currentBest
                    currentBest = fitness
                    sBestD = bestD
                    bestD = d
                else:
                    currentSbest = fitness
                    sBestD = d
        print("Best traits:")
        bestD.printTraits()
        print("Second best traits:")
        sBestD.printTraits()
        print()

        g1, g2 = Genome.crossover(bestD.genome, sBestD.genome)
        g3, g4 = Genome.crossover(bestD.genome, sBestD.genome)

        self.population = (EvolvingDog(g1), EvolvingDog(g2), EvolvingDog(g3), EvolvingDog(g4))

        for d in self.population:
            chance = random.random()
            if chance < .75:
                d.genome.mutate()

    def evolvePopulation(self):
        for i in range(self.trials):
            print("Gen %s" % i)
            self.evolveGen()
        self.printPopulation()

myEv = Evolution(3)
myEv.evolvePopulation()

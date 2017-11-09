import math
import random

movies_list ={'Willie Wonka': 'NA', 'Big Fat Greek Wedding': 'NA', 'Jurassic Park': 'NA', 'Saw': 'NA', 'Ted': 'NA'}
colors_list ={'red': 'NA', 'blue': 'NA', 'green': 'NA', 'purple': 'NA'}
books_list ={'Harry Potter': 'NA', 'Hamlet': 'NA', 'The Prince': 'NA', 'To Kill a Mockingbird': 'NA'}
animals_list ={'cats': 'NA', 'dogs': 'NA', 'gorillas': 'NA', 'snakes': 'NA'}

'''Have likes represent a class of dictionaries that associate items and ratings based on category'''
class Likes:
    def __init__(self):
        global movies_list
        global colors_list
        global books_list
        global animals_list
        self.movies = movies_list.copy()
        self.colors = colors_list.copy()
        self.books = books_list.copy()
        self.animals = animals_list.copy()

    def set_opinion(self, topic, title, score):
        if (score >= 0 and score <= 10):
            if (topic == 'movies'):
                if title in self.movies:
                    self.movies[title] = score
            if (topic == 'colors'):
                if title in self.colors:
                    self.colors[title] = score
            if (topic == 'books'):
                if title in self.books:
                    self.books[title] = score
            if (topic == 'animals'):
                if title in self.animals:
                    self.animals[title] = score
    def compare_opinions(topic, title, p1, p2):
        if (topic == 'movies'):
            opin1 = p1.movies[title]
            opin2 = p2.movies[title]
            if (opin1 != 'NA' and opin2 != 'NA'):
                return math.fabs(opin1 - opin2)
            else: return 0
        if (topic == 'colors'):
            opin1 = p1.colors[title]
            opin2 = p2.colors[title]
            if (opin1 != 'NA' and opin2 != 'NA'):
                return math.fabs(opin1 - opin2)
            return 0
        if (topic == 'books'):
            opin1 = p1.books[title]
            opin2 = p2.books[title]
            if (opin1 != 'NA' and opin2 != 'NA'):
                return math.fabs(opin1 - opin2)
            else: return 0
        if (topic == 'animals'):
            opin1 = p1.animals[title]
            opin2 = p2.animals[title]
            if (opin1 != 'NA' and opin2 != 'NA'):
                return math.fabs(opin1 - opin2)
            else: return 0

class Person:
    def __init__(self, name, likes):
        self.name = name
        self.likes = likes
    def get_name(self):
        return self.name
    def determine_pair_key(name1, name2):
        if name1 > name2:
            return name1 + " and " + name2
        else:
            return name2 + " and " + name1

class All_People:
    def __init__(self):
        self.list_of_people = {}
        self.list_of_people_friends = {}
        self.list_of_all_pairs = []

    def add_person(self, p1):
        for p in self.list_of_people:
            self.list_of_all_pairs.append((p1.name, p))
        self.list_of_people[p1.name] = p1.likes

    def find_likes_p(self, p_name):
        if p_name in self.list_of_people:
            return self.list_of_people[p_name]

    def add_friends(self, p1_name, p2_name):
        if (p1_name in self.list_of_people and p2_name in self.list_of_people):
            key = Person.determine_pair_key(p1_name, p2_name)
            self.list_of_people_friends[key] = True

    def check_friends(self, p1_name, p2_name):
        if (p1_name in self.list_of_people and p2_name in self.list_of_people):
            key = Person.determine_pair_key(p1_name, p2_name)
            return key in self.list_of_people_friends


class Friendship_Guesser:
    def __init__(self, people):
        self.weights = {}
        self.threshold = random.randrange(1,100,1)
        self.people = people
        global movies_list
        global colors_list
        global books_list
        global animals_list
        for mov in movies_list:
            self.weights[mov] = random.randrange(-10,10,1)
        for col in colors_list:
            self.weights[col] = random.randrange(-10,10,1)
        for book in books_list:
            self.weights[book] = random.randrange(-10,10,1)
        for animal in animals_list:
            self.weights[animal] = random.randrange(-10,10,1)

    def guess_for_pair(self, p1, p2):
        difference = 0
        global movies_list
        global colors_list
        global books_list
        global animals_list
        for m in movies_list:
            difference += Likes.compare_opinions('movies', m, p1, p2)* self.weights[m]
        for c in colors_list:
            difference += Likes.compare_opinions('colors', c, p1, p2)* self.weights[c]
        for b in books_list:
            difference += Likes.compare_opinions('books', b, p1, p2)* self.weights[b]
        for a in animals_list:
            difference += Likes.compare_opinions('animals', a, p1, p2)* self.weights[a]
        if difference < self.threshold:
            return True
        else: return None

    def guess_for_all(self):
        inaccuracy = 0
        for pair in self.people.list_of_all_pairs:
            likes_p0 = self.people.find_likes_p(pair[0])
            likes_p1 = self.people.find_likes_p(pair[1])
            guess = self.guess_for_pair(likes_p0, likes_p1)
            answer = self.people.check_friends(pair[0], pair[1])
            if guess != answer:
                inaccuracy= inaccuracy + 1
        return inaccuracy

    def mutate(self):
        chance = random.random()
        if (chance < .5):
            num = random.randrange(0, len(self.weights))
            for i in range(num):
                value = random.choice(list(self.weights))
                self.weights[value] = self.weights[value] + random.randrange(-2,2,1)/2

    def recombination(g1, g2, people):
        child = Friendship_Guesser(people)
        if random.random() < .5:
            for m in movies_list:
                child.weights[m] = g1.weights[m]
        else:
            for m in movies_list:
                child.weights[m] = g2.weights[m]
        if random.random() < .5:
            for b in books_list:
                child.weights[b] = g1.weights[b]
        else:
            for b in books_list:
                child.weights[b] = g2.weights[b]
        if random.random() < .5:
            for c in colors_list:
                child.weights[c] = g1.weights[c]
        else:
            for c in colors_list:
                child.weights[c] = g2.weights[c]
        if random.random() < .5:
            for a in animals_list:
                child.weights[a] = g1.weights[a]
        else:
            for a in animals_list:
                child.weights[a] = g2.weights[a]
        return child


class Evolution:

    def __init__(self, people, size_pop):
        self.people = people
        self.population = []

        if size_pop % 2 != 0:
            size_pop = size_pop + 1

        for i in range(size_pop - 1):
            self.population.append(Friendship_Guesser(self.people))

    def evolveOneGen(self):
        sorted(self.population, key = lambda g: g.guess_for_all())
        self.population = self.population[: len(self.population)//2]
        '''Need to add in crossover here'''
        for p in self.population:
            p.mutate()

    def evolveManyGens(self, numberOfEvs):
        times = numberOfEvs-1
        for i in range(times):
            self.evolveOneGen()


l1 = Likes()
l1.set_opinion('colors', 'red', 8)
p1 = Person('bill', l1)
l2 = Likes()
l2.set_opinion('colors', 'red', 3)
p2 = Person('hannah', l2)
l3 = Likes()
l3.set_opinion('colors', 'red', 1)
p3 = Person('britt', l3)
all_p = All_People()
all_p.add_person(p1)
all_p.add_person(p2)
all_p.add_person(p3)
all_p.add_friends(p1.name, p3.name)

evolution = Evolution(all_p, 4)
evolution.evolveOneGen()

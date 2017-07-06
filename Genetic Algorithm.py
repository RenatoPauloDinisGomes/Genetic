import string
import random
import math


def getRandomChar():
    return random.choice(string.letters + " 0123456789")


def calFitness(objetivo, atual):
    fitness = 0
    for i, value in enumerate(objetivo):
        if value == atual[i]:
            fitness += 1
    return fitness


def main():
    objetivo = raw_input("Enter the Objective String: ")
    print
    "Objective: " + objetivo
    dic = {}
    bestest = []
    num_generatons = raw_input("Number of Generations (# for 90000000):")
    if num_generatons == "#" or num_generatons <= 0:
        num_generatons = 90000000
    num_generatons = int(num_generatons)
    prob_cross = 90
    prob_mutate = 1
    elitismo = 10
    pop_size = 50
    population = ["" for _ in range(pop_size)]
    mattingpool = ["" for _ in range(pop_size)]
    fits = [0 for _ in range(pop_size)]

    # generate first population
    for i in range(pop_size):
        for l in range(len(objetivo)):
            population[i] += getRandomChar()

    for gen in range(num_generatons):
        # calculate fitness
        for fit in range(pop_size):
            fits[fit] = calFitness(objetivo, population[fit])

        # sort by fitness
        for c in range(pop_size - 1):
            for d in range(pop_size - c - 1):
                if fits[d] < fits[d + 1]:
                    frase = population[d]
                    population[d] = population[d + 1]
                    population[d + 1] = frase
                    c_fit = fits[d]
                    fits[d] = fits[d + 1]
                    fits[d + 1] = c_fit
        # save the best Fitness of each generation
        bestest.insert(0, fits[0])

        media = sum(fits) / pop_size
        suma = 0
        for k in fits:
            suma += (k - media) << 1
        dic.update({gen: {media: math.sqrt(suma)}})
        # stop condition
        if fits[0] == len(objetivo):
            break
        else:
            # generate matting pool (selection tournament 2 ) TODO tournament X individuals
            for i in range(elitismo):
                mattingpool[i] = population[i]
            for i in range(elitismo, pop_size):
                ind1 = random.randint(0, pop_size - 1)
                ind2 = random.randint(0, pop_size - 1)
                while ind1 == ind2:
                    ind2 = random.randint(0, pop_size - 1)
                mattingpool[i] = population[ind1] if fits[ind1] > fits[ind2] else population[ind2]

            # crossover TODO cross N intervals
            for i in range(elitismo, pop_size, 2):
                prob = random.randint(0, 100);
                if prob < prob_cross:
                    ind1 = random.randint(0, pop_size - 1)
                    ind2 = random.randint(0, pop_size - 1)
                    while ind1 == ind2:
                        ind2 = random.randint(0, pop_size - 1)

                    start = random.randint(0, len(objetivo) - 1)
                    h = 0
                    aux = ""
                    for ch in population[ind1]:
                        if h > start:
                            aux += mattingpool[ind2][h]
                        else:
                            aux += ch
                        h += 1
                    population[ind1] = aux

            # mutate
            for i in range(elitismo, pop_size):
                aux = ""
                for l in range(len(objetivo)):
                    prob = random.randint(0, 100)
                    if prob_mutate > prob:
                        aux += getRandomChar()
                    else:
                        aux += population[i][l]
                population[i] = aux

    index = 0
    maxi = 0

    for i in range(pop_size):
        if maxi < fits[i]:
            maxi = fits[i]
            index = i

    if maxi == len(objetivo):
        print
        "Reached Objective in " + str(gen) + " Generations"

    print
    "Fitness Objective -> " + str(len(objetivo)) + "\nFitness Reached -> " + str(maxi)
    res = ""
    for i in range(len(objetivo)):
        if objetivo[i] == population[index][i]:
            res += objetivo[i]
        else:
            res += " "
    print
    "Result: " + population[index]
    print
    "Equals: " + res + "\nGeneration:{Average:Standard Deviation}:"
    print
    dic


main()

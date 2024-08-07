import random

def createRoute(cityList):
    # random.seed(44)
    route = random.sample(cityList, len(cityList))
    return route

#Create first "population" (list of routes)
def initialPopulation(popSize, cityList, specialInitialSolutions):
    population = []
    population.extend(specialInitialSolutions)
    #TODO: Hinzufügen der speziellen Initiallösungen aus specialInitialSolutions
    

    numberInitialSolutions = len(specialInitialSolutions)
    print ("Number of special initial solutions:" + str(numberInitialSolutions))
    #for i in range(0, popSize):
    for i in range(numberInitialSolutions, popSize):
        population.append(createRoute(cityList))
    return population
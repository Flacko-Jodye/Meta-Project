import random, numpy as np, pandas as np
from Fitness import Fitness

#Create our initial population
#Route generator
def createRoute(cityList):
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

#Create the genetic algorithm
#Rank individuals
# use 1 = DISTANCE BASED RANKING
# use 2 = STRESS BASED RANKING
# use 3 = PARETO FITNESS BASED RANKING
def rankRoutes(population, objectiveNrUsed):
    fitnessResults = {}
    if (objectiveNrUsed == 1):
        for i in range(0,len(population)):
            fitnessResults[i] = Fitness(population[i]).routeFitnessDistanceBased()
    elif (objectiveNrUsed == 2):
        for i in range(0,len(population)):
            fitnessResults[i] = Fitness(population[i]).routeFitnessStressBased()
    elif (objectiveNrUsed == 3):
        #TODO: passender Aufruf der bestehenden Fitnessberechnung 
        fitnessResults = rankRoutesBasedOnDominance(population) # hinzugefügt
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

#Provide Pareto-Based Fitness Calculation <<<<<<<<<<<<
# Dictionary bei dem für jedes Individuum die zugehörigen Werte gespeichert werden
# IndexNr:[distance,stress,[dominated solutions], [is dominated by solutions], R(i), F(i)]    
def rankRoutesBasedOnDominance(population):
    #store single fitness values per individuum
    fitnessValuesPerIndividuum = {}
    distance = 0
    stress = 0
    for i in range(0,len(population)):
        distance = Fitness(population[i]).routeDistance()
        stress = Fitness(population[i]).routeStress() 
        fitnessValuesPerIndividuum[i] = [distance, stress, [], [], 0, 0]
    #compute number of dominated solutions
    for i in range(0,len(population)):
       for j in range(0,len(population)):
           if (i != j):
              if (fitnessValuesPerIndividuum[i][0] < fitnessValuesPerIndividuum[j][0]
              and fitnessValuesPerIndividuum[i][1] < fitnessValuesPerIndividuum[j][1]):
                   fitnessValuesPerIndividuum[i][2].append(j) #add dominated solution
                   fitnessValuesPerIndividuum[j][3].append(i) #add dominating solution
    for i in range(0,len(population)):
        for domSol in fitnessValuesPerIndividuum[i][3]:
            fitnessValuesPerIndividuum[i][4] += len(fitnessValuesPerIndividuum[domSol][2])
    distanceValuesPerIndividuum = {}
    for i in range(0,len(population)):
        distanceValuesPerIndividuum[i] = []
        for j in range(0,len(population)):
           if (i != j):
               euclDistance = computeEuclideanDistance(fitnessValuesPerIndividuum[i][0],fitnessValuesPerIndividuum[j][0],
                                        fitnessValuesPerIndividuum[i][1], fitnessValuesPerIndividuum[j][1])
               distanceValuesPerIndividuum[i].append(euclDistance)
        distanceValuesPerIndividuum[i].sort()
    #determine k-nearest neighbour    
    k = int(np.floor((np.sqrt(len(population)))))
    if (k == 0):
        print("Something went wrong.")
        k = 1
    #index der Distanzberechnung, kter-Nachbar
    k -=1
    
    fitnessResults = {}
    for i in range(0,len(population)):
        #compute D(i)
        d_i = 1/ (distanceValuesPerIndividuum[i][k] + 2)
        fitnessValuesPerIndividuum[i][5] = fitnessValuesPerIndividuum[i][4] + d_i
        fitnessResults[i] = 1/fitnessValuesPerIndividuum[i][5] #damit größte Fitness = beste
    return fitnessResults 
  
def computeEuclideanDistance(distanceA, distanceB, stressA, stressB):
    return np.sqrt( (distanceA-distanceB)** 2 + (stressA-stressB)** 2)

#Create a selection function that will be used to make the list of parent routes
def selection(popRanked, eliteSize):
    selectionResults = []
    #TODO: Z.B. Turnierbasierte Selektion statt fitnessproportionaler Selektion
    # roulette wheel by calculating a relative fitness weight for each individual
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    #We’ll also want to hold on to our best routes, so we introduce elitism
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    #we compare a randomly drawn number to these weights to select our mating pool
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

#Create mating pool
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

# Create a crossover function for two parents to create one child
def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    #In ordered crossover, we randomly select a subset of the first parent string
    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    #and then fill the remainder of the route with the genes from the second parent
    #in the order in which they appear, 
    #without duplicating any genes in the selected subset from the first parent      
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

#Create function to run crossover over full mating pool
def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    #we use elitism to retain the best routes from the current population.
    for i in range(0,eliteSize):
        children.append(matingpool[i])

    #we use the breed function to fill out the rest of the next generation.    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

#Create function to mutate a single route
#we’ll use swap mutation.
#This means that, with specified low probability, 
#two cities will swap places in our route.
def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

#Create function to run mutation over entire population
def mutatePopulation(population, mutationRate, eliteSize):
    mutatedPop = []
    
    #mating pool is sorted in order of fitness
    #here elitism instead of fixed archive
    #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
    for ind in range(0, eliteSize):
        mutatedPop.append(population[ind])
    for ind in range(eliteSize, len(population)):
    #for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

#Put all steps together to create the next generation
 
#First, we rank the routes in the current generation using rankRoutes.
#We then determine our potential parents by running the selection function,
#    which allows us to create the mating pool using the matingPool function.
#Finally, we then create our new generation using the breedPopulation function 
# and then applying mutation using the mutatePopulation function. 

def nextGeneration(currentGen, eliteSize, mutationRate, objectiveNrUsed, archiveUsed): 
   # rankRoutesBasedOnDominance(currentGen)
    popRanked = rankRoutes(currentGen,objectiveNrUsed)
    if (not archiveUsed):
        selectionResults = selection(popRanked, eliteSize)
        matingpool = matingPool(currentGen, selectionResults)
        children = breedPopulation(matingpool, eliteSize)
        nextGeneration = mutatePopulation(children, mutationRate,0)
    else:
        #<<<<< use archiv
        #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
        selectionResults = selectionWithArchive(popRanked)
        matingpool = matingPool(currentGen, selectionResults)
        archiveSize = determineNonDominatedArchiveSize(popRanked)
        children = breedPopulation(matingpool, archiveSize)
        #eliteSize is used to maintain solutions that should be in an archive
        nextGeneration = mutatePopulation(children, mutationRate, eliteSize)
    return nextGeneration

def determineNonDominatedArchiveSize(popRanked):
    archiveSize = 0
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            archiveSize += 1
    return archiveSize
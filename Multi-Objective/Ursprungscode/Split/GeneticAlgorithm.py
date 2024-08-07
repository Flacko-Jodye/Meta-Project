import random, numpy as np, pandas as np, matplotlib.pyplot as plt
from Fitness import Fitness
from config import selection_method, tournament_size, replace_size, plotting_enabled, saving_enabled, output_directory
from Mutation import mutate, mutatePopulation
from Selection import selection, selectionWithArchive
from Archive import determineNonDominatedArchiveSize, determineNonDominatedArchive
from InitialPopulation import createRoute, initialPopulation
from RankRoutes import rankRoutesBasedOnDominance, rankRoutes
from Plotting import plotPopulationAndObjectiveValues, plotRoute, plotProgress
import os


random.seed(44)
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

#Put all steps together to create the next generation
 
#First, we rank the routes in the current generation using rankRoutes.
#We then determine our potential parents by running the selection function,
#    which allows us to create the mating pool using the matingPool function.
#Finally, we then create our new generation using the breedPopulation function 
# and then applying mutation using the mutatePopulation function. 

def nextGeneration(currentGen, eliteSize, mutationRate, objectiveNrUsed, archiveUsed, seed = 44): 
    # random.seed(seed)
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

def geneticAlgorithm(objectiveNrUsed, specialInitialSolutions, population, popSize, eliteSize, mutationRate, generations, seed = 44):
    # random.seed(seed)
    #create initial population
    pop = initialPopulation(popSize, population, specialInitialSolutions)
    
    archiveUsed = False
    
    #provide statistics about best initial solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):
        print("Initial objective: " + str(1 / rankRoutes(pop,objectiveNrUsed)[0][1]))
        bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        bestRoute = pop[bestRouteIndex]
        print("Initial distance : " + str(Fitness(bestRoute).routeDistance()))
        print("Initial stress:    " + str(Fitness(bestRoute).routeStress()))
        plotRoute(bestRoute, "Best initial route")
    elif(objectiveNrUsed == 3):
        print("Initial highest fitness value: " + str(rankRoutes(pop,objectiveNrUsed)[0][1]))
        print("Initial best distance value: " + str(1/ rankRoutes(pop,1)[0][1]))
        print("Initial best stress value: " + str(1/ rankRoutes(pop,2)[0][1]))
        archiveUsed = True
        bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        bestRoute = pop[bestRouteIndex]
        plotRoute(bestRoute, "Best initial route")
    
    #plot intial population with regard to the two objectives
    plotPopulationAndObjectiveValues(pop, "Initial Population")
    
    #store infos to plot progress when finished
    progressDistance = []
    progressDistance.append(1 / rankRoutes(pop,1)[0][1])
    progressStress = []
    progressStress.append(1 / rankRoutes(pop,2)[0][1])
    
    
    #create new generations of populations
    for i in range(0, generations):
        print(i, end=", ")
        pop = nextGeneration(pop, eliteSize, mutationRate,objectiveNrUsed,archiveUsed)
        #store infos to plot progress when finished
        progressDistance.append(1 / rankRoutes(pop,1)[0][1])
        progressStress.append(1 / rankRoutes(pop,2)[0][1])
    print("Done!")
            
    if plotting_enabled:
        plotProgress(progressDistance, 'Distance', 'Progress of Distance Minimization')
        plotProgress(progressStress, 'Stress', 'Progress of Stress Minimization')
    
    #provide statistics about best final solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):
        print("Final objective: " + str(1 / rankRoutes(pop,objectiveNrUsed)[0][1])) 
        bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        bestRoute = pop[bestRouteIndex]
        print("Final distance : " + str(Fitness(bestRoute).routeDistance()))
        print("Final stress:    " + str(Fitness(bestRoute).routeStress()))

        
        #Provide special initial solutions    <<<<<<<<<<<
        #print city Indizes for initial solution
        bestRouteIndizes = []
        for city in bestRoute:
            bestRouteIndizes.append(city.nr)
    
        print("---- ")
        print("City Numbers of Best Route")
        print(bestRouteIndizes)
        print("---- ")
        plotRoute(bestRoute, "Best final route")
        
    elif(objectiveNrUsed == 3):
        print("Final highest fitness value: " + str(rankRoutes(pop,objectiveNrUsed)[0][1]))
        print("Final best distance value: " + str(1/ rankRoutes(pop,1)[0][1]))
        print("Final best stress value: " + str(1/ rankRoutes(pop,2)[0][1]))
        bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        bestRoute = pop[bestRouteIndex]
        plotRoute(bestRoute, "Best final route")
        #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist
        # dann alle Lösungen ausgeben die im Archiv sind
        
        
    #plot final population with regard to the two objectives
    plotPopulationAndObjectiveValues(pop, "Final Population")

    return bestRoute, progressDistance, progressStress, pop
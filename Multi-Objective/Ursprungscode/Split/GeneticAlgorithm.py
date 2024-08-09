import random, numpy as np, pandas as np, matplotlib.pyplot as plt
from Fitness import Fitness
from config import selection_method, tournament_size, replace_size, plotting_enabled, saving_enabled, output_directory, crossover_method, mutation_method, spea2_archive_enabled, hypervolume_enabled, hypervolume_plot_2d_enabled
from Mutation import mutate, mutatePopulation, mutatePopulationWithConfig
from Crossover import ordered_crossover, one_point_crossover, edge_recombination_crossover
from Selection import selection, selectionWithArchive
from Archive import determineNonDominatedArchiveSize, determineNonDominatedArchive
from InitialPopulation import createRoute, initialPopulation
from RankRoutes import rankRoutesBasedOnDominance, rankRoutes
from Plotting import plotPopulationAndObjectiveValues, plotRoute, plotProgress, plotHypervolume, plotHypervolume2D
from Hypervolume import HyperVolume
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

    if crossover_method == "order":
        return ordered_crossover(parent1, parent2)
    elif crossover_method == "one-point":
        return one_point_crossover(parent1, parent2)
    elif crossover_method == "edge-recombination":
        return edge_recombination_crossover(parent1, parent2)
    else:
        raise ValueError("Unknown crossover method: {}".format(crossover_method))

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
    popRanked = rankRoutes(currentGen,objectiveNrUsed)
    if (not archiveUsed):
        selectionResults = selection(popRanked, eliteSize)
        matingpool = matingPool(currentGen, selectionResults)
        children = breedPopulation(matingpool, eliteSize)
        nextGeneration = mutatePopulationWithConfig(children, mutationRate,eliteSize, 0)
    else:
        #<<<<< use archiv
        #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
        selectionResults = selectionWithArchive(popRanked)
        matingpool = matingPool(currentGen, selectionResults)
        archiveSize = determineNonDominatedArchiveSize(popRanked)
        children = breedPopulation(matingpool, archiveSize)
        nextGeneration = mutatePopulationWithConfig(children, mutationRate, eliteSize, archiveSize)
    return nextGeneration

def geneticAlgorithm(objectiveNrUsed, specialInitialSolutions, population, popSize, eliteSize, mutationRate, generations, seed = 44):
    #create initial population
    pop = initialPopulation(popSize, population, specialInitialSolutions)
    
    archiveUsed = spea2_archive_enabled
    archive = []
    
    if hypervolume_enabled:
        # Initialize the reference point for the hypervolume calculation
        ref_point = [max(Fitness(route).routeDistance() for route in pop) + 1, max(Fitness(route).routeStress() for route in pop) + 1]
        hv = HyperVolume(ref_point)  # Initialize the HyperVolume class

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
    hypervolume_progress = []
    
    #create new generations of populations
    for i in range(0, generations):
        print(i, end=", ")
        pop = nextGeneration(pop, eliteSize, mutationRate,objectiveNrUsed,archiveUsed)
        #store infos to plot progress when finished
        progressDistance.append(1 / rankRoutes(pop,1)[0][1])
        progressStress.append(1 / rankRoutes(pop,2)[0][1])

        if hypervolume_enabled:
            # Calculate the hypervolume of the current population
            front = [(Fitness(route).routeDistance(), Fitness(route).routeStress()) for route in determineNonDominatedArchive(pop, rankRoutes(pop, 3))]
            hv = HyperVolume(ref_point)
            hypervolume_progress.append(hv.compute(front))
            if i == generations - 1 and hypervolume_plot_2d_enabled:
                plotHypervolume2D(determineNonDominatedArchive(pop, rankRoutes(pop, 3)), ref_point, title=f"Hypervolume at Generation {i+1}")

        if i == generations - 1 and plotting_enabled:
            plotHypervolume2D(determineNonDominatedArchive(pop, rankRoutes(pop, 3)), ref_point, title=f"Hypervolume at Generation {i+1}")
    if hypervolume_enabled:
        plotHypervolume(hypervolume_progress, "Progress of Hypervolume")
            
    # if plotting_enabled:
    #     # plotProgress(progressDistance, 'Distance', 'Progress of Distance Minimization')
    #     # plotProgress(progressStress, 'Stress', 'Progress of Stress Minimization')
    #     plotProgress('Hypervolume', 'Progress of Hypervolume')
    
    #provide statistics about best final solution with regard to chosen objective
    if (objectiveNrUsed == 1 or objectiveNrUsed == 2):
        print("Final objective: " + str(1 / rankRoutes(pop,objectiveNrUsed)[0][1])) 
        bestRouteIndex = rankRoutes(pop,objectiveNrUsed)[0][0]
        bestRoute = pop[bestRouteIndex]
        print("Final distance : " + str(Fitness(bestRoute).routeDistance()))
        print("Final stress:    " + str(Fitness(bestRoute).routeStress()))

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
        archive = determineNonDominatedArchive(pop, rankRoutes(pop,objectiveNrUsed))
        plotRoute(bestRoute, "Best final route")
        
    #plot final population with regard to the two objectives
    plotPopulationAndObjectiveValues(pop, "Final Population")

    return bestRoute, progressDistance, progressStress, pop
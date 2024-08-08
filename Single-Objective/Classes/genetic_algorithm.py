from Operations import initialPopulation, nextGeneration, rankRoutes
from Fitness import Fitness
from plotting import plotPopulationAndObjectiveValues, plotProgress, plotRoute
import config, random
from Helpers import save_best_route_to_csv
from config import save_route_to_csv

def geneticAlgorithm(objectiveNrUsed, specialInitialSolutions, population, popSize, eliteSize, mutationRate, generations):
    random.seed(44)
    #create initial population
    pop = initialPopulation(popSize, population, specialInitialSolutions)
    
    #provide statistics about best initial solution with regard to chosen objective
    print("Initial objective: " + str(1 / rankRoutes(pop, objectiveNrUsed)[0][1]))
    bestRouteIndex = rankRoutes(pop, objectiveNrUsed)[0][0]
    bestRoute = pop[bestRouteIndex]
    print("Initial distance : " + str(Fitness(bestRoute).routeDistance()))
    print("Initial stress:    " + str(Fitness(bestRoute).routeStress()))
    
    if config.plotting_enabled:
        plotRoute(bestRoute, "Initial Route", f"Initial_Route_{popSize}_{eliteSize}_{mutationRate}_{generations}.png")
    #plot initial population with regard to the two objectives
    if config.plotting_enabled:
        plotPopulationAndObjectiveValues(pop, "Initial Population", f"Initial_Population_{popSize}_{eliteSize}_{mutationRate}_{generations}.png", Fitness)
    
    #store infos to plot progress when finished
    progressDistance = []
    progressDistance.append(1 / rankRoutes(pop, 1)[0][1])
    progressStress = []
    progressStress.append(1 / rankRoutes(pop, 2)[0][1])
    
    #create new generations of populations
    for i in range(generations):
        pop = nextGeneration(pop, eliteSize, mutationRate, objectiveNrUsed)
        #store infos to plot progress when finished
        progressDistance.append(1 / rankRoutes(pop, 1)[0][1])
        progressStress.append(1 / rankRoutes(pop, 2)[0][1])

    if config.plotting_enabled:    
        #plot progress - distance
        plotProgress(progressDistance, 'Distance', 'Progress of Distance Minimization', f"Progress_Distance_{popSize}_{eliteSize}_{mutationRate}_{generations}.png")
        #plot progress - stress
        plotProgress(progressStress, 'Stress', 'Progress of Stress Minimization', f"Progress_Stress_{popSize}_{eliteSize}_{mutationRate}_{generations}.png")
    
    #provide statistics about best final solution with regard to chosen objective
    print("Final objective: " + str(1 / rankRoutes(pop, objectiveNrUsed)[0][1]))
    bestRouteIndex = rankRoutes(pop, objectiveNrUsed)[0][0]
    bestRoute = pop[bestRouteIndex]
    
    print("Final distance : " + str(Fitness(bestRoute).routeDistance()))
    print("Final stress:    " + str(Fitness(bestRoute).routeStress()))
    
    #print city Indizes for initial solution
    bestRouteIndizes = [city.nr for city in bestRoute]
    print("---- ")
    print("City Numbers of Best Route")
    print(bestRouteIndizes)
    print("---- ")
    
    if config.plotting_enabled:
        #plot final population with regard to the two objectives
        plotPopulationAndObjectiveValues(pop, "Final Population", f"Final_Population_{popSize}_{eliteSize}_{mutationRate}_{generations}.png", Fitness)

    if save_route_to_csv:
        save_best_route_to_csv(bestRoute, 'best_route.csv')
        print("Beste Route wurde in 'Visualisation_Parameters/Best_Route.csv' gespeichert.")
    
    return bestRoute, progressDistance, progressStress, pop


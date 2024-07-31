import matplotlib.pyplot as plt
from City import City
from Operations import initialPopulation, nextGeneration, rankRoutes
from Fitness import Fitness
from Helpers import getCityBasedOnNr
import random
import os

output_dir = "Visualisation_Parameters"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def plotRoute(cityList, title, filename):
    plt.figure(figsize=(10, 10))
    x = []
    y = []
    for item in cityList:
        x.append(item.x)
        y.append(item.y)
        plt.annotate(item.nr, (item.x, item.y))
    x.append(cityList[0].x)
    y.append(cityList[0].y)
    plt.plot(x, y, marker="x")
    plt.ylabel('Y-Koordinate')
    plt.xlabel('X-Koordinate')
    plt.title(title)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def plotProgress(values, ylabel, title, filename):
    plt.figure()  # Create a new figure
    plt.plot(values)
    plt.ylabel(ylabel)
    plt.xlabel('Generation')
    plt.title(title)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def plotPopulationAndObjectiveValues(population, title, filename):
    distance = []
    stress = []
    for route in population:
        distance.append(Fitness(route).routeDistance())
        stress.append(Fitness(route).routeStress())
    plt.scatter(distance, stress, marker="o", color="black")
    plt.ylabel('Stress')
    plt.xlabel('Distance')
    plt.title(title)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def geneticAlgorithm(objectiveNrUsed, specialInitialSolutions, population, popSize, eliteSize, mutationRate, generations):
    # create initial population
    pop = initialPopulation(popSize, population, specialInitialSolutions)
    
    # provide statistics about best initial solution with regard to chosen objective
    print("Initial objective: " + str(1 / rankRoutes(pop, objectiveNrUsed)[0][1]))
    bestRouteIndex = rankRoutes(pop, objectiveNrUsed)[0][0]
    bestRoute = pop[bestRouteIndex]
    print("Initial distance : " + str(Fitness(bestRoute).routeDistance()))
    print("Initial stress:    " + str(Fitness(bestRoute).routeStress()))
    
    # store infos to plot progress when finished
    progressDistance = []
    progressDistance.append(1 / rankRoutes(pop, 1)[0][1])
    progressStress = []
    progressStress.append(1 / rankRoutes(pop, 2)[0][1])
    
    # create new generations of populations
    for i in range(generations):
        pop = nextGeneration(pop, eliteSize, mutationRate, objectiveNrUsed)
        # store infos to plot progress when finished
        progressDistance.append(1 / rankRoutes(pop, 1)[0][1])
        progressStress.append(1 / rankRoutes(pop, 2)[0][1])
        
    # provide statistics about best final solution with regard to chosen objective
    print("Final objective: " + str(1 / rankRoutes(pop, objectiveNrUsed)[0][1]))
    bestRouteIndex = rankRoutes(pop, objectiveNrUsed)[0][0]
    bestRoute = pop[bestRouteIndex]
    
    print("Final distance : " + str(Fitness(bestRoute).routeDistance()))
    print("Final stress:    " + str(Fitness(bestRoute).routeStress()))
    
    return bestRoute, progressDistance, progressStress, pop

# Running the genetic algorithm
# Create list of cities
cityList = []

random.seed(44)
for i in range(1, 26):
    cityList.append(City(nr=i, traffic=int(random.random() * 40), x=int(random.random() * 200), y=int(random.random() * 200)))

print(cityList)

# Provide special initial solutions
cityNumbersRoute1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

route1 = []
for nr in cityNumbersRoute1:
    route1.append(getCityBasedOnNr(cityList, nr))

initialSolutionsList = [route1]

# Parameter Tuning
popSizes = [50, 100, 200]
eliteSizes = [10, 20, 30]
mutationRates = [0.01, 0.05, 0.1]
generations_list = [100, 200, 500]

best_overall_route = None
best_overall_distance = float('inf')
best_progress_distance = None
best_progress_stress = None
best_final_population = None
best_params = None

for popSize in popSizes:
    for eliteSize in eliteSizes:
        for mutationRate in mutationRates:
            for generations in generations_list:
                print(f"Running GA with popSize={popSize}, eliteSize={eliteSize}, mutationRate={mutationRate}, generations={generations}")
                bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
                    objectiveNrUsed=1,
                    specialInitialSolutions=initialSolutionsList,
                    population=cityList,
                    popSize=popSize,
                    eliteSize=eliteSize,
                    mutationRate=mutationRate,
                    generations=generations
                )
                final_distance = 1 / rankRoutes([bestRoute], 1)[0][1]
                if final_distance < best_overall_distance:
                    best_overall_distance = final_distance
                    best_overall_route = bestRoute
                    best_progress_distance = progressDistance
                    best_progress_stress = progressStress
                    best_final_population = final_population
                    best_params = (popSize, eliteSize, mutationRate, generations)

# Plot the best results
if best_overall_route is not None:
    plotRoute(best_overall_route, "Best final route", f"Best_final_route_{best_params[0]}_{best_params[1]}_{best_params[2]}_{best_params[3]}.png")
    plotProgress(best_progress_distance, 'Distance', f'Progress of Distance Minimization (popSize={best_params[0]}, eliteSize={best_params[1]}, mutationRate={best_params[2]})', f"Progress_Distance_{best_params[0]}_{best_params[1]}_{best_params[2]}_{best_params[3]}.png")
    plotProgress(best_progress_stress, 'Stress', f'Progress of Stress Minimization (popSize={best_params[0]}, eliteSize={best_params[1]}, mutationRate={best_params[2]})', f"Progress_Stress_{best_params[0]}_{best_params[1]}_{best_params[2]}_{best_params[3]}.png")
    plotPopulationAndObjectiveValues(best_final_population, f"Final Population (popSize={best_params[0]}, eliteSize={best_params[1]}, mutationRate={best_params[2]})", f"Final_Population_{best_params[0]}_{best_params[1]}_{best_params[2]}_{best_params[3]}.png")

# Print the best parameters
    print(f"Best parameters found: popSize={best_params[0]}, eliteSize={best_params[1]}, mutationRate={best_params[2]}, generations={best_params[3]}")
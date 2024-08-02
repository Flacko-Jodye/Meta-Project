import matplotlib.pyplot as plt
from City import City
from Operations import initialPopulation, nextGeneration, rankRoutes
from Fitness import Fitness
from Helpers import getCityBasedOnNr
from plotting import plotPopulationAndObjectiveValues, plotProgress, plotRoute
from genetic_algorithm import geneticAlgorithm
import random
import os
import csv 
import config

#Create list of cities
cityList = []
random.seed(44)
for i in range(1,26):
    cityList.append(City(nr= i, traffic=int(random.random()*40), x=int(random.random() * 200), y=int(random.random() * 200)))
print(cityList)

# Provide special initial solutions
cityNumbersRoute1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
route1 = []
for nr in cityNumbersRoute1:
    route1.append(getCityBasedOnNr(cityList,nr))
    

initialSolutionsList = []
#TODO: Spezielle Intiallösungen der initialSolutionsList übergeben    
    
#Run the genetic algorithm
#modify parameters popSize, eliteSize, mutationRate, generations to search for the best solution
#modify objectiveNrUsed to use different objectives:
# 1= Minimize distance, 2 = Minimize stress

# Visualisierungen abspeichern
output_dir = "Visualisation_Parameters"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# CSV zum abspeichern der Ergebnisse:
results_file = os.path.join(output_dir, "Tuning_Results.csv")


def save_results_to_csv(results, filename):
    fieldnames = ["popSize", "eliteSize","mutationRate", "generations", "finalDistance", "finalStress", "params"]
    file_exists = os.path.isfile(filename)

    with open(filename, mode ="a", newline = "") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for result in results:
            writer.writerow(result)


def run_experiments(): # Tuning-Modus
    best_overall_route = None
    best_overall_distance = float('inf')
    best_progress_distance = None
    best_progress_stress = None
    best_final_population = None
    best_params = None
    results = []

    for popSize in config.popSizes:
        for eliteSize in config.eliteSizes:
            for mutationRate in config.mutationRates:
                for generations in config.generations_list:
                    print(f"Algo läuft mit folgenden Parametern: popSize={popSize}, eliteSize={eliteSize}, mutationRate={mutationRate}, generations={generations}")
                    bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
                        objectiveNrUsed = config.single_run_params["objectiveNrUsed"],
                        specialInitialSolutions=initialSolutionsList,
                        population=cityList,
                        popSize=popSize,
                        eliteSize=eliteSize,
                        mutationRate=mutationRate,
                        generations=generations
                    )
                    final_distance = 1 / rankRoutes([bestRoute], 1)[0][1]
                    final_stress = 1 / rankRoutes([bestRoute], 2)[0][1]
                    results.append({
                        "popSize": popSize,
                        "eliteSize": eliteSize,
                        "mutationRate": mutationRate,
                        "generations": generations,
                        "finalDistance": final_distance,
                        "finalStress": final_stress,
                        "params": f"{popSize}_{eliteSize}_{mutationRate}_{generations}"
                    })
                    if final_distance < best_overall_distance:
                        best_overall_distance = final_distance
                        best_overall_route = bestRoute
                        best_progress_distance = progressDistance
                        best_progress_stress = progressStress
                        best_final_population = final_population
                        best_params = (popSize, eliteSize, mutationRate, generations)
        if config.csv_enabled:
            save_results_to_csv(results, results_file)

# bestRoute = geneticAlgorithm(objectiveNrUsed=1, specialInitialSolutions = initialSolutionsList, population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)
# print(bestRoute)

# plotRoute(bestRoute, "Best final route")

    if best_overall_route is not None and config.plotting_enabled:
        plotRoute(best_overall_route, "Best final route", f"Best_final_route_{best_params[0]}_{best_params[1]}_{best_params[2]}_{best_params[3]}.png")
        plotProgress(best_progress_distance, 'Distance', 'Progress of Distance Minimization', f"Progress_Distance_{best_params[0]}_{best_params[1]}_{best_params[2]}_{best_params[3]}.png")
        plotProgress(best_progress_stress, 'Stress', 'Progress of Stress Minimization', f"Progress_Stress_{best_params[0]}_{best_params[1]}_{best_params[2]}_{best_params[3]}.png")
        plotPopulationAndObjectiveValues(best_final_population, "Final Population", f"Final_Population_{best_params[0]}_{best_params[1]}_{best_params[2]}_{best_params[3]}.png", Fitness)

    if best_params is not None:
        print("\nBeste Parameter und Ergebnisse:")
        print(f"PopSize: {best_params[0]}")
        print(f"EliteSize: {best_params[1]}")
        print(f"MutationRate: {best_params[2]}")
        print(f"Generations: {best_params[3]}")
        print(f"Final Distance: {best_overall_distance}")

def run_sinle_experiment(): # Single-Experiment-Modus
    params = config.single_run_params
    print(f"Algo läuft mit folgenden Parametern: {params}")
    bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
        objectiveNrUsed=params["objectiveNrUsed"],
        specialInitialSolutions=initialSolutionsList,
        population=cityList,
        popSize=params["popSize"],
        eliteSize=params["eliteSize"],
        mutationRate=params["mutationRate"],
        generations=params["generations"]
    )
    if config.plotting_enabled:
        plotRoute(bestRoute, "Best final route", f"Best_final_route_{params['popSize']}_{params['eliteSize']}_{params['mutationRate']}_{params['generations']}.png")
        plotProgress(progressDistance, 'Distance', 'Progress of Distance Minimization', f"Progress_Distance_{params['popSize']}_{params['eliteSize']}_{params['mutationRate']}_{params['generations']}.png")
        plotProgress(progressStress, 'Stress', 'Progress of Stress Minimization', f"Progress_Stress_{params['popSize']}_{params['eliteSize']}_{params['mutationRate']}_{params['generations']}.png")
        plotPopulationAndObjectiveValues(final_population, "Final Population", f"Final_Population_{params['popSize']}_{params['eliteSize']}_{params['mutationRate']}_{params['generations']}.png", Fitness)

    # Beste Parameter und Ergebnisse
        print("\nBeste Parameter und Ergebnisse:")
        print(f"Populationsgröße: {params['popSize']}")
        print(f"Elitegröße: {params['eliteSize']}")
        print(f"Mutationsrate: {params['mutationRate']}")
        print(f"Generationen: {params['generations']}")
        print(f"Beste Distanz: {1 / rankRoutes([bestRoute], 1)[0][1]}")

if __name__ == "__main__":
    if config.tuning_mode:
        run_experiments()
    else:
        run_sinle_experiment()
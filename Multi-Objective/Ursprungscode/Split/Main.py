import random
from City import City
from GeneticAlgorithm import geneticAlgorithm
from Helpers import getCityBasedOnNr
from config import (single_run_params, tuning_mode, popSizes, eliteSizes, mutationRates, generations_list, plotting_enabled, 
                    csv_enabled, saving_enabled, output_directory, selection_method, crossover_method, mutation_method, initial_solution, 
                    gurobi_enabled, selection_methods, crossover_methods, mutation_methods)
import config
from Plotting import plotPopulationAndObjectiveValues, plotRoute, plotProgress, plotParetoFront
from RankRoutes import rankRoutes
from Helpers import save_results_to_csv
from InitialPopulation import createGreedyRoute, create_city_list_from_csv
from gurobi import gurobi_tsp, calculate_total_distance_and_stress
from Plotting_InitialSolution import plot_initial_solutions

def print_current_config():
    print("Current configuration:")
    for key, value in single_run_params.items():
        print(f"{key}: {value}")
    print(f"Selection Method: {selection_method}")
    print(f"Crossover Method: {crossover_method}")
    print(f"Mutation Method: {mutation_method}")

random.seed(44)
cityList = []

for i in range(1,26):
    cityList.append(City(nr= i, traffic=int(random.random()*40), x=int(random.random() * 200), y=int(random.random() * 200)))
print(cityList)
cityNumbersRoute1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

route1 = []
for nr in cityNumbersRoute1:
    route1.append(getCityBasedOnNr(cityList,nr))

# Define the start city and objective
startCityNr = 1 # Starting with city number 1
objective = 2    # 1 = Minimize distance, 2 = Minimize stress

# Generate the special initial route based on the chosen objective
route2 = createGreedyRoute(cityList, startCityNr, objective)

# Beispiel: Erstellen der cityList aus der CSV-Datei
filename = 'Multi-Objective/Ursprungscode/Split/Visualisations/Best_Route.csv'
route3 = create_city_list_from_csv(filename)

if initial_solution == "random":
    initial_solutionsList = [route1]
if initial_solution == "nearest neighbour":
    initial_solutionsList = [route2]
if initial_solution == "solution phase 1":
    initial_solutionsList = [route3]




print_current_config()

# Nur mit einer Parameterkonfiguration laufen
def run_single_experiment():
    params = single_run_params
    print(f"ALgo läuft mit folgenden Parametern: {params}")
    bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
        objectiveNrUsed=params["objectiveNrUsed"],
        specialInitialSolutions=initial_solutionsList,
        population=cityList,
        popSize=params["popSize"],
        eliteSize=params["eliteSize"],
        mutationRate=params["mutationRate"],
        generations=params["generations"]
    )
    if plotting_enabled:
        plotRoute(bestRoute, "Best final route")
        plotProgress(progressDistance, 'Distance', 'Progress of Distance Minimization')
        plotProgress(progressStress, 'Stress', 'Progress of Stress Minimization')
        plotPopulationAndObjectiveValues(final_population, "Final Population")
        plotParetoFront(final_population, "Pareto Front")

    # print("\nBeste Parameter und Ergebnisse:")
    # print(f"PopSize: {params['popSize']}")
    # print(f"EliteSize: {params['eliteSize']}")
    # print(f"MutationRate: {params['mutationRate']}")
    # print(f"Generations: {params['generations']}")

def run_experiments():  # Tuning-Modus
    best_overall_route = None
    best_overall_distance = float('inf')
    best_overall_stress = float('inf')
    best_progress_distance = None
    best_progress_stress = None
    best_final_population = None
    best_params = None
    results = []

    for popSize in config.popSizes:
        for eliteSize in config.eliteSizes:
            for mutationRate in config.mutationRates:
                for generations in config.generations_list:
                    for selection_method in config.selection_methods:
                        for crossover_method in config.crossover_methods:
                            for mutation_method in config.mutation_methods:
                                print(f"Running with {popSize=}, {eliteSize=}, {mutationRate=}, {generations=}, {selection_method=}, {crossover_method=}, {mutation_method=}")
                                bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
                                    objectiveNrUsed=config.single_run_params["objectiveNrUsed"],
                                    specialInitialSolutions=initial_solutionsList, 
                                    population=cityList,
                                    popSize=popSize,
                                    eliteSize=eliteSize,
                                    mutationRate=mutationRate,
                                    generations=generations
                                )
                                final_distance = 1 / rankRoutes([bestRoute], 1)[0][1]
                                final_stress = 1 / rankRoutes([bestRoute], 2)[0][1]

                                if config.single_run_params["objectiveNrUsed"] == 1:
                                    current_metric = final_distance
                                elif config.single_run_params["objectiveNrUsed"] == 2:
                                    current_metric = final_stress
                                elif config.single_run_params["objectiveNrUsed"] == 3:
                                    current_metric = final_distance + final_stress

                                results.append({
                                    "popSize": popSize,
                                    "eliteSize": eliteSize,
                                    "mutationRate": mutationRate,
                                    "generations": generations,
                                    "selection_method": selection_method,
                                    "crossover_method": crossover_method,
                                    "mutation_method": mutation_method,
                                    "finalDistance": final_distance,
                                    "finalStress": final_stress,
                                    "current_metric": current_metric,
                                    "params": f"{popSize}_{eliteSize}_{mutationRate}_{generations}_{selection_method}_{crossover_method}_{mutation_method}"
                                })

                                if config.single_run_params["objectiveNrUsed"] == 1:
                                    if current_metric < best_overall_distance:
                                        best_overall_distance = current_metric
                                        best_overall_route = bestRoute
                                        best_progress_distance = progressDistance
                                        best_progress_stress = progressStress
                                        best_final_population = final_population
                                        best_params = (popSize, eliteSize, mutationRate, generations, selection_method, crossover_method, mutation_method)
                                elif config.single_run_params["objectiveNrUsed"] == 2:
                                    if current_metric < best_overall_stress:
                                        best_overall_stress = current_metric
                                        best_overall_route = bestRoute
                                        best_progress_distance = progressDistance
                                        best_progress_stress = progressStress
                                        best_final_population = final_population
                                        best_params = (popSize, eliteSize, mutationRate, generations, selection_method, crossover_method, mutation_method)
                                elif config.single_run_params["objectiveNrUsed"] == 3:
                                    if current_metric < best_overall_distance + best_overall_stress:
                                        best_overall_metric = current_metric
                                        best_overall_route = bestRoute
                                        best_progress_distance = progressDistance
                                        best_progress_stress = progressStress
                                        best_final_population = final_population
                                        best_params = (popSize, eliteSize, mutationRate, generations, selection_method, crossover_method, mutation_method)


    print(f"PopSize: {best_params[0]}")
    print(f"EliteSize: {best_params[1]}")
    print(f"MutationRate: {best_params[2]}")
    print(f"Generations: {best_params[3]}")
    print(f"Selection Method: {best_params[4]}")
    print(f"Crossover Method: {best_params[5]}")
    print(f"Mutation Method: {best_params[6]}")


    if config.single_run_params["objectiveNrUsed"] == 1:
        print(f"Final Distance: {best_overall_distance}")
    elif config.single_run_params["objectiveNrUsed"] == 2:
        print(f"Final Stress: {best_overall_stress}")
    elif config.single_run_params["objectiveNrUsed"] == 3:
        print(f"Final Combined Metric (Distance + Stress): {best_overall_metric}")



    if plotting_initialsolution_enabeld:
        plot_initial_solutions()

if __name__ == "__main__":
    if tuning_mode:
        run_experiments()
    elif gurobi_enabled:
        optimal_route = gurobi_tsp(cityList)
    else:
        run_single_experiment()

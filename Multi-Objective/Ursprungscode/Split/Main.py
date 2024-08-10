import random
from City import City
from GeneticAlgorithm import geneticAlgorithm
from Helpers import getCityBasedOnNr
from config import single_run_params, tuning_mode, popSizes, eliteSizes, mutationRates, generations_list, plotting_enabled, csv_enabled, saving_enabled, output_directory, selection_method, crossover_method, mutation_method, initial_solution, gurobi_enabled, plotting_initialsolution_enabeld
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

def run_experiements(): # Tuning-Modus
    results = []
    best_overall_distance = float('inf')
    best_overall_stress = float('inf')
    best_overall_route = None
    best_progress_distance = []
    best_progress_stress = []
    best_final_population = None
    best_params = None

    for popSize in popSizes:
        for eliteSize in eliteSizes:
            for mutationRate in mutationRates:
                for generations in generations_list:
                    params = {
                        "popSize": popSize,
                        "eliteSize": eliteSize,
                        "mutationRate": mutationRate,
                        "generations": generations,
                        "objectiveNrUsed": single_run_params["objectiveNrUsed"]
                    }
                    print(f"Running experiment with {params}")
                    bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
                        objectiveNrUsed=params["objectiveNrUsed"],
                        specialInitialSolutions=initial_solutionsList,
                        population=cityList,
                        popSize=params["popSize"],
                        eliteSize=params["eliteSize"],
                        mutationRate=params["mutationRate"],
                        generations=params["generations"]
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
                        best_params = params
                    if final_stress < best_overall_stress:
                        best_overall_stress = final_stress
                    print(f"Ergebnisse für popSize={popSize}, eliteSize={eliteSize}, mutationRate={mutationRate}, generations={generations}, Stress = {final_distance}:")

    if csv_enabled:
        save_results_to_csv(results, "results.csv")


    if best_overall_route is not None and plotting_enabled:
        plotRoute(best_overall_route, "Best final route")
        plotProgress(best_progress_distance, 'Distance', 'Progress of Distance Minimization')
        plotProgress(best_progress_stress, 'Stress', 'Progress of Stress Minimization')
        plotPopulationAndObjectiveValues(best_final_population, "Final Population")
        plotParetoFront(best_final_population, "Pareto Front")

    if best_params is not None:
        print("\nBeste Parameter und Ergebnisse: ")
        print(f"PopSize: {best_params['popSize']}")
        print(f"EliteSize: {best_params['eliteSize']}")
        print(f"MutationRate: {best_params['mutationRate']}")
        print(f"Generations: {best_params['generations']}")

    if plotting_initialsolution_enabeld:
        plot_initial_solutions()

if __name__ == "__main__":
    if tuning_mode:
        run_experiements()
    elif gurobi_enabled:
        optimal_route = gurobi_tsp(cityList)
    else:
        run_single_experiment()

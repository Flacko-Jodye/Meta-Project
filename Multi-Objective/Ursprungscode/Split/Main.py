import random
from City import City
from GeneticAlgorithm import geneticAlgorithm
from Helpers import getCityBasedOnNr
from config import single_run_params, tuning_mode, popSizes, eliteSizes, mutationRates, generations_list, plotting_enabled, csv_enabled, saving_enabled, output_directory
from Plotting import plotPopulationAndObjectiveValues, plotRoute, plotProgress
from RankRoutes import rankRoutes
from Helpers import save_results_to_csv

def print_current_config():
    print("Current configuration:")
    for key, value in single_run_params.items():
        print(f"{key}: {value}")

cityList = []
random.seed(44)

for i in range(1,26):
    cityList.append(City(nr= i, traffic=int(random.random()*40), x=int(random.random() * 200), y=int(random.random() * 200)))
print(cityList)
cityNumbersRoute1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

route1 = []
for nr in cityNumbersRoute1:
    route1.append(getCityBasedOnNr(cityList,nr))
initialSolutionsList = [route1]

print_current_config()

# Nur mit einer Parameterkonfiguration laufen
def run_single_experiment():
    params = single_run_params
    print(f"ALgo läuft mit folgenden Parametern: {params}")
    bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
        objectiveNrUsed=params["objectiveNrUsed"],
        specialInitialSolutions=initialSolutionsList,
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
    print("\nBeste Parameter und Ergebnisse:")
    print(f"PopSize: {params['popSize']}")
    print(f"EliteSize: {params['eliteSize']}")
    print(f"MutationRate: {params['mutationRate']}")
    print(f"Generations: {params['generations']}")
    print(f"Final Distance: {1 / rankRoutes([bestRoute], 1)[0][1]}")
    print(f"Final Stress: {1 / rankRoutes([bestRoute], 2)[0][1]}")

def run_experiements(): # Tuning-Modus
    results = []
    best_overall_distance = float('inf')
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
                        specialInitialSolutions=initialSolutionsList,
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
                    print(f"Ergebnisse für popSize={popSize}, eliteSize={eliteSize}, mutationRate={mutationRate}, generations={generations}, Stress = {final_stress}:")
    
    if csv_enabled:
        save_results_to_csv(results, "results.csv")

    if best_overall_route is not None and plotting_enabled:
        plotRoute(best_overall_route, "Best final route")
        plotProgress(best_progress_distance, 'Distance', 'Progress of Distance Minimization')
        plotProgress(best_progress_stress, 'Stress', 'Progress of Stress Minimization')
        plotPopulationAndObjectiveValues(best_final_population, "Final Population")

    if best_params is not None:
        print("\nBeste Parameter und Ergebnisse: ")
        print(f"PopSize: {best_params['popSize']}")
        print(f"EliteSize: {best_params['eliteSize']}")
        print(f"MutationRate: {best_params['mutationRate']}")
        print(f"Generations: {best_params['generations']}")
        print(f"Final Distance: {best_overall_distance}")
        print(f"Minimaler Stress: {best_overall_distance}")

if __name__ == "__main__":
    if tuning_mode:
        run_experiements()
    else:
        run_single_experiment()
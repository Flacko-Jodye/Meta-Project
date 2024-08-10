import matplotlib.pyplot as plt
from City import City
from genetic_algorithm import geneticAlgorithm
import config
import random

def plotSelectionImpact(selection_methods, progress_data, ylabel, title, filename_prefix):
    plt.figure()
    for method, data in progress_data.items():
        if len(data) > 0:
            plt.plot(data, label=f'{method}')
    plt.ylabel(ylabel)
    plt.xlabel('Generation')
    plt.title(title)
    plt.legend()
    plt.savefig(f"{filename_prefix}.png")
    plt.close()

def run_selection_impact_analysis():
    cityList = []
    random.seed(44)
    for i in range(1, 26):
        cityList.append(City(nr=i, traffic=int(random.random() * 40), x=int(random.random() * 200), y=int(random.random() * 200)))

    initialSolutionsList = []

    progress_distances = {}
    progress_stresses = {}

    selection_methods = ["roulette", "rank", "steady_state", "tournament"]

    for method in selection_methods:
        config.selection_method = method
        print(f"Running for selection method: {config.selection_method}")
        bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
            objectiveNrUsed=config.single_run_params["objectiveNrUsed"],
            specialInitialSolutions=initialSolutionsList,
            population=cityList,
            popSize=config.single_run_params["popSize"],
            eliteSize=config.single_run_params["eliteSize"],
            mutationRate=config.single_run_params["mutationRate"],
            generations=config.single_run_params["generations"]
        )
        progress_distances[method] = progressDistance
        progress_stresses[method] = progressStress

    # Plot the selection method impacts for Distance
    if config.single_run_params["objectiveNrUsed"] == 1:
        plotSelectionImpact(selection_methods, progress_distances, 'Distance', 'Impact of Selection Method on Distance', 'Impact_SelectionMethod_Distance')
    # Plot the selection method impacts for Stress
    elif config.single_run_params["objectiveNrUsed"] == 2:
        plotSelectionImpact(selection_methods, progress_stresses, 'Stress', 'Impact of Selection Method on Stress', 'Impact_SelectionMethod_Stress')

if __name__ == "__main__":
    run_selection_impact_analysis()

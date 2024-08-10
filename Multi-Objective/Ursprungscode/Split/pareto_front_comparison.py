import matplotlib.pyplot as plt
from City import City
from GeneticAlgorithm import geneticAlgorithm
import config
import random
from Plotting import get_pareto_front
from Fitness import Fitness

def plot_pareto_fronts(selection_methods, pareto_fronts, title, filename_prefix):
    plt.figure()
    for method, front in pareto_fronts.items():
        distances = [Fitness(route).routeDistance() for route in front]
        stresses = [Fitness(route).routeStress() for route in front]
        plt.scatter(distances, stresses, label=f'{method}')
    plt.xlabel('Distance')
    plt.ylabel('Stress')
    plt.title(title)
    plt.legend()
    plt.savefig(f"{filename_prefix}.png")
    plt.show()
    plt.close()

def run_selection_pareto_front_analysis():
    cityList = []
    random.seed(44)
    for i in range(1, 26):
        cityList.append(City(nr=i, traffic=int(random.random() * 40), x=int(random.random() * 200), y=int(random.random() * 200)))

    initialSolutionsList = []

    pareto_fronts = {}

    selection_methods = ["roulette", "rank", "steady_state", "tournament"]

    for method in selection_methods:
        config.selection_method = method
        print(f"Running for selection method: {config.selection_method}")
        _, _, _, final_population = geneticAlgorithm(
            objectiveNrUsed=3,  # Pareto front for multiobjective
            specialInitialSolutions=initialSolutionsList,
            population=cityList,
            popSize=config.single_run_params["popSize"],
            eliteSize=config.single_run_params["eliteSize"],
            mutationRate=config.single_run_params["mutationRate"],
            generations=config.single_run_params["generations"]
        )
        pareto_fronts[method] = get_pareto_front(final_population)

    # Plot the Pareto fronts for different selection methods
    plot_pareto_fronts(selection_methods, pareto_fronts, 'Pareto Fronts of Different Selection Methods', 'Pareto_Front_SelectionMethods')

if __name__ == "__main__":
    run_selection_pareto_front_analysis()

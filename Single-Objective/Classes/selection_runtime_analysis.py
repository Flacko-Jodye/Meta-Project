import time
import matplotlib.pyplot as plt
import random
from City import City
from genetic_algorithm import geneticAlgorithm
import config

def measure_runtime(selection_method):
    config.selection_method = selection_method
    start_time = time.time()

    # Erstellen Sie eine Liste von Städten
    cityList = []
    random.seed(44)
    for i in range(1, 26):
        cityList.append(City(nr=i, traffic=int(random.random() * 40), x=int(random.random() * 200), y=int(random.random() * 200)))

    # Run genetic algorithm with the current selection method
    bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
        objectiveNrUsed=config.single_run_params["objectiveNrUsed"],
        specialInitialSolutions=[],
        population=cityList,
        popSize=config.single_run_params["popSize"],
        eliteSize=config.single_run_params["eliteSize"],
        mutationRate=config.single_run_params["mutationRate"],
        generations=config.single_run_params["generations"]
    )

    end_time = time.time()
    return end_time - start_time

def run_selection_runtime_analysis():
    selection_methods = ["roulette", "rank", "steady_state", "tournament"]
    runtimes = []

    for method in selection_methods:
        print(f"Measuring runtime for selection method: {method}")
        runtime = measure_runtime(method)
        runtimes.append(runtime)
        print(f"Runtime for {method}: {runtime:.2f} seconds")

    # Plotting the runtime as a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(selection_methods, runtimes, color='skyblue')
    plt.xlabel('Selection Method')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime of Selection Methods')
    plt.savefig("selection_method_runtime.png")
    plt.show()

if __name__ == "__main__":
    run_selection_runtime_analysis()

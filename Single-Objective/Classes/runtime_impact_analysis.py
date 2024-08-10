import time
import matplotlib.pyplot as plt
from City import City
from genetic_algorithm import geneticAlgorithm
import random
import config

def measure_runtime(params, cityList):
    start_time = time.time()
    bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
        objectiveNrUsed=params["objectiveNrUsed"],
        specialInitialSolutions=[],
        population=cityList,
        popSize=params["popSize"],
        eliteSize=params["eliteSize"],
        mutationRate=params["mutationRate"],
        generations=params["generations"]
    )
    end_time = time.time()
    return end_time - start_time

def plot_runtime_impact(parameter_name, parameter_values, runtimes, ylabel, title, filename_prefix):
    plt.figure()
    plt.plot(parameter_values, runtimes, marker='o')
    plt.ylabel(ylabel)
    plt.xlabel(parameter_name)
    plt.title(title)
    plt.savefig(f"{filename_prefix}_{parameter_name}.png")
    plt.close()

def run_runtime_impact_analysis():
    cityList = []
    random.seed(44)
    for i in range(1, 26):
        cityList.append(City(nr=i, traffic=int(random.random() * 40), x=int(random.random() * 200), y=int(random.random() * 200)))

    runtime_results = { 'popSize': [], 'eliteSize': [], 'mutationRate': [], 'generations': [] }

    # Measure impact of popSize on runtime
    for popSize in config.popSizes:
        params = {
            "popSize": popSize,
            "eliteSize": config.single_run_params["eliteSize"],
            "mutationRate": config.single_run_params["mutationRate"],
            "generations": config.single_run_params["generations"],
            "objectiveNrUsed": config.single_run_params["objectiveNrUsed"]
        }
        runtime = measure_runtime(params, cityList)
        runtime_results['popSize'].append(runtime)

    # Measure impact of eliteSize on runtime
    for eliteSize in config.eliteSizes:
        params = {
            "popSize": config.single_run_params["popSize"],
            "eliteSize": eliteSize,
            "mutationRate": config.single_run_params["mutationRate"],
            "generations": config.single_run_params["generations"],
            "objectiveNrUsed": config.single_run_params["objectiveNrUsed"]
        }
        runtime = measure_runtime(params, cityList)
        runtime_results['eliteSize'].append(runtime)

    # Measure impact of mutationRate on runtime
    for mutationRate in config.mutationRates:
        params = {
            "popSize": config.single_run_params["popSize"],
            "eliteSize": config.single_run_params["eliteSize"],
            "mutationRate": mutationRate,
            "generations": config.single_run_params["generations"],
            "objectiveNrUsed": config.single_run_params["objectiveNrUsed"]
        }
        runtime = measure_runtime(params, cityList)
        runtime_results['mutationRate'].append(runtime)

    # Measure impact of generations on runtime
    for generations in config.generations_list:
        params = {
            "popSize": config.single_run_params["popSize"],
            "eliteSize": config.single_run_params["eliteSize"],
            "mutationRate": config.single_run_params["mutationRate"],
            "generations": generations,
            "objectiveNrUsed": config.single_run_params["objectiveNrUsed"]
        }
        runtime = measure_runtime(params, cityList)
        runtime_results['generations'].append(runtime)

    # Plot the runtime impacts
    plot_runtime_impact('popSize', config.popSizes, runtime_results['popSize'], 'Runtime (seconds)', 'Impact of PopSize on Runtime', 'Impact_PopSize_Runtime')
    plot_runtime_impact('eliteSize', config.eliteSizes, runtime_results['eliteSize'], 'Runtime (seconds)', 'Impact of EliteSize on Runtime', 'Impact_EliteSize_Runtime')
    plot_runtime_impact('mutationRate', config.mutationRates, runtime_results['mutationRate'], 'Runtime (seconds)', 'Impact of MutationRate on Runtime', 'Impact_MutationRate_Runtime')
    plot_runtime_impact('generations', config.generations_list, runtime_results['generations'], 'Runtime (seconds)', 'Impact of Generations on Runtime', 'Impact_Generations_Runtime')

if __name__ == "__main__":
    run_runtime_impact_analysis()

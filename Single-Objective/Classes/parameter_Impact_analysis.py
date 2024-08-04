import matplotlib.pyplot as plt
import config
from City import City
from genetic_algorithm import geneticAlgorithm
import random

def plotParameterImpact(parameter_name, parameter_values, progress_data, ylabel, title, filename_prefix):
    plt.figure()
    for i, param_value in enumerate(parameter_values):
        if len(progress_data[i]) > 0:
            plt.plot(progress_data[i], label=f'{parameter_name}={param_value}')
    plt.ylabel(ylabel)
    plt.xlabel('Generation')
    plt.title(title)
    plt.legend()
    plt.savefig(f"{filename_prefix}_{parameter_name}.png")
    plt.close()

def run_parameter_impact_analysis():
    cityList = []
    random.seed(44)
    for i in range(1, 26):
        cityList.append(City(nr=i, traffic=int(random.random() * 40), x=int(random.random() * 200), y=int(random.random() * 200)))

    initialSolutionsList = []

    progress_distances = { 'popSize': [], 'eliteSize': [], 'mutationRate': [], 'generations': [] }
    progress_stresses = { 'popSize': [], 'eliteSize': [], 'mutationRate': [], 'generations': [] }

    # Analyze impact of popSize
    for popSize in config.popSizes:
        bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
            objectiveNrUsed=config.single_run_params["objectiveNrUsed"],
            specialInitialSolutions=initialSolutionsList,
            population=cityList,
            popSize=popSize,
            eliteSize=config.single_run_params["eliteSize"],
            mutationRate=config.single_run_params["mutationRate"],
            generations=config.single_run_params["generations"]
        )
        progress_distances['popSize'].append(progressDistance)
        progress_stresses['popSize'].append(progressStress)

    # Analyze impact of eliteSize
    for eliteSize in config.eliteSizes:
        bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
            objectiveNrUsed=config.single_run_params["objectiveNrUsed"],
            specialInitialSolutions=initialSolutionsList,
            population=cityList,
            popSize=config.single_run_params["popSize"],
            eliteSize=eliteSize,
            mutationRate=config.single_run_params["mutationRate"],
            generations=config.single_run_params["generations"]
        )
        progress_distances['eliteSize'].append(progressDistance)
        progress_stresses['eliteSize'].append(progressStress)

    # Analyze impact of mutationRate
    for mutationRate in config.mutationRates:
        bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
            objectiveNrUsed=config.single_run_params["objectiveNrUsed"],
            specialInitialSolutions=initialSolutionsList,
            population=cityList,
            popSize=config.single_run_params["popSize"],
            eliteSize=config.single_run_params["eliteSize"],
            mutationRate=mutationRate,
            generations=config.single_run_params["generations"]
        )
        progress_distances['mutationRate'].append(progressDistance)
        progress_stresses['mutationRate'].append(progressStress)

    # Analyze impact of generations
    for generations in config.generations_list:
        bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
            objectiveNrUsed=config.single_run_params["objectiveNrUsed"],
            specialInitialSolutions=initialSolutionsList,
            population=cityList,
            popSize=config.single_run_params["popSize"],
            eliteSize=config.single_run_params["eliteSize"],
            mutationRate=config.single_run_params["mutationRate"],
            generations=generations
        )
        progress_distances['generations'].append(progressDistance)
        progress_stresses['generations'].append(progressStress)

    # Plot the parameter impacts for Distance
    if config.single_run_params["objectiveNrUsed"] == 1:
        plotParameterImpact('popSize', config.popSizes, progress_distances['popSize'], 'Distance', 'Impact of PopSize on Distance', 'Impact_PopSize_Distance')
        plotParameterImpact('eliteSize', config.eliteSizes, progress_distances['eliteSize'], 'Distance', 'Impact of EliteSize on Distance', 'Impact_EliteSize_Distance')
        plotParameterImpact('mutationRate', config.mutationRates, progress_distances['mutationRate'], 'Distance', 'Impact of MutationRate on Distance', 'Impact_MutationRate_Distance')
        plotParameterImpact('generations', config.generations_list, progress_distances['generations'], 'Distance', 'Impact of Generations on Distance', 'Impact_Generations_Distance')
    # Plot the parameter impacts for Stress
    elif config.single_run_params["objectiveNrUsed"] == 2:
        plotParameterImpact('popSize', config.popSizes, progress_stresses['popSize'], 'Stress', 'Impact of PopSize on Stress', 'Impact_PopSize_Stress')
        plotParameterImpact('eliteSize', config.eliteSizes, progress_stresses['eliteSize'], 'Stress', 'Impact of EliteSize on Stress', 'Impact_EliteSize_Stress')
        plotParameterImpact('mutationRate', config.mutationRates, progress_stresses['mutationRate'], 'Stress', 'Impact of MutationRate on Stress', 'Impact_MutationRate_Stress')
        plotParameterImpact('generations', config.generations_list, progress_stresses['generations'], 'Stress', 'Impact of Generations on Stress', 'Impact_Generations_Stress')

if __name__ == "__main__":
    run_parameter_impact_analysis()

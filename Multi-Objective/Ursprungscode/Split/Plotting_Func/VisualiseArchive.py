import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Fitness import Fitness
from Plotting import plotRoute
from RankRoutes import rankRoutes, rankRoutesBasedOnDominance
from Archive import determineNonDominatedArchive

def visualize_archive(population, objectiveNrUsed):
    archive = determineNonDominatedArchive(population, rankRoutes(population, objectiveNrUsed))
    print(f"No. of solutions in archive: {len(archive)}")
    for i, route in enumerate(archive):
        print(f"Archive Solution {i + 1}")
        print(f"Distance: {Fitness(route).routeDistance()}")
        print(f"Stress: {Fitness(route).routeStress()}")
        print(f"Fitness: {rankRoutes([route], 3)[0][1]}")
        print("----")
        plotRoute(route, f"Archive Solution {i + 1}")

if __name__ == "__main__":
    from GeneticAlgorithm import geneticAlgorithm
    from config import single_run_params, initial_solution
    from InitialPopulation import createGreedyRoute, create_city_list_from_csv
    from City import City
    import random

    random.seed(44)
    cityList = []
    for i in range(1, 26):
        cityList.append(City(nr=i, traffic=int(random.random() * 40), x=int(random.random() * 200), y=int(random.random() * 200)))

    cityNumbersRoute1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    route1 = [city for city in cityList if city.nr in cityNumbersRoute1]

    startCityNr = 1  # Starting with city number 1
    objective = 1  # 1 = Minimize distance, 2 = Minimize stress
    route2 = createGreedyRoute(cityList, startCityNr, objective)

    filename = '../Visualisations/Best_Route.csv'  # Adjust the path as necessary
    route3 = create_city_list_from_csv(filename)

    if initial_solution == "random":
        initial_solutionsList = [route1]
    elif initial_solution == "nearest neighbour":
        initial_solutionsList = [route2]
    elif initial_solution == "solution phase 1":
        initial_solutionsList = [route3]

    bestRoute, progressDistance, progressStress, final_population = geneticAlgorithm(
        objectiveNrUsed=single_run_params["objectiveNrUsed"],
        specialInitialSolutions=initial_solutionsList,
        population=cityList,
        popSize=single_run_params["popSize"],
        eliteSize=single_run_params["eliteSize"],
        mutationRate=single_run_params["mutationRate"],
        generations=single_run_params["generations"]
    )

    visualize_archive(final_population, single_run_params["objectiveNrUsed"])

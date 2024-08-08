import random
from Helpers import getCityBasedOnNr 
import csv
from City import City

def findNearestCity(currentCity, remainingCities, objective=1):
    """
    Finds the nearest city based on the given objective.
    :param currentCity: The current city object.
    :param remainingCities: List of remaining city objects.
    :param objective: 1 for distance, 2 for stress.
    :return: The nearest city object based on the selected metric.
    """
    nearestCity = None
    minMetric = float('inf')
    
    for city in remainingCities:
        if objective == 1:  # Minimierung der Distanz
            metric = currentCity.distance(city)
        elif objective == 2:  # Minimierung des Stresses
            metric = currentCity.stress(city)
        
        if metric < minMetric:
            minMetric = metric
            nearestCity = city
            
    return nearestCity

def createGreedyRoute(cityList, startCityNr, objective=1):
    """
    Creates a route using a greedy algorithm based on the specified objective.
    :param cityList: List of all city objects.
    :param startCityNr: The starting city's number.
    :param objective: 1 for minimizing distance, 2 for minimizing stress.
    :return: A list representing the route.
    """
    remainingCities = cityList[:]
    startCity = getCityBasedOnNr(remainingCities, startCityNr)
    route = [startCity]
    remainingCities.remove(startCity)
    
    currentCity = startCity
    while remainingCities:
        nextCity = findNearestCity(currentCity, remainingCities, objective)
        route.append(nextCity)
        remainingCities.remove(nextCity)
        currentCity = nextCity
    
    return route

def create_city_list_from_csv(filename):
    city_list = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Überspringen des Headers, falls vorhanden
        for row in reader:
            if len(row) < 4:
                print(f"Skipping incomplete row: {row}")
                continue
            try:
                nr = int(row[0])
                traffic = int(row[1])
                x = int(row[2])
                y = int(row[3])
                city = City(nr, traffic, x, y)
                city_list.append(city)
            except ValueError as e:
                print(f"Skipping row due to conversion error: {row}, Error: {e}")
                continue
    return city_list

def createRoute(cityList):
    # random.seed(44)
    route = random.sample(cityList, len(cityList))
    return route

#Create first "population" (list of routes)
def initialPopulation(popSize, cityList, specialInitialSolutions):
    population = []
    population.extend(specialInitialSolutions)
    #TODO: Hinzufügen der speziellen Initiallösungen aus specialInitialSolutions
    

    numberInitialSolutions = len(specialInitialSolutions)
    print ("Number of special initial solutions:" + str(numberInitialSolutions))
    #for i in range(0, popSize):
    for i in range(numberInitialSolutions, popSize):
        population.append(createRoute(cityList))
    return population

import random
from config import mutation_method, spea2_archive_enabled

#Create function to mutate a single route
#we’ll use swap mutation.
#This means that, with specified low probability, 
#two cities will swap places in our route.
def swap_mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual


"Reverse Sequence und Partial Shuffle Mutation einbauen"   

def inversion_mutation(individual, mutation_rate):
    if random.random() < mutation_rate:
        # 2 Indizes zufällig auswählen
        index1, index2 = sorted(random.sample(range(len(individual)), 2))
        # Invertieren der Reihenfolge innerhalb des Intervalls
        individual[index1:index2] = reversed(individual[index1:index2])
    return individual

def mutate(individual, mutation_rate):
    if mutation_method == "swap":
        return swap_mutate(individual, mutation_rate)
    elif mutation_method == "inversion":
        return inversion_mutation(individual, mutation_rate)
    else:
        raise ValueError("Unknown mutation method: {}".format(mutation_method))

#Create function to run mutation over entire population
def mutatePopulation(population, mutationRate, archiveSize):
    # random.seed(44)
    mutatedPop = []
    
    #mating pool is sorted in order of fitness
    #here elitism instead of fixed archive
    #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
    for ind in range(0, archiveSize):
        mutatedPop.append(population[ind])
    for ind in range(archiveSize, len(population)):
    #for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def mutatePopulationWithConfig(population, mutationRate, eliteSize, archiveSize):
    size = archiveSize if spea2_archive_enabled else eliteSize
    return mutatePopulation(population, mutationRate, size)
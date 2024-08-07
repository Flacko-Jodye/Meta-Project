import random
#TODO: Ggf. noch weitere Crossover-Methoden hinzufügen


# Standard-Methoden für Crossover
def ordered_crossover (parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)
    #In ordered crossover, we randomly select a subset of the first parent string
    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    #and then fill the remainder of the route with the genes from the second parent
    #in the order in which they appear, 
    #without duplicating any genes in the selected subset from the first parent    
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

def one_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point]

    for city in parent2:
        if city not in child:
            child.append(city)

    return child

def edge_recombination_crossover(parent1, parent2):
    def build_edge_map(p1, p2):
        edge_map = {i: set() for i in range(1, len(p1) + 1)}
        for p in [p1, p2]:
            for i in range(len(p)):
                left = p[i - 1] if i > 0 else p[-1]
                right = p[i + 1] if i < len(p) - 1 else p[0]
                edge_map[p[i].nr].update({left.nr, right.nr})
        return edge_map
    
    edge_map = build_edge_map(parent1, parent2)
    current_city = random.choice(parent1)
    child = [current_city]

    while len(child) < len(parent1):
        for neighbors in edge_map.values():
            neighbors.discard(current_city.nr)
        
        if edge_map[current_city.nr]:
            next_city_nr = min(edge_map[current_city.nr], key=lambda x: len(edge_map[x]))
        else:
            remaining_cities = [city for city in parent1 if city not in child]
            next_city_nr = random.choice(remaining_cities).nr
        
        current_city = next(city for city in parent1 if city.nr == next_city_nr)
        child.append(current_city)
    
    return child
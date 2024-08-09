import numpy as np
from Fitness import Fitness, isSameSolution, computeEuclideanDistance
from config import use_fixed_archive, max_archive_size

def determineNonDominatedArchive(currentGen, popRanked):
    archive = []
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            archive.append(currentGen[popRanked[i][0]])
    # Prüfen auf doppelte Lösungen
    sameSolutions = []

    for i in range(0, len(archive)-1):
        for j in range(i+1, len(archive)):
            if isSameSolution(archive[i], archive[j]):
                sameSolutions.append(j)

    newArchive = []
    for i in range(0, len(archive)):
        if (not sameSolutions.__contains__(i)):
            newArchive.append(archive[i])
    
    if use_fixed_archive and len(newArchive) > max_archive_size:
        newArchive = reduceArchive(newArchive, max_archive_size)
    return newArchive

#falls max_archive_size überschritten wird:weniger diverse und weniger fitte Lösungen werden entfernt
def reduceArchive(archive, max_size):
    if len(archive) <= max_size:
        return archive

    combined_scores = []
    for i in range(len(archive)):
        distances = []
        for j in range(len(archive)):
            if i != j:
                distances.append(computeEuclideanDistance(
                    Fitness(archive[i]).routeDistance(),
                    Fitness(archive[j]).routeDistance(),
                    Fitness(archive[i]).routeStress(),
                    Fitness(archive[j]).routeStress()
                ))
        diversity_score = min(distances) # Kleinster Abstand zu den Nachbarn
        fitness_distance = 1 / Fitness(archive[i]).routeFitnessDistanceBased()
        fitness_stress = 1 / Fitness(archive[i]).routeFitnessStressBased()
        combined_fitness = 0.5 * fitness_distance + 0.5 * fitness_stress    # Gewichtete Kombination beide Fitness-Werte

        combined_score = 0.7 * combined_fitness + 0.3 * diversity_score     # Gewichteter kombinierter Score (70% Fitness, 30% Diversität)
        combined_scores.append((combined_score, archive[i]))

    # Archiv sortieren basiend auf kombinierten Scores
    sorted_archive = [solution for _, solution in sorted(combined_scores, key=lambda x: x[0])]
    
    # Entferne die wenigsten diversen oder ältesten Lösungen bis Archiv die MaxGröße erreicht
    return sorted_archive[:max_size]

def determineNonDominatedArchiveSize(popRanked):
    archiveSize = 0
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            archiveSize += 1
    return min(archiveSize, max_archive_size if use_fixed_archive else archiveSize)

def isSameSolution(individuumA, individuumB):
    length = len(individuumA)
    i = 0
    isSameSolution = True
    while i < length and isSameSolution:
        if not (individuumA[i].nr == individuumB[i].nr):
            isSameSolution = False
            break
        i += 1
    return isSameSolution
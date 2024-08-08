import numpy as np
from Fitness import Fitness, isSameSolution

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
    return newArchive

def determineNonDominatedArchiveSize(popRanked):
    archiveSize = 0
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            archiveSize += 1
    return archiveSize

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
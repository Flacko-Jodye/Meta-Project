import random, pandas as pd, numpy as np
from config import selection_method, tournament_size, replace_size

def selection(popRanked, eliteSize):
    if selection_method == "roulette":
        return rouletteWheelSelection(popRanked, eliteSize)
    elif selection_method == "rank":
        return rankBasedSelection(popRanked, eliteSize)
    elif selection_method == "tournament":
        return tournamentSelection(popRanked, eliteSize, tournament_size)
    elif selection_method == "steady_state":
        return steadyStateSelection(popRanked, eliteSize, replace_size)
    elif selection_method == "archive":
        return selectionWithArchive(popRanked)
    else:
        raise ValueError("Unknown selection method: {}".format(selection_method))

    
def rouletteWheelSelection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

def tournamentSelection(popRanked, eliteSize, tournamentSize):
    selectionResults = []
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        tournament = random.sample(popRanked, tournamentSize)
        winner = max(tournament, key=lambda x: x[1])
        selectionResults.append(winner[0])
    return selectionResults

def rankBasedSelection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df["rank"] = df.Fitness.rank(ascending=False)
    df['cum_sum'] = df["rank"].cumsum()             
    df['cum_perc'] = 100 * df.cum_sum/df["rank"].sum()
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100 *random.random()
        for j in range(0, len(popRanked)):
            if pick <= df.iat[j, df.columns.get_loc("cum_perc")]:
                selectionResults.append(popRanked[j][0])
                break
    return selectionResults

def steadyStateSelection(popRanked, eliteSize, replaceSize):
    selectionResults = []
    for i in range(eliteSize):
        selectionResults.append(popRanked[i][0])
    replaceIndices = random.sample(range(eliteSize, len(popRanked)), replaceSize)
    for index in replaceIndices:
        selectionResults.append(popRanked[index][0])
    return selectionResults

def selectionWithArchive(popRanked):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    for i in range(0, len(popRanked)):
        if (popRanked[i][1] > 1):
            selectionResults.append(popRanked[i][0])
    currentArchiveSize = len(selectionResults)
    for i in range(0, len(popRanked) - currentArchiveSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

# #Create a selection function that will be used to make the list of parent routes
# def selection(popRanked, eliteSize):
#     selectionResults = []
#     #TODO: Z.B. Turnierbasierte Selektion statt fitnessproportionaler Selektion
#     # roulette wheel by calculating a relative fitness weight for each individual
#     df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
#     df['cum_sum'] = df.Fitness.cumsum()
#     df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
#     #We’ll also want to hold on to our best routes, so we introduce elitism
#     for i in range(0, eliteSize):
#         selectionResults.append(popRanked[i][0])
#     #we compare a randomly drawn number to these weights to select our mating pool
#     for i in range(0, len(popRanked) - eliteSize):
#         pick = 100*random.random()
#         for i in range(0, len(popRanked)):
#             if pick <= df.iat[i,3]:
#                 selectionResults.append(popRanked[i][0])
#                 break
#     return selectionResults
    
# def selectionWithArchive(popRanked):
#     selectionResults = []
#     #TODO: Z.B. Turnierbasierte Selektion statt fitnessproportionaler Selektion
#     # roulette wheel by calculating a relative fitness weight for each individual
#     df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
#     df['cum_sum'] = df.Fitness.cumsum()
#     df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
#     #We’ll also want to hold on to our best routes, so we introduce elitism
#     #here wie hold all non-dominated solutions
#     #TODO: ein festes Archiv vorsehen wie es im ursprünglichen SPEA2 vorgesehen ist 
#     for i in range(0, len(popRanked)):
#         if (popRanked[i][1] > 1):
#             selectionResults.append(popRanked[i][0])
#     currentArchiveSize = len(selectionResults)

#     #we compare a randomly drawn number to these weights to select our mating pool
#     for i in range(0, len(popRanked) - currentArchiveSize):
#         pick = 100*random.random()
#         for i in range(0, len(popRanked)):
#             if pick <= df.iat[i,3]:
#                 selectionResults.append(popRanked[i][0])
#                 break
#     return selectionResults
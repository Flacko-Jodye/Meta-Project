# Experiment configurations
plotting_enabled = False
csv_enabled = False
tuning_mode = False

# Selection method: "roulette", "rank", "steady_state", or "tournament"
selection_method = "roulette"
tournament_size = 5             # Relevant for tournament selection
replace_size = 2                # Relevant for steady_state selection

# Parameters for single run
single_run_params = {
    "popSize": 100,
    "eliteSize": 20,
    "mutationRate": 0.01,
    "generations": 500,
    "objectiveNrUsed": 1  # 1 = Minimize distance, 2 = Minimize stress, 3 = Minimize both
}

# Parameters for tuning mode
popSizes = [50, 100, 200, 300]
eliteSizes = [10, 20, 30]
mutationRates = [0.01, 0.02, 0.05, 0.1]
generations_list = [100, 200, 500]
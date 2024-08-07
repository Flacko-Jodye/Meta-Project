import os

# Experiment configurations "Noch alle Modi ermöglichen"
plotting_enabled = False
saving_enabled = False
csv_enabled = True
tuning_mode = False                  # Noch anpassen, dass sowohl seleciton, mutation und rekombination getuned werden können

# Selection method: "roulette", "rank", "steady_state", or "tournament"
selection_method = "roulette"
tournament_size = 5             # Relevant for tournament selection
replace_size = 2                # Relevant for steady_state selection

# Cross-over methods: "order", "one-point", "edge-recombination"

# Mutation Methods: "swap", "inversion", ""


# Parameters for single run
single_run_params = {
    "popSize": 100,
    "eliteSize": 20,
    "mutationRate": 0.02,
    "generations": 500,
    "objectiveNrUsed": 3  # 1 = Minimize distance, 2 = Minimize stress, 3 = Minimize both
}

# Parameters for tuning mode
popSizes = [50, 100, 200, 300]
eliteSizes = [10, 20, 30]
mutationRates = [0.01, 0.02, 0.05, 0.1]
generations_list = [100, 200, 500]

# Output directories
base_dir = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(base_dir, "Visualisations")



# Beste Parameter und Ergebnisse:
# PopSize: 100
# EliteSize: 20
# MutationRate: 0.02
# Generations: 500
# Final Distance: 899.3941604883003
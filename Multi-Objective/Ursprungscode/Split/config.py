import os

# Experiment configurations "Noch alle Modi ermöglichen"
plotting_enabled = True
saving_enabled = False
csv_enabled = False
tuning_mode = False                 #TODO Noch anpassen, dass seleciton, mutation und rekombination getuned werden können
spea2_archive_enabled = False       # Enable SPEA2 archive
plotting_initialsolution_enabeld = False         

# Archiv-Konfiguration
use_fixed_archive = False                # True für festes Arhive, False für dynamisches Archiv
max_archive_size = 20                   # Größe des Archivs

# Hypervolume config
hypervolume_enabled = False              # Enable hypervolume calculation und plotting
hypervolume_plot_2d_enabled = False      # 2D-Plotting of hypervolume
spea2_archive_enabled = False  # Enable SPEA2 archive

gurobi_enabled = False # Enable gurobi solution

#select initial solution: "random", "nearest neighbour", "solution phase 1"
initial_solution = "random"

# Selection method: "roulette", "rank", "steady_state", or "tournament"
selection_method = "roulette"
tournament_size = 5                     # Relevant for tournament selection
replace_size = 2                        # Relevant for steady_state selection

# Cross-over methods: "order", "one-point", "edge-recombination"
crossover_method = "order"

# Mutation Methods: "swap", "inversion"
mutation_method = "swap"


# Parameters for single run
single_run_params = {
    "popSize": 100,
    "eliteSize": 20,
    "mutationRate": 0.02,
    "generations": 10,
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
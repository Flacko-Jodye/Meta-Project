import os

# Configurations
plotting_enabled = False                # Enable plotting
saving_enabled = False                  # Enable saving of plots
csv_enabled = False                     # Enable saving of csv files
tuning_mode = False                     # Enable tuning mode
spea2_archive_enabled = True            # Enable SPEA2 archive

# Archiv-Konfiguration
use_fixed_archive = True               # True für festes Arhive, False für dynamisches Archiv
max_archive_size = 20                   # Größe des Archivs

# Hypervolume config
hypervolume_enabled = True              # Enable hypervolume calculation und plotting
hypervolume_plot_2d_enabled = True      # 2D-Plotting of hypervolume
spea2_archive_enabled = True            # Enable SPEA2 archive

gurobi_enabled = False # Enable gurobi solution

#select initial solution: "random", "nearest neighbour", "solution phase 1"
initial_solution = "solution phase 1"

# Selection method: "roulette", "rank", "steady_state", or "tournament"
selection_method = "tournamnet"
tournament_size = 5                     # Relevant for tournament selection
replace_size = 2                        # Relevant for steady_state selection

# Cross-over methods: "order", "ein_punkt", "edge-recombination"
crossover_method = "ein_punkt"

# Mutation Methods: "swap", "inversion"
mutation_method = "swap"


# Parameters for single run
single_run_params = {
    "popSize": 100,
    "eliteSize": 20,
    "mutationRate": 0.02,
    "generations": 500,
    "objectiveNrUsed": 3  # 1 = Minimize distance, 2 = Minimize stress, 3 = Minimize both
}

# Parameters for tuning mode
popSizes = [100]
eliteSizes = [20]
mutationRates = [0.01]
generations_list = [500]

# Selektionsmethoden für das Tuning
selection_methods = ["roulette", "rank", "steady_state", "tournament"]

# Rekombinationsmethoden für das Tuning
crossover_methods = ["order", "one-point", "edge-recombination"]

# Mutationsmethoden für das Tuning
mutation_methods = ["swap", "inversion"]

# Output directories
base_dir = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(base_dir, "Visualisations")


# Selektionsmethoden für das Tuning
selection_methods = ["roulette", "rank", "steady_state", "tournament"]

# Rekombinationsmethoden für das Tuning
crossover_methods = ["order", "one-point", "edge-recombination"]

# Mutationsmethoden für das Tuning
mutation_methods = ["swap", "inversion"]

# Auswahl der initialen Lösung
# initial_solutions = ["random", "nearest neighbour", "solution phase 1"]

# spea2_archive_enabled_options = [True, False]

# max_archive_sizes = [10, 20, 30, 50]  # Different archive sizes for tuning
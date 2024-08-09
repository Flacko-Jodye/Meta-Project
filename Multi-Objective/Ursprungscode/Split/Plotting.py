import matplotlib.pyplot as plt
from Fitness import Fitness
import os 
from config import plotting_enabled, output_directory, saving_enabled


def plotPopulationAndObjectiveValues(population,title):
    distance = []
    stress = []
    for route in population:
        distance.append(Fitness(route).routeDistance())
        stress.append(Fitness(route).routeStress())
    plt.scatter(distance,stress,marker = "o",color="black")
    plt.ylabel('Stress')
    plt.xlabel('Distance')
    plt.title(title)
    if saving_enabled:
        save_path = os.path.join(output_directory, f"{title.replace(' ', '_')}.png")
        os.makedirs(output_directory, exist_ok=True)
        plt.savefig(save_path)
    if plotting_enabled:
        plt.show()
    plt.clf()

def plotRoute(cityList, title):
    x = []
    y = []
    for item in cityList:
        x.append(item.x)
        y.append(item.y)
        plt.annotate(item.nr,(item.x,item.y))
    x.append(cityList[0].x)
    y.append(cityList[0].y)
    plt.plot(x,y,marker = "x")
    plt.ylabel('Y-Coordinate')
    plt.xlabel('X-Coordinate')
    plt.title(title)
    if saving_enabled:
        save_path = os.path.join(output_directory, f"{title.replace(' ', '_')}.png")
        os.makedirs(output_directory, exist_ok=True)
        plt.savefig(save_path)
    if plotting_enabled:
        plt.show()
    plt.clf()

def plotProgress(progress, ylabel, title):
    plt.plot(progress)
    plt.ylabel(ylabel)
    plt.xlabel('Generation')
    plt.title(title)
    if saving_enabled:
        save_path = os.path.join(output_directory, f"{title.replace(' ', '_')}.png")
        os.makedirs(output_directory, exist_ok=True)
        plt.savefig(save_path)
    if plotting_enabled:
        plt.show()
    plt.clf()

# Funktion zur Bestimmung der nicht-dominanten Lösungen (Pareto-Front)
def get_pareto_front(population):
    pareto_front = []
    for candidate in population:
        candidate_fitness = Fitness(candidate)
        candidate_dominated = False
        for other in population:
            other_fitness = Fitness(other)
            if (other_fitness.routeDistance() <= candidate_fitness.routeDistance() and
                other_fitness.routeStress() <= candidate_fitness.routeStress() and
                (other_fitness.routeDistance() < candidate_fitness.routeDistance() or
                 other_fitness.routeStress() < candidate_fitness.routeStress())):
                candidate_dominated = True
                break
        if not candidate_dominated:
            pareto_front.append(candidate)
    return pareto_front

# Darstellung der Pareto-Front
def plotParetoFront(population, title="Pareto Front"):
    pareto_front = get_pareto_front(population)
    distance = []
    stress = []

    for route in pareto_front:
        fitness = Fitness(route)
        distance.append(fitness.routeDistance())
        stress.append(fitness.routeStress())

    # Sortiere die Punkte der Pareto-Front
    sorted_indices = sorted(range(len(distance)), key=lambda i: distance[i])
    sorted_distance = [distance[i] for i in sorted_indices]
    sorted_stress = [stress[i] for i in sorted_indices]

    # Plot der Pareto-Front
    plt.figure()
    plt.scatter(sorted_distance, sorted_stress, c="blue", alpha=0.6, edgecolors="black")
    plt.plot(sorted_distance, sorted_stress, 'b-', alpha=0.6)

    plt.title(title)
    plt.xlabel("Distance")
    plt.ylabel("Stress")
    plt.grid(True)

    if saving_enabled:
        save_path = os.path.join(output_directory, f"{title.replace(' ', '_')}.png")
        os.makedirs(output_directory, exist_ok=True)
        plt.savefig(save_path)

    plt.show()

def plotHypervolume(hypervolume_progress, title = "Progress of Hypervolume"):
    plt.figure()
    plt.plot(hypervolume_progress)
    plt.ylabel('Hypervolume')
    plt.xlabel('Generation')
    plt.title(title)
    plt.grid(True)
    plt.show()

def plotHypervolume2D(pareto_front, reference_point, title="Hypervolume in 2D Space", point_size = 10):
    distances = [Fitness(route).routeDistance() for route in pareto_front]
    stresses = [Fitness(route).routeStress() for route in pareto_front]

    sorted_pairs = sorted(zip(distances, stresses))
    sorted_distances, sorted_stresses = zip(*sorted_pairs)
    
    plt.figure()
    plt.fill_between(sorted_distances, sorted_stresses, reference_point[1], color="orange", alpha=0.3, label="Hypervolume")
    plt.scatter(sorted_distances, sorted_stresses, marker='o', color='black', s = point_size)
    plt.plot(reference_point[0], reference_point[1], 'ro', label='Reference Point')
    plt.xlabel('Distance (Objective 1)')
    plt.ylabel('Stress (Objective 2)')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    
    if saving_enabled:
        save_path = os.path.join(output_directory, f"{title.replace(' ', '_')}.png")
        os.makedirs(output_directory, exist_ok=True)
        plt.savefig(save_path)
        
    plt.show()

def plotArchiveRoutes(archive):
    for i, route in enumerate(archive):
        plotRoute(route, f"Archived Soulution {i + 1}")





# def plotProgress(progress, ylabel, title):
#     plt.plot(progress)
#     plt.ylabel(ylabel)
#     plt.xlabel('Generation')
#     plt.title(title)
#     plt.show()

# def plotParameterImpact(parameter_name, parameter_values, progress_data, ylabel, title, filename_prefix):
#     plt.figure()
#     for i, param_value in enumerate(parameter_values):
#         if len(progress_data[i]) > 0:
#             plt.plot(progress_data[i], label=f'{parameter_name}={param_value}')
#     plt.ylabel(ylabel)
#     plt.xlabel('Generation')
#     plt.title(title)
#     plt.legend()
#     plt.savefig(f"{filename_prefix}_{parameter_name}.png")
#     plt.close()
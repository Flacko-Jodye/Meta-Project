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
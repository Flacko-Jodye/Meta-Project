import matplotlib.pyplot as plt
import os

output_dir = "Visualisation_Parameters"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def plotRoute(cityList, title, filename):
    plt.figure(figsize=(10, 10))
    x, y = [], []
    for item in cityList:
        x.append(item.x)
        y.append(item.y)
        plt.annotate(item.nr, (item.x, item.y))
    x.append(cityList[0].x)
    y.append(cityList[0].y)
    plt.plot(x, y, marker="x")
    plt.ylabel('Y-Koordinate')
    plt.xlabel('X-Koordinate')
    plt.title(title)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def plotPopulationAndObjectiveValues(population, title, filename, Fitness):
    distance, stress = [], []
    for route in population:
        distance.append(Fitness(route).routeDistance())
        stress.append(Fitness(route).routeStress())
    plt.scatter(distance, stress, marker="o", color="black")
    plt.ylabel('Stress')
    plt.xlabel('Distance')
    plt.title(title)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

def plotProgress(data, ylabel, title, filename):
    plt.figure()
    plt.plot(data)
    plt.ylabel(ylabel)
    plt.xlabel('Generation')
    plt.title(title)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()
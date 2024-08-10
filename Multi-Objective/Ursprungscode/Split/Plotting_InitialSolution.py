import numpy as np
import matplotlib.pyplot as plt

def plot_initial_solutions():
    # Definition der x-Werte
    x = np.linspace(0, 10, 100)

    # Vier Beispiel-Initiallösungen (können durch beliebige Funktionen ersetzt werden)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.exp(-x)
    y4 = np.log(x + 1)

    # Plotten der Initiallösungen
    plt.figure(figsize=(10, 6))
    plt.plot(x, y1, label='Initiallösung 1: sin(x)', color='blue')
    plt.plot(x, y2, label='Initiallösung 2: cos(x)', color='red')
    plt.plot(x, y3, label='Initiallösung 3: exp(-x)', color='green')
    plt.plot(x, y4, label='Initiallösung 4: log(x + 1)', color='purple')

    # Beschriftungen und Titel
    plt.title('Plot der vier Initiallösungen')
    plt.xlabel('x-Werte')
    plt.ylabel('y-Werte')
    plt.legend()
    plt.grid(True)

    # Anzeige des Plots
    plt.show()
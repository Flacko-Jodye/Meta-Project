import csv
import os

def getCityBasedOnNr(cityList,nr):
    if (nr <= 0 or nr > len(cityList)):
        print("Something is wrong!")
        return cityList[0]
    else:
        return cityList[nr-1]  
    
def save_best_route_to_csv(route, filename):
    """
    Speichert die beste Route in einer CSV-Datei.
    :param route: Liste von City-Objekten.
    :param filename: Name der CSV-Datei.
    """

    # Erstellen des Pfades zur Speicherung
    file_path = os.path.join('Multi-Objective/Ursprungscode/Split/Visualisations', filename)

    # Schreiben der Stadt-Indizes in eine CSV-Datei
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Schreiben des Headers
        writer.writerow(['CityNr', 'traffic', 'x', 'y'])  # Passen Sie dies an die Attribute der City-Klasse an
        # Schreiben der Daten für jede Stadt
        for city in route:
            writer.writerow([city.nr, city.traffic, city.x, city.y])

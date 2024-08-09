from gurobipy import Model, GRB, quicksum
import numpy as np, random

# Beispiel: Umformulierung des Problems mit Gurobi
def gurobi_tsp(cityList):
    # Anzahl der Städte
    n = len(cityList)

    # Berechnung der Entfernungen zwischen den Städten
    distance_matrix = np.zeros((n, n))
    stress_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i+1, n):
            distance_matrix[i][j] = cityList[i].distance(cityList[j])
            distance_matrix[j][i] = distance_matrix[i][j]
            stress_matrix[i][j] = cityList[i].stress(cityList[j])
            stress_matrix[j][i] = stress_matrix[i][j]

    # Modell initialisieren
    m = Model("tsp")

    # Variablen: x[i, j] ist 1, wenn Stadt j direkt nach Stadt i besucht wird
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = m.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    # Variablen u[i] zur Vermeidung von Subtouren
    u = {}
    for i in range(n):
        u[i] = m.addVar(vtype=GRB.INTEGER, name=f"u_{i}")

    # Zielfunktion: Minimierung der Gesamtentfernung und/oder Stress
    m.setObjective(quicksum(distance_matrix[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j) +
                   quicksum(stress_matrix[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j), GRB.MINIMIZE)

    # Einschränkungen: Jede Stadt muss genau einmal besucht werden
    for i in range(n):
        m.addConstr(quicksum(x[i, j] for j in range(n) if i != j) == 1, name=f"visit_{i}")
        m.addConstr(quicksum(x[j, i] for j in range(n) if i != j) == 1, name=f"leave_{i}")
    
    # Subtour-Eliminierungsbedingungen (MTZ-Formulierung)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                m.addConstr(u[i] - u[j] + n * x[i, j] <= n-1, name=f"subtour_{i}_{j}")

    # Modell optimieren
    m.optimize()

    # Ergebnis abrufen und Route ausgeben
    if m.status == GRB.OPTIMAL:
        solution = []
        for i in range(n):
            for j in range(n):
                if i != j and x[i, j].x > 0.5:
                    solution.append((i, j))
        print("Optimale Route:", solution)
        return solution
    else:
        print("Keine optimale Lösung gefunden.")

# Berechnungsfunktion für die Gesamtdistanz und den Gesamtstress basierend auf der optimierten Route
def calculate_total_distance_and_stress(cityList, route):
    total_distance = 0
    total_stress = 0

    for i in range(len(route)):
        from_city_index = route[i][0]
        to_city_index = route[i][1]

        from_city = cityList[from_city_index]
        to_city = cityList[to_city_index]

        total_distance += from_city.distance(to_city)
        total_stress += from_city.stress(to_city)

    return total_distance, total_stress
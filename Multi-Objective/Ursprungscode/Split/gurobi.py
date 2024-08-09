from gurobipy import Model, GRB, quicksum
import numpy as np, random
from City import City

def extract_route(cityList, x):
    n = len(cityList)
    route = []
    visited = set()

    current_city = 0  # Start from the first city
    while len(visited) < n:
        visited.add(current_city)
        for j in range(n):
            if j != current_city and x[current_city, j].x > 0.5:  # If the city is part of the route
                route.append((current_city, j))
                current_city = j
                break

    return route

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

def gurobi_tsp(cityList):
    n = len(cityList)
    distance_matrix = np.zeros((n, n))
    stress_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i+1, n):
            distance_matrix[i][j] = cityList[i].distance(cityList[j])
            distance_matrix[j][i] = distance_matrix[i][j]
            stress_matrix[i][j] = cityList[i].stress(cityList[j])
            stress_matrix[j][i] = stress_matrix[i][j]
    
    m = Model("tsp")
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = m.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    u = {}
    for i in range(n):
        u[i] = m.addVar(vtype=GRB.INTEGER, name=f"u_{i}")

    m.setObjective(quicksum(distance_matrix[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j) +
                   quicksum(stress_matrix[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j), GRB.MINIMIZE)

    for i in range(n):
        m.addConstr(quicksum(x[i, j] for j in range(n) if i != j) == 1, name=f"visit_{i}")
        m.addConstr(quicksum(x[j, i] for j in range(n) if i != j) == 1, name=f"leave_{i}")

    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                m.addConstr(u[i] - u[j] + n * x[i, j] <= n-1, name=f"subtour_{i}_{j}")

    m.optimize()

    if m.status == GRB.OPTIMAL:
        optimal_route = extract_route(cityList, x)
        total_distance, total_stress = calculate_total_distance_and_stress(cityList, optimal_route)
        print(f"Optimale Route: {optimal_route}")
        print(f"Gesamtdistanz: {total_distance}")
        print(f"Gesamtstress: {total_stress}")
        return optimal_route
    else:
        print("Keine optimale Lösung gefunden.")
        return None

    return total_distance, total_stress

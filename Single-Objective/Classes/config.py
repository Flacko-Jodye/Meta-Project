# config.py
# plotting_enabled = False    # Auf True setzen um die Visualisierungen zu speichern
# csv_enabled = True         # Auf True setzen um die Ergebnisse in einer CSV-Datei zu speichern
# tuning_mode = False        # Auf True setzen um den Tuning-Modus zu aktivieren --> Parameter-Set in Main.py

plotting_enabled = False
csv_enabled = True
tuning_mode = False
save_route_to_csv = True

# Auswahl der Selektionsmethodik: "roulette", "rank", "steady_state" oder "tournament"
selection_method = "roulette"
tournament_size = 5             # Nur für Turnierselektion relevant
replace_size = 2                # Nur für steady_state Selektion relevant

# Einstellen der Parameter für den Single-Experiment-Modus
single_run_params = {
    "popSize": 100,
    "eliteSize": 20,       
    "mutationRate": 0.01,
    "generations": 500,
    "objectiveNrUsed": 2  # 1 = Distanz minimieren, 2 = Stress minimieren
    }

# Einstellen der Parameter für den Tuning-Modus
popSizes = [50, 100, 200]
eliteSizes = [10, 20, 30]
mutationRates = [0.01, 0.05, 0.1]
generations_list = [100, 200, 500]

# config.py
# Einstellen der verschiedenen Modi für das Plotting und den CSV-Export
# plotting_enabled = False    # Auf True setzen um die Visualisierungen zu speichern
# csv_enabled = True         # Auf True setzen um die Ergebnisse in einer CSV-Datei zu speichern
# tuning_mode = False        # Auf True setzen um den Tuning-Modus zu aktivieren --> Parameter-Set in Main.py

plotting_enabled = False
csv_enabled = True

tuning_mode = True

single_run_params = {
    "popSize": 100,
    "eliteSize": 20,
    "mutationRate": 0.01,
    "generations": 500,
    "objectiveNrUsed": 1  # 1 = Distanz minimieren, 2 = Stress minimieren
    }

# popSizes = [50, 100, 200]
# eliteSizes = [10, 20, 30]
# mutationRates = [0.01, 0.05, 0.1]
# generations_list = [100, 200, 500]
popSizes = [50, 100]
eliteSizes = [10, 20]
mutationRates = [0.01, 0.05]
generations_list = [100, 200]


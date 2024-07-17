Aufgabenstellung:
**Phase 1:** Bestehendes Framework nutzen, um eine gute Lösung jeweils einzeln für die beiden Zielstellungen zu finden, dabei
Untersuchung der Auswirkung von Parameteränderungen
- Parameteränderungen von Populationsgröße, Generationsanzahl, Elitismus, Mutationsrate
- Optional:
    -    bereits die Erweiterungen des Lösungsframeworks umsetzen, die in Phase I durchführbar sind
        (im Code „#TODO“; Einbinden von Initiallösungen, Veränderung der Selektions-Methode, Tuning des Codes)

**Phase 2:** Bestehendes Framework erweitern und Auswirkungen auf Lösungsprozess, Konvergenz der Lösungen durch
Parameteränderungen untersuchen; gesucht wird eine passende Menge an Alternativlösungen, d.h. eine gute „Pareto-Front“
- Mehrkriterialität in der Fitnessberechnung berücksichtigen
- Differenzierterer Umgang mit Initiallösungen, z.B. bereits bekannte (gute) Lösungen für Zielsetzung nach
Distanzminimierung sowie für Stressminimierung als Teil der Initiallösungen verwenden
- Darüber hinaus:
  - Dominierende Lösungen hinsichtlich der Einzelzielsetzungen dauerhaft in ein Archiv speichern und als Lösung mit ausgeben
  - Ändern des Mutations-Operators, Auswahl anderer Crossover-Methoden
  - optional:Tuning des Codes (Distanz/Stress-Berechnung nur 1x, Rückgriff auf Liste/Array)
    

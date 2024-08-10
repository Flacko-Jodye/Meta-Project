import random
#TODO: Ggf. noch weitere Crossover-Methoden hinzufügen


# Standard-Methoden für Crossover
def ordered_crossover (parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)
    #In ordered crossover, we randomly select a subset of the first parent string
    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    #and then fill the remainder of the route with the genes from the second parent
    #in the order in which they appear, 
    #without duplicating any genes in the selected subset from the first parent    
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

def ein_punkt_crossover(elter1, elter2):
    ueberkreuzungspunkt = random.randint(1, len(elter1) - 1)
    kind = elter1[:ueberkreuzungspunkt]

    for stadt in elter2:
        if stadt not in kind:
            kind.append(stadt)

    return kind

def edge_recombination_crossover(elter1, elter2):
    def erstelle_kantenkarte(e1, e2):
        karten_map = {i: set() for i in range(1, len(e1) + 1)}
        for elternteil in [e1, e2]:
            for index in range(len(elternteil)):
                links = elternteil[index - 1] if index > 0 else elternteil[-1]
                rechts = elternteil[index + 1] if index < len(elternteil) - 1 else elternteil[0]
                karten_map[elternteil[index].nr].update([links.nr, rechts.nr])
        return karten_map

    karten_map = erstelle_kantenkarte(elter1, elter2)
    aktuelle_stadt = random.choice(elter1)
    nachkomme = [aktuelle_stadt]

    while len(nachkomme) < len(elter1):
        for nachbarn in karten_map.values():
            nachbarn.discard(aktuelle_stadt.nr)

        if karten_map[aktuelle_stadt.nr]:
            naechste_stadt_nr = min(karten_map[aktuelle_stadt.nr], key=lambda x: len(karten_map[x]))
        else:
            uebrige_staedte = [stadt.nr for stadt in elter1 if stadt not in nachkomme]
            naechste_stadt_nr = random.choice(uebrige_staedte)

        naechste_stadt = next(stadt for stadt in elter1 if stadt.nr == naechste_stadt_nr)
        nachkomme.append(naechste_stadt)
        aktuelle_stadt = naechste_stadt

    return nachkomme
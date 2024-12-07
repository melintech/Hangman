import random
from drawing import afiseaza_spanzuratoarea

def incarca_cuvinte(categorie):
    fisier = f"categorii/{categorie}.txt"
    try:
        with open(fisier, "r") as f:
            return [linie.strip().upper() for linie in f if linie.strip()]
    except FileNotFoundError:
        print(f"Eroare: Fisierul pentru categoria '{categorie}' nu exista.")
        return []

def salveaza_scor(nume, categorie, scor):
    with open("scoruri.txt", "a") as f:
        f.write(f"{nume.upper()},{categorie.capitalize()},{scor}\n")

def selecteaza_cuvant(categorie):
    cuvinte = incarca_cuvinte(categorie)
    if not cuvinte:
        return None
    return random.choice(cuvinte)

def afiseaza_scoruri():
    try:
        scoruri = []
        with open("scoruri.txt", "r") as f:
            for linie in f:
                nume, categorie, scor = linie.strip().split(",")
                scoruri.append((nume, categorie, int(scor)))
        scoruri.sort(key=lambda x: x[2])
        print("\n--- Scoruri ---")
        for index, (nume, categorie, scor) in enumerate(scoruri[:10], start=1):
            print(f"{index}. {nume}: {scor} greseli ({categorie})")
    except FileNotFoundError:
        print("\nNu exista scoruri salvate.")

def selecteaza_categorie(categorii):
    print("\n--- Categorii disponibile ---")
    for index, categorie in enumerate(categorii, start=1):
        print(f"{index}. {categorie.capitalize()}")
    while True:
        optiune = input("Selecteaza o categorie: ").strip()
        if optiune.isdigit():
            optiune = int(optiune)
            if 1 <= optiune <= len(categorii):
                return categorii[optiune - 1]
        print("Optiunea aleasa nu este valida. Incearca din nou.")

def joc():
    print("\nBine ai venit la jocul de ghicit cuvinte!")
    categorii = ["alimente", "animale", "sport", "tari"]

    categorie = selecteaza_categorie(categorii)
    cuvant = selecteaza_cuvant(categorie)
    if not cuvant:
        return

    nume_utilizator = input("\nIntrodu numele tau: ").strip()

    cuvant_ghicit = ["_" for _ in cuvant]
    litere_incercate = set()
    greseli = 0
    incercari_maxime = max(6, len(cuvant))

    while "_" in cuvant_ghicit and greseli < incercari_maxime:
        afiseaza_spanzuratoarea(greseli)
        print("\nCuvantul curent:", " ".join(cuvant_ghicit))
        print("Litere incercate:", ", ".join(sorted(litere_incercate)))
        print("Incercari ramase:", incercari_maxime - greseli)

        litera = input("Ghiceste o litera sau cuvantul complet: ").strip().upper()

        if len(litera) == len(cuvant):
            if litera == cuvant:
                cuvant_ghicit = list(cuvant)
                break
            else:
                print(f"Cuvantul {litera} nu este corect!")
                greseli += 1
                continue

        if len(litera) != 1 or not litera.isalpha():
            print("Te rog sa introduci o singura litera valida sau un cuvant de aceeasi lungime.")
            continue

        if litera in litere_incercate:
            print("Ai incercat deja aceasta litera. Alege alta.")
            continue

        litere_incercate.add(litera)

        if litera in cuvant:
            print(f"Corect! Litera {litera} apare in cuvant.")
            for index, char in enumerate(cuvant):
                if char == litera:
                    cuvant_ghicit[index] = litera
        else:
            print(f"Gresit! Litera {litera} nu apare in cuvant.")
            greseli += 1

    print("\n--- Sfarsitul jocului ---")
    if "_" not in cuvant_ghicit:
        print(f"Felicitari, ai ghicit cuvantul: {cuvant}")
    else:
        print(f"Ai pierdut. Cuvantul era: {cuvant}")

    print(f"Numarul total de greseli: {greseli}")
    salveaza_scor(nume_utilizator, categorie, greseli)

def meniu_principal():
    while True:
        print("\n--- Meniu ---")
        print("1. Incepe un joc nou")
        print("2. Afiseaza scorurile")
        print("3. Iesi din aplicatie")

        optiune = input("Alege o optiune (1/2/3): ").strip()
        if optiune == "1":
            joc()
        elif optiune == "2":
            afiseaza_scoruri()
        elif optiune == "3":
            print("La revedere!")
            break
        else:
            print("Optiune invalida. Incearca din nou.")

if __name__ == "__main__":
    print("\n--- Spânzurătoarea ---")
    meniu_principal()
import requests
import os

# Configuration
DEPARTEMENT = "21"
ANNEE = "2023"

URL = f"https://files.data.gouv.fr/geo-dvf/latest/csv/{ANNEE}/departements/{DEPARTEMENT}.csv.gz"
DOSSIER_DESTINATION = "data"
FICHIER_DESTINATION = os.path.join(DOSSIER_DESTINATION, f"dvf_{DEPARTEMENT}_{ANNEE}.csv.gz")


def telecharger_donnees(url, destination):
    print(f"Début du téléchargement depuis {url}...")

    reponse = requests.get(url, stream=True)

    if reponse.status_code == 200: #200 = OK
        with open(destination, 'wb') as fichier:
            for chunk in reponse.iter_content(chunk_size=8192): #ne pas saturer la RAM
                fichier.write(chunk)
        print(f"Succès ! Fichier sauvegardé sous : {destination}")
    else:
        print(f"Erreur lors du téléchargement : Code {reponse.status_code}")


if __name__ == "__main__":
    telecharger_donnees(URL, FICHIER_DESTINATION)
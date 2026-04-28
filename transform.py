import pandas as pd
import os

FICHIER_SOURCE = os.path.join("data", "dvf_21_2023.csv.gz")
FICHIER_PROPRE = os.path.join("data", "dijon_immobilier_propre.csv")


def nettoyer_donnees():
    print("Chargement des données en cours")
    #low_memory=False évite des avertissements sur les types de données
    df = pd.read_csv(FICHIER_SOURCE, low_memory=False)
    print(f"Nombre de lignes au départ (Toute la Côte-d'Or) : {len(df)}")

    df_dijon = df[df['nom_commune'] == 'Dijon'].copy()
    print(f"Nombre de lignes pour Dijon : {len(df_dijon)}")

    df_dijon = df_dijon[df_dijon['nature_mutation'] == 'Vente']

    df_dijon = df_dijon[df_dijon['type_local'].isin(['Appartement', 'Maison'])]

    #Gérer les valeurs manquantes
    df_dijon = df_dijon.dropna(subset=['valeur_fonciere', 'surface_reelle_bati', 'longitude', 'latitude'])

    df_dijon['prix_m2'] = df_dijon['valeur_fonciere'] / df_dijon['surface_reelle_bati']

    df_dijon = df_dijon[(df_dijon['prix_m2'] >= 500) & (df_dijon['prix_m2'] <= 10000)]

    df_dijon['prix_m2'] = df_dijon['prix_m2'].round(2)

    # Sélectionner uniquement les colonnes utiles pour PowerBI
    colonnes_utiles = [
        'date_mutation', 'valeur_fonciere', 'adresse_nom_voie',
        'code_postal', 'nom_commune', 'type_local',
        'surface_reelle_bati', 'nombre_pieces_principales',
        'prix_m2', 'longitude', 'latitude'
    ]
    df_final = df_dijon[colonnes_utiles]

    df_final.to_csv(FICHIER_PROPRE, index=False)
    print(f"Fichier propre pour PowerBI sauvegardé sous : {FICHIER_PROPRE}")
    print(f"Nombre de transactions finales conservées : {len(df_final)}")


if __name__ == "__main__":
    nettoyer_donnees()
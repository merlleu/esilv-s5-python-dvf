import numpy as np
import pandas as pd
import json
import requests
#import io
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas
from datetime import datetime
import plotly.graph_objects as go
from bs4 import BeautifulSoup

df = pd.read_csv('https://cdn.merll.eu/ext-esilv/202401_PYPRJ/dvf_merged_clean_PROD2.csv')
df["Code departement"]=df["Code departement"].astype(str)
df['Date mutation'] = pd.to_datetime(df['Date mutation'], format='%d/%m/%Y', errors='coerce')
df = df.dropna(subset=['Date mutation'])
df["Code postal"]=df["Code postal"].astype(int)

# on passe les départements  à leur code:
url = "https://fr.wikipedia.org/wiki/Liste_des_d%C3%A9partements_fran%C3%A7ais"
soup = BeautifulSoup(requests.get(url).content, "html.parser")

table = soup.find("table", {"class": "wikitable sortable centre"})
rows = table.find_all("tr")[3:]

departements_nom_to_code = {}
departements_code_to_nom = {}
departements_code_to_region = {}

for row in rows:
    c = row.find_all("td")
    if len(c) == 0:
        continue
    code_dpt, nom, * _ = c
    code_dpt = code_dpt.text.strip()

    if not code_dpt.isdigit():
        # on ne prend pas les DOM-TOM + Corse
        continue

    code_dpt = code_dpt.zfill(2)

    caractères_speciaux = {
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'à': 'a',
        'ç': 'c',
        'ô': 'o',
        'î': 'i',
        'û': 'u',
        'ù': 'u',
        'à': 'a',
    }

    nom = nom.find('a').text.strip()

    # on ne garde que le nom sous la forme MAJUSCULE-AVEC-TIRETS
    nom_upper = "".join([caractères_speciaux.get(c, c) for c in nom]).upper().replace(' ', '-')

    nom_region = c[9].find('a').text.strip()

    departements_nom_to_code[nom_upper] = code_dpt
    departements_code_to_nom[code_dpt] = nom
    departements_code_to_region[code_dpt] = nom_region

df["Nom Département"] = df["Code departement"].map(departements_code_to_nom)
df["Region"] = df["Code departement"].map(departements_code_to_region)

def get_df_by_year(year):
    if year == 0:
        return df
    year += 2017

    return df[df['Date mutation'].dt.year == year]



# geojson
geojson_departements = geopandas.read_file("https://cdn.merll.eu/ext-esilv/202401_PYPRJ/departements.geojson")
geojson_departements["code"]=geojson_departements["code"].str.zfill(2)


# gares 
df_gares = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/d22ba593-90a4-4725-977c-095d1f654d28', sep=";")
df_gares['num_dpt'] = df_gares['departemen'].map(departements_nom_to_code) # departements_nom_to_code provient de wikipedia au début du notebook
df_gares['Code departement'] = df_gares['num_dpt'].astype(str).str.zfill(2)

df_gares_par_dpt = df_gares.groupby('Code departement').count().reset_index()
df_gares_par_dpt["Nombre de gares"]= df_gares_par_dpt['code_uic']
df_gares_par_dpt = df_gares_par_dpt[["Nombre de gares", "Code departement"]]
# from get_match_details import *
import pandas as pd
from implicit.als import AlternatingLeastSquares
from scipy.sparse import csr_matrix
from sklearn.preprocessing import OneHotEncoder
import os
from threadpoolctl import threadpool_limits
os.environ["OPENBLAS_NUM_THREADS"] = "1"
threadpool_limits(1, "blas")

# API CALLS
# dict_source = get_match_details()
# dict_source_df = pd.DataFrame.from_dict(dict_source)
#
# dict_source_df.to_csv("output.csv", sep=",", header=False, index=False, mode="a")

# DATA PROCESSING + TRANSFORMATION

df = pd.read_csv("output.csv")

# Preprocesare date
df["items"] = df["items"].apply(lambda x: x.split(", "))
df["items"] = df["items"].apply(lambda x: [item for item in x if item != "Unknown Item"])  # Excludem Unknown Item
df["KDA"] = (df["kills"] + df["assists"]) / df["deaths"].replace(0, 1)  # Calculăm KDA

# Convertim `tags` și `lane` în reprezentări numerice
encoder = OneHotEncoder()
tags_encoded = encoder.fit_transform(df[["tags", "lane"]]).toarray()

# Construim mapări pentru campioni și iteme
champions = df["champion_name"].unique()
items = list(set(item for sublist in df["items"] for item in sublist))
champion_to_id = {champ: i for i, champ in enumerate(champions)}
item_to_id = {item: i for i, item in enumerate(items)}

# Construim matricea utilizator-item ponderată
rows, cols, data = [], [], []
for idx, row in df.iterrows():
    champion_id = champion_to_id[row["champion_name"]]
    for item in row["items"]:
        item_id = item_to_id[item]
        weight = row["KDA"]  # Ponderăm interacțiunile cu KDA
        if row["has_won"]:
            weight *= 1.5  # Creștem greutatea pentru victorii
        rows.append(champion_id)
        cols.append(item_id)
        data.append(weight)

interaction_matrix = csr_matrix((data, (rows, cols)), shape=(len(champions), len(items)))

# Model ALS
model = AlternatingLeastSquares(factors=15, regularization=0.1, iterations=20)
model.fit(interaction_matrix)


# Funcție pentru recomandare
def recommend_items_with_tags(champion_name, tags_input, n_recommendations, model, interaction_matrix, df):
    # Verificăm dacă campionul există
    if champion_name not in champion_to_id:
        # Filtrăm campionii pe baza tags-urilor date
        filtered_champions = df[df["tags"].str.contains('|'.join(tags_input.split(", ")), na=False)]
        if filtered_champions.empty:
            return f"Nu am găsit campioni cu tags-urile '{tags_input}'."

        # Adunăm toate itemele din campionii filtrați
        all_items = pd.Series(
            [item for sublist in filtered_champions["items"] for item in sublist]
        )
        # Calculăm frecvența itemelor și returnăm primele 6
        recommended_items = all_items.value_counts().index.tolist()[:n_recommendations]
        return recommended_items

    # Dacă campionul există, folosim ALS
    champion_id = champion_to_id[champion_name]
    try:
        recommended = model.recommend(champion_id, interaction_matrix[champion_id], N=n_recommendations)
        if not recommended:  # Dacă lista este goală
            return f"Nu există suficiente date pentru a genera recomandări pentru '{champion_name}'."
    except Exception as e:
        return f"Eroare în generarea recomandărilor: {str(e)}"

    # Mapăm ID-urile itemelor la numele lor
    recommended_items = []
    for rec in recommended:
        if len(rec) == 2:  # Verificăm structura perechii
            item_id, _ = rec
            recommended_items.append(list(item_to_id.keys())[list(item_to_id.values()).index(item_id)])
    return recommended_items

# Exemplu de utilizare
champion = "Lux "  # Poți schimba campionul pentru teste
tags_input = "Mage, Support"
recommended = recommend_items_with_tags(champion, tags_input, 6, model, interaction_matrix, df)
print(f"Recomandări pentru {champion} cu tags-urile '{tags_input}': {recommended}")
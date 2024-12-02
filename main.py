# from get_match_details import *
import pandas as pd
from implicit.als import AlternatingLeastSquares
from scipy.sparse import csr_matrix
import os
from threadpoolctl import threadpool_limits

os.environ["OPENBLAS_NUM_THREADS"] = "1"
threadpool_limits(1, "blas")

# # API CALLS
# dict_source = get_match_details()
# dict_source_df = pd.DataFrame.from_dict(dict_source)
#
# dict_source_df.to_csv("output.csv", sep=",", header=False, index=False, mode="a")


df = pd.read_csv("output.csv")

def preprocess_and_train_model(df):
    if isinstance(df["items"].iloc[0], str):
        df["items"] = df["items"].apply(lambda x: x.split(", "))

    df["items"] = df["items"].apply(lambda x: [item for item in x if item != "Unknown Item"])
    df["KDA"] = (df["kills"] + df["assists"]) / df["deaths"].replace(0, 1)

    champions = df["champion_name"].unique()
    items = list(set(item for sublist in df["items"] for item in sublist))
    champion_to_id = {champ: i for i, champ in enumerate(champions)}
    item_to_id = {item: i for i, item in enumerate(items)}

    rows, cols, data = [], [], []
    for idx, row in df.iterrows():
        if isinstance(row["items"], list):
            champion_id = champion_to_id[row["champion_name"]]
            for item in row["items"]:
                if item in item_to_id:
                    item_id = item_to_id[item]
                    rows.append(champion_id)
                    cols.append(item_id)
                    weight = (row["kills"] + row["assists"]) / max(1, row["deaths"])
                    if row["has_won"]:
                        weight *= 1.5
                    data.append(weight)

    interaction_matrix = csr_matrix((data, (rows, cols)), shape=(len(champion_to_id), len(item_to_id)))

    model = AlternatingLeastSquares(factors=15, regularization=0.1, iterations=50)
    model.fit(interaction_matrix)

    return model, interaction_matrix, champion_to_id, item_to_id


def debug_recommend_items_for_champion(champion_name, tags_input, n_recommendations, model, interaction_matrix, df,
                                       champion_to_id, item_to_id):
    excluded_items = {"Unknown Item", "Control Ward", "Stealth Ward", "Farsight Alteration", "Zombie Ward"}
    boots_items = {
        "Berserker's Greaves", "Boots of Swiftness", "Ionian Boots of Lucidity",
        "Mercury's Treads", "Plated Steelcaps", "Sorcerer's Shoes", "Symbiotic Soles",
        "Boots", "Slightly Magical Boots"
    }

    if champion_name not in champion_to_id:
        return f"Campionul {champion_name} nu există în dataset."

    champion_id = champion_to_id[champion_name]
    print(f"Champion ID for {champion_name}: {champion_id}")
    champion_interactions = interaction_matrix[champion_id].toarray()

    try:
        recommended = model.recommend(champion_id, interaction_matrix[champion_id], N=n_recommendations * 2)

        if isinstance(recommended, tuple) and len(recommended) == 2:
            recommended = list(zip(recommended[0], recommended[1]))

        recommended_items = [
            list(item_to_id.keys())[list(item_to_id.values()).index(item_id)]
            for item_id, _ in recommended
            if list(item_to_id.keys())[list(item_to_id.values()).index(item_id)] not in excluded_items
        ]
    except Exception as e:
        return f"Eroare în generarea recomandărilor pentru {champion_name}: {str(e)}"

    print(f"Raw ALS recommendations for {champion_name}: {recommended_items}")

    filtered_champions = df[df["tags"].str.contains('|'.join(tags_input.split(", ")), na=False)]
    relevant_items = set(
        item for sublist in filtered_champions["items"] for item in sublist if item not in excluded_items
    )
    print(f"Relevant items for tags {tags_input}: {relevant_items}")
    filtered_items = [item for item in recommended_items if item in relevant_items]

    if not filtered_items:
        print("No overlap with relevant items. Returning raw ALS recommendations.")
        filtered_items = [item for item in recommended_items if item not in excluded_items]

    final_items = []
    boots_included = False
    for item in filtered_items:
        if item in boots_items:
            if not boots_included:
                final_items.append(item)
                boots_included = True
        else:
            final_items.append(item)
        if len(final_items) >= n_recommendations:
            break

    return final_items


model, interaction_matrix, champion_to_id, item_to_id = preprocess_and_train_model(df)
champ_to_recommand = "Nami"
tags = "Support, Mage"

recommended_debug = debug_recommend_items_for_champion(
    champion_name=champ_to_recommand,
    tags_input=tags,
    n_recommendations=6,
    model=model,
    interaction_matrix=interaction_matrix,
    df=df,
    champion_to_id=champion_to_id,
    item_to_id=item_to_id
)
print(f"Recommended items for {champ_to_recommand}:", recommended_debug)

# from get_match_details import *
import pandas as pd
from implicit.als import AlternatingLeastSquares
from scipy.sparse import csr_matrix
import os
from threadpoolctl import threadpool_limits
import numpy as np

np.random.seed(42)  # Seed for reproducibility
os.environ["OPENBLAS_NUM_THREADS"] = "1"
threadpool_limits(1, "blas")

# # API CALLS
# dict_source = get_match_details()
# dict_source_df = pd.DataFrame.from_dict(dict_source)
#
# dict_source_df.to_csv("output.csv", sep=",", header=False, index=False, mode="a")


df = pd.read_csv("output.csv")

def preprocess_and_train_model(df):
    df["items"] = df["items"].str.split(", ").apply(lambda x: [item for item in x if item != "Unknown Item"])
    df["KDA"] = (df["kills"] + df["assists"]) / np.maximum(df["deaths"].values, 1)

    champions = sorted(df["champion_name"].unique())  # Sort for consistent mapping
    items = sorted(set(item for sublist in df["items"] for item in sublist))
    champion_to_id = {champ: i for i, champ in enumerate(champions)}
    item_to_id = {item: i for i, item in enumerate(items)}

    rows = df["champion_name"].map(champion_to_id).repeat(df["items"].str.len())
    cols = df["items"].explode().map(item_to_id).dropna()
    data = (df["kills"] + df["assists"]) / np.maximum(df["deaths"], 1)
    data = data.repeat(df["items"].str.len())
    data[df["has_won"].repeat(df["items"].str.len())] *= 1.5

    interaction_matrix = csr_matrix((data, (rows, cols)), shape=(len(champion_to_id), len(item_to_id)))

    model = AlternatingLeastSquares(factors=15, regularization=0.1, iterations=50, use_native=True)
    model.fit(interaction_matrix)

    return model, interaction_matrix, champion_to_id, item_to_id


def debug_recommend_items_for_champion(champion_name, n_recommendations, model, interaction_matrix, champion_to_id, item_to_id):
    # Lista de iteme excluse
    excluded_items = {
        "Unknown Item", "Control Ward", "Stealth Ward", "Farsight Alteration", "Zombie Ward", "Watchful Wardstone"
    }
    incomplete_items = {
        "Amplifying Tome", "B. F. Sword", "Blasting Wand", "Cloak of Agility", "Cloth Armor",
        "Dagger", "Faerie Charm", "Glowing Mote", "Long Sword", "Needlessly Large Rod",
        "Null-Magic Mantle", "Pickaxe", "Rejuvenation Bead", "Ruby Crystal", "Sapphire Crystal",
        "Aether Wisp", "Bami's Cinder", "Bandleglass Mirror", "Blighting Jewel", "Bramble Vest",
        "Catalyst of Aeons", "Caulfield's Warhammer", "Chain Vest", "Crystalline Bracer",
        "Executioner's Calling", "Fated Ashes", "Fiendish Codex", "Forbidden Idol", "Giant's Belt",
        "Glacial Buckler", "Haunting Guise", "Hearthbound Axe", "Hexdrinker", "Hextech Alternator",
        "Kindlegem", "Last Whisper", "Lost Chapter", "Negatron Cloak", "Noonquiver",
        "Oblivion Orb", "Phage", "Quicksilver Sash", "Rectrix", "Recurve Bow", "Runic Compass",
        "Scout's Slingshot", "Seeker's Armguard", "Serrated Dirk", "Shattered Armguard", "Sheen",
        "Spectre's Cowl", "Steel Sigil", "The Brutalizer", "Tiamat", "Tunneler", "Vampiric Scepter",
        "Verdant Barrier", "Warden's Mail", "Watchful Wardstone", "Winged Moonplate", "Zeal", "Doran's Blade", "Boots", "Doran's Shield"
    }
    excluded_items.update(incomplete_items)

    # Lista boots eligibili
    boots_items = sorted({
        "Berserker's Greaves", "Boots of Swiftness", "Ionian Boots of Lucidity",
        "Mercury's Treads", "Plated Steelcaps", "Sorcerer's Shoes", "Symbiotic Soles"
    })

    if champion_name not in champion_to_id:
        return f"Campionul {champion_name} nu există în dataset."

    champion_id = champion_to_id[champion_name]

    # Extrage interacțiunile doar pentru campionul specific
    user_interactions = interaction_matrix[champion_id]

    # Obține recomandările folosind modelul
    recommended = model.recommend(champion_id, user_interactions, N=n_recommendations * 2)
    recommended_with_scores = [
        (list(item_to_id.keys())[item_id], score)
        for item_id, score in zip(recommended[0], recommended[1])
        if list(item_to_id.keys())[item_id] not in excluded_items and list(item_to_id.keys())[item_id] not in boots_items
    ]

    # Sortează după scor descrescător și lexicografic
    recommended_with_scores.sort(key=lambda x: (-x[1], x[0]))
    recommended_items = [item for item, _ in recommended_with_scores]

    # Calculează scorurile pentru boots
    boots_indices = [item_to_id[boot] for boot in boots_items if boot in item_to_id]
    boots_scores = model.item_factors[boots_indices].dot(model.user_factors[champion_id])

    # Selectează boots-ul cel mai potrivit și sortat lexicografic în caz de egalitate
    boots_with_scores = list(zip(boots_items, boots_scores))
    boots_with_scores.sort(key=lambda x: (-x[1], x[0]))  # Sortare după scor și lexicografic
    selected_boots = boots_with_scores[0][0]

    # Completează lista finală de recomandări
    final_items = [selected_boots]
    final_items += recommended_items[:n_recommendations - 1]

    # Fixăm lista finală în ordinea deterministă
    final_items = sorted(final_items)

    return sorted(final_items)
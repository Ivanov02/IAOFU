import pandas as pd
import numpy as np
from implicit.als import AlternatingLeastSquares
from scipy.sparse import csr_matrix
from typing import List, Tuple, Dict
from threadpoolctl import threadpool_limits
import os
from pathlib import Path
from django.conf import settings


class ItemRecommenderService:
    def __init__(self):
        # Set up environment variables for performance
        os.environ["OPENBLAS_NUM_THREADS"] = "1"
        threadpool_limits(1, "blas")
        np.random.seed(42)

        # Initialize model parameters
        self.model = None
        self.interaction_matrix = None
        self.champion_to_id = None
        self.item_to_id = None

    def initialize_from_csv(self, csv_path: str) -> None:
        """Initialize the recommender with data from a CSV file."""
        df = pd.read_csv(csv_path)
        self.preprocess_and_train_model(df)

    def preprocess_and_train_model(self, df: pd.DataFrame) -> None:
        """Preprocess data and train the recommendation model."""
        # Convert items string to list and clean unknown items
        df["items"] = df["items"].str.split(", ").apply(
            lambda x: [item for item in x if item != "Unknown Item"]
        )

        # Calculate KDA
        df["KDA"] = (df["kills"] + df["assists"]) / np.maximum(df["deaths"], 1)

        # Create mappings
        champions = sorted(df["champion_name"].unique())
        items = sorted(set(item for sublist in df["items"] for item in sublist))
        self.champion_to_id = {champ: i for i, champ in enumerate(champions)}
        self.item_to_id = {item: i for i, item in enumerate(items)}

        # Create interaction matrix
        rows = df["champion_name"].map(self.champion_to_id).repeat(df["items"].str.len())
        cols = df["items"].explode().map(self.item_to_id).dropna()
        data = (df["kills"] + df["assists"]) / np.maximum(df["deaths"], 1)
        data = data.repeat(df["items"].str.len())
        data[df["has_won"].repeat(df["items"].str.len())] *= 1.5

        self.interaction_matrix = csr_matrix(
            (data, (rows, cols)),
            shape=(len(self.champion_to_id), len(self.item_to_id))
        )

        # Train model
        self.model = AlternatingLeastSquares(
            factors=15,
            regularization=0.1,
            iterations=50,
            use_native=True
        )
        self.model.fit(self.interaction_matrix)

    def recommend_items_for_champion(
            self,
            champion_name: str,
            n_recommendations: int = 6
    ) -> List[str]:
        """Recommend items for a specific champion."""
        # Items to exclude
        excluded_items = {
            "Unknown Item", "Control Ward", "Stealth Ward", "Farsight Alteration", "Zombie Ward", "Watchful Wardstone",
        }

        # Incomplete items to exclude
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
            "Verdant Barrier", "Warden's Mail", "Watchful Wardstone", "Winged Moonplate", "Zeal", "Doran's Blade",
            "Boots", "Doran's Shield", "Tear of Goddess"
        }
        excluded_items.update(incomplete_items)

        # Eligible boots
        boots_items = {
            "Berserker's Greaves", "Boots of Swiftness", "Ionian Boots of Lucidity",
            "Mercury's Treads", "Plated Steelcaps", "Sorcerer's Shoes", "Symbiotic Soles",
        }

        if champion_name not in self.champion_to_id:
            return []

        champion_id = self.champion_to_id[champion_name]
        user_interactions = self.interaction_matrix[champion_id]

        # Get recommendations
        recommended = self.model.recommend(
            champion_id,
            user_interactions,
            N=n_recommendations * 2
        )

        # Process recommendations
        recommended_items = []
        for item_id, score in zip(recommended[0], recommended[1]):
            item_name = list(self.item_to_id.keys())[item_id]
            if item_name not in excluded_items and item_name not in boots_items:
                recommended_items.append((item_name, score))

        # Sort by score and name
        recommended_items.sort(key=lambda x: (-x[1], x[0]))

        # Get best boots
        boots_indices = [
            self.item_to_id[boot] for boot in boots_items
            if boot in self.item_to_id
        ]
        if boots_indices:
            boots_scores = self.model.item_factors[boots_indices].dot(
                self.model.user_factors[champion_id]
            )
            boots_with_scores = list(zip(boots_items, boots_scores))
            boots_with_scores.sort(key=lambda x: (-x[1], x[0]))
            selected_boots = boots_with_scores[0][0]
        else:
            selected_boots = None

        # Compile final recommendations
        final_items = []
        if selected_boots:
            final_items.append(selected_boots)

        final_items.extend([item for item, _ in recommended_items[:n_recommendations - 1]])
        return sorted(final_items)

    def save_matches_to_csv(self, username: str, tagline: str, start: int = 0, count: int = 1) -> None:
        """Save match data to CSV files."""

        # Get paths
        last_run_path = Path(settings.BASE_DIR) / 'last_run.csv'
        output_path = Path(settings.BASE_DIR) / 'output.csv'

        # Get match data
        matches_data = self.get_matches_data(username, tagline, start, count)

        # Update last_run.csv
        unique_combination = f"{username}{tagline}"
        new_row = pd.DataFrame([{
            'summoner_name': username,
            'summoner_tag_name': tagline,
            'match_to_pull_from': start,
            'number_of_matches_to_pull': count,
            'last_pulled': start + count,
            'unique_combination': unique_combination
        }])

        if last_run_path.exists():
            last_run_df = pd.read_csv(last_run_path)
            last_run_df = pd.concat([last_run_df, new_row], ignore_index=True)
        else:
            last_run_df = new_row

        last_run_df.to_csv(last_run_path, index=False)

        # Update output.csv
        matches_df = pd.DataFrame(matches_data)
        if output_path.exists():
            matches_df.to_csv(output_path, mode='a', header=False, index=False)
        else:
            matches_df.to_csv(output_path, index=False)
from typing import List, Optional
from models import SkinLogEntry, IngredientFact

from datetime import date

class FakeUserHistoryStore:
    def __init__(self):
        self._entries: dict[str, List[SkinLogEntry]] = {
            "user_1": [
                SkinLogEntry(
                    date=date(2026, 8, 1),
                    symptoms=["mild dryness"],
                    severity=2,
                    products_used=["CeraVe Moisturizing Cream", "Neutrogena Sunscreen SPF 50"],
                    notes="Skin feeling pretty normal",
                ),
                SkinLogEntry(
                    date=date(2026, 8, 8),
                    symptoms=["redness", "dryness"],
                    severity=3,
                    products_used=["CeraVe Moisturizing Cream", "The Ordinary Retinol 0.5%"],
                    notes="Started retinol this week",
                ),
                SkinLogEntry(
                    date=date(2026, 8, 15),
                    symptoms=["redness", "flaking", "irritation"],
                    severity=4,
                    products_used=["CeraVe Moisturizing Cream", "The Ordinary Retinol 0.5%"],
                    notes="Getting worse, considering stopping retinol",
                ),
                SkinLogEntry(
                    date=date(2026, 8, 22),
                    symptoms=["mild redness"],
                    severity=2,
                    products_used=["CeraVe Moisturizing Cream"],
                    notes="Stopped retinol, calming down",
                ),
            ],
            "user_2": [
                SkinLogEntry(
                    date=date(2026, 8, 5),
                    symptoms=["breakout", "oiliness"],
                    severity=3,
                    products_used=["Cetaphil Gentle Cleanser"],
                    notes="Small breakout near chin",
                ),
                SkinLogEntry(
                    date=date(2026, 8, 12),
                    symptoms=["breakout"],
                    severity=2,
                    products_used=["Cetaphil Gentle Cleanser", "The Ordinary Niacinamide 10%"],
                    notes="Added niacinamide, seems to be helping a bit",
                ),
            ],
        }
    
    def get_history(self, user_id: str) -> List[SkinLogEntry]:
        if user_id not in self._entries:
            raise ValueError(f"No history found for user: {user_id} ")
        return self._entries[user_id]

class FakeIngredientKnowledgeBase:
    def __init__(self):
        self._facts: List[IngredientFact] = [
            IngredientFact(
                ingredient_name="Retinol",
                category="active",
                effects=[
                    "increases skin cell turnover",
                    "can cause dryness, redness, and flaking during initial adjustment period",
                    "reduces appearance of fine lines over time",
                ],
                warnings="Increases sun sensitivity — daily SPF strongly recommended. Start with low frequency (2-3x/week) to build tolerance.",
            ),
            IngredientFact(
                ingredient_name="Niacinamide",
                category="active",
                effects=[
                    "reduces redness and inflammation",
                    "helps regulate oil production",
                    "generally well-tolerated, safe to combine with most other actives",
                ],
                warnings=None,
            ),
            IngredientFact(
                ingredient_name="Hyaluronic Acid",
                category="moisturizer",
                effects=[
                    "draws moisture into the skin",
                    "helps with dryness and dehydration",
                ],
                warnings="Best applied to damp skin — can pull moisture from deeper layers if used on very dry skin without a moisturizer sealing it in.",
            ),
            IngredientFact(
                ingredient_name="Salicylic Acid",
                category="exfoliant",
                effects=[
                    "exfoliates inside pores, helpful for blackheads and breakouts",
                    "can cause dryness or peeling if overused",
                ],
                warnings="Avoid combining with retinol initially — increases irritation risk.",
            ),
            IngredientFact(
                ingredient_name="Zinc Oxide",
                category="sunscreen",
                effects=[
                    "provides broad-spectrum UV protection",
                    "generally gentle, suitable for sensitive skin",
                ],
                warnings=None,
            ),
        ]
    
    def search(self, query: str) -> List[IngredientFact]:
        matches = []
        for fact in self._facts:
            if query.lower() in fact.ingredient_name.lower():
                matches.append(fact)
        return matches

if __name__ == "__main__":
    kb = FakeIngredientKnowledgeBase()
    results = kb.search("retin")
    print(results)
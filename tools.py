import json
from rag import search_ingredient_semantics
from fake_data import FakeUserHistoryStore, FakeIngredientKnowledgeBase

store = FakeUserHistoryStore()
kb = FakeIngredientKnowledgeBase()

def get_user_history(user_id: str) -> str:
    entries = store.get_history(user_id)
    entries_as_dicts = [entry.model_dump() for entry in entries]
    return json.dumps(entries_as_dicts, default=str)

get_user_history_schema = {
    "name": "get_user_history",
    "description": "Retrieves the logged skin condition history for a given user, including symptoms, severity, products used, and notes over time.",
    "input_schema": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The unique identifier of the user whose history should be retrieved."
            }
        },
        "required": ["user_id"]
    }
}


# --- search_ingredients ---

def search_ingredients(query: str) -> str:
    ingredients = search_ingredient_semantics(query)
    ingreidents_as_dict = []
    for ingredient_name, category, effects, warnings in ingredients:
        ingreidents_as_dict.append({
            "ingredient_name": ingredient_name,
            "category": category,
            "effects": effects,
            "warnings": warnings
        })
    return json.dumps(ingreidents_as_dict, default=str)

search_ingredients_schema = {
    "name": "search_ingredients",
    "description": "Searches a knowledge base of skincare ingredient facts by name, returning matching ingredients along with their known effects and warnings.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The ingredient name or partial name to search for, e.g. 'retinol' or 'niacinamide'."
            }
        },
        "required": ["query"]
    }
}

TOOLS = [get_user_history_schema, search_ingredients_schema]

TOOL_FUNCTIONS = {
    "get_user_history": get_user_history,
    "search_ingredients": search_ingredients,
}
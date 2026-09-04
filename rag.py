from models import IngredientFact
from dotenv import load_dotenv
import os, voyageai 
import psycopg2


load_dotenv()

from fake_data import FakeUserHistoryStore, FakeIngredientKnowledgeBase

store = FakeUserHistoryStore()
kb = FakeIngredientKnowledgeBase()

vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))


def build_embedding_text(fact: IngredientFact) -> str:
    effects_text = ", ".join(fact.effects)
    text = f"{fact.ingredient_name} ({fact.category}). Effects: {effects_text}"
    if fact.warnings:
        text += f"Warnings: {fact.warnings}"
    return text

def embed_all_facts(facts: list[IngredientFact]):
    texts = [build_embedding_text(fact) for fact in facts]
    result = vo.embed(
        texts=texts,
        model="voyage-3.5-lite",
        input_type="document",
        output_dimension=512
    )
    return result.embeddings

def insert_facts(facts, embeddings):
    conn = psycopg2.connect(
        host="localhost",
        port=5433,
        dbname="skincare",
        user="postgres",
        password="devpassword"
    )
    cur = conn.cursor()
    
    for fact, embedding in zip(facts, embeddings):
        cur.execute(
            "INSERT INTO ingredient_facts (ingredient_name, category, effects, warnings, embedding) VALUES (%s, %s, %s, %s, %s)",
            (fact.ingredient_name, fact.category, fact.effects, fact.warnings, embedding)
        )
    
    conn.commit()
    cur.close()
    conn.close()

def search_ingredient_semantics(query: str, top_k: int = 3):
    query_embeddings = vo.embed(
        texts=[query],
        model="voyage-3.5-lite",
        input_type="query",
        output_dimension=512
    )
    conn = psycopg2.connect(
            host="localhost",
            port=5433,
            dbname="skincare",
            user="postgres",
            password="devpassword"
        )
    cur = conn.cursor()
    cur.execute(
        "SELECT ingredient_name, category, effects, warnings FROM ingredient_facts ORDER BY embedding <=> %s::vector LIMIT %s",
        (query_embeddings.embeddings[0], top_k)
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
    

if __name__ == "__main__":
    facts = kb.get_all_facts()
    embeddings = embed_all_facts(facts)
    insert_facts(facts, embeddings)
    print(search_ingredient_semantics("i have a lot of dryness today", 3))
import os
from dotenv import load_dotenv
import voyageai

load_dotenv()

vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

result = vo.embed(
    texts=["Retinol increases skin cell turnover and can cause dryness."],
    model="voyage-3.5-lite",
    input_type="document"
)

embedding = result.embeddings[0]
print(len(embedding))  # should print 512
print(embedding[:5])   # first few numbers, just to see what a vector looks like
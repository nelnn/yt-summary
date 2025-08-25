import os
import textwrap

from llama_index.core import Document, SimpleDirectoryReader, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.postgres import PGVectorStore
from youtube_transcript_api import YouTubeTranscriptApi

from src.config import settings

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
embed_model = OpenAIEmbedding(api_key=settings.OPENAI_API_KEY)

video_id = "1lm4Wlpy2wU"  # Example YouTube video ID
ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch(video_id)

with open(f"data/{video_id}.txt", "w") as f:
    for i in transcript.snippets:
        f.write(i.text + "\n")

# texts = " ".join([t.text for t in transcript.snippets])
# documents = [Document(text=texts)]


documents = SimpleDirectoryReader("data").load_data()

db_name = "yt"
vector_store = PGVectorStore.from_params(
    database=db_name,
    table_name="llama_embeddings",
    host=settings.POSTGRES_HOST,
    password=settings.POSTGRES_PASSWORD,
    port=str(settings.POSTGRES_PORT),
    user=settings.POSTGRES_USER,
    embed_dim=1536,  # openai embedding dimension
    hnsw_kwargs={
        "hnsw_m": 16,
        "hnsw_ef_construction": 64,
        "hnsw_ef_search": 40,
        "hnsw_dist_method": "vector_cosine_ops",
    },
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True, embed_model=embed_model
)
query_engine = index.as_query_engine()
response = query_engine.query("how to get a transcript of any YouTube video?")

print(response)

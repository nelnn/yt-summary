import os

from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, Document
from llama_index.core.vector_stores import FilterOperator, MetadataFilter, MetadataFilters
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.postgres import PGVectorStore
from youtube_transcript_api import YouTubeTranscriptApi

from src.config import settings


# Initial embedding (run this only once)
def embed_documents_once():
    # os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    embed_model = OpenAIEmbedding(api_key=settings.OPENAI_API_KEY)
    # embed_model = GoogleGenAIEmbedding(api_key=settings.GOOGLE_API_KEY)
    video_id = "viWXQzD-r_c"
    video_id = "xwx0mf8aGC4"
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)

    with open(f"data/{video_id}.txt", "w") as f:
        for i in transcript.snippets:
            f.write(i.text + "\n")

    documents = SimpleDirectoryReader("data").load_data()
    db_name = "yt"
    vector_store = PGVectorStore.from_params(
        database=db_name,
        # table_name="llama_embeddings_gemini",
        table_name="llama_embeddings",
        host=settings.POSTGRES_HOST,
        password=settings.POSTGRES_PASSWORD,
        port=str(settings.POSTGRES_PORT),
        user=settings.POSTGRES_USER,
        embed_dim=1536,
        # embed_dim=768,
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
    return index


# Retrieve from existing vector store (run this for subsequent queries)
def load_existing_index():
    # os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    # os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
    embed_model = GoogleGenAIEmbedding(api_key=settings.GOOGLE_API_KEY)
    # embed_model = OpenAIEmbedding(api_key=settings.OPENAI_API_KEY)

    db_name = "yt"
    vector_store = PGVectorStore.from_params(
        database=db_name,
        table_name="llama_embeddings_gemini",
        # table_name="llama_embeddings",
        host=settings.POSTGRES_HOST,
        password=settings.POSTGRES_PASSWORD,
        port=str(settings.POSTGRES_PORT),
        user=settings.POSTGRES_USER,
        # embed_dim=1536,
        embed_dim=768,
        hnsw_kwargs={
            "hnsw_m": 16,
            "hnsw_ef_construction": 64,
            "hnsw_ef_search": 40,
            "hnsw_dist_method": "vector_cosine_ops",
        },
    )

    # Load existing index from vector store
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)
    return index


# Usage example
# First time: embed the documents
# index = embed_documents_once()

# Subsequent times: just load the existing index
index = load_existing_index()
llms = GoogleGenAI(api_key=settings.GOOGLE_API_KEY)
# llms = OpenAI(api_key=settings.OPENAI_API_KEY)
# filters = MetadataFilters(
#     filters=[MetadataFilter(key="file_name", value="xwx0mf8aGC4.txt", operator=FilterOperator.EQ)]
# )
# query_engine = index.as_query_engine(llm=llms, filters=filters)
query_engine = index.as_query_engine(llm=llms)
response = query_engine.query("give me the file names which the content are about F1")
print(response)
print(123)

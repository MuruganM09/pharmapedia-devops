from dotenv import load_dotenv
import os
load_dotenv()

# Use relative paths so it works both locally and in Docker
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "doc", "sample_001-0013.json")
drug_file_path = os.path.join(BASE_DIR, "drugs.txt")

EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
model_name = 'GLM-4.7-Flash'
base_url = 'https://api.z.ai/api/paas/v4/'
Persistant_dir = os.path.join(BASE_DIR, "..", "chromadb")
collection_name = 'pharmapedia_embed_by_BAAI'

pg_connection = f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_Name')}"
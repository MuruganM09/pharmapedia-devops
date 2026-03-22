from data_loader import load_json
from data_cleaning import clean_json
from data_transformation import transform_json
from data_chunking import chunk_document
from create_vectordb import VectorDB
from dotenv import load_dotenv
from config import Persistant_dir,pg_connection,collection_name

load_dotenv()
collection_name = collection_name
persist_dir = Persistant_dir
connection = pg_connection

print("data loading......")
data = load_json()
print("data cleaning......")
cleaned_data = clean_json(data)
print("data transforming")
transformed_data = transform_json(cleaned_data)
print("data chunking......")
document = chunk_document(transformed_data)

db=VectorDB()
print("----chroma embedding started-----")
chroma=db.exists_chroma_db(document,persist_dir,collection_name)
print("----chroma embedding completed-----")

print("----pgvector embedding started-----")
pgvector=db.exists_pgvector(document,connection,collection_name)
print("----pgvector embedding completed-----")


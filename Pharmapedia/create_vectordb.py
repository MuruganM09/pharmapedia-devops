import os
from langchain_chroma.vectorstores import Chroma
from langchain_postgres import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL
from tqdm import tqdm
import logging 
import math
class VectorDB():
    def __init__(self):
        self.embedding=self.load_embed()

    def store_embedding(self,db_obj,doc):
        logging.basicConfig(level=logging.INFO,format="%(asctime)s|%(levelname)s|%(message)s")
        batch_size=16
        total_doc=len(doc)
        num_batch=math.ceil(total_doc/batch_size)

        for i in tqdm(range(num_batch)):
            start=i*batch_size
            end=min(batch_size+start,total_doc)
            batch=doc[start:end]

            try:
                db_obj.add_documents(batch)
                logging.info(f"Embedding batch {i}/{num_batch}| docs {start}--{end}")
            except Exception as e:
                logging.error(f"batch fails at {i} - {e}")

    def load_embed(self):
        embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL,encode_kwargs={"batch_size":16})
        return embeddings  
    
    def chroma_db(self,collection_name,persist_dir):
        try:
            if not os.path.exists(persist_dir):
                raise Exception("given path doesn't exists")
            else:
                db=Chroma(
                    collection_name=collection_name,
                    embedding_function=self.embedding,
                    persist_directory=persist_dir
                )
                return db
        except Exception as e:
            raise Exception(e)
        
    def create_chroma_db(self,document,collection_name,persist_dir):
        try:
            if not os.path.exists(persist_dir):
                raise Exception("given path doesn't exists")
            else:
                db=Chroma.from_documents(
                    collection_name=collection_name,
                    documents=document,
                    embedding=self.embedding,
                    persist_directory=persist_dir
                )
                return db
        except Exception as e:
            raise Exception(e)    

    def exists_chroma_db(self,document,persist_dir,collection_name):
        try:
            if not os.path.exists(persist_dir):
                raise Exception("given path doesn't exists")
            else:
                db=Chroma(
                    collection_name=collection_name,
                    embedding_function=self.embedding,
                    persist_directory=persist_dir
                )
                self.store_embedding(db_obj=db,doc=document)
                return db
        except Exception as e:
            raise Exception(e)  
         
    def pgvector(self,connection,collection_name):
        try:
            db=PGVector(
                embeddings=self.embedding,
                connection=connection,
                use_jsonb=True,
                collection_name=collection_name
            )
            return db
        except Exception as e:
            raise Exception(e)

    def create_pgvector(self,document,connection,collection_name):
        try:
            db=PGVector.from_documents(
                documents=document,
                collection_name=collection_name,
                connection=connection,
                embedding=self.embedding,
                use_jsonb=True
            )     
            return db
        except Exception as e:
            raise Exception(e)

    def exists_pgvector(self,document,connection,collection_name):       
        try:
            db=PGVector(
                embeddings=self.embedding,
                connection=connection,
                use_jsonb=True,
                collection_name=collection_name
            )
            self.store_embedding(db,document)
            return db
        except Exception as e:
            raise Exception(e)
        
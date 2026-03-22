from utils import load_model,load_rewritten_prompt,load_AI_prompt
from create_vectordb import VectorDB
from config import Persistant_dir,pg_connection,collection_name
def chaining(user_query):
    model = load_model()
    query_prompt=load_AI_prompt()
    rewritten_prom=load_rewritten_prompt()

    rewritten_chain = rewritten_prom|model|(lambda message:message.content.strip())
    rewritten_query = rewritten_chain.invoke(user_query)

    db=VectorDB()
    database=db.pgvector(pg_connection,collection_name)
    # database=db.chroma_db(collection_name,Persistant_dir)
    retrieverr = database.as_retriever(search_kwargs={"k":5})
    # retrieverr = database.as_retriever(search_type="mmr",search_kwargs={
    #     "k": 5,
    #     "fetch_k": 10,
    #     "lambda_mult": 0.7
    # }
    # )
    doc = retrieverr.invoke(rewritten_query)
    content = " \n\n".join(docs.page_content for docs in doc)
    print(rewritten_query)
    print(content)
    query_chain = query_prompt|model|(lambda message:message.content.strip())

    response=query_chain.invoke({"question":user_query,"context":content})

    return response

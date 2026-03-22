from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_document(document):
    doc=[]
    for item in document:
        doc.append(Document(
            page_content=item["page_content"],
            metadata={**item['metadata'],"id":item['id']},
        ))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,separators=["\n\n","\n2.","\n3.","\n•","\n",". "]
    )
    chunked_doc=splitter.split_documents(doc) 

    for idx,docs in enumerate(chunked_doc):
        base_id = docs.metadata['id']
        docs.metadata['id'] = f"{base_id}chunk_{idx}"
    
    return chunked_doc

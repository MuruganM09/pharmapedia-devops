from chaining import chaining
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
class UserQuery(BaseModel):
    question:str

@app.post("/query")
async def question(data:UserQuery):
    user_query=data.question.lower().strip()
    answer =await run_in_threadpool(chaining,user_query)
    return {"answer":answer}

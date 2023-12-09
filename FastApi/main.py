from  fastapi import FastAPI,HTTPException,Depends
from typing import Annotated,List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import sessionLocal,engine
import model

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# cross origin access providing
origins = [
    'http://localhost:3000',


]
app.add_middleware(
    CORSMiddleware,allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
                   )
class TransactionBase(BaseModel):
    amount: float
    category: str
    description:str
    is_income:bool
    date:str
class TransactionModel(TransactionBase):
    id:int
    class Config:
        from_attributes = True

def get_db():
    db = sessionLocal()
    try :
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

model.Base.metadata.create_all(bind=engine)

@app.post("/transactions/",response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    db_transaction = model.Transactions(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
@app.get("/transactions/",response_model=List[TransactionModel])
async def list_transactions(db: db_dependency,skip: int =0, limit: int=100):
    transactions = db.query(model.Transactions).offset(skip).limit(limit).all()
    return transactions
    

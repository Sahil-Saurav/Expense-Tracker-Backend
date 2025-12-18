from fastapi import FastAPI,status
import app.models as models
from app.database import engine
from .routers import user,expense,util,debt,authenticate
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

@app.get('/root',status_code=status.HTTP_200_OK)
def root():
    return "OK"

app.include_router(user.router)
app.include_router(expense.router)
app.include_router(debt.router)
app.include_router(util.router)
app.include_router(authenticate.router)

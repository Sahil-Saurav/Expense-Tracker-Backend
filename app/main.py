from fastapi import FastAPI,status
import app.models as models
from app.database import engine
from .routers import user,expense,util,debt
app = FastAPI()

models.Base.metadata.create_all(bind = engine)

@app.get('/',status_code=status.HTTP_200_OK)
def root():
    return "OK"

app.include_router(user.router)
app.include_router(expense.router)
app.include_router(debt.router)
app.include_router(util.router)
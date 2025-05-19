from fastapi import FastAPI
from app.routers import auth, books, readers, borrow
from app.database import Base, engine
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Библиотека")


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(readers.router, prefix="/readers", tags=["Readers"])
app.include_router(borrow.router, prefix="/borrow", tags=["Borrow"])


@app.get("/", summary="Главная ручка", tags=["Основная ручка"])
def home():
    return {"message": "Добро пожаловать в библиотеку"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

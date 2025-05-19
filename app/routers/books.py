from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.depend import get_current_user
from typing import List
from app.database import get_db

router = APIRouter()


@router.get("/all", response_model=List[schemas.Book])
def get_all_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    data = book.model_dump()
    if not data.get("isbn"):
        data["isbn"] = None

    db_book = models.Book(**data)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=List[schemas.Book])
def read_books(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        user: models.User = Depends(get_current_user)
):
    return db.query(models.Book).offset(skip).limit(limit).all()


@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(models.Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдено")
    return book


@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updated_book: schemas.BookCreate,
                db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    book = db.get(models.Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдено")
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    book = db.get(models.Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдено")
    db.delete(book)
    db.commit()
    return {"msg": "Книга удалена"}

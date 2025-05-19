from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.depend import get_current_user
from datetime import datetime
from typing import List


router = APIRouter()


@router.post("/borrow", response_model=schemas.BorrowedBookSchema)
def borrow_book(req: schemas.BorrowRequest, db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    book = db.query(models.Book).get(req.book_id)
    if not book or book.quantity < 1:
        raise HTTPException(status_code=400, detail="Книга недоступна")

    active_borrows = db.query(models.BorrowedBook).filter_by(reader_id=req.reader_id, return_date=None).count()
    if active_borrows >= 3:
        raise HTTPException(status_code=400, detail="Читатель уже взял 3 книги")

    borrowed = models.BorrowedBook(book_id=req.book_id, reader_id=req.reader_id)
    db.add(borrowed)
    book.quantity -= 1
    db.commit()
    db.refresh(borrowed)
    return borrowed


@router.post("/return", response_model=schemas.BorrowedBookSchema)
def return_book(req: schemas.BorrowRequest, db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    borrowed = db.query(models.BorrowedBook).filter_by(
        book_id=req.book_id, reader_id=req.reader_id, return_date=None
    ).first()
    if not borrowed:
        raise HTTPException(status_code=400, detail="Книга не была взята или уже возвращена")

    borrowed.return_date = datetime.utcnow()

    book = db.get(models.Book, req.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    book.quantity += 1
    db.commit()
    db.refresh(borrowed)
    return borrowed


@router.get("/reader/{reader_id}", response_model=List[schemas.BorrowedBookSchema])
def get_reader_borrowed_books(reader_id: int, db: Session = Depends(get_db),
                              user: models.User = Depends(get_current_user)):
    borrowed = db.query(models.BorrowedBook).filter_by(reader_id=reader_id, return_date=None).all()
    return borrowed

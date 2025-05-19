from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.depend import get_current_user
from typing import List

router = APIRouter()


@router.post("/", response_model=schemas.Reader)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db),
                  user: models.User = Depends(get_current_user)):
    if db.query(models.Reader).filter_by(email=reader.email).first():
        raise HTTPException(status_code=400, detail="Читатель уже существует")
    db_reader = models.Reader(**reader.dict())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader


@router.get("/", response_model=List[schemas.Reader])
def read_readers(db: Session = Depends(get_db),
                 user: models.User = Depends(get_current_user)):
    return db.query(models.Reader).all()


@router.get("/{reader_id}", response_model=schemas.Reader)
def read_reader(reader_id: int, db: Session = Depends(get_db),
                user: models.User = Depends(get_current_user)):
    reader = db.query(models.Reader).get(reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    return reader


@router.put("/{reader_id}", response_model=schemas.Reader)
def update_reader(reader_id: int, updated: schemas.ReaderCreate, db: Session = Depends(get_db),
                  user: models.User = Depends(get_current_user)):
    reader = db.query(models.Reader).get(reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    for key, value in updated.dict().items():
        setattr(reader, key, value)
    db.commit()
    db.refresh(reader)
    return reader


@router.delete("/{reader_id}")
def delete_reader(reader_id: int, db: Session = Depends(get_db),
                  user: models.User = Depends(get_current_user)):
    reader = db.query(models.Reader).get(reader_id)
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")
    db.delete(reader)
    db.commit()
    return {"msg": "Читатель удален"}

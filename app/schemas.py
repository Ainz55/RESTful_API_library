from pydantic import BaseModel, EmailStr, Field
from fastapi import Form
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OAuth2EmailRequestForm:
    def __init__(
        self,
        username: str = Form(...),
        password: str = Form(...)
    ):
        self.username = username
        self.password = password


"""Books"""


class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    quantity: int = Field(default=1, ge=0)
    description: Optional[str] = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True


"""Readers"""


class ReaderBase(BaseModel):
    name: str
    email: EmailStr


class ReaderCreate(ReaderBase):
    pass


class Reader(ReaderBase):
    id: int

    class Config:
        from_attributes = True


"""Borrow"""


class BorrowRequest(BaseModel):
    book_id: int
    reader_id: int


class BorrowedBookSchema(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True

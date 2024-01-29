from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import schemas, models, crud
from sqlalchemy.orm import Session
from dependency import get_db, get_current_active_user

book_router = APIRouter(prefix="/books", tags=["Books"], dependencies=[Depends(get_current_active_user)])

@book_router.post("/create")
def create_book(book: schemas.BookCreate, current_user: Annotated[schemas.User, Depends(get_current_active_user)],db: Session = Depends(get_db)):
    return crud.create_book(db, book, current_user)

@book_router.get("/{id}")
def read_book(id: int, db: Session = Depends(get_db)):
    return crud.get_book(db, id)


@book_router.delete("/{book_id}")
def delete_book(book_id: int, current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id, current_user)


@book_router.get("/list/")
def read_books(db: Session = Depends(get_db)):
    return crud.get_books(db)

@book_router.get("/borrowers/{book_id}", response_model=list[dict])
def get_borrowers_of_book(book_id: int, db: Session = Depends(get_db)):
    borrowers = crud.get_all_borrowers_of_book(db, book_id)
    if not borrowers:
        raise HTTPException(status_code=404, detail="No borrowers found for the book.")
    return borrowers













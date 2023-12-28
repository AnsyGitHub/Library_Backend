from fastapi import APIRouter, Depends
import schemas, models, crud
from sqlalchemy.orm import Session
from dependency import get_db
from typing import List
from dependency import get_db, get_current_active_user

borrow_router = APIRouter(prefix="/borrow", tags=["Borrow"],dependencies=[Depends(get_current_active_user)])

@borrow_router.post("/")
def borrow_book(member_id: str, book_id:str, db: Session = Depends(get_db)):
    return crud.borrow_book(db, book_id, member_id)

@borrow_router.post("/return")
def return_borrow(member_id: str, book_id:str, db: Session = Depends(get_db)):
    return crud.return_book(db, book_id, member_id)

@borrow_router.get("/list/")
def get_borrowed_books(db: Session = Depends(get_db)):
    borrowed_books = crud.get_borrowed_members_and_books(db)
    return borrowed_books







# @book_router.get("/{id}")
# def read_book(id: int, db: Session = Depends(get_db)):
#     return crud.get_book(db, id)


# @book_router.delete("/{book_id}")
# def delete_book(book_id: int, db: Session = Depends(get_db)):
#     crud.delete_book(db=db, book_id=book_id)
#     return {"Book Deleted"}

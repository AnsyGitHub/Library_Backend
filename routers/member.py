from fastapi import APIRouter, Depends, HTTPException
import schemas, models, crud
from sqlalchemy.orm import Session
from dependency import get_db
from typing import List
from dependency import get_db, get_current_active_user

member_router = APIRouter(prefix="/members", tags=["Members"], dependencies=[Depends(get_current_active_user)])

@member_router.post("/create")
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    return crud.create_member(db, member)

@member_router.get("/{id}")
def read_member(id: int, db: Session = Depends(get_db)):
    return crud.get_member(db, id)

@member_router.get("/list/")
def read_member(db: Session = Depends(get_db)):
    return crud.get_members(db)

@member_router.get("/member/{member_id}/borrowed-books/")
async def get_member_borrowed_books(member_id: int, db: Session = Depends(get_db)):
    borrowed_books = crud.get_books_borrowed_by_member(db, member_id)
    if not borrowed_books:
        raise HTTPException(status_code=404, detail="Member not found or has not borrowed any books.")
    return borrowed_books

@member_router.delete("/{id}")
def delete_member(id: int, db: Session = Depends(get_db)):
    crud.delete_member(db, id)
    return {"Book Deleted"}



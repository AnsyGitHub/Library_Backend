import datetime
from typing import Annotated
from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import update, func
from fastapi import Response, Depends
from dependency import get_current_active_user

#-------------------------------------------------------------------------------------------#

def create_book(db: Session, book: schemas.BookCreate,current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    id = current_user.id
    db_book = models.Book(**book.model_dump(),user_add = id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return Response("Book Added",status_code=201)

def get_book(db: Session, id: int):
    return db.query(models.Book).filter(models.Book.id == id).first()

def delete_book(db:Session, id: int, current_user: schemas.User):
    user = current_user.id
    book =db.query(models.Book).filter(
        models.Book.id == id,
        models.Book.user_add == user
        ).first()
    if book:
        book.delete()
        db.commit()
        return "Book Deleted"
    else:
        return "Not allowed"
    

def get_books(db: Session):
    return db.query(models.Book).all()

#---------------------------------------------------------------------------------------------#

def create_member(db:Session, member: schemas.MemberCreate):
    db_member = models.Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return {"Member Added"}

def get_member(db: Session, id: int):
    return db.query(models.Member).filter(models.Member.id == id).first()

def get_members(db: Session):
    return db.query(models.Member).all()

def delete_member(db:Session, id: int):
    db.query(models.Member).filter(models.Member.id == id).delete()
    db.commit()
    return {"Book Deleted"}


#-------------------------------------------------------------------------------------------#


def borrow_book(db: Session, book_id: int, member_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        print("The Book is not in the Library")
        return None
    
    member = db.query(models.Member).filter(models.Member.id == member_id).first()
    if not member:
        print("Member does not exist")
        return None

    if book.is_borrowed:
        print("Book is already borrowed")
        return None
    
    book.is_borrowed = True

    borrow_record = models.BorrowRecord(book_id=book_id, member_id=member_id, borrow_date=func.now(), return_date=None)
    db.add(borrow_record)
    db.commit()
    db.refresh(borrow_record)

    return borrow_record



def return_book(db: Session, book_id: int, member_id: int):
    # Get the borrow record for the specified book and member
    borrow_record = (
        db.query(models.BorrowRecord)
        .filter(
            models.BorrowRecord.book_id == book_id,
            models.BorrowRecord.member_id == member_id,
            models.BorrowRecord.return_date.is_(None), 
        )
        .first()
    )

    if not borrow_record:
        print("Book is not currently borrowed by the specified member")
        return None
    
    borrow_record.return_date = datetime.utcnow()

    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        book.is_borrowed = False 
        db.commit()
    else:
        print("Book not found")

    db.commit()

    return borrow_record

def get_borrowed_members_and_books(db: Session):
    borrowed_records = (
        db.query(models.BorrowRecord)
        .filter(models.BorrowRecord.return_date.is_(None))
        .all()
    )
    result = [
        {"member_id": record.member_id, "book_id": record.book_id}
        for record in borrowed_records
    ]

    return result


def get_books_borrowed_by_member(db: Session, member_id: int):
    borrowed_records = (
        db.query(models.BorrowRecord)
        .filter(models.BorrowRecord.member_id == member_id, models.BorrowRecord.return_date.is_(None))
        .all()
    )
    
    result = [
        {
            "member_id": record.member_id,
            "book_id": record.book_id,
            "book": db.query(models.Book).filter(models.Book.id == record.book_id).first(),
        }
        for record in borrowed_records
    ]

    return result


def get_all_borrowers_of_book(db: Session, book_id: int):
    borrowed_records = (
        db.query(models.BorrowRecord)
        .filter(models.BorrowRecord.book_id == book_id)
        .all()
    )

    result = [{"member_id": record.member_id, "book_id": record.book_id} for record in borrowed_records]

    return result















# def get_book_by_name(db: Session, name: str):
#     return db.query(models.Book).filter(models.Book.name == name).first()


# def get_books_names(db: Session):
#     book_names = []
#     for naming in db.query(models.Book.name).all():
#         book_names.append(naming[0]) 
#     return book_names

# def update_record(db:Session, id:int, new_data: schemas.book_body):
#     stmt = update(models.Book).where(models.Book.id == id).values(**new_data.model_dump())
#     db.execute(stmt)
#     db.commit()
#     return "Updated"

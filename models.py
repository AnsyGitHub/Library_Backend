from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    ISBN = Column(String, unique=True, index=True)
    is_borrowed = Column(Boolean, default=False)
    user_add = Column(Integer, ForeignKey("users.id"))


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    # borrow = relationship("borrow_records", back_populates="borrow_records")

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrow_date = Column(DateTime(timezone=True), server_default=func.now())
    return_date = Column(DateTime(timezone=True), nullable=True)
    
    member = relationship("Member", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")

# Add a bidirectional relationship for Member and BorrowRecord
Member.borrow_records = relationship("BorrowRecord", back_populates="member")

# Add a bidirectional relationship for Book and BorrowRecord
Book.borrow_records = relationship("BorrowRecord", back_populates="book")



# ------------------------------------Authentication------------------------------------ #

class UserInDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String, index=True)
    token_type = Column(String)


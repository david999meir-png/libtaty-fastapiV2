from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
import logging
from typing import Literal
from database.books_db import BookDAL
from database.members_db import MemberDAL


class Book(BaseModel):
    title: str = Field(max_length=50)
    author: str = Field(max_length=50)
    genre: Literal['Fiction', 'NON-Fiction', 'Science', 'History', 'Other']

class BookUP(BaseModel):
    title: str | None = Field(max_length=50, default=None)
    author: str | None = Field(max_length=50, default=None)
    genre: Literal['Fiction', 'NON-Fiction', 'Science', 'History', 'Other'] | None = None


router = APIRouter()


@router.get("")
def get_all_books():
    logging.info("A request to accept all members has been received.")
    return BookDAL.get_all_bodks()


@router.post("", status_code=201)
def create_books(data:Book):
    new_id = BookDAL.create_book(data.model_dump())
    return {"new id": new_id}


@router.get("/{id}")
def get_book_by_id(id: int):
    found = BookDAL.get_book_by_id(id)
    if not found:
        raise HTTPException(status_code=404, detail=f"book id {id} not found.")
    
    return found


@router.patch("/{id}")
def update_book(id: int, data: BookUP):
    found = BookDAL.get_book_by_id(id)

    if not found:
        raise HTTPException(status_code=404, detail=f"book id {id} not found.")
    
    changed = BookDAL.update_book(id, data.model_dump(exclude_none=True))

    if not changed:
        raise HTTPException(status_code=400, detail=f"book id {id} not changed")
    
    return {"msg": f"book {id} updated"}


@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    try:

        found = MemberDAL.get_member_by_id(member_id)
        if not found:
            raise HTTPException(status_code=404, detail=f"member id {member_id} not found.")
        
        active = found["is_active"]
        if not active:
            raise HTTPException(status_code=400, detail=f"member id {member_id} not active.")
        
        book_found = BookDAL.get_book_by_id(id)
        if not book_found:
            raise HTTPException(status_code=404, detail="book id {id} not found.")
        
        available = book_found["is_available"]
        if not available:
            raise HTTPException(status_code=400, detail=f"book id {id} not available.")
        
        books_borrowed = BookDAL.count_active_borrows_by_member(member_id)
        if books_borrowed["total_member_books"] >= 3:
            raise HTTPException(status_code=400, detail=f"member id {id} alrady borrow the max number of books")
        
        BookDAL.set_available(id, False, member_id)
        return {"msg": f"book id {id} borrow to member id {member_id}"}
    
    except Exception as e:
        logging.exception(e)   
        raise  


@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    found = MemberDAL.get_member_by_id(member_id)
    if not found:
        raise HTTPException(status_code=404, detail=f"member id {member_id} not found.")

    book_found = BookDAL.get_book_by_id(id)
    if not book_found:
        raise HTTPException(status_code=404, detail=f"book id {id} not found.")
    
    if member_id != book_found["borrowed_by_member_id"]:
        raise HTTPException(status_code=400, detail="this book not borrowed to this member.")
    
    BookDAL.set_available(id, True)
    return {"msg": f"book id {id} returned by member id {member_id}"}
    
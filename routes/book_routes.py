from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from database.books_db import BookDAL


router = APIRouter()


@router.get("")
def get_all_books():
    return BookDAL.get_all_bodks()


@router.post("")
def create_books(data):
    pass


@router.get("/{id}")
def get_book_by_id(id: int):
    found = BookDAL.update_book(id)
    if not found:
        raise HTTPException(status_code=404, detail=f"book id {id} not found.")
    
    return found


@router.patch("/{id}")
def update_book(id: int):
    found = BookDAL.update_book(id)
    if not found:
        raise HTTPException(status_code=404, detail=f"book id {id} not found.")
    
    return found


@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    pass


@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    pass

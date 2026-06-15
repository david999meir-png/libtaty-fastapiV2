from fastapi import APIRouter, HTTPException, Query
from database import members_db, books_db
import logging


router = APIRouter()

@router.get("/summary")
def get_general_report():
    total_books = books_db.BookDAL.count_total_books()
    available_books = books_db.BookDAL.count_available_books()
    borrowed_books = books_db.BookDAL.count_borrowed_books()
    active_members = members_db.MemberDAL.count_active_members()

    return {**total_books, **available_books, **borrowed_books, **active_members}


@router.get("/books-by-genre")
def get_books_by_genre(genre: str = Query(...)):
    return books_db.BookDAL.count_by_genre(genre.title())


@router.get("/top-member")
def get_top_member():
    logging.info("A request for Top Member has been received.")
    return members_db.MemberDAL.get_top_member()

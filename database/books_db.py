import logging
from database.db_connection import get_connection

class BookDAL:
    @staticmethod
    def create_book(data: dict):
        with get_connection() as conn:
            with conn.cursor() as cursor:

                sql = """
                    INSERT INTO books(title, author, genre)
                      VALUES (%s, %s, %s)
                """
                cursor.execute(sql, list(data.values()))
                conn.commit()
                return cursor.lastrowid
    @staticmethod
    def get_all_bodks():
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql ="SELECT * FROM books"
                cursor.execute(sql)

                return cursor.fetchall()
    
    @staticmethod
    def get_book_by_id(id: int):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM books WHERE id = %s"
                cursor.execute(sql, (id,))

                return cursor.fetchone()
    
    @staticmethod
    def update_book(id: int, data: dict):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                list_cause = [f"{key}=%s" for key in data]
                txt_cause = ", ".join(list_cause)

                sql = f"UPDATE books SET {txt_cause} WHERE id = %s"
                vaues = list(data.values()) + [id]

                cursor.execute(sql, vaues)
                conn.commit()

                return cursor.rowcount > 0
    
    @staticmethod
    def set_available(id: int, val: bool, member_id: int | None = None):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """UPDATE books SET is_available = %s ,borrowed_by_member_id = %s WHERE id = %s"""
                cursor.execute(sql, (val, member_id, id))

                conn.commit()
                return cursor.rowcount > 0
    
    @staticmethod
    def count_total_books():
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(*) AS total_books FROM books"""
                cursor.execute(sql)

                return cursor.fetchone()
    
    @staticmethod
    def count_available_books():
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(is_available) AS total_available WHERE is_available = TRUE"""
                cursor.execute(sql)

                return cursor.fetchone()

    @staticmethod
    def count_borrowed_books():
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(is_available) AS total_available WHERE is_available = FALSE"""
                cursor.execute(sql)

                return cursor.fetchone()

    @staticmethod        
    def count_by_genre(genre):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(*) FROM books WHERE genre = %s"""
                cursor.execute(sql, (genre,))

                return cursor.fetchall()

    @staticmethod       
    def count_active_borrows_by_member(member_id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(*) AS total_member_books
                        FROM books WHERE borrowed_by_member_id = %s"""
                
                cursor.execute(sql)
                return cursor.fetchone()
            

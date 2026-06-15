import logging
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="root",
        database="librery_db"
    )


def create_tables():
    with get_connection() as conn:
        with conn.cursor as cursor:
            sql_members = """
                    CREATE TABLE IF NOT EXIST members(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(50) NOT NULL, 
                    email VARCHAR(255) UNIQUE NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE NOT NULL,
                    total_borrows INT DEFAULT 0 NOT NULL
                    )
                    """
            sql_books = """CREATE TABLE IF NOT EXIST books(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        title VARCHAR(50) NOT NULL,
                        author VARCHAR(50) NOT NULL,
                        genre ENUM('Fiction', 'NON-Fiction', 'Science', 'History', 'Other') NOT NULL,
                        is_available BOOLEAN DEFAULT TRUE, NOT NULL,
                        borrowed_by_member_id INT DEFAULT NULL
                        )"""
            cursor.execute(sql_books)
            cursor.execute(sql_members)

            conn.commit()
            
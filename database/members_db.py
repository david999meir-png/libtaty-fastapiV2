from database.db_connection import get_connection

class MemberDAL:
    @staticmethod
    def create_member(data: dict):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """INSERT INTO members (name, email) VALUES (%s, %s)"""
                cursor.execute(sql,list(data.values()))

                conn.commit()
                return cursor.lastrowid

    @staticmethod
    def get_all_members():
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql  = """SELECT * FROM members"""
                cursor.execute(sql)

                return cursor.fetchall()
            
    @staticmethod
    def get_member_by_id(id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql  = """SELECT * FROM members WHERE id = %s"""
                cursor.execute(sql, (id,))

                return cursor.fetchone()
    
    @staticmethod
    def update_member(id: int, data: dict):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                list_couse = [f"{key}=%s" for key in data.keys()]
                txt_couse = ", ".join(list_couse)

                sql = f"UPDATE members SET {txt_couse} WHERE id = %s"
                values = list(data.values()) + [id]

                cursor.execute(sql, values)
                conn.commit()

                return cursor.rowcount > 0
    
    @staticmethod
    def deactivate_member(id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """UPDATE members SET is_active = FALSE WHERE id = %s"""
                cursor.execute(sql, (id,))

                conn.commit()
                return cursor.rowcount > 0
    
    @staticmethod
    def activate_member(id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """UPDATE members SET is_active = TRUE WHERE id = %s"""
                cursor.execute(sql, (id,))

                conn.commit()
                return cursor.rowcount > 0
    
    @staticmethod
    def increment_borrows(id):
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """UPDATE members SET total_borrows = total_borrows + 1 WHERE id = %s"""
                cursor.execute(sql, (id,))
                conn.commit()

                return cursor.rowcount > 0
    
    @staticmethod
    def count_active_members():
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT COUNT(*) FROM members WHERE is_active = TRUE"""
                cursor.execute(sql)

                return cursor.fetchone()

    @staticmethod       
    def get_top_member():
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                sql = """SELECT * FROM members 
                        ORDER BY total_borrows DESC
                        LIMIT 1"""
                cursor.execute(sql)
                top = cursor.fetchone()

                return top
            
            

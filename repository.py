import sqlite3


class CustomerRepository:
    def __init__(self):
        self.conn = sqlite3.connect("crs.db")

    def get_total(self):
        cursor = self.conn.cursor()
        try:
            return cursor.execute("SELECT COUNT(*) FROM customer").fetchone()[0]
        finally:
            cursor.close()

    def get_all(self, limit, offset):
        cursor = self.conn.cursor()
        try:
            return cursor.execute(
                "SELECT * FROM customer LIMIT ? OFFSET ?", (limit, offset)
            ).fetchall()
        finally:
            cursor.close()

    def search(self, keyword):
        cursor = self.conn.cursor()
        try:
            return cursor.execute(
                """SELECT * FROM customer
                    WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ?""",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
            ).fetchall()
        finally:
            cursor.close()

    def add(self, first_name, last_name, email, phone):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO customer (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
                (first_name, last_name, email, phone),
            )
            self.conn.commit()
        finally:
            cursor.close()

    def update(self, first_name, last_name, email, phone, id):
        cursor = self.conn.cursor()
        try:
            update_fields = []
            if first_name:
                update_fields.append(f"first_name = '{first_name}'")
            if last_name:
                update_fields.append(f"last_name = '{last_name}'")
            if email:
                update_fields.append(f"email = '{email}'")
            if phone:
                update_fields.append(f"phone = '{phone}'")

            if not update_fields:
                return

            update_fields = ", ".join(update_fields)
            cursor.execute(
                f"UPDATE customer SET {update_fields} WHERE id = {id}"
            )
            self.conn.commit()
        finally:
            cursor.close()

    def delete(self, id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM customer WHERE id = ?", (id,))
            self.conn.commit()
        finally:
            cursor.close()

    def __del__(self):
        self.conn.close()

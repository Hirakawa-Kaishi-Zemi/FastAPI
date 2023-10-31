import sqlite3

from settings import DB_DATABASE


def init_db(pre_insert=False, drop_if_exists=False):
    with sqlite3.connect(DB_DATABASE) as conn:
        if drop_if_exists:
            conn.execute('''
            DROP TABLE IF EXISTS 'users';
            ''')

            conn.execute('''        
            DROP TABLE IF EXISTS 'responses';
            ''')

        conn.execute('''
        CREATE TABLE IF NOT EXISTS `users` (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            token TEXT UNIQUE
        );
        ''')

        conn.execute('''
        CREATE TABLE IF NOT EXISTS `responses` (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            system_prompt TEXT,
            assistant_prompt TEXT,
            user_prompt TEXT,
            chat_gpt_answer TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        ''')

        if pre_insert:
            conn.execute('''
            INSERT INTO `users` (`email`) 
            VALUES 
            ("sato@test.com"), ("mineno@test.com"), ("tooyama@test.com"), 
            ("hirayama@test.com"), ("sakai@test.com");            
            ''')


class DataModel(object):

    def __init__(self, table: str, db_path: str or None = DB_DATABASE):
        self._table = table
        self._select_tokens: list[str] = ['*']
        self._where_tokens: list[tuple[str, any, str, str]] = []
        self._limit: int or None = None

        self._conn = sqlite3.connect(db_path)
        self._cursor = self._conn.cursor()

    def __del__(self):
        self.close()

    def select(self, *columns: str) -> 'DataModel':
        if columns:
            self._select_tokens = [f"`{column}`" for column in columns]
        return self

    def where(self, column: str, value: any, cmp_op: str = '=') -> 'DataModel':
        self._where_tokens.append(('AND', column, value, cmp_op))
        return self

    def or_where(self, column: str, value: any, cmp_op: str = '=') -> 'DataModel':
        self._where_tokens.append(('OR', column, value, cmp_op))
        return self

    def limit(self, limit: int) -> 'DataModel':
        self._limit = limit
        return self

    def _build_query(self) -> str:
        select_clause = f"SELECT {', '.join(self._select_tokens)}"
        from_clause = f"FROM `{self._table}`"

        where_clauses = []
        for logical_op, column, value, cmp_op in self._where_tokens:
            if where_clauses:
                where_clauses.append(logical_op)
            where_clauses.append(f"`{column}` {cmp_op} ?")

        where_clause = f"WHERE {' '.join(where_clauses)}" if where_clauses else ""
        query = f"{select_clause} {from_clause} {where_clause}"

        return query

    def get(self) -> list[tuple]:
        query = self._build_query()

        values = [value for _, _, value, _ in self._where_tokens]

        self._cursor.execute(query, values)
        results = self._cursor.fetchall()

        return results

    def first(self) -> tuple or None:
        results = self.get()
        return results[0] if results else None

    def get_query(self) -> str:
        return self._build_query()

    def insert(self, data: dict[str, any]) -> bool:
        columns = ', '.join(f"`{column}`" for column in data.keys())
        placeholders = ', '.join('?' for _ in data.values())

        query = f"INSERT INTO `{self._table}` ({columns}) VALUES ({placeholders})"

        try:
            self._cursor.execute(query, tuple(data.values()))
            self._conn.commit()
            return True
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return False

    def update(self, data: dict[str, any]) -> bool:
        if not self._where_tokens:
            raise ValueError("Update operation requires at least one WHERE clause.")

        set_clauses = ', '.join(f"`{column}` = ?" for column in data.keys())
        where_clauses = []
        values = []

        for logical_op, column, value, cmp_op in self._where_tokens:
            if where_clauses:
                where_clauses.append(logical_op)
            where_clauses.append(f"`{column}` {cmp_op} ?")
            values.append(value)

        query = f"UPDATE `{self._table}` SET {set_clauses} WHERE {' '.join(where_clauses)}"

        try:
            self._cursor.execute(query, tuple(data.values()) + tuple(values))
            self._conn.commit()
            return True
        except sqlite3.Error as e:
            print("SQLite error:", e)
            return False

    def close(self) -> None:
        if self._conn:
            self._conn.close()


def main():
    user_model = DataModel('users')

    results = (user_model
               .select('id', 'token')
               .where('email', 'test@test.com')
               .first())

    from pprint import pprint

    pprint(results)
    pprint(user_model.get_query())

    # is_ok = user_model.insert({
    #        'email': 'hirakawa.hideki@kaishi-pu.ac.jp',
    #        'token': 'ototototo',
    #    })

    user_model.update({
        'email': '2221@test.com'
    })


if __name__ == '__main__':
    main()

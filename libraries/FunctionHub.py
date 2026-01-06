from psycopg2.extensions import cursor

class FunctionHub():
    def __init__(self, cursor: cursor, table):
        self.cursor = cursor
        self.table = table

    def addFuzzyTable(self):
        # Если нет таблицы с нечеткими значениями, то создать
        self.cursor.execute(f"SELECT EXISTS ("
                            f"SELECT FROM information_schema.tables "
                            f"WHERE table_schema=\'public\' AND table_name=\'{self.table.get('fvtname')}\')")
        exists = self.cursor.fetchone()[0]
        if not exists:
            #print(f"Создается служебная таблица {self.table.get('fvtname')}")
            self.cursor.execute(f"CREATE TABLE {self.table.get('fvtname')} (name VARCHAR(50) PRIMARY KEY, a REAL, b REAL, c REAL, d REAL)")
        else:
            pass #print(f"Служебная таблица {self.table.get('fvtname')} уже создана")

    def removeConstrains(self, tableName):
        res = ""
        query = f"SELECT constraint_name, constraint_type "\
                f"FROM information_schema.table_constraints "\
                f"WHERE table_name = \'{tableName}\' "\
                f"AND constraint_type IN ('PRIMARY KEY', 'UNIQUE');"
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        while not row is None:
            res += f"DROP CONSTRAINT {row[0]},\n"
            row = self.cursor.fetchone()
        return res

    def isFuzzy(self, tableName, column):
        names = [column + self.table.get('columnsuffix') + str(i) for i in range(1, 5)]
        for name in names:
            query = f"""SELECT 
                            column_name,
                            data_type
                        FROM information_schema.columns 
                        WHERE table_name = \'{tableName}\' 
                        AND column_name = \'{name}\'
                        AND data_type = 'real';"""
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is None:
                return False
        return True



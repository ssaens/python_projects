import MySQLdb

class TableInserter:

    def __init__(self, database_name, table_name):
        self.name = table_name

        table_header = self.name + str(self.columns)
        value_string = ','.join('%s' for _ in columns)
        self.query = 'INSERT INTO {0} VALUES ({1})'.format(self.name, value_string)
        try:
            self.conn = MySQLdb.connect(host= "localhost",
                      user="dillon",
                      passwd="q0W9e8r7",
                      db=database_name)
            self.cursor = self.conn.cursor()
        self.columns = self.get_columns()
        except Exception as e:
            print('Exception:', e)

    #takes a tuple representing a table row into the table
    def insert(self, row):
        try:
            self.cursor.execute(self.query, row)
            self.conn.commit()
        except Exception as e:
            print('failed:', str(e), 'on query:', self.query)
            self.conn.rollback()

    #takes multiple rows and inserts them into the table
    def insert_multiple(self, rows):
        for row in rows:
            insert(col, row)

    def show_table(self):
        self.cursor.execute('SELECT * FROM %s;'%self.name)
        print(self.cursor.fetchall())

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

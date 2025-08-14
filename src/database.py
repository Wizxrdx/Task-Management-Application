from dotenv import load_dotenv
import mysql.connector
import os

class Database:
    def __init__(self):
        """
            Connect to database and initialize tables database
        """
        load_dotenv()

        print('Connecting to database...')
        self.cnx = mysql.connector.connect(user='root', password=os.getenv("MYSQL_ROOT_PASSWORD"),
                                    host='localhost',
                                    database=os.getenv("MYSQL_DATABASE"))
        print('Database Connected.')

        cursor = self.cnx.cursor()
        with open("./database.sql", "r") as f:
            cursor.execute(f.read())

    def create_task(self, title, desc, due_date, priority):
        """
            title: string
            desc: string
            due_date: 'YYYY-MM-DD'
            priority: string = 'Low' | 'Medium' | 'High'
            status: string = 'Pending' | 'In Progress' | 'Completed'

        """
        cursor = self.cnx.cursor()
        
        query = 'INSERT INTO tasks (title, description, due_date, priority) VALUES (%s, %s, %s, %s)'
        cursor.execute(query, (title, desc, due_date, priority))
        emp_no = cursor.lastrowid
        self.cnx.commit()
        cursor.close()
        return emp_no
    
    def read_task(self, idx):
        """
            Returns 1 task with the idx
        """
        cursor = self.cnx.cursor()

        query = 'SELECT * FROM tasks WHERE id = %s'
        cursor.execute(query, [idx])
        data = cursor.fetchall()
        cursor.close()
        return data

    def read_tasks(self, page_num, limit, due_date = 'ASC', priority = None, status = None):
        """
            page_num: int
            limit: int
            due_date: string = 'ASC' | 'DESC'
            priority: string = 'Low' | 'Medium' | 'High'
            status: string = 'Pending' | 'In Progress' | 'Completed'

            Returns task/s based on page, limit, sorted by due_date, and filtered using priority or status
        """
        cursor = self.cnx.cursor()

        offset = (page_num - 1) * limit
        filters = []
        values = [limit, offset]

        if priority:
            filters.append('priority = %s')
            values.append(priority)

        if status:
            filters.append('status = %s')
            values.append(status)

        filters_query = f' WHERE {' AND '.join(filters)}' if filters else ''
        query = 'SELECT * FROM tasks LIMIT %s OFFSET %s' + filters_query
        cursor.execute(query, values)
        data = cursor.fetchall()
        cursor.close()
        return data

    def update_task(self, idx, **kwargs):
        """
            idx: int
            kwargs: Any fields ['title', 'desc', 'due_date', 'priority', 'status']
        """
        if not kwargs:
            return
        
        cursor = self.cnx.cursor()
        
        fields = ', '.join(f'{k} = %s' for k in kwargs)
        values = list(kwargs.values())

        query = f'UPDATE tasks SET {fields} WHERE id = %s'
        cursor.execute(query, values + [idx])
        self.cnx.commit()
        cursor.close()

    def delete_task(self, idx):
        """
            idx: int = ID to delete

            Returns boolean if successful or not
        """
        cursor = self.cnx.cursor()

        query = 'DELETE FROM tasks WHERE id = %s'
        cursor.execute(query, [idx])
        self.cnx.commit()
        deleted = cursor.rowcount
        cursor.close()
        return deleted != 0

    def __del__(self):
        """
            Close connection to database
        """
        if self.cnx is not None:
            print('Closing database connection...')
            self.cnx.close()
            print('Database closed.')


db = None

def get_db():
    global db
    if db is None:
        db = Database()
    return db

if __name__ == '__main__':
    # For Testing

    db = get_db()
    # db.create_task('title 1', 'desc 1', '2025-08-10', 'Low', 'Pending')
    # for x in db.read_tasks(1, 5):
    #     print(x)

    # print(db.read_task(1))
    # db.update_task(1, title='update title 2')
    # print(db.read_task(1))

    for x in db.read_tasks(1, 100):
        print(x)

    print(db.delete_task(10))

    for x in db.read_tasks(1, 100):
        print(x)
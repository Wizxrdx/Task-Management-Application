from src.helper import Helper
from src.task import Task
from src.database import get_db

class TaskManager:
    def __init__(self):
        self.database = None

    def set_db(self, db):
        self.database = get_db()

    def create_task(self):
        task = Task()
        task.set_title(Helper.get_input('Enter title: '))

        # desc
        task.set_description(Helper.get_input('Enter description: '))

        # due_date
        task.set_due_date(Helper.get_input('Enter due date (YYYY-MM-DD): '))

        # priority
        while task._priority_level is None:
            x = Helper.get_input('Enter priority (Low, Medium, High): ')
            task.set_priority(x)

        idx = self.database.create_task(
            task._title,
            task._description,
            task._due_date,
            task._priority_level
        )
        print(f'Task Created with id {idx}')

    def list_tasks(self):
        due_date_sorting = None
        priority_filter = None
        status_filter = None

        while due_date_sorting is None:
            x = self.__get_input('Enter due date sorting (ASC, DESC): ')
            if x in ('ASC', 'DESC'):
                due_date_sorting = x

        x = self.__get_input('Enter priority (Low, Medium, High, None) or press Enter to skip: ')
        if x in ('Low', 'Medium', 'High'):
            priority_filter = x
        elif x in ('None', ''):
            priority_filter = None

        x = self.__get_input('Enter status (Pending, In Progress, Completed, None) or press Enter to skip: ')
        if x in ('Pending', 'In Progress', 'Completed'):
            status_filter = x
        elif x in ('None', ''):
            status_filter = None

        try:
            page_num = int(self.__get_input('Enter page number: '))
            limit = int(self.__get_input('Enter number of tasks per page: '))
        except ValueError:
            print('Invalid number.')
            return

        tasks = self.database.read_tasks(
            page_num=page_num,
            limit=limit,
            due_date=due_date_sorting,
            priority=priority_filter,
            status=status_filter
        )

        for task in tasks:
            print(task)


    def update_task(self):
        pass

    def complete_task(self):
        try:
            task_id = int(self.__get_input('Enter task ID to mark as Completed: '))
        except ValueError:
            print('Invalid ID.')
            return

        self.database.u(task_id)
        print(f'Task {task_id} marked as Completed.')

    def delete_task(self):
        try:
            task_id = int(self.__get_input('Enter task ID to delete: '))
        except ValueError:
            print('Invalid ID.')
            return

        self.database.delete_task(task_id)
        print(f'Task {task_id} deleted.')

task_manager = None

def get_task_manager(db):
    global task_manager
    if task_manager is None:
        task_manager = TaskManager(db)
    return task_manager
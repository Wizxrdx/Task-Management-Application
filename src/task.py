from datetime import datetime


class Task:
    def __init__(self):
        self._title = None
        self._description = None
        self._due_date = None
        self._priority_level = None

        self._id = None
        self._status = None
        self._creation_timestamp = None

    def __str__(self):
        pass

    def title(self, title):
        self._title = title

    def desc(self, desc):
        self._description = desc

    def due_date(self, due_date):
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except:
            return
        self._due_date = due_date

    def priority(self, priority):
        if priority not in ('Low', 'Medium', 'High'):
            return
        self._priority_level = priority


class TaskManager:
    def __init__(self):
        self.database = Database()

    def __get_input(self, message):
        try:
            x = input(message)
            return x
        except KeyboardInterrupt:
            raise

    def create_task(self):
        task = Task()

        # title
        while task._title is None:
            x = self.__get_input('Enter title: ')
            task.title(x)

        # desc
        while task._description is None:
            x = input('Enter description: ')
            task.desc(x)

        # due_date
        while task._due_date is None:
            x = input('Enter due date (YYYY-MM-DD): ')
            task.due_date(x)

        # priority
        while task._priority_level is None:
            x = input('Enter priority (Low, Medium, High): ')
            task.priority(x)

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

        self.database.complete_task(task_id)
        print(f'Task {task_id} marked as Completed.')

    def delete_task(self):
        try:
            task_id = int(self.__get_input('Enter task ID to delete: '))
        except ValueError:
            print('Invalid ID.')
            return

        self.database.delete_task(task_id)
        print(f'Task {task_id} deleted.')

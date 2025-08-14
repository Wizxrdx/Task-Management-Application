from src.enums import Status
from src.helper import get_input
from src.task import Task
from datetime import datetime
from src.validators import (
    parse_description,
    parse_due_date,
    parse_sorting,
    parse_status,
    parse_title,
    parse_priority
)


class TaskManager:
    def __init__(self, db):
        self.database = db

    def create_task(self):
        # title
        title = get_input('Enter title.', parse_title)
        description = get_input('Enter description.', parse_description)
        due_date = get_input('Enter due date (YYYY-MM-DD).', parse_due_date)
        priority = get_input('Enter priority (Low, Medium, High).', parse_priority)

        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority
        )

        print(task)

        idx = self.database.create_task(
            task.title,
            task.description,
            task.due_date,
            task.priority,
        )

        print(f'Task Created with id {idx}')

    def list_tasks(self):
        due_date_sorting = get_input('Enter due date sorting (ASC, DESC)', parse_sorting)
        priority_filter = get_input('Enter priority (Low, Medium, High or Empty)', parse_priority, allow_empty=True)
        status_filter = get_input('Enter status (Pending, In Progress, Completed or Empty)', parse_status, allow_empty=True)
        page_num = get_input('Enter page number', int)
        limit = get_input('Enter number of tasks per page', int)

        tasks = self.database.read_tasks(
            page_num=page_num,
            limit=limit,
            due_date=due_date_sorting,
            priority=priority_filter.value if priority_filter else None,
            status=status_filter.value if status_filter else None
        )

        for task in tasks:
            print(task)

    def update_task(self):
        idx = get_input('Enter task ID to update.', int)
        title = get_input('Enter new title (or press Enter to skip).', parse_title, allow_empty=True)
        description = get_input('Enter new description (or press Enter to skip).', parse_description, allow_empty=True)
        due_date = get_input('Enter new due date (or press Enter to skip).', parse_due_date, allow_empty=True)
        priority = get_input('Enter new priority (or press Enter to skip).', parse_priority, allow_empty=True)

        new_values = {}
        if title:
            new_values['title'] = title
        if description:
            new_values['description'] = description
        if due_date:
            new_values['due_date'] = due_date
        if priority:
            new_values['priority'] = priority

        self.database.update_task(
            idx,
            **{k: v for k, v in new_values.items() if v is not None}
        )

    def complete_task(self):
        task_id = get_input('Enter task ID to update.', int)

        self.database.update_task(task_id, status=Status.COMPLETED)
        print(f'Task {task_id} marked as Completed.')

    def start_task(self):
        task_id = get_input('Enter task ID to start: ', int)

        self.database.update_task(task_id, status=Status.IN_PROGRESS)
        print(f'Task {task_id} marked as In Progress.')

    def delete_task(self):
        task_id = get_input('Enter task ID to delete: ', int)

        self.database.delete_task(task_id)
        print(f'Task {task_id} deleted.')

task_manager = None

def get_task_manager(db):
    global task_manager
    if task_manager is None:
        task_manager = TaskManager(db)
    return task_manager
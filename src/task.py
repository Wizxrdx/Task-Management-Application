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
from todoist_api_python.api import TodoistAPI
from ConfigHandler import ConfigHandler

config = ConfigHandler()


class Values(object):
    pass


class ToDoData(object):
    def __init__(self, todoapikey, projectid):
        self._todoapikey = todoapikey
        self._projectid = projectid
        self.todolist = None

    def _trim_string(self, task, limit, ellipsis):
        try:
            task = task.strip()
            if len(task) > limit:
                return task[: limit - 1].strip() + ellipsis
            return task
        except:
            print("Could not split string")

    def _parse_data(self, tasklist):
        val = Values()
        val.tasks = []
        print("Parsing task data")
        
        for task in tasklist:
            trimmed_task = self._trim_string(task.content, 37, "...")
            val.tasks.append(trimmed_task)

        if len(val.tasks) > 14:
            remaining_tasks = len(val.tasks) - 14
            last_task = "+ %x other tasks..." % remaining_tasks
            del val.tasks[13:]
            val.tasks.append(last_task)

        return val

    def GetTodoList(self):
        print(f"Getting ToDoList for API Key: {self._todoapikey} and project: {self._projectid}")
        
        api = TodoistAPI(self._todoapikey)
        todolist = api.get_tasks(project_id=self._projectid)
        self.todolist = self._parse_data(todolist)

from todoist_api_python.api import TodoistAPI
from ConfigHandler import ConfigHandler
config = ConfigHandler()

class Values(object):
  pass

class ToDoData(object):
    def __init__(self,todoapikey,projectid):
        self._todoapikey = todoapikey
        self._projectid = projectid
        self.todolist = None
    
    def _parse_data(self,tasklist):
        val = Values()
        val.tasks=[]
        #TODO - cut the end of the task if its to long HELLO
        for task in tasklist:
            val.tasks.append(task.content)

        return val

    def GetTodoList(self):
        print("Getting ToDoList")
        api = TodoistAPI(self._todoapikey)
        todolist = api.get_tasks(project_id=self._projectid)
        #print(todolist)

        self.todolist = self._parse_data(todolist)
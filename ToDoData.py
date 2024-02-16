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
    
    def _trim_string(self, task, limit, ellipsis):
        try:        
            task = task.strip()
            if len(task) > limit:
                return task[:limit-1].strip() + ellipsis
            return task
        except:
            print("Could not split string")

    def _parse_data(self,tasklist):
        val = Values()
        val.tasks=[]

        for task in tasklist:
            trimmed_task = self._trim_string(task.content, 30,'...')
            val.tasks.append(trimmed_task)

        return val

    def GetTodoList(self):
        print("Getting ToDoList")
        api = TodoistAPI(self._todoapikey)
        todolist = api.get_tasks(project_id=self._projectid)
        self.todolist = self._parse_data(todolist)
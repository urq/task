from task import Task
# commands
#add - create new task
#done - complete a task
#delete - delete tasks
#modify - change task(s)
#sync (gcal|jira) [down|up] - use this to sync data with external services
#config - use this to set defaults
#alias - use this to create shorthands for new filters
#ids - prints the ids of the filtered tasks
#undo - undo the last action
#redo - redo the last action
#snapshot in time - roll back state to a certain time
#show - show the details of the selected tasks

#t add -> scheduled:today

class Command(object):
    def __init__(self, config, db):
        self.config = config
        self.db = db

    def init(self):
        self.db.initialize_task_db()

    def add(self, **kwargs):
        self.db.save(Task.from_json(**kwargs))

    def mod(self, **kwargs):
        tasks_to_change = []
        for task in self.db.load(kwargs['ids']):
            tasks_to_change.append(task.merge_with(Task(**kwargs)))
        self.db.save(tasks_to_change)

    def show(self, **task_filter):
        tasks = self.db.load()
        ans = []
        if len(task_filter) > 0:
            for task in tasks:
                for key, val in task_filter:
                    if key in task.__dict__ and val == task.__dict__[val]:
                        ans.append(task)
        else:
            ans = tasks
        print '\n'.join(str(t) for t in ans)

    def done(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


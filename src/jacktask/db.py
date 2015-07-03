import pickle
import os.path
import utils

class Database(object):
    def __init__(self, storage_path):
        self.storage_path = os.path.expanduser(storage_path)

    def initialize_task_db(self):
        if not os.path.exists(self.storage_path):
            utils.mkdir_p(os.path.dirname(self.storage_path))
            with open(self.storage_path,'wb') as f:
                pickle.dump([], f)

    def save(self, tasks):
        if not hasattr(tasks, '__iter__'):
            tasks = [tasks]
        with open(self.storage_path,'rb') as f:
            old_tasks = pickle.load(f)
        with open(self.storage_path,'wb') as f:
            pickle.dump(self._merge_tasks(old_tasks, tasks), f)

    def load(self, keys=None):
        with open(self.storage_path, 'rb') as f:
            tasks = pickle.load(f)
        return (task for task in tasks if task.id in keys) if keys else tasks

    def _merge_tasks(self, old_tasks, new_tasks):
        ans = []
        new_task_ids = {task.id for task in new_tasks}
        old_task_ids = {task.id for task in old_tasks}
        to_replace_ids = old_task_ids.intersection(new_task_ids)
        ans.extend(old for old in old_tasks if old.id not in to_replace_ids)
        ans.extend(new_tasks)
        ans.sort(key=lambda x: x.id)
        return ans

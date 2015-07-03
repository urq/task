# task fields
#description
#status
#estimated_time|est
#actual_time|act
#dependencies|depends|deps
#tags
#priority|pri
#due
#recur
#until
#resources

# hidden:
#uuid
#create_time
#done_time
#delete_time
#last_modified_time
import datetime
from enum import Enum
import os.path
import db

Status = Enum('Status', ['pending','completed'])
Priority = Enum('Priority', ['low','medium','high'])

class Task(object):

    def __init__(self, description, id=None, status=Status.pending, time_tracking=None,
            dependencies=None, tags=None, priority=Priority.low, due=None,
            resources=None):
        self.description = description
        self.tags = tags
        self.status = status
        self.id = id
        #self.priority = priority
        #self.dependencies = dependencies
        #self.time_tracking = time_tracking
        #self.due = due
        #self.resources = resources
        #self._uuid =
        #self._create_time =
        #self._done_time = None
        #self._delete_time =
        #self._last_modified_time =

    def __repr__(self):
        return str(self.to_json())

    @classmethod
    def from_json(cls, **kwargs):
        return cls(**kwargs)

    def to_json(self):
        return self.__dict__

    def merge_with(self, task):
        keys = self.__dict__.keys()
        for key, val in task.__dict__:
            if key in keys:
                self.__dict__[key] = val
        return self


#class Calendar(object):

    #def __init__(self, start_time, end_time, recur):
        #self.start_time = start_time
        #self.end_time = end_time
        #self.recur = recur


#class Recurrence(object):

    #def __init__(self, recur, until):
        #self.recur = recur
        #self.until = until

#class TimeTracking(object):

    #def __init__(self, estimated_time, actual_time):
        #pass


#class Resource(object):

    #def __init__(self, link, description=''):
        #self.link = link
        #self.description = description


#class Reminder(object):
    #pass


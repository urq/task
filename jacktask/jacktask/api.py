from jacktask.models import Task,Tag
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

class TaskResource(ModelResource):
    class Meta:
        queryset = Task.objects.all()
        authorization = Authorization()

class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        authorization = Authorization()


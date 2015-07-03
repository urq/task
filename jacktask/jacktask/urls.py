from django.conf.urls import patterns, include, url
from django.contrib import admin
from jacktask.api import TaskResource,TagResource
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(TagResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jacktask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    (r'^api/', include(v1_api.urls)),
)

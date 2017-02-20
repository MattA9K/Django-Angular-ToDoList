# TODO_APP

from django.conf.urls import url
from todo import views


urlpatterns = [
    url(r'^todotagslist/$', views.ToDoTagsList.as_view(), name='todo_tag_list'),
    url(r'^todotag/(?P<name>[\w-]+)/$', views.ToDoTagDetail.as_view(), name='todo_tag_detail'),

    url(r'^todolist/$', views.ToDoList.as_view(), name='todo_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ToDoDetail.as_view(), name='todo_detail'),
]
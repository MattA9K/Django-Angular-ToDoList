# MAIN
from django.conf.urls import url, include
from django.contrib import admin
from todo import views

# Django URLs:
urlpatterns = [

    # REST DOCUMENTATION:
    url(r'^docs/', include('rest_framework_docs.urls')),

    # Django
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),

    # Django-REST
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


    url(r'^todo/', include('todo.urls')),


]




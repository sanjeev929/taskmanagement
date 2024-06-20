from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("registration/",views.registration,name="registration"),
    path("login/",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
    path("createtask/",views.createtask,name="createtask"),
    path("tasks/",views.tasks,name="tasks"),
    path("notifications/",views.notifications,name="notifications")
]

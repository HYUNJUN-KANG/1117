from django.urls import path

from . import views

app_name = 'todos'
urlpatterns = [
    path('', views.todo_create_read, name='todo_cr'),
    path('<int:todo_id>/', views.todo_update_delete, name='todo_ud'),
]
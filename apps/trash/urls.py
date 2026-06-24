from django.urls import path
from . import views

urlpatterns = [
    path('', views.trash_list, name='trash-list'),
    path('auto-remove/', views.auto_remove_oos, name='auto-remove'),
    path('restore/<int:trash_id>/', views.restore_item, name='restore-item'),
]

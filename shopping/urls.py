from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_list, name='shopping-list'),  
    path("add/", views.add_item, name="add-item"),
    path('toggle/<int:item_id>/', views.toggle_item, name='toggle-item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete-item'),
]   

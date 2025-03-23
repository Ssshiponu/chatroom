from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.rooms, name='rooms'),
    path('room/<int:room_id>/', views.room),
    path('room/create/', views.create_room, name='create_room'),
    path('room/edit/<int:room_id>', views.edit_room),
    path('room/del/<int:room_id>', views.del_room)
]
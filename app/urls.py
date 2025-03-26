from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.rooms, name='rooms'),
    path('room/<int:room_id>/', views.room, name='room'),
    path('room/create/', views.create_room, name='create_room'),
    path('room/edit/<int:room_id>', views.edit_room),
    path('room/del/<int:room_id>', views.del_room),
    path('login', views.log_in, name='login'),
    path("logout", views.log_out, name='logout'),
    path("signup", views.sign_up, name="signup"),
    path('msg/del/<int:msg_id>', views.del_msg, name='del_msg'),
]
from django.urls import path
from core import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("register/", views.login_register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("room/<int:pk>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<int:pk>", views.updateRoom, name="update-room"),
    path("delete-room/<int:pk>", views.deleteRoom, name="delete-room"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_page, name="register"),
    
    path('', views.home, name='home'),
    path('create_vault/', views.create_vault, name='create_vault'),
    path('password_vault/', views.passwords_vault, name='password_vault'),
    path('delete-room/<int:pk>/', views.delete_room, name='delete-room'),
    path('update-room/<int:pk>/', views.update_room, name='update-room'),
]
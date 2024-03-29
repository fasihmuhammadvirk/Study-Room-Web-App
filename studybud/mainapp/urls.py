from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('otp_input/<str:email>', views.otp_input, name='otp_input'),
    path('change_password/<str:email>/',
         views.change_password, name='change_password'),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('predict/', views.predict_sgpa_cgpa, name='predict_sgpa_cgpa'),
    
    path('room/<int:pk>/request/', views.request_join_room, name='request_join_room'),
    path('room/<int:pk>/accept/', views.accept_join_requests, name='accept_join_requests'),
]

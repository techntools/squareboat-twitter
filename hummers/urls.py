from django.urls import path

from hummers import views


urlpatterns = [
    path('profile/', views.HummerProfile.as_view()),
    path('<str:username>/profile/', views.HummerProfile.as_view()),
    path(r'<str:username>/follow/', views.Follow.as_view()),
    path(r'<str:username>/unfollow/', views.Unfollow.as_view()),
]

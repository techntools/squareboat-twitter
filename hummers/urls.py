from django.urls import path

from hummers import views


urlpatterns = [
    path('profile/', views.HummerProfile.as_view()),
    path('profile/<str:username>/', views.HummerProfile.as_view()),

    path('follow/<str:username>/', views.Follow.as_view()),
    path('unfollow/<str:username>/', views.Unfollow.as_view()),

    path('tweet/', views.Tweeting.as_view()),
    path('tweet/<int:pk>/', views.Tweeting.as_view()),
    path('tweet/feed/', views.TweetFeed.as_view()),
]

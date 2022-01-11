from django.urls import path

from accounts import views


urlpatterns = [
    path('create/', views.Create.as_view()),
    path('login/', views.Login.as_view()),
    path('renew-token/', views.NewAccessToken.as_view()),
    path('details/', views.Profile.as_view()),
]

from django.urls import path,re_path,include
from . import views
from social_django.urls import urlpatterns as social_django_urls

urlpatterns = [
    path('', views.index,name='index'),
    path('login/', views.login_view,name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('signup/', views.signup_view,name='signup'),
    path('profile/', views.profile_management,name='profile'),
    path('search/', views.search_video,name='search'),
    path('login/facebook/', views.facebook_login, name='facebook_login'),
    path('autocomplete/', views.video_autocomplete, name='video_autocomplete'),
]

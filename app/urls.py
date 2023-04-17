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
    path('autocomplete/', views.video_autocomplete, name='video_autocomplete'),
    path('videoactivity/save/', views.video_activity, name='video_activity'),
    path('about_me/',views.about_me,name='about'),
    path('how_to/',views.how_to,name='howto'),
    path('profit/',views.payment_list,name='profit'),
    path("password_change/", views.password_change, name="password_change"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("reset_password/validate/",views.reset_password_validate,name='reset_password_validate'),
    path("reset_password/confirm/",views.reset_password_confirm,name='reset_password_confirm'),
    path('pdf/', views.MyPDF.as_view(template_name='account/profitpdf.html',
                                             filename='my_pdf.pdf'), name='pdf'),
]

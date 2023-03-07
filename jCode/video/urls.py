from django.contrib import admin
from django.urls import path,re_path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index,name='index'),
    path('detail/<slug:slug>/', views.VideoDetailView.as_view(), name='detail'),
    path("course/", views.management_course, name='management_course'),
    path("chapter/", views.management_chapter, name="management_chapter"),
    path("lesson/", views.management_lesson, name="management_lesson"),
    path('deletevideo/<int:id>', views.video_delete, name='video_delete'),
    path('deletechapter/<int:id>', views.chapter_delete, name='chapter_delete'),
    path('deletelesson/<int:id>', views.lesson_delete, name='lesson_delete'),
    path('updatevideo/<int:id>',views.update_video,name='update_course'),
    path('updatechapter/<int:id>',views.update_chapter,name='update_chapter'),
    path('updatelesson/<int:id>',views.update_lesson,name='update_lesson'),
    path('add/', views.video_add, name='video_add'),
    path('addchapter/', views.video_addchapter, name='video_addchapter'),
    path('addlesson/', views.video_addlesson, name='video_addlesson'),
    path('payment/<slug:slug>/', views.payment, name='payment'),
    path('history/',views.payment_history,name='history'),
    # rating url
    path('rate/<int:video_id>/<int:rating>/', views.rating_video,name='rate'),
]

import random
import jwt
import time
import uuid
import os
from datetime import datetime, timedelta
from pathlib import Path
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView, DetailView
from .models import Video,VideoLesson,VideoChapter,Payment, Rating
from app.models import Category,CategorySub,Member,UserActivity
from .forms import VideoForm,VideochapterForm,VideolessonForm
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.conf import settings
from slugify import slugify
from django.contrib.auth.models import User
import subprocess
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from datetime import timedelta


#------------------------------------------------------
#Video page
#------------------------------------------------------


def index(request):
    video = Video.objects.filter(published=True).order_by('name')
    categ_id = request.GET.get('categoryid')
    subcateg_id = request.GET.get('subcategoryid')
    if categ_id:
        video = video.filter(category_id=categ_id)
    elif subcateg_id:
        video = video.filter(category_sub_id=subcateg_id)
    context = {'video_list':video,}

    return render(request,'video/index.html',context)


#------------------------------------------------------
#Purchase History
#------------------------------------------------------


def payment_history(request):
    member = Member.objects.filter(user_id=request.user.id).first()
    history = Payment.objects.filter(member_id=member.id)
    context={'payment_list':history}
    return render(request,'video/history.html',context)

#------------------------------------------------------
#Detail Course
#------------------------------------------------------


class VideoDetailView(DetailView):
    model = Video
    template_name = 'video/detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(VideoDetailView, self).get_context_data(*args, **kwargs)

        count_obj = 0
        if self.request.user.is_authenticated:
            slug = self.kwargs['slug']
            video = Video.objects.filter(slug=slug).first()
            member = Member.objects.filter(user_id=self.request.user.id).first()
            count_obj = Payment.objects.filter(member_id=member.id, video_id=video.id).count()
        payload = {'user_id': "", 'lesson_id': ""}
        expiration_time = datetime.now() + timedelta(days=15)
        payload['exp'] = int(expiration_time.timestamp())

        key = settings.SECRET_KEY
        encoded_token = jwt.encode(payload, key, algorithm='HS256')
        context['count_payment'] = count_obj
        context['token']= encoded_token
        return context


#------------------------------------------------------
#payment Course
#------------------------------------------------------

@login_required
def payment(request, slug):
    if request.user.is_authenticated:
        video = Video.objects.filter(slug=slug).first()
        member = Member.objects.filter(user_id=request.user.id).first()
        count_obj = Payment.objects.filter(member_id=member.id, video_id=video.id).count()
        if not count_obj:
            p = Payment(video=video,member=member,payment_amount=video.price)
            p.save()
        messages.success(request, 'คุณได้ชำระเงินเรียบร้อยแล้ว')
    return HttpResponseRedirect(reverse('video:detail', args={slug}))


#------------------------------------------------------
#load category_sub by category
#------------------------------------------------------


def load_category_sub(request):
    category_id = request.GET.get('category')
    category_sub = CategorySub.objects.filter(category_id=category_id)
    print(category_sub)
    return render(request, 'video/category_sub_dropdown_list_options.html', {'category_subs': category_sub})


#------------------------------------------------------
#visit Course
#------------------------------------------------------


def visit(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        activity_list = UserActivity.objects.filter(user_id=user_id).order_by('-activity_time')
        rows = []
        for a in activity_list:
            lesson = VideoLesson.objects.filter(id=a.lesson_id).first()
            rows.append({
                'lesson_id': a.lesson_id,
                'lesson': lesson,
                'activity_time': a.activity_time,
                'video_id': lesson.videos.id,
            })
        rows.sort(key=lambda x: (x.get('video_id'), x.get('activity_time')), reverse=True)
    return render(request, 'video/visit.html', {'lesson_list':rows})


#Show Course
@login_required
def management_course(request):
    videos = Video.objects.filter(member__user=request.user.id)
    return render(request,'video/course/course.html',{"video_list":videos})


#Add Course
@login_required
def video_add(request):
    form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST,request.FILES)
        if form.is_valid():
            video = form.save(commit=False)

            # check existing video upload file
            if request.FILES.get('videoexample'):
                BASE_DIR = Path(__file__).resolve().parent.parent
                video_file = request.FILES['videoexample']

                file_name, file_extension = os.path.splitext(video_file.name)
                upload_file_name = '{0}{1}'.format(uuid.uuid1(), file_extension)
                upload_file_media = '/media/video/example/'

                media_path = upload_file_media + '' + upload_file_name
                absolute_path = str(BASE_DIR) + '' + media_path

                with open(absolute_path, 'wb+') as fs_dest:
                    for chunk in video_file.chunks():
                        fs_dest.write(chunk)
                # save media path to video url
                video.videoexample_url = media_path
            video.slug = slugify(video.name)
            video.member = Member.objects.filter(user_id=request.user.id).first()
            video.published = True
            video.save()
            form.save_m2m()
            messages.success(request, 'บันทึกสำเร็จ')
            return HttpResponseRedirect(reverse('video:management_course'))
        messages.error(request, 'บันทึกไม่สำเร็จ!')
    return render(request, 'video/course/add_course.html', {
        'form': form,
    })


#Edit Course
@login_required
def update_video(request, id):
    videos= Video.objects.get(id=id)
    if request.method == 'POST':
        form = VideoForm(request.POST,request.FILES, instance=videos)
        if form.is_valid():
            video = form.save(commit=False)
                        # check existing video upload file
            if request.FILES.get('videoexample'):
                BASE_DIR = Path(__file__).resolve().parent.parent
                video_file = request.FILES['videoexample']

                file_name, file_extension = os.path.splitext(video_file.name)
                upload_file_name = '{0}{1}'.format(uuid.uuid1(), file_extension)
                upload_file_media = '/media/video/example/'

                media_path = upload_file_media + '' + upload_file_name
                absolute_path = str(BASE_DIR) + '' + media_path

                with open(absolute_path, 'wb+') as fs_dest:
                    for chunk in video_file.chunks():
                        fs_dest.write(chunk)
                # save media path to video url
                video.videoexample_url = media_path
            video.save()
            messages.success(request, 'บันทึกสำเร็จ')
            return redirect('video:management_course')
    else:
        form = VideoForm(instance=videos)
    return render(request, 'video/course/update_course.html', {'form': form})


#Delete Course
@login_required
def video_delete(request, id):
    videos = Video.objects.get(id=id)
    videos.delete()
    messages.success(request, 'ลบสำเร็จ')
    return redirect(reverse('video:management_course'))


#------------------------------------------------------
#chapter management
#------------------------------------------------------


#Show Chapter
@login_required
def management_chapter(request):
    courseid=request.GET.get('courseid')
    chapters = VideoChapter.objects.filter(video__id=courseid)
    return render(request,'video/chapter/chapter.html',{"chapters_list":chapters,"courseid":courseid})


#Add Chapter
@login_required
def video_addchapter(request):
    form = VideochapterForm()
    courseid=request.GET.get('courseid')
    if request.method == 'POST':
        form = VideochapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.video_id=courseid
            chapter.save()
            form.save_m2m()
            messages.success(request, 'บันทึกสำเร็จ')
            return HttpResponseRedirect(reverse('video:management_chapter')+'?courseid='+str(courseid))
        messages.error(request, 'บันทึกไม่สำเร็จ!')
    return render(request, 'video/chapter/add_chapter.html', {
        'form': form,
        "courseid":courseid
    })


#Edit Chapter
@login_required
def update_chapter(request, id):
    courseid=request.GET.get('courseid')
    chapters= VideoChapter.objects.get(id=id)
    if request.method == 'POST':
        form = VideochapterForm(request.POST,  instance=chapters)
        if form.is_valid():
            form.save()
            messages.success(request, 'บันทึกสำเร็จ')
            return redirect(reverse('video:management_chapter')+'?courseid='+str(courseid))
    else:
        form = VideochapterForm(instance=chapters)
    return render(request, 'video/chapter/update_chapter.html', {'form': form,'courseid':courseid})


#Delete Chapter
@login_required
def chapter_delete(request, id):
    courseid=request.GET.get('courseid')
    chaptervideo = VideoChapter.objects.get(id=id)
    chaptervideo.delete()
    messages.success(request, 'ลบสำเร็จ')
    return redirect(reverse('video:management_chapter')+'?courseid='+str(courseid))



#------------------------------------------------------
#lesson management
#------------------------------------------------------


#Show Lesson
@login_required
def management_lesson(request):
    courseid=request.GET.get('courseid')
    chapterid=request.GET.get('chapterid')
    lesson = VideoLesson.objects.filter(chapter__id=chapterid)
    return render(request,'video/lesson/lesson.html',{"lesson_list":lesson,"courseid":courseid,"chapterid":chapterid})


#Add Lesson
@login_required
def video_addlesson(request):
    form = VideolessonForm()
    courseid=request.GET.get('courseid')
    chapterid=request.GET.get('chapterid')
    if request.method == 'POST':
        form = VideolessonForm(request.POST)
        if form.is_valid():
            lesson_obj = form.save(commit=False)
                        # check existing video upload file
            if request.FILES.get('lessonvideo'):
                BASE_DIR = Path(__file__).resolve().parent.parent
                video_file = request.FILES['lessonvideo']

                file_name, file_extension = os.path.splitext(video_file.name)
                upload_file_name = '{0}{1}'.format(uuid.uuid1(), file_extension)
                upload_file_media = '/media/video/lesson/video/'

                media_path = upload_file_media + '' + upload_file_name
                absolute_path = str(BASE_DIR) + '' + media_path

                with open(absolute_path, 'wb+') as fs_dest:
                    for chunk in video_file.chunks():
                        fs_dest.write(chunk)
                # save media path to video url
                lesson_obj.video_url = media_path
            lesson_obj.videos_id=courseid
            lesson_obj.chapter_id=chapterid
            lesson_obj.save()
            form.save_m2m()
            messages.success(request, 'บันทึกสำเร็จ')
            return redirect(reverse('video:management_lesson')+'?courseid='+str(courseid)+'&chapterid='+str(chapterid))
        messages.error(request, 'บันทึกไม่สำเร็จ!')
    return render(request, 'video/lesson/add_lesson.html', {
        'form': form,
        'courseid':courseid,
        'chapterid':chapterid,
    })


def format_duration_time(duration, extension):
    """
    Format duration time from seconds to HH:MM:SS format.
    """
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:02d}:{:02d}:{:02d}.{}'.format(hours, minutes, seconds, extension)
#Edit Lesson

@login_required

def update_lesson(request, id):
    courseid=request.GET.get('courseid')
    chapterid=request.GET.get('chapterid')
    lessons= VideoLesson.objects.get(id=id)
    if request.method == 'POST':
        form = VideolessonForm(request.POST,  instance=lessons)
        if form.is_valid():
            lesson_obj = form.save(commit=False)
            if request.FILES.get('lessonvideo'):
                BASE_DIR = Path(__file__).resolve().parent.parent
                video_file = request.FILES['lessonvideo']


                file_name, file_extension = os.path.splitext(video_file.name)


                upload_file_name = '{0}{1}'.format(uuid.uuid1(), file_extension)
                upload_file_media = '/media/video/lesson/video/'

                media_path = upload_file_media + '' + upload_file_name
                absolute_path = str(BASE_DIR) + '' + media_path

                with open(absolute_path, 'wb+') as fs_dest:
                    for chunk in video_file.chunks():
                        fs_dest.write(chunk)

            lesson_obj.videos_id=courseid
            lesson_obj.chapter_id=chapterid
            lesson_obj.save()
            form.save()
            messages.success(request, 'แก้ไขสำเร็จ')
            return redirect(reverse('video:management_lesson')+'?courseid='+str(courseid)+'&chapterid='+str(chapterid))
    else:
        form = VideolessonForm(instance=lessons)
    return render(request, 'video/lesson/update_lesson.html', {
        'form': form,
        'courseid':courseid,
        'chapterid':chapterid,
        })


#Delete Lesson
@login_required
def lesson_delete(request, id):
    courseid=request.GET.get('courseid')
    chapterid=request.GET.get('chapterid')
    lessonvideo = VideoLesson.objects.get(id=id)
    lessonvideo.delete()
    messages.success(request, 'ลบสำเร็จ')
    return redirect(reverse('video:management_lesson')+'?courseid='+str(courseid)+'&chapterid='+str(chapterid))



# Rating video
@login_required
def rating_video(request, video_id, rating):
    # print('********* rating33333 **************')
    # print('request.user.id=', request.user.id)
    video = Video.objects.get(id=video_id)
    Rating.objects.filter(video_id=video.id, user_id=request.user.id).delete()
    user_obj = User.objects.get(id=request.user.id)
    video.rating_set.create(user=user_obj, rating=rating)
    return HttpResponseRedirect(reverse('video:detail', args={video.slug}))

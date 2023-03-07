from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import AbstractUser,User
from video.models import Video,VideoLesson,Member
from .models import Category,CategorySub
from .forms import EmailAuthenticationForm,SignUpForm,ProfileForm
from django.contrib import messages


#Landing page
def index(request):
    video = Video.objects.filter(published=True)
    context = {'video_list':video,}
    return render(request,'index.html',context)


#------------------------------------------------------
#Login with email
#------------------------------------------------------


def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('app:index')
    else:
        form = EmailAuthenticationForm()
    return render(request,'account/login.html',{
            'form':form
        })


#------------------------------------------------------
#Logout
#------------------------------------------------------
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('app:index')


#------------------------------------------------------
#Sign up from email and save member default
#------------------------------------------------------


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            username = email.split('@')[0]
            user.username = username
            user.save()
            member = Member(user=user,user_code=username)
            member.save()
            return redirect('app:login')
    else:
        form = SignUpForm()
    return render(request,'account/signup.html',{
            'form':form
        })

#------------------------------------------------------
#edit profile // Member models
#------------------------------------------------------


def profile_management(request):
    profile=Member.objects.filter(user_id=request.user.id).first()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user.first_name = request.POST.get('firstname')
            user.last_name = request.POST.get('lastname')
            user.save()
            profile = form.save()
            profile.save()
            messages.success(request, 'แก้ไขสำเร็จ')
            return redirect('app:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request,'account/profile.html',{
            'form':form,
            'profile':profile
        })


#------------------------------------------------------
#Search page (default)
#------------------------------------------------------


def search_video(request):
    txt_search = request.POST.get('txtSearch')
    video_list = Video.objects.filter(name__contains=txt_search,published=True)
    return render(request, 'search.html', {'video_list': video_list})


#------------------------------------------------------
#Search autocomplete
#------------------------------------------------------
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q


@require_GET
def video_autocomplete(request):
    query = request.GET.get('qry', '')
    if len(query) < 2:
        return JsonResponse({'results': []})
    results = Video.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).values('id', 'name', 'image','slug')
    return JsonResponse({'results': list(results)})


#------------------------------------------------------
#facebook login (not finish)
#------------------------------------------------------
def facebook_login(request):
    user = request.email
    if user.is_authenticated:
        return redirect('home')
    else:
        login(request, user)
        return redirect('home')

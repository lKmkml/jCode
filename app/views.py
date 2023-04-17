from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import AbstractUser,User
from video.models import Video,VideoLesson,Member,Avg,Payment
from .models import Category,CategorySub,UserActivity
from .forms import EmailAuthenticationForm,SignUpForm,ProfileForm,SetPasswordForm,EmailInputForm
from django.contrib import messages
from datetime import datetime
from django.db.models import Sum
import random
from django.core.mail import EmailMessage
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from social_django.models import UserSocialAuth
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from wkhtmltopdf.views import PDFTemplateView

#Landing page
def index(request):
    video = Video.objects.filter(published=True).annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:4]
    video_new = Video.objects.filter(published=True).order_by('-created')[:4]
    context = {'video_list':video,'videonew_list':video_new}
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
        messages.error(request, 'ไม่ถูกต้อง')
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


# บันทึกกิจกรรมว่า user ดู video อะไรอยู่
def video_activity(request):
    lesson_id = request.GET.get('lesson_id')
    user_id = request.user.id
    if request.user.is_authenticated:
        act_obj = UserActivity.objects.filter(lesson_id=lesson_id,user_id=user_id)
        if act_obj:
            # update
            # act_obj = UserActivity.objects.filter(lesson_id=lesson_id,user_id=user_id).first()
            # act_obj.activity_time = datetime.now()
            # act_obj.save()
            act_obj.update(activity_time=datetime.now())
        else:
            # insert
            act_obj = UserActivity()
            act_obj.user_id = user_id
            act_obj.lesson_id = int(lesson_id)
            act_obj.activity_name = "View video lesson {0}".format(lesson_id)
            act_obj.activity_time = datetime.now()
            act_obj.save()
    return JsonResponse({'results': 'success'})


def about_me(request):
    img_num=[]
    for i in range (1,3):
        img_num.append(i)
    return render(request,'about_me.html',{'img':img_num})

def how_to(request):
    img_num=[]
    for i in range (1,7):
        img_num.append(i)
    return render(request,'how_to.html',{'img':img_num})


def password_change(request):
    if request.user.is_authenticated:
        user = request.user
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('app:login')
        form = SetPasswordForm(user)
        return render(request, 'account/change_password.html', {'form': form})



def reset_password(request):
    form = EmailInputForm()
    return render(request, 'account/reset_password.html', {'form': form})


def reset_password_validate(request):
    email = request.GET.get('email')
    new_password1 = request.GET.get('new_password1')
    new_password2 = request.GET.get('new_password2')


    random_int = random.randint(10000, 99999)
    subject= 'Code reset password'
    body = '''Your generated is <br> {0} '''.format(random_int)
    print(email)
    email_send = EmailMessage(subject=subject,body=body,to=[email])
    email_send.content_subtype = 'html'
    email_send.send()

    print('random_int=', random_int)
    return JsonResponse({'results': 'ok', 'random_int': random_int})

def reset_password_confirm(request):
    print('reset_password_confirm')
    email = request.GET.get('email')
    new_password1 = request.GET.get('new_password1')
    new_password2 = request.GET.get('new_password2')
    print('email=', email)
    print('new_password1=', new_password1)
    print('new_password2=', new_password2)

    user = User.objects.get(email=email)
    user.set_password(new_password1)
    user.save()
    return JsonResponse({'results': 'ok'})

@login_required
def payment_list(request):
    user = request.user
    payment = Payment.objects.filter(video__member__user=user)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        payment = payment.filter(payment_date__range=[start_date, end_date])

    payments = payment.values('video__name') \
                     .annotate(total_payment=Sum('payment_amount'))

    total_payment = payment.aggregate(total=Sum('payment_amount'))['total']
    fee= total_payment * 5 /100
    total_fee = total_payment-fee
    context={'payment': payments,'total_payment': total_payment,'fee':fee,'total_fee':total_fee}
    return render(request, 'account/profit.html', context)


class MyPDF(PDFTemplateView):
    def get_context_data(self, **kwargs):
        context = super(MyPDF, self).get_context_data(**kwargs)
        user = self.request.user
        payment = Payment.objects.filter(video__member__user=user)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            payment = payment.filter(payment_date__range=[start_date, end_date])

        payments = payment.values('video__name') \
                        .annotate(total_payment=Sum('payment_amount'))

        total_payment = payment.aggregate(total=Sum('payment_amount'))['total']
        fee= total_payment * 5 /100
        total_fee = total_payment-fee
        context={'payment': payments,'total_payment': total_payment,'fee':fee,'total_fee':total_fee,'start_date':start_date,'end_date':end_date}
        return context




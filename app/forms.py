from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm

#------------------------------------------------------
#Form การ Login ด้วย Email
#------------------------------------------------------
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


#------------------------------------------------------
#Form การ register ด้วย Email
#------------------------------------------------------
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')


    class Meta:
        model = User
        fields = ( 'email', 'password1', 'password2')


#------------------------------------------------------
#Form การจัดการ Profile
#------------------------------------------------------
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['id','user', 'created', 'updated']
        labels ={
            'user_code':'ชื่อผู้ใช้',
            'description':'รายละเอียด',
            'Profile_image':'รูปโปรไฟล์',
        }


    def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'


# class SetPasswordForm1(SetPasswordForm):
#     class Meta:
#         new_password1 = forms.CharField(
#         label=_('รหัสผ่านใหม่'),
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         strip=False,
#     )

#         new_password2 = forms.CharField(
#         label=_('ยืนยันรหัสผ่านใหม่'),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#     )


class CustomPasswordChangeForm(PasswordChangeForm):

    error_messages = {
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
    }


class EmailInputForm(forms.Form):
    email = forms.EmailField(
    label='อีเมล',
    widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'กรอกอีเมลของคุณ',
        'autocomplete': 'email',
        'required': True,
    }),
    max_length=254,
    )

    new_password1 = forms.CharField(
        label='รหัสผ่านใหม่',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'กรอกรหัสผ่านใหม่',
            'autocomplete': 'new-password',
            'required': True,
            'pattern': '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}',
            'title': 'รหัสผ่านต้องประกอบด้วยอักขระอย่างน้อย 8 ตัว ประกอบด้วยตัวอักษรตัวเล็ก ตัวอักษรตัวใหญ่ และตัวเลข',
        }),
        # help_text='รหัสผ่านต้องประกอบด้วยอักขระอย่างน้อย 8 ตัว ประกอบด้วยตัวอักษรตัวเล็ก ตัวอักษรตัวใหญ่ และตัวเลข <br>'
    )

    new_password2 = forms.CharField(
        label='ยืนยันรหัสผ่านใหม่',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'กรอกรหัสผ่านใหม่อีกครั้ง',
            'autocomplete': 'new-password',
            'required': True,
        }),
    )


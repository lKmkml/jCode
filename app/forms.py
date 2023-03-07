from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member


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

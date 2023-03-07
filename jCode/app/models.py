from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


#------------------------------------------------------
#Model ของ Category
#------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


#------------------------------------------------------
#Model ของ Sub Category
#------------------------------------------------------
class CategorySub(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


#------------------------------------------------------
#Model ของ Profile
#------------------------------------------------------
class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_code = models.CharField(max_length=50)
    Profile_image = models.FileField(upload_to='Profile', null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.user_code

from django.contrib import admin
from .models import Category,CategorySub,Member
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']
    list_filter=['updated']
    search_fields=['name']
class CategorySubAdmin(admin.ModelAdmin):
    list_display=['category','name']
    list_filter=['updated']
    search_fields=['name']


admin.site.register(Category,CategoryAdmin)
admin.site.register(CategorySub,CategorySubAdmin)
admin.site.register(Member)

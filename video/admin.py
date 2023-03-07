from django.contrib import admin
from .models import Video,VideoChapter,VideoLesson,Payment,Rating
# Register your models here.
class VideolessonAdmin(admin.ModelAdmin):
    list_display=['name','updated','is_locked']

class VideoChapterAdmin(admin.ModelAdmin):
   list_display=['name','updated']


class VideoAdmin(admin.ModelAdmin):
    list_display=['name','price','published','category','category_sub']
    list_filter = ['published']
    search_fields =['name']
    prepopulated_fields = {'slug':['name']}

admin.site.register(VideoLesson,VideolessonAdmin)
admin.site.register(VideoChapter,VideoChapterAdmin)
admin.site.register(Video,VideoAdmin)
admin.site.register(Payment)
admin.site.register(Rating)

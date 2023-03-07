from django import forms
from .models import Video,VideoChapter,VideoLesson

#------------------------------------------------------
#ฟอร์มเกี่ยวกับ course
#------------------------------------------------------
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ['id','member', 'slug', 'created', 'updated']
        labels ={
            'name':'ชื่อ',
            'description':'รายละเอียด',
            'image':'ภาพคอร์ส',
            'videoexample':'วิดีโอตัวอย่าง',
            'category':'ประเภทหลัก',
            'category_sub':'ประเภทย่อย',
            'price':'ราคา',
            'price_before':'ราคาเต็ม'
        }



    def __init__(self, *args, **kwargs):
            super(VideoForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'


#------------------------------------------------------
#ฟอร์มเกี่ยวกับ chapter
#------------------------------------------------------
class VideochapterForm(forms.ModelForm):
    class Meta:
        model = VideoChapter
        exclude = ['id','video', 'created', 'updated']
        labels ={
            'name':'ชื่อ',
            'ordered':'ลำดับ'
        }


    def __init__(self, *args, **kwargs):
            super(VideochapterForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'


#------------------------------------------------------
#ฟอร์มเกี่ยวกับ lesson
#------------------------------------------------------
class VideolessonForm(forms.ModelForm):
    class Meta:
        model = VideoLesson
        exclude = ['id','videos','chapter', 'created', 'updated']
        labels ={
            'name':'ชื่อ',
            'duration_time':'ระยะเวลา',
            'lessonvideo':'วิดีโอ',
            'video_url':'ลิงค์วิดีโอ',
            'is_locked':'ดูได้เฉพาะผู้ซื้อคอร์สแล้ว',
            'ordered':'ลำดับ',
        }


    def __init__(self, *args, **kwargs):
        super(VideolessonForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

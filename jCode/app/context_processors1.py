from app.models import Category,CategorySub,Member
from django import template
from django.conf import settings

#------------------------------------------------------
#send category and sub category to all page
#------------------------------------------------------
def category_list(request):
    categories = Category.objects.all()
    category_subs = CategorySub.objects.all().order_by('category')
    ip=settings.VIDEO_SERVER_URL
    context = {
        'category_list':categories,
        'subcategory_list':category_subs,
        'ip':ip
    }
    # Return a dictionary with the data you want to load
    # on every request call or every page.'
    return context


#------------------------------------------------------
#send member on profile management
#------------------------------------------------------
def member_list(request):
    members=Member.objects.filter(user_id=request.user.id).first()
    context={
        'member_list':members
    }
    return context

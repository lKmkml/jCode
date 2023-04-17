from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from social_django.models import UserSocialAuth
from app.models import Member

@receiver(post_save, sender=get_user_model())
def create_member(sender, instance, created, **kwargs):
    if created:
        social_auth = UserSocialAuth.objects.filter(user=instance).first()
        if social_auth and social_auth.provider == 'google':
            Member.objects.create(user=instance, user_code=instance.email.split('@')[0], profile_image=social_auth.extra_data['picture'])
        elif social_auth and social_auth.provider == 'facebook':
            Member.objects.create(user=instance, user_code=instance.email.split('@')[0], profile_image=f"https://graph.facebook.com/{social_auth.uid}/picture?type=large")

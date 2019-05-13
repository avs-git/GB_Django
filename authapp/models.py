from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta


def activation_key_expires():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=256, unique=True)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)
    is_active = models.BooleanField(verbose_name='Аквтивен', default=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=activation_key_expires)

    def is_activation_key_valid(self):
        return now() <= self.activation_key_expires


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'МУЖСКОЙ'),
        (FEMALE, 'ЖЕНСКИЙ'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    locale = models.CharField(verbose_name='Страна/язык', max_length=128, blank=True)
    vk_link = models.URLField(verbose_name='Ссылка на профиль VK', max_length=256, blank=True)
    vk_photo = models.URLField(verbose_name='Ссылка на фото VK', max_length=512, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)
        else:
            instance.shopuserprofile.save()

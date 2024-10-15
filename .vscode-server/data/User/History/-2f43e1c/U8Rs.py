from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=False)  # username 필드
    kakao_oid = models.BigIntegerField(
        null=True, unique=True, blank=False
    )  # 카카오 user_id

    position = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.URLField(max_length=200, blank=True)

    is_staff = models.BooleanField(default=False)  # 슈퍼유저 권한
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # 계정 활성화 상태
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

class Event(models.Model):
    event_title = models.CharField(max_length=200)
    event_image_url = models.URLField(max_length=200, blank=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=255)
    event_info = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_title


class UserApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.email} applied for {self.event.event_title}"
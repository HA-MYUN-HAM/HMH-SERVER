from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from accounts import managers

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
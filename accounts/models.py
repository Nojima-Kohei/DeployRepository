from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class LyricInformation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # 曲名を保存
    artist = models.CharField(max_length=255, blank=True, null=True)  # アーティスト名を保存
    create_at = models.DateTimeField(auto_now_add=True)
    hiragana_lyrics = models.TextField(default="")  # ひらがな歌詞を保存

class AnnotationInformation(models.Model):
    song = models.ForeignKey(LyricInformation, on_delete=models.CASCADE, related_name='annotations')
    line_number = models.IntegerField()  # 注釈が付けられた行番号
    annotation_data = models.TextField()  # 注釈の内容（HTMLなど）

    def __str__(self):
        return f"Annotation for {self.song.title} on line {self.line_number}"



class UserManager(BaseUserManager): # ☆3

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email!')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    twitter_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # ここはemailのままでOK
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email or self.twitter_id or self.username

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Lyric(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    hiragana_lyrics = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class Annotation(models.Model):
    lyric = models.ForeignKey(Lyric, on_delete=models.CASCADE, related_name='annotations')
    text = models.TextField(null=True, blank=True)  # 必須でない場合
    color = models.CharField(max_length=7, null=True, blank=True)  # 必須でない場合（例: #FF0000）
    image_path = models.CharField(max_length=255, null=True, blank=True)  # 画像パス（オプション）
    position = models.CharField(max_length=255, null=True, blank=True)  # 文字の位置や行番号など（オプション）
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.text} ({self.lyric.title})"

    
# class Annotation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # 注釈を追加したユーザー
#     line = models.IntegerField()  # 注釈が追加された行番号
#     type = models.CharField(max_length=100)  # 注釈の種類
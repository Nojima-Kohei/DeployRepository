from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Annotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 注釈を追加したユーザー
    line = models.IntegerField()  # 注釈が追加された行番号
    type = models.CharField(max_length=100)  # 注釈の種類
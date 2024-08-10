from django.db import models
from django.contrib.auth.models import User

class SongInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # 曲のタイトル
    create_at = models.DateTimeField(auto_now_add=True)

class AnnotationInformation(models.Model):
    song = models.ForeignKey(SongInformation, on_delete=models.CASCADE, related_name='annotations')
    line_number = models.IntegerField()  # 注釈が付けられた行番号
    annotation_data = models.TextField()  # 注釈の内容（HTMLなど）

    def __str__(self):
        return f"Annotation for {self.song.title} on line {self.line_number}"

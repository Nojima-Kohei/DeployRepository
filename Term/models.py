from django.db import models  # Djangoのモデルクラスをインポートします。
from markdownx.models import MarkdownxField  # MarkdownxFieldをインポートします。

# Termモデルを定義します。
class Term(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="用語名")  # 用語名を保存するフィールドです。名前は100文字以内で、ユニークでなければなりません。
    description = MarkdownxField(verbose_name="説明")  # MarkdownxFieldを使用して説明を保存します。
    order = models.PositiveIntegerField(default=0, verbose_name="表示順")  # 並び順を管理するフィールド

    # メタクラスを使用してカスタム権限を定義します。
    class Meta:
        ordering = ['order']  # orderフィールドで並べ替え
        permissions = [
            ("can_edit_glossary", "Can edit glossary terms"),  # 管理者が用語集を編集できる権限を追加します。
        ]

    # オブジェクトを文字列として表示するときの名前を返します。
    def __str__(self):
        return self.name  # 用語名を返します。

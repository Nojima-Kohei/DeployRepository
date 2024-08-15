from django import forms  # Djangoのフォームクラスをインポートします。
from .models import Term  # Termモデルをインポートします。

# Termモデル用のフォームクラスを定義します。
class TermForm(forms.ModelForm):
    class Meta:
        model = Term  # このフォームが対応するモデルはTermです。
        fields = ['name', 'description']  # フォームに表示するフィールドを指定します。

from django.contrib import admin  # Djangoの管理画面機能をインポートします。
from markdownx.admin import MarkdownxModelAdmin  # MarkdownxModelAdminをインポートします。
from .models import Term  # Termモデルをインポートします。
from adminsortable2.admin import SortableAdminMixin

# Termモデルを管理画面に登録します。
@admin.register(Term)
class TermAdmin(SortableAdminMixin, MarkdownxModelAdmin):
    list_display = ('name', 'order')  # 管理画面で表示するフィールドを指定
    ordering = ('order',)  # orderフィールドで並び替え

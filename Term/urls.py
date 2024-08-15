from django.urls import path  # DjangoのURLパターンを定義する関数をインポートします。
from . import views  # views.pyファイルをインポートします。

app_name = 'Term'  # 名前空間を設定

# TermアプリのURLパターンを定義します。
urlpatterns = [
    path('', views.term_list, name='term_list'),  # これにより、/term/ でterm_listビューが呼び出されます
    path('terms/', views.term_list, name='term_list'),  # 用語集リストページへのURLパターン
    path('terms/add/', views.add_term, name='add_term'),  # 用語追加ページへのURLパターン
    path('terms/edit/<int:term_id>/', views.edit_term, name='edit_term'),  # 用語編集ページへのURLパターン
]
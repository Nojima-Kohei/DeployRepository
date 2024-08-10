from django.urls import path
from . import views

urlpatterns = [
    path('convert/', views.lyrics_convert, name='lyrics_convert'),  # 歌詞をひらがなに変換するビュー
    path('input/', views.lyrics_input, name='lyrics_input'),  # 歌詞入力ページを表示するビュー
    path('annotate/', views.lyrics_annotate, name='lyrics_annotate'),  # 歌詞注釈ページを表示するビュー
    path('save_hiragana/', views.save_hiragana, name='save_hiragana'),  # 新しいURLパターンを追加
    path('get_annotations/', views.get_annotations, name='get_annotations'),  # 注釈データを取得するビュー
    path('save_annotations/', views.save_annotations, name='save_annotations'),  # 注釈データを保存するビュー
    path('input_return/', views.lyrics_input_return, name='lyrics_input_return'),
]

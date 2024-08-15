from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse  # JSON形式のレスポンスを返すためのクラスをインポート
from .models import LyricInformation, AnnotationInformation  # クラス名を変更
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomSignupForm

import json  # JSONデータを扱うためのモジュールをインポート

# ユーザー登録ビュー
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # カスタムバックエンドを指定してログイン
            login(request, user, backend='accounts.authentication.EmailBackend')
            return redirect('/accounts/mypage/')  # ログイン後にリダイレクトするビューを指定
    else:
        form = CustomSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

# ログインビュー
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mypage')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# マイページのビュー
@login_required
def mypage(request):
    songs = LyricInformation.objects.filter(user=request.user)  # ユーザーに関連付けられた歌詞カードを取得
    print(songs)  # デバッグ用にクエリセットを出力
    return render(request, 'accounts/mypage.html', {'songs': songs})  # テンプレートにデータを渡す


@login_required  # ログインしているユーザーのみアクセスを許可する
def save_annotations(request):
    if request.method == 'POST':  # リクエストがPOSTか確認
        lyric_id = request.POST.get('lyric_id')  # POSTデータから曲IDを取得
        title = request.POST.get('title')  # 曲名を取得
        artist = request.POST.get('artist')  # アーティスト名を取得        
        annotations = request.POST.get('annotations')  # POSTデータから注釈を取得
        hiragana_lyrics = request.POST.get('hiragana_lyrics')  # POSTデータからひらがな歌詞を取得

        lyric = get_object_or_404(LyricInformation, id=lyric_id, user=request.user)  # 指定された曲情報を取得（ユーザーと一致するか確認）
        lyric.title = title  # 曲名を更新
        lyric.artist = artist  # アーティスト名を更新        
        lyric.hiragana_lyrics = hiragana_lyrics  # ひらがな歌詞を曲情報に保存
        lyric.save()  # データベースに保存

        annotations_data = json.loads(annotations)  # 注釈データをJSONからオブジェクトに変換
        AnnotationInformation.objects.filter(lyric=lyric).delete()  # 古い注釈データを削除

        for annotation in annotations_data:  # 注釈データを1つずつ処理
            line_number = annotation.get('line')  # 注釈の行番号を取得
            annotation_data = annotation.get('data')  # 注釈の内容を取得
            AnnotationInformation.objects.create(
                lyric=lyric,  # 関連する曲情報を設定
                line_number=line_number,  # 行番号を設定
                annotation_data=annotation_data  # 注釈内容を設定
            )

        return redirect('accounts:mypage')  # 保存後、マイページにリダイレクト
    return JsonResponse({'status': 'error'}, status=400)  # POSTリクエストでなければエラーレスポンスを返す


# 注釈の表示ビュー
@login_required
def view_annotations(request, lyric_id):
    song = get_object_or_404(LyricInformation, id=lyric_id, user=request.user)  # クラス名を変更
    annotations = song.annotations.all().order_by('line_number')
    return render(request, 'lyrics/view_annotations.html', {'song': song, 'annotations': annotations})

# 曲の削除ビュー（オプション）
@login_required
def delete_song(request, lyric_id):
    song = get_object_or_404(LyricInformation, id=lyric_id, user=request.user)  # クラス名を変更
    if request.method == 'POST':
        song.delete()
        return redirect('mypage')
    return render(request, 'accounts/confirm_delete.html', {'song': song})

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/mypage.html'
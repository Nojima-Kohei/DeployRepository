from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import SongInformation, AnnotationInformation  # クラス名を変更

# ユーザー登録のビュー
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lyrics_input')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# マイページのビュー
@login_required
def mypage(request):
    songs = SongInformation.objects.filter(user=request.user)  # クラス名を変更
    return render(request, 'accounts/mypage.html', {'songs': songs})

# 注釈の保存ビュー
@login_required
def save_annotations(request):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        annotations = request.POST.get('annotations')

        song = get_object_or_404(SongInformation, id=song_id, user=request.user)  # クラス名を変更
        lines = annotations.splitlines()

        for line_number, line in enumerate(lines, start=1):
            AnnotationInformation.objects.create(  # クラス名を変更
                song=song,
                line_number=line_number,
                annotation_data=line
            )

        return redirect('mypage')

# 注釈の表示ビュー
@login_required
def view_annotations(request, song_id):
    song = get_object_or_404(SongInformation, id=song_id, user=request.user)  # クラス名を変更
    annotations = song.annotations.all().order_by('line_number')
    return render(request, 'lyrics/view_annotations.html', {'song': song, 'annotations': annotations})

# 曲の削除ビュー（オプション）
@login_required
def delete_song(request, song_id):
    song = get_object_or_404(SongInformation, id=song_id, user=request.user)  # クラス名を変更
    if request.method == 'POST':
        song.delete()
        return redirect('mypage')
    return render(request, 'accounts/confirm_delete.html', {'song': song})

from django.shortcuts import render, get_object_or_404, redirect  # 必要なショートカット関数をインポートします。
from django.urls import reverse  # reverse関数をインポート
from django.contrib.auth.decorators import login_required, permission_required  # ログインと権限を確認するデコレーターをインポートします。
from .models import Term  # Termモデルをインポートします。
from .forms import TermForm  # Termフォームをインポートします。

# 用語のリストを表示するビューを定義します。
@login_required  # このビューにはログインが必要です。
def term_list(request):
    terms = Term.objects.all().order_by('order')  # 'order'フィールドで並べ替え  # すべての用語をデータベースから取得します。
    return render(request, 'Term/term_list.html', {'terms': terms})  # 用語リストをテンプレートに渡してレンダリングします。

# 用語を編集するビューを定義します。このビューにはログインと特定の権限が必要です。
@login_required  # このビューにはログインが必要です。
@permission_required('Term.can_edit_glossary', raise_exception=True)  # このビューにはcan_edit_glossary権限が必要です。
def edit_term(request, term_id):
    term = get_object_or_404(Term, id=term_id)  # 指定されたIDの用語を取得します。見つからない場合は404エラーを返します。
    if request.method == 'POST':  # フォームが送信された場合の処理です。
        form = TermForm(request.POST, instance=term)  # POSTデータとともにフォームをインスタンス化します。
        if form.is_valid():  # フォームが有効かどうかを確認します。
            saved_term = form.save(commit=False)  # フォームの内容を保存しますが、まだコミットしません。
            saved_term.save()  # 変換後のデータを保存します。
            return redirect(reverse('Term:term_list'))  # 名前空間を含めてURLを指定してリダイレクトします。
    else:  # フォームが送信されていない場合の処理です。
        form = TermForm(instance=term)  # 用語のデータでフォームをインスタンス化します。
    return render(request, 'Term/edit_term.html', {'form': form})  # フォームをテンプレートに渡してレンダリングします。

# 新しい用語を追加するビューを定義します。このビューにはログインと特定の権限が必要です。
@login_required  # このビューにはログインが必要です。
@permission_required('Term.can_edit_glossary', raise_exception=True)  # このビューにはcan_edit_glossary権限が必要です。
def add_term(request):
    if request.method == 'POST':  # フォームが送信された場合の処理です。
        form = TermForm(request.POST)  # POSTデータとともにフォームをインスタンス化します。
        if form.is_valid():  # フォームが有効かどうかを確認します。
            new_term = form.save(commit=False)  # フォームの内容を保存しますが、まだコミットしません。
            new_term.save()  # 変換後のデータを保存します。
            return redirect(reverse('Term:term_list'))  # 名前空間を含めてURLを指定してリダイレクトします。
    else:  # フォームが送信されていない場合の処理です。
        form = TermForm()  # 空のフォームをインスタンス化します。
    return render(request, 'Term/add_term.html', {'form': form})  # フォームをテンプレートに渡してレンダリングします。

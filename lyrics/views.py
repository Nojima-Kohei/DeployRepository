import os  # OS関連の機能を使用するためのモジュールをインポート
import json  # JSONデータを扱うためのモジュールをインポート
from django.http import JsonResponse  # JSON形式のレスポンスを返すためのクラスをインポート
from django.conf import settings  # Djangoの設定を取得するためのモジュールをインポート
from django.shortcuts import render, redirect  # テンプレートをレンダリングするための関数をインポート
from accounts.models import SongInformation, AnnotationInformation
from django.shortcuts import get_object_or_404, redirect
import MeCab  # MeCabモジュールをインポート
import ipadic  # ipadic

# 歌詞をひらがなに変換する関数
def convert_to_hiragana(text):
    mecab = MeCab.Tagger(ipadic.MECAB_ARGS)  # MeCabのTaggerを初期化（ipadicの設定を使用）
    mecab.parse('')  # これを呼び出さないと、文字化けする可能性があります
    node = mecab.parseToNode(text)  # テキストを形態素解析
    result = []

    while node:  # 形態素解析の結果を順に処理
        try:
            if node.feature.split(',')[0] != 'BOS/EOS':  # 形態素が文の先頭・末尾でない場合
                reading = node.feature.split(',')[7]  # 読みを取得
                if reading == '*':  # 読みが存在しない場合
                    reading = node.surface  # 表層形を使用
                # カタカナをひらがなに変換
                reading = reading.replace('ァ','ぁ').replace('ィ','ぃ').replace('ゥ','ぅ').replace('ェ','ぇ').replace('ォ','ぉ')
                reading = reading.replace('ッ','っ').replace('ャ','ゃ').replace('ュ','ゅ').replace('ョ','ょ')
                reading = reading.replace('ア','あ').replace('イ','い').replace('ウ','う').replace('エ','え').replace('オ','お')
                reading = reading.replace('カ','か').replace('キ','き').replace('ク','く').replace('ケ','け').replace('コ','こ')
                reading = reading.replace('サ','さ').replace('シ','し').replace('ス','す').replace('セ','せ').replace('ソ','そ')
                reading = reading.replace('タ','た').replace('チ','ち').replace('ツ','つ').replace('テ','て').replace('ト','と')
                reading = reading.replace('ナ','な').replace('ニ','に').replace('ヌ','ぬ').replace('ネ','ね').replace('ノ','の')
                reading = reading.replace('ハ','は').replace('ヒ','ひ').replace('フ','ふ').replace('ヘ','へ').replace('ホ','ほ')
                reading = reading.replace('マ','ま').replace('ミ','み').replace('ム','む').replace('メ','め').replace('モ','も')
                reading = reading.replace('ヤ','や').replace('ユ','ゆ').replace('ヨ','よ')
                reading = reading.replace('ラ','ら').replace('リ','り').replace('ル','る').replace('レ','れ').replace('ロ','ろ')
                reading = reading.replace('ワ','わ').replace('ヲ','を').replace('ン','ん')
                reading = reading.replace('ガ','が').replace('ギ','ぎ').replace('グ','ぐ').replace('ゲ','げ').replace('ゴ','ご')
                reading = reading.replace('ザ','ざ').replace('ジ','じ').replace('ズ','ず').replace('ゼ','ぜ').replace('ゾ','ぞ')
                reading = reading.replace('ダ','だ').replace('ヂ','ぢ').replace('ヅ','づ').replace('デ','で').replace('ド','ど')
                reading = reading.replace('バ','ば').replace('ビ','び').replace('ブ','ぶ').replace('ベ','べ').replace('ボ','ぼ')
                reading = reading.replace('パ','ぱ').replace('ピ','ぴ').replace('プ','ぷ').replace('ペ','ぺ').replace('ポ','ぽ')
                result.append(reading)  # 変換結果をリストに追加
        except IndexError:  # インデックスエラーが発生した場合
            result.append(node.surface)  # 表層形を使用
        node = node.next
    
    return ''.join(result)  # 結果リストを結合して返す

# 歌詞をひらがなに変換するビュー
def lyrics_convert(request):
    if request.method == 'POST':  # POSTリクエストかどうかをチェック
        lyrics_text = request.POST.get('lyrics', '')  # POSTリクエストから歌詞を取得
        hiragana_text = request.POST.get('hiragana', '')  # 手動修正されたひらがな文章を取得
        if not hiragana_text:  # ひらがな文章がない場合は変換
            hiragana_text = convert_to_hiragana(lyrics_text)
        
        # 変換結果をセッションに保存(改行と半角スペース、全角スペースをエスケープ)
        request.session['hiragana'] = hiragana_text.replace('\n', '<br>').replace(' ', '&nbsp;').replace('　', '&nbsp;')
        request.session['lyrics'] = lyrics_text.replace('\n', '<br>').replace(' ', '&nbsp;').replace('　', '&nbsp;')
        return render(request, 'lyrics/lyrics_input.html', {'lyrics': lyrics_text, 'hiragana': hiragana_text})
    return render(request, 'lyrics/lyrics_input.html')

# 手動修正されたひらがなをセッションに保存するビュー
def save_hiragana(request):
    if request.method == 'POST':
        hiragana = request.POST.get('hiragana', '')
        lyrics = request.POST.get('lyrics', '')
        hiragana = hiragana.replace('<br>', '\n').replace('&nbsp;', ' ').replace('&nbsp;', '　')  # ここで <br> を \n に戻す
        request.session['hiragana'] = hiragana.replace('\n', '<br>').replace(' ', '&nbsp;').replace('　', '&nbsp;')
        request.session['lyrics'] = lyrics.replace('\n', '<br>').replace(' ', '&nbsp;').replace('　', '&nbsp;')
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


# 歌詞入力ページを表示するビュー
def lyrics_input(request):
    lyrics = request.session.get('lyrics', '')  # セッションから元の歌詞を取得
    hiragana = request.session.get('hiragana', '')  # セッションからひらがなを取得
    return render(request, 'lyrics/lyrics_input.html', {'lyrics': lyrics, 'hiragana': hiragana})  # テンプレートにデータを渡してレンダリング

# 歌詞注釈ページを表示するビュー
def lyrics_annotate(request):
    hiragana = request.session.get('hiragana', '').replace('\n', '<br>').replace(' ', '&nbsp;').replace('　', '&nbsp;')  # セッションからひらがな変換結果を取得し、改行やタグに変換
    annotations = request.session.get('annotations', '[]')  # セッションから注釈データを取得
    return render(request, 'lyrics/lyrics_annotate.html', {'hiragana': hiragana, 'annotations': annotations})

# 歌詞入力ページに戻るビュー
def lyrics_input_return(request):
    lyrics_text = request.session.get('lyrics', '').replace('<br>', '\n').replace('&nbsp;', ' ')  # セッションから歌詞を取得して改行と空白を元に戻す
    hiragana_text = request.session.get('hiragana', '').replace('<br>', '\n').replace('&nbsp;', ' ')  # セッションからひらがなを取得して改行と空白を元に戻す
    return render(request, 'lyrics/lyrics_input.html', {'lyrics': lyrics_text, 'hiragana': hiragana_text})  # テンプレートをレンダリングして返す

# 注釈データを取得するビュー
def get_annotations(request):
    annotations = [  # ダミーの注釈データを作成
        {"id": 1, "line": 1, "type": "ビブラート"},
        {"id": 2, "line": 2, "type": "スタッカート"},
    ]
    return JsonResponse({"annotations": annotations}, safe=False)  # 注釈データをJSON形式で返す

def save_annotations(request):
    if request.method == 'POST':
        annotations = request.POST.get('annotations', '[]')
        request.session['annotations'] = annotations

        lyric_id = request.POST.get('lyric_id')
        if not lyric_id:
            return JsonResponse({'status': 'error', 'message': 'Lyric ID is missing'}, status=400)

        lyric = get_object_or_404(SongInformation, id=lyric_id)

        annotations_data = json.loads(annotations)
        for annotation in annotations_data:
            line_number = annotation.get('line')
            annotation_type = annotation.get('type')
            AnnotationInformation.objects.create(
                lyric=lyric,
                user=request.user,
                line_number=line_number,
                annotation_data=annotation_type
            )

        return redirect('lyrics_annotate')
    return JsonResponse({'status': 'error'}, status=400)
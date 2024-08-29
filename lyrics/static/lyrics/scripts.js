// DOMが完全にロードされた後にスクリプトを実行するためのイベントリスナーを追加
document.addEventListener("DOMContentLoaded", function() {
    // DOMが完全にロードされたことをログに出力
    console.log("DOM fully loaded and parsed");

    // 「前回の続きから始める」ボタンの参照を取得
    const continueButton = document.getElementById("continue-button");
    if (continueButton) {
        // ボタンがクリックされたときの処理を定義
        continueButton.onclick = function() {
            // クリック時に `lyrics_annotate.html` へ遷移
            window.location.href = "/lyrics/annotate/";
        };
    }

    // ローカルストレージから注釈データを復元
    const savedAnnotations = localStorage.getItem("annotationsData");
    if (savedAnnotations && window.location.pathname === "/lyrics/annotate/") {

        // annotated-lyrics の内容をクリア
        document.getElementById('annotated-lyrics').innerHTML = '';

        const annotationsData = JSON.parse(savedAnnotations);
        document.getElementById("lyric_id").value = annotationsData.lyric_id; // 歌詞IDを復元
        document.getElementById("title").value = annotationsData.title; // 曲名を復元
        document.getElementById("artist").value = annotationsData.artist; // アーティスト名を復元
        // 保存された注釈を反映
        document.getElementById('annotated-lyrics').innerHTML = annotationsData.fullText; // 全文を反映

        console.log("Annotations restored from local storage");
    }

    // 保存ボタンの参照を取得
    const saveButton = document.getElementById("save-button");
    // 保存ボタンが存在するか確認
    if (saveButton) {
        // 保存ボタンがクリックされたときの処理を定義
        saveButton.onclick = function(event) {
            // デフォルトの動作を防ぐ（フォームの送信を防止）
            event.preventDefault();
            // ボタンがクリックされたことをログに出力
            console.log("Save button clicked");

            // annotated-lyrics の全文を取得して保存
            const fullText = document.getElementById('annotated-lyrics').innerHTML;

            // ローカルストレージに注釈データを保存
            const annotationsData = {
                lyric_id: document.getElementById("lyric_id").value || '', // 歌詞IDを取得（空の場合は空文字列を使用）
                title: document.getElementById("title").value, // 曲名を取得
                artist: document.getElementById("artist").value, // アーティスト名を取得
                fullText: fullText, // annotated-lyrics の全文を保存
            };
            // 注釈データをJSON形式に変換してローカルストレージに保存
            localStorage.setItem("annotationsData", JSON.stringify(annotationsData));

            // 保存成功をログに出力
            console.log("Annotations saved to local storage");
        };
    } else {
        // 保存ボタンが見つからない場合、エラーメッセージをログに出力
        console.error("Save button not found.");
    }
    
    // ファイルに保存する機能
    const saveToFileButton = document.getElementById("save-to-file-button");
    if (saveToFileButton) {
        saveToFileButton.onclick = function() {
            // 曲名とアーティスト名を取得し、未入力の場合は "Unknown" を設定
            const titleField = document.getElementById("title");
            const artistField = document.getElementById("artist");

            const title = titleField ? (titleField.value || 'Unknown') : 'Unknown';
            const artist = artistField ? (artistField.value || 'Unknown') : 'Unknown';
            
            // 日時を取得してファイル名に追加するためにフォーマット
            const now = new Date();
            const formattedDate = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}-${String(now.getMinutes()).padStart(2, '0')}-${String(now.getSeconds()).padStart(2, '0')}`;
            
            // 完全なファイル名を生成
            const fileName = `${title}-${artist}-歌詞カード進捗-${formattedDate}.json`;
            
            // 編集状態を保存するためのデータを収集
            const annotationsData = {
                lyric_id: document.getElementById("lyric_id").value || '',
                title: title,
                artist: artist,
                fullText: document.getElementById('annotated-lyrics').innerHTML
            };

            // データをJSON形式に変換し、Blobを作成
            const json = JSON.stringify(annotationsData, null, 2);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            // ダウンロード用リンクを作成してクリック
            const a = document.createElement('a');
            a.href = url;
            a.download = fileName; // 自動生成したファイル名を設定
            a.click();

            // オブジェクトURLを解放
            URL.revokeObjectURL(url);
        };
    }
    
        // 新しい機能：ファイルから復元する機能
        const loadFromFileButton = document.getElementById("load-from-file-button");
        if (loadFromFileButton) {
            loadFromFileButton.addEventListener('change', function(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        try {
                            const annotationsData = JSON.parse(e.target.result);
                            document.getElementById("lyric_id").value = annotationsData.lyric_id;
                            document.getElementById("title").value = annotationsData.title;
                            document.getElementById("artist").value = annotationsData.artist;
                            document.getElementById('annotated-lyrics').innerHTML = annotationsData.fullText;
                        } catch (error) {
                            console.error("Error loading annotations:", error);
                        }
                    };
                    reader.readAsText(file);
                }
            });
        }
    
    
    
    
// PDF保存ボタンのクリックイベント
document.addEventListener("DOMContentLoaded", function() {
    const exportPdfButton = document.getElementById("export-pdf-button");
    if (exportPdfButton) {
        exportPdfButton.onclick = function() {
            // annotated-lyrics の全文を取得して保存
            const fullText = document.getElementById('annotated-lyrics').innerHTML;

            // JSON形式で必要なデータを作成
            const annotationsData = {
                title: document.getElementById("title").value, // 曲名を取得
                artist: document.getElementById("artist").value, // アーティスト名を取得
                fullText: fullText, // annotated-lyrics の全文を保存
            };

            // フォームを作成してデータを送信
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = "/lyrics/generate_pdf/";

            // CSRFトークンの追加
            const csrfToken = document.createElement('input');
            csrfToken.type = 'hidden';
            csrfToken.name = 'csrfmiddlewaretoken';
            csrfToken.value = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            form.appendChild(csrfToken);

            // annotationsData をJSON文字列にして送信
            const annotationsInput = document.createElement('input');
            annotationsInput.type = 'hidden';
            annotationsInput.name = 'annotations_data';
            annotationsInput.value = JSON.stringify(annotationsData); // JSON形式で送信
            form.appendChild(annotationsInput);

            document.body.appendChild(form);
            form.submit();
        };
    }
});


    // 全てリセットボタンの機能を実装
    const resetButton = document.getElementById("reset-button");
    if (resetButton) {
        resetButton.onclick = function() {
            localStorage.removeItem("annotationsData"); // ローカルストレージの注釈データを削除
            document.getElementById('annotated-lyrics').innerHTML = ''; // 表示されている注釈をクリア
            console.log("Annotations reset");
        };
    }
    


    // 注釈データを取得する関数
    function getAnnotations() {
        // 注釈を格納する配列を定義
        const annotations = [];
        // 注釈がついた歌詞内のすべての<span>および<img>要素を取得
        const annotatedElements = document.querySelectorAll('#annotated-lyrics span, #annotated-lyrics img');
        // 注釈要素が存在するか確認
        if (annotatedElements.length > 0) {
            // 各注釈要素をループ処理
            annotatedElements.forEach(element => {
                // 注釈データをオブジェクトにまとめる
                const annotation = {
                    text: element.textContent || '', // 注釈のテキストを取得
                    color: element.style.backgroundColor || '', // 注釈の背景色を取得
                    tagName: element.tagName.toLowerCase(), // 要素のタグ名を取得
                    src: element.tagName.toLowerCase() === 'img' ? element.src : '', // 画像の場合、画像パスを取得
                    className: element.className || '' // クラス名を取得
                };
                // 注釈配列に追加
                annotations.push(annotation);
            });
        } else {
            // 注釈要素が見つからない場合、警告をログに出力
            console.warn("No annotations found in the lyrics.");
        }
        // 注釈配列を返す
        return annotations;
    }

    // CSRFトークンを取得する関数
    function getCookie(name) {
        let cookieValue = null;
        // クッキーが存在するか確認
        if (document.cookie && document.cookie !== '') {
            // クッキーを分割して配列に変換
            const cookies = document.cookie.split(';');
            // 各クッキーをループ処理
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // 指定されたクッキー名が一致するか確認
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    // クッキーの値をデコードして変数に設定
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;  // クッキーが見つかったらループを終了
                }
            }
        }
        // クッキーの値を返す
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');
    
    // 以下は他のイベントリスナーやDOM操作のコードです

    // annotated-lyrics要素とコンテキストメニューの要素を取得
    const annotatedLyricsDiv = document.getElementById('annotated-lyrics');
    const contextMenu = document.getElementById('context-menu');

    // annotated-lyrics要素が存在する場合、以下のマウスアップ時に選択範囲を更新するイベントリスナーを追加
    if (annotatedLyricsDiv) {
        annotatedLyricsDiv.addEventListener('mouseup', function(event) {
            // マウスアップ時に選択範囲を取得して保存
            const selection = window.getSelection();
            if (!selection.isCollapsed) {
                selectedRange = selection.getRangeAt(0);
            }
        });

        annotatedLyricsDiv.addEventListener('contextmenu', function(event) {
            // 右クリックメニューをカスタマイズ
            event.preventDefault();
            const selection = window.getSelection();
            if (!selection.isCollapsed) {
                selectedRange = selection.getRangeAt(0);
                showContextMenu(event.pageX, event.pageY);
            }
        });
    }

    // contextMenu要素が存在する場合、以下のイベントリスナーを追加
    if (contextMenu) {
        contextMenu.addEventListener('click', function(event) {
            // コンテキストメニューから注釈を追加する処理
            const selectedButton = event.target;
            const imagePath = selectedButton.getAttribute('data-image-path');
            if (imagePath) {
                addAnnotation(imagePath);
            }
        });
    }

    let selectedRange = null;  // 選択範囲を格納する変数
    let undoStack = [];  // 元に戻すためのスタック
    let redoStack = [];  // やり直すためのスタック

    // 現在の状態を保存する関数
    function saveState() {
        undoStack.push(annotatedLyricsDiv.innerHTML);  // 現在のHTMLをスタックに保存
        redoStack = [];  // やり直しのスタックをリセット
    }

    // 元に戻す関数
    window.undo = function() {
        if (undoStack.length > 0) {  // スタックに元に戻す状態がある場合
            redoStack.push(annotatedLyricsDiv.innerHTML);  // 現在の状態をやり直しのために保存
            const previousState = undoStack.pop();  // スタックから最後の状態を取得
            annotatedLyricsDiv.innerHTML = previousState;  // 取得した状態を反映
        }
    }

    // やり直す関数
    window.redo = function() {
        if (redoStack.length > 0) {  // やり直しスタックに状態がある場合
            undoStack.push(annotatedLyricsDiv.innerHTML);  // 現在の状態を元に戻すために保存
            const nextState = redoStack.pop();  // スタックから次の状態を取得
            annotatedLyricsDiv.innerHTML = nextState;  // 取得した状態を反映
        }
    }

    // 注釈ツールボタンに選択イベントを追加
    document.querySelectorAll('#annotation-tools button').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('#annotation-tools button').forEach(btn => btn.classList.remove('selected'));  // すべてのボタンから選択状態を解除
            button.classList.add('selected');  // クリックされたボタンに選択状態を追加
            const color = button.getAttribute('data-color');  // ボタンの色を取得
            highlightSelection(color);  // 選択範囲にマーカーを引く
        });
    });

    // 選択範囲にマーカーを引く関数
    function highlightSelection(color) {
        saveState();  // 現在の状態を保存

        if (selectedRange) {  // 選択範囲が存在する場合
            const span = document.createElement('span');  // 新しいspan要素を作成
            span.style.backgroundColor = color;  // spanの背景色を設定
            span.style.color = '#000';  // spanのテキストカラーを設定
            span.appendChild(selectedRange.extractContents());  // 選択範囲の内容をspanに追加
            selectedRange.insertNode(span);  // spanを文書内に挿入
        }

        window.getSelection().removeAllRanges();  // 選択範囲を解除
        selectedRange = null;  // 選択範囲をリセット
    }

    // 注釈を追加する関数
    function addAnnotation(imagePath) {
        saveState();  // 現在の状態を保存

        const img = document.createElement('img');  // 新しいimg要素を作成
        img.src = imagePath;  // 画像のパスを設定
        img.alt = '注釈画像';  // 画像のalt属性を設定
        img.classList.add('annotation-image');  // 画像にクラスを追加
        
        if (selectedRange) {  // 選択範囲が存在する場合
            const range = selectedRange.cloneRange();  // 選択範囲をクローン
            range.collapse(false);  // 選択範囲を終了位置に縮める
            range.insertNode(img);  // 画像を挿入
        }

        contextMenu.style.display = 'none';  // カスタムコンテキストメニューを非表示にする
        window.getSelection().removeAllRanges();  // 選択範囲を解除
        selectedRange = null;  // 選択範囲をリセット
    }

    // コンテキストメニューを表示する関数
    function showContextMenu(x, y) {
        contextMenu.style.left = `${x}px`;  // メニューの表示位置を設定
        contextMenu.style.top = `${y}px`;  // メニューの表示位置を設定
        contextMenu.style.display = 'block';  // メニューを表示
    }

    // ドキュメントクリック時にカスタムコンテキストメニューを非表示にするイベント
    document.addEventListener('click', function(event) {
        if (!contextMenu.contains(event.target)) {  // クリックがメニューの外で発生した場合
            contextMenu.style.display = 'none';  // メニューを非表示にする
        }
    });

    // 注釈画像をコンテキストメニューから選択して追加するイベント
    contextMenu.addEventListener('click', function(event) {
        const selectedButton = event.target;  // クリックされたボタンを取得
        const imagePath = selectedButton.getAttribute('data-image-path');  // 画像パスを取得
        if (imagePath) {  // 画像パスが存在する場合
            addAnnotation(imagePath);  // 画像を挿入
        }
    });

    // 歌詞をエクスポートする関数
    window.exportLyrics = function() {
        const lyrics = document.getElementById('annotated-lyrics').innerHTML;  // 注釈付き歌詞を取得
        const blob = new Blob([lyrics], { type: 'text/html' });  // 歌詞をBlobとして作成
        const url = URL.createObjectURL(blob);  // BlobからURLを作成

        const a = document.createElement('a');  // 新しいリンク要素を作成
        a.href = url;  // リンクにURLを設定
        a.download = 'annotated_lyrics.html';  // ダウンロード名を設定
        a.click();  // リンクをクリックしてダウンロードを開始

        URL.revokeObjectURL(url);  // オブジェクトURLを解放
    }
    

});

    // 保存ボタンの参照を取得してクリックイベントを設定
    const saveButton = document.getElementById("save-button");
    if (saveButton) {
        saveButton.onclick = function(event) {
            event.preventDefault();
            console.log("Save button clicked");

            // Ajaxリクエストを送信して注釈を保存
            fetch(saveAnnotationsUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken  // CSRFトークンをリクエストに含める
                },
                body: JSON.stringify({
                    lyric_id: document.getElementById("lyric_id").value || '',
                    title: document.getElementById("title").value,
                    artist: document.getElementById("artist").value,
                    hiragana_lyrics: document.getElementById("hiragana_lyrics").value,
                    annotations: getAnnotations()
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    console.log("Annotations saved successfully");
                    window.location.href = "{% url 'mypage' %}";
                } else {
                    console.error("Error saving annotations:", data);
                }
            })
            .catch(error => {
                console.error("There was a problem with the fetch operation:", error);
            });
        };
    } else {
        console.error("Save button not found.");
    }

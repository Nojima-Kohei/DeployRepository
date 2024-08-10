document.addEventListener('DOMContentLoaded', function() {
    const annotatedLyricsDiv = document.getElementById('annotated-lyrics');
    const contextMenu = document.getElementById('context-menu');
    let selectedRange = null;
    let undoStack = [];
    let redoStack = [];

    // 現在の状態を保存
    function saveState() {
        undoStack.push(annotatedLyricsDiv.innerHTML);
        redoStack = [];
    }

    // 元に戻す
    window.undo = function() {
        if (undoStack.length > 0) {
            redoStack.push(annotatedLyricsDiv.innerHTML);
            const previousState = undoStack.pop();
            annotatedLyricsDiv.innerHTML = previousState;
        }
    }

    // やりなおし
    window.redo = function() {
        if (redoStack.length > 0) {
            undoStack.push(annotatedLyricsDiv.innerHTML);
            const nextState = redoStack.pop();
            annotatedLyricsDiv.innerHTML = nextState;
        }
    }

    // 注釈ツールボタンに選択イベントを追加
    document.querySelectorAll('#annotation-tools button').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('#annotation-tools button').forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');
            const color = button.getAttribute('data-color');
            highlightSelection(color);
        });
    });

    // 選択範囲にマーカーを引く
    function highlightSelection(color) {
        saveState();

        if (selectedRange) {
            const span = document.createElement('span');
            span.style.backgroundColor = color;
            span.style.color = '#000';
            span.appendChild(selectedRange.extractContents());
            selectedRange.insertNode(span);
        }

        window.getSelection().removeAllRanges();
        selectedRange = null;
    }

    // 注釈を追加
    function addAnnotation(imagePath) {
        saveState();

        const img = document.createElement('img');
        img.src = imagePath;
        img.alt = '注釈画像';
        img.classList.add('annotation-image');
        
        if (selectedRange) {
            const range = selectedRange.cloneRange();
            range.collapse(false);
            range.insertNode(img);
        }

        contextMenu.style.display = 'none';
        window.getSelection().removeAllRanges();
        selectedRange = null;
    }

    // マウスアップ時に選択範囲を更新
    annotatedLyricsDiv.addEventListener('mouseup', function(event) {
        const selection = window.getSelection();
        if (!selection.isCollapsed) {
            selectedRange = selection.getRangeAt(0);
        }
    });

    // コンテキストメニュー（右クリックメニュー）をカスタマイズ
    annotatedLyricsDiv.addEventListener('contextmenu', function(event) {
        event.preventDefault();
        const selection = window.getSelection();
        if (!selection.isCollapsed) {
            selectedRange = selection.getRangeAt(0);
            showContextMenu(event.pageX, event.pageY);
        }
    });

    // カスタムコンテキストメニューを表示
    function showContextMenu(x, y) {
        contextMenu.style.left = `${x}px`;
        contextMenu.style.top = `${y}px`;
        contextMenu.style.display = 'block';
    }

    // ドキュメントクリック時にカスタムコンテキストメニューを非表示
    document.addEventListener('click', function(event) {
        if (!contextMenu.contains(event.target)) {
            contextMenu.style.display = 'none';
        }
    });

    // 注釈画像をコンテキストメニューから選択して追加
    contextMenu.addEventListener('click', function(event) {
        const selectedButton = event.target;
        const imagePath = selectedButton.getAttribute('data-image-path');
        if (imagePath) {
            addAnnotation(imagePath);
        }
    });

    // 歌詞をエクスポートする関数
    window.exportLyrics = function() {
        const lyrics = document.getElementById('annotated-lyrics').innerHTML;
        const blob = new Blob([lyrics], { type: 'text/html' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'annotated_lyrics.html';
        a.click();

        URL.revokeObjectURL(url);
    }
});

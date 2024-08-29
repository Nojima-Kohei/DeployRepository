import sqlite3
import csv
import os

# データベースファイルの名前を指定
db_name = 'db.sqlite3' 

# データベースに接続
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# 出力先ディレクトリを作成
output_dir = 'exported_csvs'
os.makedirs(output_dir, exist_ok=True)

# データベース内の全テーブルを取得
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# 各テーブルをCSVとしてエクスポート
for table_name in tables:
    table_name = table_name[0]
    cursor.execute(f"SELECT * FROM {table_name}")
    
    # CSVファイル名はテーブル名に基づく
    csv_file_path = os.path.join(output_dir, f"{table_name}.csv")
    
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # ヘッダー行を書き込み
        writer.writerow([i[0] for i in cursor.description])
        # データ行を書き込み
        writer.writerows(cursor.fetchall())
    
    print(f"Exported {table_name} to {csv_file_path}")

# 接続を閉じる
conn.close()

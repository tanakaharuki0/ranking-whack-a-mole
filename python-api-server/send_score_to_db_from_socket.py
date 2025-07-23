import socket
import os
import psycopg2
from dotenv import load_dotenv

HOST = '' #空欄で良い
PORT = 50007 #送信側と同じポート番号を指定

load_dotenv(dotenv_path=".env.local") # .env ファイルから環境変数をロード

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# ... (データベース操作の関数群) ...


def add_score_direct(nickname: str, score: int):
    """
    データベースに直接新しいスコアを追加します。
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores (nickname, score) VALUES (%s, %s)", (nickname, score))
        conn.commit()
        print(f"データベースに直接スコアを追加しました: Nickname='{nickname}', Score={score}")
    except Exception as e:
        print(f"直接スコア追加エラー: {e}")
    finally:
        if conn:
            conn.close()

def get_scores_direct():
    """
    データベースから直接、各ニックネームの最高スコアを取得し、ランキング形式で表示します。
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nickname, MAX(score) as max_score
            FROM scores
            GROUP BY nickname
            ORDER BY max_score DESC
            LIMIT 10
        ''')
        scores = cursor.fetchall()
        
        print("\n--- 現在の直接ランキング ---")
        if scores:
            for i, s in enumerate(scores):
                print(f"{i+1}. Nickname: {s[0]}, Score: {s[1]}") # s[0]はnickname, s[1]はmax_score
        else:
            print("ランキングデータがありません。")
        print("--------------------------")
    except Exception as e:
        print(f"直接ランキング取得エラー: {e}")
    finally:
        if conn:
            conn.close()

# main関数 (スクリプト実行時の処理)
if __name__ == "__main__":
    print("nicknameを入力してください:")

    nickname = input().strip()
    if not nickname:
        print("ニックネームが入力されていません。終了します。")
        exit(1)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"サーバーがポート {PORT} で待機中...")

        conn, addr = s.accept()
        with conn:
            print(f"接続されました: {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                score = int(data.decode('utf-8'))
                print(f"受信したスコア: {score}")

                # データベースにスコアを追加
                add_score_direct(nickname, score)

    # 追加後のランキング表示
    get_scores_direct()
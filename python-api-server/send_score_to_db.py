import os
import psycopg2
from dotenv import load_dotenv

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

def delete_score_direct(nickname: str):
    """
    データベースから直接、指定されたニックネームのすべてのスコアを削除します。
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scores WHERE nickname = %s", (nickname,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"データベースから直接 '{nickname}' のスコアを {cursor.rowcount} 件削除しました。")
        else:
            print(f"データベースに '{nickname}' のスコアは見つかりませんでした。")
    except Exception as e:
        print(f"直接スコア削除エラー: {e}")
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
    print("デプロイ済みデータベースへの直接操作を開始します。")
    print("スクリプト実行前に 'DATABASE_URL' 環境変数を設定してください。")

    # 現在のランキング表示
    get_scores_direct()

    # スコアの追加
    # print("\n--- スコア直接追加のテスト ---")
    # add_score_direct("DirectAlice", 100)
    # add_score_direct("DirectBob", 150)
    # add_score_direct("DirectAlice", 120) 
    # add_score_direct("DirectCharlie", 80)
    # add_score_direct("DirectBob", 180) 

    # 追加後のランキング表示
    get_scores_direct()

    # スコアの削除
    print("\n--- スコア直接削除のテスト ---")
    # 例: DirectAliceのスコアを全て削除
    delete_score_direct("fugafuga")

    # 削除後のランキング表示
    get_scores_direct()

    delete_score_direct("NonExistentDirectNickname") 
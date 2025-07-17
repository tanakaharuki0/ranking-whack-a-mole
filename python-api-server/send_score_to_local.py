import requests
import json

#local環境でのAPIサーバーのURLを指定
# ここではローカルホストの5000番ポートを使用していますが
# 実際の環境に応じて変更してください。

# databaseを叩くのはsend_score_to_db.pyで行えます


API_BASE_URL = 'http://localhost:5000/api'

def add_score(nickname: str, score: int):
    """
    APIを介して新しいスコアを追加します。
    """
    url = f"{API_BASE_URL}/score"
    headers = {'Content-Type': 'application/json'}
    data = {'nickname': nickname, 'score': score}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() # HTTPエラーが発生した場合に例外を発生させる
        print(f"スコア追加成功: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"スコア追加エラー: {e}")
        if response and response.text:
            print(f"レスポンス内容: {response.text}")

def delete_score(nickname: str):
    """
    APIを介して指定されたニックネームのすべてのスコアを削除します。
    """
    url = f"{API_BASE_URL}/score/{nickname}"

    try:
        response = requests.delete(url)
        response.raise_for_status() # HTTPエラーが発生した場合に例外を発生させる
        print(f"スコア削除成功: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"スコア削除エラー: {e}")
        if response and response.text:
            print(f"レスポンス内容: {response.text}")

def get_scores():
    """
    APIを介して現在のランキングを取得します。
    """
    url = f"{API_BASE_URL}/scores"
    try:
        response = requests.get(url)
        response.raise_for_status() # HTTPエラーが発生した場合に例外を発生させる
        scores = response.json()
        print("\n--- 現在のランキング ---")
        if scores:
            for i, s in enumerate(scores):
                print(f"{i+1}. Nickname: {s['nickname']}, Score: {s['score']}")
        else:
            print("ランキングデータがありません。")
        print("--------------------")
    except requests.exceptions.RequestException as e:
        print(f"ランキング取得エラー: {e}")
        if response and response.text:
            print(f"レスポンス内容: {response.text}")


if __name__ == "__main__":
    # ランキング表示
    get_scores()

    # スコアの追加
    print("\n--- スコア追加のテスト ---")
    add_score("Alice", 100)
    add_score("Bob", 150)
    add_score("Alice", 120) # Aliceのスコアを更新（最高スコアが120になるはず）
    add_score("Charlie", 80)
    add_score("Bob", 180) # Bobのスコアを更新

    # 追加後のランキング表示
    get_scores()

    # スコアの削除
    print("\n--- スコア削除のテスト ---")
    # delete_score("Alice")

    # 削除後のランキング表示
    get_scores()

    delete_score("NonExistentNickname") # 存在しないニックネームの削除テスト
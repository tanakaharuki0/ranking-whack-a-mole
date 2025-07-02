import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv() # .env ファイルから環境変数をロード

app = Flask(__name__)

# CORSを有効にする。OPTIONSメソッドとDELETEメソッドを許可するように設定を強化
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "OPTIONS"]}}, supports_credentials=True)

# データベース接続情報の取得
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set.")
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# データベースの初期化（テーブル作成）
def init_db():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id SERIAL PRIMARY KEY,
                nickname TEXT NOT NULL,
                score INTEGER NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("Ensured database table 'scores' exists.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

@app.route('/api/scores', methods=['GET'])
def get_scores():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 各ニックネームの最高スコアを取得し、降順で上位10件
        cursor.execute('''
            SELECT nickname, MAX(score) as max_score
            FROM scores
            GROUP BY nickname
            ORDER BY max_score DESC
            LIMIT 10
        ''')
        scores = cursor.fetchall()
        
        scores_list = [{"nickname": nickname, "score": score} for nickname, score in scores]
        return jsonify(scores_list)
    except Exception as e:
        print(f"Error fetching scores: {e}")
        return jsonify({"error": "Failed to fetch scores"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/score', methods=['POST'])
def add_score():
    conn = None
    try:
        data = request.json
        nickname = data.get('nickname')
        score = data.get('score')

        if not isinstance(nickname, str) or not isinstance(score, int):
            return jsonify({"error": "Invalid data format. Expected {'nickname': 'str', 'score': int}."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores (nickname, score) VALUES (%s, %s)", (nickname, score))
        conn.commit()
        print(f"Saved: Nickname='{nickname}', Score={score}")
        return jsonify({"message": "Score saved successfully."}), 201
    except Exception as e:
        print(f"Error saving score: {e}")
        return jsonify({"error": "Failed to save score."}), 500
    finally:
        if conn:
            conn.close()

# ニックネームを指定してスコアを削除するエンドポイント
@app.route('/api/score/<nickname>', methods=['DELETE'])
def delete_score(nickname):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 指定されたニックネームのすべてのスコアを削除
        cursor.execute("DELETE FROM scores WHERE nickname = %s", (nickname,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Deleted scores for nickname: '{nickname}'")
            return jsonify({"message": f"Scores for nickname '{nickname}' deleted successfully."}), 200
        else:
            print(f"No scores found for nickname: '{nickname}'." ), 404
            return jsonify({"error": f"No scores found for nickname '{nickname}'."}), 404
    except Exception as e:
        print(f"Error deleting score: {e}")
        return jsonify({"error": "Failed to delete score."}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/score/<nickname>', methods=['OPTIONS'])
def options_score(nickname):
    response = app.make_default_options_response()
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE,OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


if __name__ == '__main__':
    init_db() # サーバー起動時にデータベースを初期化
    app.run(host='0.0.0.0', port=5000)
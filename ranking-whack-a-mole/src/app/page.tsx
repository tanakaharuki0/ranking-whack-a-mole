'use client';

import { useState, useEffect, useCallback } from 'react';

interface Score {
  nickname: string;
  score: number;
}

export default function Home() {
  const [scores, setScores] = useState<Score[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // 新しいスコア追加用のstate
  const [newNickname, setNewNickname] = useState<string>('');
  const [newScore, setNewScore] = useState<string>(''); // 入力は文字列として受け取る

  // APIサーバーのURLを環境変数から取得
  // Vercelにデプロイする際、この環境変数を設定
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:5000';

  const fetchScores = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/scores`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: unknown = await response.json();

      // Score[] かどうかチェック
      if (Array.isArray(data) && data.every(item =>
            typeof item === 'object' &&
            item !== null &&
            'nickname' in item &&
            typeof (item as { nickname?: unknown }).nickname === 'string' &&
            'score' in item &&
            typeof (item as { score?: unknown }).score === 'number'
        )) {
        setScores(data as Score[]);
      } else {
        throw new Error('Invalid data format received.');
      }
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError('An unknown error occurred.');
      }
    } finally {
      setLoading(false);
    }
  }, [API_BASE_URL]);

  useEffect(() => {
    fetchScores();
  }, []);

  const handleSubmitScore = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null); // エラーをリセット
    try {
      const scoreNum = parseInt(newScore, 10);
      if (isNaN(scoreNum)) {
        throw new Error("Score must be a number.");
      }

      const response = await fetch(`${API_BASE_URL}/api/score`, { // 環境変数を使用
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nickname: newNickname, score: scoreNum }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Failed to save score: ${errorData.error || response.statusText}`);
      }

      setNewNickname('');
      setNewScore('');
      // スコア保存後、ランキングを再フェッチ
      fetchScores();
    } catch (e: any) {
      setError(e.message);
    }
  };

  // 削除機能の追加
  const handleDeleteScore = async (nicknameToDelete: string) => {
    setError(null);
    if (!confirm(`Are you sure you want to delete all scores for ${nicknameToDelete}?`)) {
      return; // ユーザーがキャンセルした場合
    }

    try {
      console.log(nicknameToDelete)
      const response = await fetch(`${API_BASE_URL}/api/score/${nicknameToDelete}`, {
        method: 'DELETE', // DELETEメソッドを使用
        headers: {
          'Content-Type': 'application/json'
        },
      });
      console.log("1")
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Failed to delete score: ${errorData.error || response.statusText}`);
      }
      console.log("2")
      // 削除成功後、ランキングを再取得してUIを更新
      fetchScores();
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError('An unknown error occurred.');
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-xl text-gray-700">Loading ranking...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-xl text-red-600">Error: {error}</p>
        <p className="text-gray-500">Please ensure the Python API server is running at {API_BASE_URL}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-100 flex flex-col items-center justify-center p-4">
      <h1 className="text-5xl font-extrabold text-gray-900 mb-8 drop-shadow-lg">
        🏆 Game Ranking 🏆
      </h1>

      {/* スコア入力フォーム */}
      <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Add Your Score</h2>
        <form onSubmit={handleSubmitScore} className="space-y-4">
          <div>
            <label htmlFor="nickname" className="block text-sm font-medium text-gray-700">Nickname</label>
            <input
              type="text"
              id="nickname"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              value={newNickname}
              onChange={(e) => setNewNickname(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="score" className="block text-sm font-medium text-gray-700">Score</label>
            <input
              type="number"
              id="score"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              value={newScore}
              onChange={(e) => setNewScore(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Submit Score
          </button>
        </form>
      </div>

      {scores.length === 0 ? (
        <p className="text-2xl text-gray-700 mt-8">No scores yet. Play a game!</p>
      ) : (
        <div className="w-full max-w-2xl bg-white rounded-xl shadow-2xl p-8 transform hover:scale-105 transition-transform duration-300">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nickname</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>{/* 削除ボタン用の列を追加 */}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {scores.map((score, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{index + 1}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{score.nickname}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{score.score}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleDeleteScore(score.nickname)} // 削除ボタンのクリックイベント
                      className="text-red-600 hover:text-red-900 px-3 py-1 rounded-md border border-red-600 hover:border-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
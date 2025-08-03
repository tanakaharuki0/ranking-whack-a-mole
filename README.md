# ranking-whack-a-mole

## 概要
 - モグラたたきゲームのランキング表示

## フロントエンド (./ranking-whack-a-mole)
 - 推奨実行環境
   - Node.js >= 18.17.0（または v20.x 推奨）
   - npm >= 9
     
## バックエンド (./python-api-server)
 - 推奨実行環境（動作確認済み）
   - Python 3.10.12

## 開発環境セットアップ

1. ローカルでの DB 作成
   ```
   cd ranking-whack-a-moke
   docker compose up -d
   ```
2. フロントエンドパッケージインストール
   ```
   cd ranking-whack-a-moke
   npm install
   ```
3. バックエンドパッケージインストール
   ```
   cd ../python-api-server
   pip install -r requirements.txt
   ```
4. 開発サーバー立ち上げ
   ```
   npm run dev
   ```

## デプロイ方法
 - クライアントで動作する"./ranking-whack-a-mole"をクライアントサイドサーバに紐づける。vercelなどのサーバレスの場合、以下の環境変数を設定すると動作する。
   - NEXT_PUBLIC_API_BASE_URL
 - サーバで動作する"./python-api-server"をサーバサイドに紐づける。renderは一つのプロジェクトのみ1か月無料で動かせるプランがあるが、期限が切れるとDBが使用できなくなるため、DBを削除して再びデプロイする必要がある。バックエンド側に以下の環境変数を設定する必要がある。
   - DATABASE_URL

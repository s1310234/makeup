<!-- # React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project. -->

# Beauty Frontend

## 概要
React + Viteを使った美容関連のメイク情報入力画面のフロントエンドです。  
ユーザーが入力したメイク情報をバックエンドAPI（ポート3001）へ送信し、解析や生成AI連携を行います。

## 通信関連スペック
- 通信方式：HTTP REST API（JSON形式）
- バックエンドAPI URL：`http://localhost:3001`
- 主なAPIエンドポイント：
  - `POST /makeup` : メイク情報送信・解析
- 認証方式：APIキー認証（HTTPヘッダーにAPIキーを含める。APIキーは環境変数で管理）

## 環境構築・立ち上げ手順

1. Node.js（推奨バージョン16以上）とnpmがインストールされていることを確認してください。

2. 依存パッケージをインストールします。

```bash
npm install

3. バックエンドAPIサーバーを起動

4. フロントエンド開発サーバーを起動

npm run dev

5. ブラウザで http://localhost:5173 にアクセスするとアプリが動作する
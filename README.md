# オセロゲーム

Python バックエンドと React フロントエンドで構築された AI 対戦オセロ（リバーシ）ゲーム。

## 使用技術

### バックエンド

-   **Python 3.11+**
-   **FastAPI** - 高速な WebAPI フレームワーク
-   **NumPy** - 数値計算とゲーム盤面処理
-   **Pydantic** - データバリデーション
-   **uvicorn** - ASGI サーバー
-   **pytest** - テストフレームワーク

### フロントエンド

-   **React 18** - UI ライブラリ
-   **TypeScript** - 型安全性
-   **Vite** - 高速ビルドツール
-   **Deno** - モダンな JavaScript/TypeScript ランタイム

### AI・ゲームロジック

-   **Minimax アルゴリズム** - AI 思考エンジン
-   **αβ 剪定** - 探索効率化
-   **難易度調整** - 1-8 レベル対応

## プロジェクト構成

```
othello-game/
├── backend/                 # Pythonバックエンド
│   ├── app/
│   │   ├── main.py         # FastAPIアプリケーション
│   │   ├── api/            # API層
│   │   │   ├── models.py   # データモデル
│   │   │   └── routes.py   # エンドポイント
│   │   └── game/           # ゲームロジック
│   │       └── othello.py  # オセロ実装+AI
│   ├── tests/              # テスト
│   └── pyproject.toml      # 依存関係
├── frontend/               # Reactフロントエンド
│   ├── src/
│   │   ├── components/     # UIコンポーネント
│   │   ├── api/           # APIクライアント
│   │   └── types/         # TypeScript型定義
│   └── vite.config.ts     # Vite設定
└── README.md              # このファイル
```

## セットアップ方法

### 前提条件

-   Python 3.11 以上
-   uv（Python パッケージマネージャー）
-   Deno（フロントエンド用）

### 1. バックエンドセットアップ

```bash
# バックエンドディレクトリに移動
cd backend

# 依存関係をインストール
uv sync

# テストを実行（オプション）
uv run pytest

# APIサーバーを起動
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. フロントエンドセットアップ

```bash
# フロントエンドディレクトリに移動
cd frontend

# 開発サーバーを起動
deno task dev
```

## ゲーム開始方法

### 1. サーバー起動

**ターミナル 1（バックエンド）:**

```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**ターミナル 2（フロントエンド）:**

```bash
cd frontend
deno task dev
```

### 2. ゲームプレイ

1. バックエンドサーバーが起動していることを確認（`http://localhost:8000`）
2. フロントエンドサーバーが起動していることを確認（`http://localhost:3000`）
3. ブラウザで `http://localhost:3000` にアクセス
4. AI とオセロ対戦を楽しもう！

## ゲーム機能

-   **AI 対戦**: 8 段階の難易度調整可能
-   **リアルタイム対戦**: HTTP API 経由でのスムーズな操作
-   **ゲーム機能**:
    -   手の妥当性チェック
    -   スコア表示
    -   ゲーム状態管理
    -   リセット機能
    -   難易度変更

## API エンドポイント

-   `GET /api/game/new` - 新しいゲームを開始
-   `POST /api/game/move` - プレイヤーの手を実行
-   `POST /api/game/cpu-move` - CPU の手を取得
-   `GET /api/game/valid-moves/{player}` - 有効な手を取得

## 開発・テスト

### バックエンド

```bash
# テスト実行
uv run pytest

# コードフォーマット
uv run ruff format .

# コードチェック
uv run ruff check .

# 型チェック
uv run pyright
```

### フロントエンド

```bash
# 開発サーバー起動
deno task dev

# TypeScript型チェック
deno check src/main.tsx
```

## ゲームルール

オセロは 8×8 のボードで黒と白の石を使って対戦するゲームです：

1. 黒が先手
2. 相手の石を自分の石で挟むように配置
3. 挟まれた石はすべて自分の色に変わる
4. 有効な手がない場合はパス
5. 両プレイヤーが打てなくなったら終了
6. 石の数が多い方が勝利

## AI の戦略

AI は難易度に応じて異なる戦略を使用：

-   **レベル 1-2**: ランダムな手
-   **レベル 3-4**: 貪欲法（最も多く石を取る手）
-   **レベル 5-8**: Minimax アルゴリズム
    -   位置価値（角は有利、角隣接は不利）
    -   石数差評価
    -   機動性（打てる手の数）
    -   終盤評価

## ライセンス

このプロジェクトは教育目的で作成されています。

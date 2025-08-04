# GitHubアカウント作成・設定ガイド

## 1. GitHubアカウント作成手順

### 1.1 アカウント作成
1. **GitHubにアクセス**
   - https://github.com/ にアクセス

2. **アカウント情報入力**
   ```
   ユーザー名: [推奨] amazon-ec-tool または [あなたの名前]-dev
   メールアドレス: [あなたのメールアドレス]
   パスワード: [安全なパスワード]
   ```

3. **アカウント確認**
   - メールアドレスの確認
   - 2段階認証の設定（推奨）

### 1.2 プロフィール設定
1. **プロフィール編集**
   - Settings → Profile
   - 名前: Amazon商品データ管理システム開発者
   - Bio: Python | API連携 | データ分析 | Amazon商品管理システム開発中

2. **プロフィール画像**
   - プロフェッショナルな画像を設定

## 2. リポジトリ作成

### 2.1 新しいリポジトリ作成
1. **リポジトリ作成**
   ```
   リポジトリ名: amazon-ec-tool
   説明: Amazon商品データ管理システム
   公開設定: Public
   ```

2. **README.md作成**
   ```markdown
   # Amazon商品データ管理システム

   Amazon商品の価格・在庫情報を自動取得し、Googleスプレッドシートで管理するシステムです。

   ## 主な機能

   - 🔍 商品検索・分析
   - 📈 価格追跡
   - 📊 在庫監視
   - 🏆 競合分析
   - 📋 Google Sheets連携

   ## 技術スタック

   - **開発言語**: Python
   - **API**: Amazon Product Advertising API
   - **データ管理**: Google Sheets API
   - **自動化**: 定期実行・スケジューラー

   ## 開発状況

   - ✅ プロジェクト基盤構築
   - ✅ Amazon APIクライアント実装
   - ✅ モックデータシステム実装
   - 🔄 Amazon API認証申請中
   - ⏳ Google Sheets連携実装予定

   ## ライセンス

   MIT License
   ```

## 3. Amazon申請用の設定

### 3.1 申請時の情報
```
サイト名: Amazon商品データ管理システム
サイトURL: https://github.com/[あなたのユーザー名]/amazon-ec-tool
サイト説明: Amazon商品の価格・在庫情報を自動取得し、Googleスプレッドシートで管理するシステムです。商品分析、価格追跡、在庫監視機能を提供します。
```

### 3.2 アプリ情報
```
アプリ名: Amazon商品管理アプリ
プラットフォーム: Webアプリケーション
アプリURL: https://github.com/[あなたのユーザー名]/amazon-ec-tool
アプリ説明: Amazon商品の価格・在庫情報を管理するWebアプリケーションです。商品検索、価格追跡、データ分析機能を提供します。
```

## 4. プロジェクトファイルのアップロード

### 4.1 ローカルプロジェクトをGitHubにアップロード
```bash
# 1. 現在のプロジェクトディレクトリでGit初期化
cd /Users/fuuka/Desktop/実務プロジェクト/ECサイト:googleスプレットシート
git init

# 2. リモートリポジトリを追加
git remote add origin https://github.com/[あなたのユーザー名]/amazon-ec-tool.git

# 3. ファイルを追加
git add .

# 4. コミット
git commit -m "Initial commit: Amazon商品データ管理システム基盤構築"

# 5. プッシュ
git push -u origin main
```

### 4.2 .gitignoreファイルの作成
```bash
# .gitignoreファイルを作成
cat > .gitignore << EOF
# 環境変数
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 仮想環境
amazon_ec_env/
venv/
ENV/

# ログファイル
logs/
*.log

# データファイル
data/raw/
data/processed/*.json
data/processed/*.csv
data/processed/*.xlsx

# 認証ファイル
credentials.json
*.pem
*.key

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
```

## 5. 申請時の注意点

### 5.1 GitHubの利点
- **開発者として適切**: コードが公開されている
- **プロフェッショナル**: 技術的な内容が明確
- **継続的な更新**: 開発進捗が分かる
- **コミュニティ**: オープンソースとして認識される

### 5.2 申請理由の記載
```
申請理由: 
Amazon商品データを自動取得し、Googleスプレッドシートで管理するシステムを開発しています。
商品の価格変動分析、在庫監視、競合分析などの機能を提供する予定です。
GitHubでオープンソースとして開発を進めており、審査期間中に機能を充実させ、承認後に本格運用を開始します。
```

## 6. 次のステップ

1. **GitHubアカウント作成**
2. **リポジトリ作成**
3. **プロジェクトファイルアップロード**
4. **Amazonアソシエイトプログラム申請**
5. **審査期間中の開発継続**

## 7. トラブルシューティング

### 7.1 よくある問題
- **ユーザー名が既に使用されている**: 別のユーザー名を選択
- **リポジトリ名が既に使用されている**: 別のリポジトリ名を選択
- **Git認証エラー**: Personal Access Tokenを使用

### 7.2 代替案
- **ユーザー名**: `amazon-ec-dev-[数字]`
- **リポジトリ名**: `amazon-product-manager` 
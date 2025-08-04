# Amazonアソシエイトプログラム申請用URL設定ガイド

## URL問題の解決方法

### 1. 無料ホスティングサービスの利用

#### 1.1 GitHub Pages（推奨）
**手順**:
1. **GitHubアカウント作成**
   - https://github.com/ にアクセス
   - アカウント作成・ログイン

2. **リポジトリ作成**
   ```
   リポジトリ名: amazon-ec-tool
   説明: Amazon商品データ管理システム
   公開設定: Public
   ```

3. **静的ページ作成**
   ```html
   <!-- index.html -->
   <!DOCTYPE html>
   <html>
   <head>
       <title>Amazon商品データ管理システム</title>
       <meta charset="UTF-8">
   </head>
   <body>
       <h1>Amazon商品データ管理システム</h1>
       <p>Amazon商品の価格・在庫情報を自動取得し、Googleスプレッドシートで管理するシステムです。</p>
       <p>機能:</p>
       <ul>
           <li>商品検索・分析</li>
           <li>価格追跡</li>
           <li>在庫監視</li>
           <li>競合分析</li>
       </ul>
   </body>
   </html>
   ```

4. **GitHub Pages有効化**
   - リポジトリ設定 → Pages
   - Source: Deploy from a branch
   - Branch: main
   - URL: `https://[username].github.io/amazon-ec-tool`

#### 1.2 Netlify（代替案）
**手順**:
1. **Netlifyアカウント作成**
   - https://netlify.com/ にアクセス
   - GitHubアカウントでログイン

2. **サイト作成**
   - "New site from Git"
   - GitHubリポジトリを選択
   - 自動デプロイ設定

3. **URL取得**
   - 自動生成URL: `https://random-name.netlify.app`
   - カスタムドメイン設定可能

### 2. 申請時のURL設定

#### 2.1 推奨URL設定
```
サイト名: Amazon商品データ管理システム
サイトURL: https://[username].github.io/amazon-ec-tool
サイト説明: Amazon商品の価格・在庫情報を自動取得し、Googleスプレッドシートで管理するシステムです。商品分析、価格追跡、在庫監視機能を提供します。
```

#### 2.2 アプリ情報設定
```
アプリ名: Amazon商品管理アプリ
プラットフォーム: Webアプリケーション
アプリURL: https://[username].github.io/amazon-ec-tool
アプリ説明: Amazon商品の価格・在庫情報を管理するWebアプリケーションです。商品検索、価格追跡、データ分析機能を提供します。
```

### 3. 実際のサイト作成手順

#### 3.1 GitHub Pagesサイトの作成
```bash
# 1. GitHubでリポジトリ作成
# 2. ローカルでクローン
git clone https://github.com/[username]/amazon-ec-tool.git
cd amazon-ec-tool

# 3. 静的ファイル作成
mkdir docs
touch docs/index.html
```

#### 3.2 index.htmlの内容
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Amazon商品データ管理システム</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .header {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .feature {
            background: #fff;
            border: 1px solid #ddd;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .feature h3 {
            color: #007bff;
            margin-top: 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Amazon商品データ管理システム</h1>
        <p>Amazon商品の価格・在庫情報を自動取得し、Googleスプレッドシートで管理するシステムです。</p>
    </div>

    <h2>主な機能</h2>
    
    <div class="feature">
        <h3>🔍 商品検索・分析</h3>
        <p>Amazon商品の詳細情報を自動取得し、価格や在庫状況を分析します。</p>
    </div>

    <div class="feature">
        <h3>📈 価格追跡</h3>
        <p>商品の価格変動を自動追跡し、最適な購入タイミングを把握します。</p>
    </div>

    <div class="feature">
        <h3>📊 在庫監視</h3>
        <p>商品の在庫状況をリアルタイムで監視し、在庫切れを事前に察知します。</p>
    </div>

    <div class="feature">
        <h3>🏆 競合分析</h3>
        <p>類似商品の価格比較を行い、競合状況を分析します。</p>
    </div>

    <div class="feature">
        <h3>📋 Google Sheets連携</h3>
        <p>取得したデータをGoogleスプレッドシートに自動反映し、データ管理を効率化します。</p>
    </div>

    <h2>技術仕様</h2>
    <ul>
        <li><strong>開発言語:</strong> Python</li>
        <li><strong>API:</strong> Amazon Product Advertising API</li>
        <li><strong>データ管理:</strong> Google Sheets API</li>
        <li><strong>自動化:</strong> 定期実行・スケジューラー</li>
    </ul>

    <h2>開発状況</h2>
    <p>現在、Amazon API連携機能の開発を進めています。審査期間中はモックデータを使用して開発を継続し、承認後に実際のAPI呼び出しを開始する予定です。</p>

    <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666;">
        <p>© 2024 Amazon商品データ管理システム</p>
    </footer>
</body>
</html>
```

### 4. 申請時の注意点

#### 4.1 URLの要件
- **実際にアクセス可能**であること
- **HTTPS**でアクセス可能であること
- **サイト内容**が申請内容と一致していること

#### 4.2 申請理由の記載
```
申請理由: 
Amazon商品データを自動取得し、Googleスプレッドシートで管理するシステムを開発しています。
商品の価格変動分析、在庫監視、競合分析などの機能を提供する予定です。
現在は開発段階ですが、審査期間中に機能を充実させ、承認後に本格運用を開始します。
```

### 5. 代替案

#### 5.1 既存のブログ・サイトを利用
- **個人ブログ**のURLを使用
- **企業サイト**のURLを使用
- **SNSプロフィール**のURLを使用

#### 5.2 一時的なURL作成
- **Heroku**の無料プラン
- **Vercel**の無料プラン
- **Firebase Hosting**の無料プラン

## 次のステップ

1. **GitHub Pagesサイトを作成**
2. **申請用URLを取得**
3. **Amazonアソシエイトプログラムに申請**
4. **審査期間中に開発継続** 
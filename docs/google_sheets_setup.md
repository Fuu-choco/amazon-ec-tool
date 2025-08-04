# Google Sheets API設定ガイド

## 概要

このガイドでは、Amazon EC ToolでGoogle Sheets APIを使用するための設定手順を説明します。

## 前提条件

- Googleアカウント
- Google Cloud Consoleへのアクセス権限

## 設定手順

### 1. Google Cloud Projectの作成

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成
3. プロジェクト名を設定（例: "Amazon EC Tool"）

### 2. Google Sheets APIの有効化

1. **APIライブラリ**にアクセス
2. **Google Sheets API**を検索
3. **有効にする**をクリック
4. **Google Drive API**も有効化

### 3. サービスアカウントの作成

1. **IAM & Admin** → **サービスアカウント**にアクセス
2. **サービスアカウントを作成**をクリック
3. サービスアカウント名を入力（例: "amazon-ec-tool"）
4. **キーを作成** → **JSON**を選択
5. ダウンロードしたJSONファイルを`credentials.json`として保存

### 4. 認証ファイルの配置

1. ダウンロードしたJSONファイルをプロジェクトルートに`credentials.json`として配置
2. ファイルの権限を確認（読み取り可能）

### 5. スプレッドシートの準備

1. Google Sheetsで新しいスプレッドシートを作成
2. スプレッドシートIDを取得（URLから）
3. サービスアカウントのメールアドレスに編集権限を付与

### 6. 環境変数の設定

`.env`ファイルに以下の設定を追加：

```bash
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
SPREADSHEET_ID=your_spreadsheet_id_here
```

## ファイル構造

```
ECサイト:googleスプレットシート/
├── credentials.json          # Google API認証ファイル
├── .env                      # 環境変数設定
├── src/
│   └── google_sheets/
│       ├── client.py         # Google Sheets APIクライアント
│       └── data_sync.py     # データ同期機能
└── docs/
    └── google_sheets_setup.md  # このファイル
```

## スプレッドシート構造

作成されるスプレッドシートには以下のワークシートが含まれます：

### 1. 商品マスター
- ASIN、商品タイトル、ブランド、カテゴリ
- 現在価格、元価格、割引率
- 在庫状況、評価、レビュー数

### 2. 価格履歴
- 日付、ASIN、商品タイトル
- 価格、価格変動、変動率
- 割引率、更新日時

### 3. 在庫管理
- ASIN、商品タイトル、ブランド
- 在庫状況、在庫カテゴリ
- 最終確認日時、アラート

### 4. 分析ダッシュボード
- 分析項目、値、単位
- 更新日時

## トラブルシューティング

### よくある問題

#### 1. 認証エラー
**症状**: `Invalid Credentials` エラー
**解決方法**:
- credentials.jsonファイルが正しく配置されているか確認
- ファイルの権限を確認
- サービスアカウントキーが有効か確認

#### 2. 権限エラー
**症状**: `Permission denied` エラー
**解決方法**:
- スプレッドシートにサービスアカウントの権限が付与されているか確認
- サービスアカウントのメールアドレスを確認

#### 3. API制限エラー
**症状**: `Quota exceeded` エラー
**解決方法**:
- Google Cloud Consoleでクォータを確認
- API使用量を監視

### 設定確認

以下のコマンドで設定を確認できます：

```bash
python test_google_sheets.py
```

## セキュリティ注意事項

1. **credentials.jsonファイルの管理**
   - バージョン管理システムにコミットしない
   - .gitignoreに追加
   - 適切な権限で管理

2. **サービスアカウントの権限**
   - 必要最小限の権限のみ付与
   - 定期的に権限を確認

3. **スプレッドシートの共有設定**
   - 必要最小限のユーザーのみアクセス可能に設定
   - 定期的に共有設定を確認

## 次のステップ

設定が完了したら、以下の機能をテストできます：

1. **スプレッドシート作成テスト**
2. **データ同期テスト**
3. **分析ダッシュボードテスト**

詳細は`test_google_sheets.py`を実行して確認してください。 
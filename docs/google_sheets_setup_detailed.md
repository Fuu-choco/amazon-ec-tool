# Google Sheets API設定詳細ガイド

## 1. Google Cloud Console設定

### 1.1 Google Cloud Consoleにアクセス
1. **Google Cloud Console**にアクセス
   - https://console.cloud.google.com/
   - Googleアカウントでログイン

2. **プロジェクト作成**
   ```
   プロジェクト名: amazon-ec-tool
   プロジェクトID: amazon-ec-tool-[数字]
   説明: Amazon商品データ管理システム用プロジェクト
   ```

### 1.2 Google Sheets API有効化
1. **APIライブラリにアクセス**
   - 左メニュー → "APIとサービス" → "ライブラリ"

2. **Google Sheets APIを検索・有効化**
   - 検索: "Google Sheets API"
   - "有効にする"をクリック

3. **Google Drive APIも有効化**
   - 検索: "Google Drive API"
   - "有効にする"をクリック

## 2. サービスアカウント作成

### 2.1 サービスアカウント作成
1. **IAMと管理** → "サービスアカウント"
2. **サービスアカウントを作成**
   ```
   サービスアカウント名: amazon-ec-tool-service
   サービスアカウントID: amazon-ec-tool-service
   説明: Amazon商品データ管理システム用サービスアカウント
   ```

3. **役割の設定**
   - 役割: "編集者" または "ビューアー"（必要に応じて）

### 2.2 キーの作成
1. **サービスアカウント詳細** → "キー"
2. **新しいキーを作成** → "JSON"
3. **JSONファイルをダウンロード**
4. **ファイル名を変更**: `credentials.json`（推奨）

**ファイル名の選択肢**:
- `credentials.json`（推奨）
- `google-sheets-credentials.json`
- `amazon-ec-tool-credentials.json`
- `service-account-key.json`

## 3. スプレッドシート作成

### 3.1 Google Sheetsでスプレッドシート作成
1. **Google Sheets**にアクセス
   - https://sheets.google.com/

2. **新しいスプレッドシート作成**
   ```
   スプレッドシート名: Amazon商品データ管理
   説明: Amazon商品の価格・在庫情報を管理
   ```

3. **スプレッドシートIDを取得**
   - URLからIDをコピー
   - 例: `https://docs.google.com/spreadsheets/d/[スプレッドシートID]/edit`

### 3.2 サービスアカウントにアクセス権限を付与
1. **スプレッドシートを開く**
2. **共有** → "ユーザーやグループを追加"
3. **サービスアカウントのメールアドレスを追加**
   - 形式: `amazon-ec-tool-service@[プロジェクトID].iam.gserviceaccount.com`
4. **権限**: "編集者"

## 4. 環境変数の設定

### 4.1 .envファイルの更新
```bash
# .envファイルを編集
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
SPREADSHEET_ID=[スプレッドシートID]
```

### 4.2 credentials.jsonの配置
```bash
# credentials.jsonをプロジェクトルートに配置
cp [ダウンロードしたファイル] credentials.json

# または、別の名前を使用する場合
cp [ダウンロードしたファイル] google-sheets-credentials.json
# その場合、.envファイルも更新
# GOOGLE_SHEETS_CREDENTIALS_FILE=google-sheets-credentials.json
```

## 5. テスト実行

### 5.1 基本接続テスト
```bash
python test_google_sheets.py
```

### 5.2 期待される結果
- Google Sheets API接続成功
- スプレッドシートへの書き込み成功
- データ読み込み成功

## 6. トラブルシューティング

### 6.1 よくある問題
1. **認証エラー**
   - credentials.jsonが正しく配置されているか確認
   - サービスアカウントに適切な権限があるか確認

2. **権限エラー**
   - スプレッドシートにサービスアカウントが追加されているか確認
   - 権限が"編集者"以上になっているか確認

3. **API制限エラー**
   - Google Cloud ConsoleでAPIが有効になっているか確認
   - クォータ制限に達していないか確認

### 6.2 確認事項
- [ ] Google Cloud Consoleでプロジェクト作成済み
- [ ] Google Sheets API有効化済み
- [ ] サービスアカウント作成済み
- [ ] JSONキーファイルダウンロード済み
- [ ] ファイル名を`credentials.json`に変更済み
- [ ] スプレッドシート作成済み
- [ ] サービスアカウントにアクセス権限付与済み
- [ ] .envファイルに認証情報設定済み
- [ ] 接続テスト成功

## 7. 次のステップ

1. **Google Cloud Console設定**
2. **サービスアカウント作成**
3. **スプレッドシート作成**
4. **認証情報設定**
5. **接続テスト実行**
6. **データ書き込み機能実装** 
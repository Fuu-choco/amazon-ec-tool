# Amazon Product Advertising API 設定ガイド

## 1. Amazonアソシエイトプログラム登録

### 1.1 アソシエイトプログラムへの参加
1. **Amazonアソシエイトプログラム**にアクセス
   - URL: https://affiliate-program.amazon.com/
   - または: https://affiliate-program.amazon.co.jp/ (日本)

2. **アカウント作成**
   - Amazonアカウントでログイン
   - アソシエイトプログラムに参加申請
   - 審査期間: 通常1-2週間

3. **承認後の準備**
   - Associate Tag（アソシエイトタグ）を取得
   - 例: `yourname-20` のような形式

### 1.2 必要な情報
- **Associate Tag**: アソシエイトプログラムで取得
- **AWS Access Key ID**: AWSアカウントで作成
- **AWS Secret Access Key**: AWSアカウントで作成

## 2. AWS認証情報の作成

### 2.1 AWSアカウントの準備
1. **AWSアカウント作成**（既存の場合は不要）
   - https://aws.amazon.com/ にアクセス
   - アカウント作成・ログイン

2. **IAMユーザーの作成**
   - AWS Management Consoleにログイン
   - IAMサービスに移動
   - 新しいユーザーを作成

### 2.2 IAMユーザー作成手順
1. **IAMコンソールにアクセス**
   ```
   https://console.aws.amazon.com/iam/
   ```

2. **ユーザー作成**
   - 「ユーザー」→「ユーザーの作成」
   - ユーザー名: `amazon-api-user`（推奨）

3. **アクセスキーの作成**
   - アクセスタイプ: 「プログラムによるアクセス」
   - 「アクセスキーID」と「シークレットアクセスキー」を保存

4. **権限の設定**
   - ポリシー: `AmazonProductAdvertisingAPIFullAccess`
   - または: カスタムポリシーを作成

### 2.3 カスタムポリシーの作成（推奨）
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ProductAdvertisingAPI:*"
            ],
            "Resource": "*"
        }
    ]
}
```

## 3. 環境変数の設定

### 3.1 .envファイルの更新
```bash
# .envファイルを編集
AWS_ACCESS_KEY_ID=your_actual_access_key_id
AWS_SECRET_ACCESS_KEY=your_actual_secret_access_key
ASSOCIATE_TAG=your_associate_tag
AWS_REGION=us-east-1
```

### 3.2 設定確認
```bash
# 設定が正しく読み込まれるかテスト
python -c "from src.utils.config import config_manager; print('Amazon設定:', config_manager.get_amazon_config())"
```

## 4. API接続テスト

### 4.1 基本接続テスト
```bash
python test_amazon_api.py
```

### 4.2 期待される結果
- API接続成功
- 基本的な商品検索が動作
- エラーハンドリングが正常に動作

## 5. トラブルシューティング

### 5.1 よくある問題
1. **認証エラー**
   - アクセスキーが正しく設定されているか確認
   - IAMユーザーに適切な権限があるか確認

2. **API制限エラー**
   - レート制限に達していないか確認
   - リクエスト頻度を調整

3. **Associate Tagエラー**
   - アソシエイトプログラムが承認されているか確認
   - Associate Tagが正しく設定されているか確認

### 5.2 確認事項
- [ ] Amazonアソシエイトプログラムに登録済み
- [ ] Associate Tagを取得済み
- [ ] AWS IAMユーザーを作成済み
- [ ] アクセスキーを取得済み
- [ ] .envファイルに認証情報を設定済み
- [ ] API接続テストが成功

## 6. 次のステップ

認証情報の設定が完了したら：
1. 基本的な商品検索機能の実装
2. 商品詳細取得機能の実装
3. エラーハンドリングの強化 
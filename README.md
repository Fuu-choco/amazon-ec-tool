# Amazon商品データ管理システム

Amazon商品の価格・在庫情報を自動取得し、Googleスプレッドシートで管理するシステムです。

## 🚀 主な機能

- 🔍 **商品検索・分析**: Amazon商品の詳細情報を自動取得し、価格や在庫状況を分析
- 📈 **価格追跡**: 商品の価格変動を自動追跡し、最適な購入タイミングを把握
- 📊 **在庫監視**: 商品の在庫状況をリアルタイムで監視し、在庫切れを事前に察知
- 🏆 **競合分析**: 類似商品の価格比較を行い、競合状況を分析
- 📋 **Google Sheets連携**: 取得したデータをGoogleスプレッドシートに自動反映し、データ管理を効率化

## 🛠️ 技術スタック

- **開発言語**: Python 3.8+
- **API**: Amazon Product Advertising API
- **データ管理**: Google Sheets API
- **データ処理**: pandas, numpy
- **設定管理**: PyYAML, python-dotenv
- **ログ管理**: logging
- **自動化**: schedule, cron

## 📁 プロジェクト構造

```
amazon-ec-tool/
├── src/                    # ソースコード
│   ├── amazon_api/        # Amazon API関連
│   │   ├── client.py      # Amazon APIクライアント
│   │   └── mock_client.py # モッククライアント（開発用）
│   ├── data_processor/    # データ処理
│   │   ├── amazon_data_processor.py
│   │   └── data_exporter.py
│   ├── google_sheets/     # Google Sheets連携
│   │   ├── client.py
│   │   └── data_sync.py
│   └── utils/             # ユーティリティ
│       ├── config.py      # 設定管理
│       └── logger.py      # ログ機能
├── tests/                 # テストコード
├── data/                  # データファイル
│   ├── raw/              # 生データ
│   └── processed/        # 処理済みデータ
├── logs/                  # ログファイル
├── config/                # 設定ファイル
├── docs/                  # ドキュメント
├── requirements.txt       # 依存ライブラリ
├── config.yaml           # 設定ファイル
└── README.md             # このファイル
```

## ⚡ クイックスタート

### 1. 環境構築

```bash
# リポジトリをクローン
git clone https://github.com/[username]/amazon-ec-tool.git
cd amazon-ec-tool

# 仮想環境を作成
python3 -m venv amazon_ec_env

# 仮想環境をアクティベート
source amazon_ec_env/bin/activate  # macOS/Linux
# または
amazon_ec_env\Scripts\activate     # Windows

# 必要なライブラリをインストール
pip install -r requirements.txt
```

### 2. 設定ファイルの準備

```bash
# 環境変数テンプレートをコピー
cp env.template .env

# .envファイルを編集して認証情報を設定
```

### 3. 基本機能テスト

```bash
# 基本機能テスト
python test_basic_setup.py

# モックAPIテスト
python test_mock_amazon_api.py
```

## 🔧 設定

### Amazon API設定
- AWS Access Key ID
- AWS Secret Access Key
- Associate Tag

### Google Sheets API設定
- サービスアカウントキー（JSONファイル）
- スプレッドシートID

## 📊 開発状況

### ✅ 完了済み
- [x] プロジェクト基盤構築
- [x] 設定管理機能
- [x] ログ機能
- [x] Amazon APIクライアント実装
- [x] モックデータシステム実装
- [x] データ処理機能
- [x] 基本ディレクトリ構造

### 🔄 開発中
- [ ] Amazon API認証申請
- [ ] Google Sheets連携実装
- [ ] 自動化機能実装
- [ ] UI/UX改善

### ⏳ 予定
- [ ] 価格分析機能
- [ ] 在庫監視機能
- [ ] 競合分析機能
- [ ] ダッシュボード機能

## 🧪 テスト

```bash
# 基本機能テスト
python test_basic_setup.py

# Amazon APIテスト（モック）
python test_mock_amazon_api.py

# データ処理テスト
python test_data_processing.py

# Google Sheetsテスト
python test_google_sheets.py
```

## 📖 使用方法

### 基本機能テスト

```python
from src.utils.config import config_manager
from src.utils.logger import logger

# 設定確認
amazon_config = config_manager.get_amazon_config()
print(amazon_config)

# ログ機能
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
```

### モックAPI使用

```python
from src.amazon_api.mock_client import mock_amazon_client

# 商品検索
result = mock_amazon_client.search_items("iPhone", item_count=5)
print(result)
```

## 🤝 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 📞 サポート

- **バグ報告**: [GitHub Issues](https://github.com/[username]/amazon-ec-tool/issues)
- **機能要望**: [GitHub Issues](https://github.com/[username]/amazon-ec-tool/issues)
- **質問**: [GitHub Discussions](https://github.com/[username]/amazon-ec-tool/discussions)

## 📈 更新履歴

### v0.2.0 (2024-08-04)
- Amazon APIクライアント実装
- モックデータシステム実装
- データ処理機能実装
- テストコード充実

### v0.1.0 (2024-08-02)
- プロジェクト基盤構築
- 設定管理機能の実装
- ログ機能の実装
- 基本ディレクトリ構造の作成

## ⭐ スター

このプロジェクトが役に立った場合は、⭐を押していただけると励みになります！

---

**開発者**: Amazon商品データ管理システム開発者  
**技術**: Python | API連携 | データ分析 
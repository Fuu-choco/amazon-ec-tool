#!/usr/bin/env python3
"""
Amazon API接続テストスクリプト
Amazon APIの接続とデータ処理機能をテスト
"""

import sys
import os
import json
from datetime import datetime

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from amazon_api.client import amazon_client
from data_processor.amazon_data_processor import amazon_data_processor
from utils.logger import logger


def test_amazon_api_connection():
    """Amazon API接続テスト"""
    print("=== Amazon API接続テスト ===")
    
    try:
        # 設定を確認
        config = amazon_client.config
        print(f"Amazon設定: {config}")
        
        # AWSセッション作成テスト
        session = amazon_client.session
        print(f"AWSセッション作成: 成功")
        
        # 認証情報の確認
        credentials = session.get_credentials()
        if credentials:
            print("✓ AWS認証情報: 設定済み")
        else:
            print("✗ AWS認証情報: 未設定")
            return False
        
        print("✓ Amazon API接続テスト完了\n")
        return True
        
    except Exception as e:
        print(f"✗ Amazon API接続エラー: {e}")
        print("\n設定が必要です:")
        print("1. .envファイルにAWS認証情報を設定")
        print("2. AWS_ACCESS_KEY_ID")
        print("3. AWS_SECRET_ACCESS_KEY")
        print("4. ASSOCIATE_TAG")
        return False


def test_mock_search():
    """モック検索テスト（実際のAPI呼び出しなし）"""
    print("=== モック検索テスト ===")
    
    # モック検索結果
    mock_search_result = {
        "SearchResult": {
            "Items": [
                {
                    "ASIN": "B08N5WRWNW",
                    "ItemInfo": {
                        "Title": {
                            "DisplayValue": "テスト商品"
                        },
                        "ByLineInfo": {
                            "Brand": {
                                "DisplayValue": "テストブランド"
                            }
                        }
                    },
                    "Offers": {
                        "CurrentPrice": {
                            "Amount": 1000,
                            "Currency": "JPY"
                        },
                        "ListPrice": {
                            "Amount": 1200,
                            "Currency": "JPY"
                        },
                        "Availability": {
                            "Message": "在庫あり"
                        }
                    },
                    "CustomerReviews": {
                        "Rating": 4.5,
                        "ReviewCount": 100
                    },
                    "Images": {
                        "Primary": {
                            "Large": {
                                "URL": "https://example.com/image.jpg"
                            }
                        }
                    }
                }
            ]
        }
    }
    
    # データ処理テスト
    normalized_items = amazon_data_processor.normalize_search_result(mock_search_result)
    
    if normalized_items:
        print(f"✓ モック検索結果処理: {len(normalized_items)}件")
        print(f"処理結果: {json.dumps(normalized_items[0], ensure_ascii=False, indent=2)}")
    else:
        print("✗ モック検索結果処理: 失敗")
    
    print("✓ モック検索テスト完了\n")


def test_data_save_load():
    """データ保存・読み込みテスト"""
    print("=== データ保存・読み込みテスト ===")
    
    # テストデータ
    test_data = [
        {
            "asin": "B08N5WRWNW",
            "title": "テスト商品",
            "brand": "テストブランド",
            "current_price": 1000,
            "original_price": 1200,
            "discount_rate": 16.67,
            "currency": "JPY",
            "availability": "在庫あり",
            "rating": 4.5,
            "review_count": 100,
            "image_url": "https://example.com/image.jpg",
            "processed_at": datetime.now().isoformat()
        }
    ]
    
    # データ保存テスト
    test_file = "data/processed/test_data.json"
    amazon_data_processor.save_to_json(test_data, test_file)
    
    # データ読み込みテスト
    loaded_data = amazon_data_processor.load_from_json(test_file)
    
    if loaded_data:
        print(f"✓ データ保存・読み込み: 成功 ({len(loaded_data)}件)")
    else:
        print("✗ データ保存・読み込み: 失敗")
    
    print("✓ データ保存・読み込みテスト完了\n")


def test_config_validation():
    """設定検証テスト"""
    print("=== 設定検証テスト ===")
    
    # 必要な環境変数をチェック
    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'ASSOCIATE_TAG'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing_vars.append(var)
        else:
            print(f"✓ {var}: 設定済み")
    
    if missing_vars:
        print(f"✗ 未設定の環境変数: {missing_vars}")
        print("\n.envファイルを編集して以下の値を設定してください:")
        for var in missing_vars:
            print(f"  {var}=実際の値")
    else:
        print("✓ すべての環境変数が設定されています")
    
    print("✓ 設定検証テスト完了\n")


def main():
    """メイン関数"""
    print("Amazon API接続テスト")
    print("=" * 50)
    
    # 各テストを実行
    test_config_validation()
    test_amazon_api_connection()
    test_mock_search()
    test_data_save_load()
    
    print("=" * 50)
    print("✓ Amazon API接続テスト完了！")
    print("\n次のステップ:")
    print("1. .envファイルに実際のAWS認証情報を設定")
    print("2. Amazon Associates Programに参加")
    print("3. 実際のAPI呼び出しテスト")
    print("4. Google Sheets連携の実装")


if __name__ == "__main__":
    main() 
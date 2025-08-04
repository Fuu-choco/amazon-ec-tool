#!/usr/bin/env python3
"""
モックAmazon APIテストスクリプト
審査期間中の開発用にモックデータでテスト
"""

import sys
import os
import json
from datetime import datetime

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from amazon_api.mock_client import mock_amazon_client
from data_processor.amazon_data_processor import amazon_data_processor
from utils.logger import logger


def test_mock_search():
    """モック検索テスト"""
    print("=== モック検索テスト ===")
    
    # テストキーワード
    test_keywords = ["iPhone", "Sony", "Nintendo"]
    
    for keyword in test_keywords:
        print(f"\nキーワード: {keyword}")
        
        # 検索実行
        result = mock_amazon_client.search_items(keyword, item_count=5)
        
        if result and "SearchResult" in result:
            items = result["SearchResult"]["Items"]
            print(f"検索結果: {len(items)}件")
            
            for i, item in enumerate(items[:3], 1):  # 最初の3件を表示
                title = item["ItemInfo"]["Title"]["DisplayValue"]
                brand = item["ItemInfo"]["ByLineInfo"]["Brand"]["DisplayValue"]
                price = item["Offers"]["CurrentPrice"]["Amount"]
                currency = item["Offers"]["CurrentPrice"]["Currency"]
                
                print(f"  {i}. {title}")
                print(f"     ブランド: {brand}")
                print(f"     価格: {price:,} {currency}")
        else:
            print("検索結果なし")
    
    print("✓ モック検索テスト完了\n")


def test_mock_item_details():
    """モック商品詳細テスト"""
    print("=== モック商品詳細テスト ===")
    
    # テストASIN
    test_asins = ["B08N5WRWNW"]
    
    for asin in test_asins:
        print(f"\nASIN: {asin}")
        
        # 商品詳細取得
        result = mock_amazon_client.get_items([asin])
        
        if result and "ItemsResult" in result:
            items = result["ItemsResult"]["Items"]
            
            if items:
                item = items[0]
                title = item["ItemInfo"]["Title"]["DisplayValue"]
                brand = item["ItemInfo"]["ByLineInfo"]["Brand"]["DisplayValue"]
                price = item["Offers"]["CurrentPrice"]["Amount"]
                currency = item["Offers"]["CurrentPrice"]["Currency"]
                
                print(f"商品名: {title}")
                print(f"ブランド: {brand}")
                print(f"価格: {price:,} {currency}")
                
                # 価格履歴
                if "PriceHistory" in item["Offers"]:
                    print("価格履歴:")
                    for history in item["Offers"]["PriceHistory"]:
                        print(f"  {history['date']}: {history['price']:,} {currency}")
                
                # レビュー詳細
                if "ReviewDetails" in item["CustomerReviews"]:
                    print("レビュー詳細:")
                    details = item["CustomerReviews"]["ReviewDetails"]
                    for star, data in details.items():
                        print(f"  {star}: {data['Percentage']}%")
            else:
                print("商品詳細なし")
        else:
            print("商品詳細取得エラー")
    
    print("✓ モック商品詳細テスト完了\n")


def test_mock_similar_items():
    """モック類似商品テスト"""
    print("=== モック類似商品テスト ===")
    
    # テストASIN
    test_asin = "B08N5WRWNW"
    
    print(f"ASIN: {test_asin}")
    
    # 類似商品取得
    result = mock_amazon_client.get_similar_items(test_asin, item_count=3)
    
    if result and "SimilarItemsResult" in result:
        items = result["SimilarItemsResult"]["Items"]
        print(f"類似商品: {len(items)}件")
        
        for i, item in enumerate(items, 1):
            title = item["ItemInfo"]["Title"]["DisplayValue"]
            brand = item["ItemInfo"]["ByLineInfo"]["Brand"]["DisplayValue"]
            price = item["Offers"]["CurrentPrice"]["Amount"]
            currency = item["Offers"]["CurrentPrice"]["Currency"]
            
            print(f"  {i}. {title}")
            print(f"     ブランド: {brand}")
            print(f"     価格: {price:,} {currency}")
    else:
        print("類似商品なし")
    
    print("✓ モック類似商品テスト完了\n")


def test_data_processing():
    """データ処理テスト"""
    print("=== データ処理テスト ===")
    
    # モック検索結果を取得
    search_result = mock_amazon_client.search_items("iPhone", item_count=3)
    
    if search_result and "SearchResult" in search_result:
        # データ正規化
        normalized_items = amazon_data_processor.normalize_search_result(search_result)
        
        print(f"正規化結果: {len(normalized_items)}件")
        
        for i, item in enumerate(normalized_items[:2], 1):
            print(f"\n商品 {i}:")
            print(f"  ASIN: {item['asin']}")
            print(f"  タイトル: {item['title']}")
            print(f"  ブランド: {item['brand']}")
            print(f"  現在価格: {item['current_price']:,} {item['currency']}")
            print(f"  割引率: {item['discount_rate']}%")
            print(f"  在庫状況: {item['availability']}")
            print(f"  評価: {item['rating']} ({item['review_count']}件)")
        
        # データ保存テスト
        test_file = "data/processed/mock_test_data.json"
        amazon_data_processor.save_to_json(normalized_items, test_file)
        print(f"\nデータ保存: {test_file}")
        
        # データ読み込みテスト
        loaded_data = amazon_data_processor.load_from_json(test_file)
        print(f"データ読み込み: {len(loaded_data)}件")
        
    else:
        print("検索結果なし")
    
    print("✓ データ処理テスト完了\n")


def test_rate_limiting():
    """レート制限テスト"""
    print("=== レート制限テスト ===")
    
    import time
    
    print("連続リクエストテスト（レート制限シミュレーション）")
    
    start_time = time.time()
    
    # 連続で5回リクエスト
    for i in range(5):
        result = mock_amazon_client.search_items("test", item_count=1)
        print(f"リクエスト {i+1}: {'成功' if result else '失敗'}")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"総実行時間: {elapsed_time:.2f}秒")
    print(f"平均リクエスト時間: {elapsed_time/5:.2f}秒")
    
    print("✓ レート制限テスト完了\n")


def main():
    """メイン関数"""
    print("モックAmazon APIテスト")
    print("=" * 50)
    
    # 各テストを実行
    test_mock_search()
    test_mock_item_details()
    test_mock_similar_items()
    test_data_processing()
    test_rate_limiting()
    
    print("=" * 50)
    print("✓ モックAmazon APIテスト完了！")
    print("\n次のステップ:")
    print("1. Amazonアソシエイトプログラムに申請")
    print("2. 審査期間中はモックデータで開発継続")
    print("3. Google Sheets連携の実装")
    print("4. 承認後に実際のAPI呼び出しテスト")


if __name__ == "__main__":
    main() 
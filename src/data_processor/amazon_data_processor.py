"""
Amazonデータ処理モジュール
取得したAmazon商品データを正規化・加工する機能を提供
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.utils.logger import get_logger


class AmazonDataProcessor:
    """Amazonデータ処理クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_logger("data_processor")
    
    def normalize_search_result(self, search_result: Dict) -> List[Dict]:
        """
        検索結果を正規化
        
        Args:
            search_result: Amazon API検索結果
            
        Returns:
            正規化された商品データリスト
        """
        try:
            normalized_items = []
            
            # 検索結果から商品リストを取得
            items = search_result.get('SearchResult', {}).get('Items', [])
            
            for item in items:
                normalized_item = self._normalize_item(item)
                if normalized_item:
                    normalized_items.append(normalized_item)
            
            self.logger.info(f"検索結果を正規化: {len(normalized_items)}件")
            return normalized_items
            
        except Exception as e:
            self.logger.error(f"検索結果正規化エラー: {e}")
            return []
    
    def normalize_items_result(self, items_result: Dict) -> List[Dict]:
        """
        商品詳細結果を正規化
        
        Args:
            items_result: Amazon API商品詳細結果
            
        Returns:
            正規化された商品データリスト
        """
        try:
            normalized_items = []
            
            # 商品詳細結果から商品リストを取得
            items = items_result.get('ItemsResult', {}).get('Items', [])
            
            for item in items:
                normalized_item = self._normalize_item(item)
                if normalized_item:
                    normalized_items.append(normalized_item)
            
            self.logger.info(f"商品詳細結果を正規化: {len(normalized_items)}件")
            return normalized_items
            
        except Exception as e:
            self.logger.error(f"商品詳細結果正規化エラー: {e}")
            return []
    
    def _normalize_item(self, item: Dict) -> Optional[Dict]:
        """
        個別商品データを正規化
        
        Args:
            item: 商品データ
            
        Returns:
            正規化された商品データ
        """
        try:
            # 基本情報
            asin = item.get('ASIN', '')
            title = item.get('ItemInfo', {}).get('Title', {}).get('DisplayValue', '')
            brand = item.get('ItemInfo', {}).get('ByLineInfo', {}).get('Brand', {}).get('DisplayValue', '')
            
            # 価格情報
            price_info = self._extract_price_info(item)
            
            # 在庫情報
            availability = self._extract_availability(item)
            
            # 評価情報
            rating_info = self._extract_rating_info(item)
            
            # 画像情報
            image_url = self._extract_image_url(item)
            
            # 正規化されたデータ
            normalized_item = {
                'asin': asin,
                'title': title,
                'brand': brand,
                'current_price': price_info.get('current_price'),
                'original_price': price_info.get('original_price'),
                'discount_rate': price_info.get('discount_rate'),
                'currency': price_info.get('currency', 'JPY'),
                'availability': availability,
                'rating': rating_info.get('rating'),
                'review_count': rating_info.get('review_count'),
                'image_url': image_url,
                'processed_at': datetime.now().isoformat()
            }
            
            return normalized_item
            
        except Exception as e:
            self.logger.error(f"商品データ正規化エラー: {e}")
            return None
    
    def _extract_price_info(self, item: Dict) -> Dict:
        """価格情報を抽出"""
        try:
            offers = item.get('Offers', {})
            list_price = offers.get('ListPrice', {})
            current_price = offers.get('CurrentPrice', {})
            
            # 現在価格
            current_price_amount = current_price.get('Amount', 0)
            current_price_currency = current_price.get('Currency', 'JPY')
            
            # 元価格
            original_price_amount = list_price.get('Amount', current_price_amount)
            original_price_currency = list_price.get('Currency', current_price_currency)
            
            # 割引率計算
            discount_rate = 0
            if original_price_amount > 0 and current_price_amount < original_price_amount:
                discount_rate = ((original_price_amount - current_price_amount) / original_price_amount) * 100
            
            return {
                'current_price': current_price_amount,
                'original_price': original_price_amount,
                'discount_rate': round(discount_rate, 2),
                'currency': current_price_currency
            }
            
        except Exception as e:
            self.logger.error(f"価格情報抽出エラー: {e}")
            return {
                'current_price': 0,
                'original_price': 0,
                'discount_rate': 0,
                'currency': 'JPY'
            }
    
    def _extract_availability(self, item: Dict) -> str:
        """在庫状況を抽出"""
        try:
            offers = item.get('Offers', {})
            availability = offers.get('Availability', {})
            return availability.get('Message', 'Unknown')
        except Exception as e:
            self.logger.error(f"在庫状況抽出エラー: {e}")
            return 'Unknown'
    
    def _extract_rating_info(self, item: Dict) -> Dict:
        """評価情報を抽出"""
        try:
            customer_reviews = item.get('CustomerReviews', {})
            rating = customer_reviews.get('Rating', 0)
            review_count = customer_reviews.get('ReviewCount', 0)
            
            return {
                'rating': rating,
                'review_count': review_count
            }
            
        except Exception as e:
            self.logger.error(f"評価情報抽出エラー: {e}")
            return {
                'rating': 0,
                'review_count': 0
            }
    
    def _extract_image_url(self, item: Dict) -> str:
        """画像URLを抽出"""
        try:
            images = item.get('Images', {})
            primary = images.get('Primary', {})
            return primary.get('Large', {}).get('URL', '')
        except Exception as e:
            self.logger.error(f"画像URL抽出エラー: {e}")
            return ''
    
    def save_to_json(self, data: List[Dict], filepath: str):
        """
        データをJSONファイルに保存
        
        Args:
            data: 保存するデータ
            filepath: 保存先ファイルパス
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"データを保存: {filepath}")
            
        except Exception as e:
            self.logger.error(f"データ保存エラー: {e}")
    
    def load_from_json(self, filepath: str) -> List[Dict]:
        """
        JSONファイルからデータを読み込み
        
        Args:
            filepath: 読み込みファイルパス
            
        Returns:
            読み込んだデータ
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"データを読み込み: {filepath}")
            return data
            
        except Exception as e:
            self.logger.error(f"データ読み込みエラー: {e}")
            return []


# グローバルデータ処理インスタンス
amazon_data_processor = AmazonDataProcessor() 
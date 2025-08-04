"""
Amazon Product Advertising API クライアント
商品データ取得の基本機能を提供
"""

import os
import time
import requests
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from typing import Dict, List, Optional, Any
from src.utils.config import config_manager
from src.utils.logger import get_logger


class AmazonAPIClient:
    """Amazon Product Advertising API クライアント"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_logger("amazon_api")
        self.config = config_manager.get_amazon_config()
        self.session = self._create_session()
        self.base_url = "https://webservices.amazon.co.jp/paapi5"
        
    def _create_session(self) -> boto3.Session:
        """AWSセッションを作成"""
        try:
            session = boto3.Session(
                aws_access_key_id=self.config.get('access_key_id'),
                aws_secret_access_key=self.config.get('secret_access_key'),
                region_name=self.config.get('region', 'us-east-1')
            )
            self.logger.info("AWSセッションを作成しました")
            return session
        except Exception as e:
            self.logger.error(f"AWSセッション作成エラー: {e}")
            raise
    
    def _sign_request(self, method: str, url: str, params: Dict = None, data: Dict = None) -> Dict:
        """
        AWS Signature Version 4 でリクエストに署名
        
        Args:
            method: HTTPメソッド
            url: リクエストURL
            params: クエリパラメータ
            data: リクエストボディ
            
        Returns:
            署名済みリクエストヘッダー
        """
        try:
            # リクエストを作成
            request = AWSRequest(
                method=method,
                url=url,
                data=data,
                params=params
            )
            
            # 署名を作成
            credentials = self.session.get_credentials()
            SigV4Auth(credentials, "us-east-1", "execute-api").add_auth(request)
            
            # 署名済みヘッダーを取得
            return dict(request.headers)
            
        except Exception as e:
            self.logger.error(f"リクエスト署名エラー: {e}")
            raise
    
    def search_items(self, keywords: str, search_index: str = "All", item_count: int = 10) -> Dict:
        """
        商品検索を実行
        
        Args:
            keywords: 検索キーワード
            search_index: 検索インデックス
            item_count: 取得件数
            
        Returns:
            検索結果
        """
        try:
            self.logger.info(f"商品検索を実行: {keywords}")
            
            # リクエストパラメータ
            params = {
                'Keywords': keywords,
                'SearchIndex': search_index,
                'ItemCount': item_count,
                'PartnerTag': self.config.get('associate_tag'),
                'PartnerType': 'Associates',
                'Marketplace': 'www.amazon.co.jp'
            }
            
            # リクエストURL
            url = f"{self.base_url}/searchitems"
            
            # 署名済みヘッダーを取得
            headers = self._sign_request('GET', url, params=params)
            
            # リクエストを実行
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"検索成功: {len(result.get('SearchResult', {}).get('Items', []))}件")
                return result
            else:
                self.logger.error(f"検索エラー: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            self.logger.error(f"商品検索エラー: {e}")
            return {}
    
    def get_items(self, asins: List[str]) -> Dict:
        """
        商品詳細情報を取得
        
        Args:
            asins: ASINリスト
            
        Returns:
            商品詳細情報
        """
        try:
            self.logger.info(f"商品詳細取得: {len(asins)}件")
            
            # リクエストパラメータ
            params = {
                'ItemIds': ','.join(asins),
                'PartnerTag': self.config.get('associate_tag'),
                'PartnerType': 'Associates',
                'Marketplace': 'www.amazon.co.jp'
            }
            
            # リクエストURL
            url = f"{self.base_url}/getitems"
            
            # 署名済みヘッダーを取得
            headers = self._sign_request('GET', url, params=params)
            
            # リクエストを実行
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"商品詳細取得成功: {len(result.get('ItemsResult', {}).get('Items', []))}件")
                return result
            else:
                self.logger.error(f"商品詳細取得エラー: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            self.logger.error(f"商品詳細取得エラー: {e}")
            return {}
    
    def get_similar_items(self, asin: str, item_count: int = 10) -> Dict:
        """
        類似商品を取得
        
        Args:
            asin: 商品ASIN
            item_count: 取得件数
            
        Returns:
            類似商品情報
        """
        try:
            self.logger.info(f"類似商品取得: {asin}")
            
            # リクエストパラメータ
            params = {
                'ItemId': asin,
                'ItemCount': item_count,
                'PartnerTag': self.config.get('associate_tag'),
                'PartnerType': 'Associates',
                'Marketplace': 'www.amazon.co.jp'
            }
            
            # リクエストURL
            url = f"{self.base_url}/getsimilaritems"
            
            # 署名済みヘッダーを取得
            headers = self._sign_request('GET', url, params=params)
            
            # リクエストを実行
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"類似商品取得成功: {len(result.get('SimilarItemsResult', {}).get('Items', []))}件")
                return result
            else:
                self.logger.error(f"類似商品取得エラー: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            self.logger.error(f"類似商品取得エラー: {e}")
            return {}
    
    def rate_limit_delay(self, seconds: float = 1.0):
        """
        レート制限対応のための遅延
        
        Args:
            seconds: 遅延秒数
        """
        time.sleep(seconds)
        self.logger.debug(f"レート制限対応: {seconds}秒遅延")


# グローバルクライアントインスタンス
amazon_client = AmazonAPIClient() 
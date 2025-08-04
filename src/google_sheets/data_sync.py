"""
Google Sheets データ同期モジュール
AmazonデータをGoogle Sheetsに反映する機能を提供
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.google_sheets.client import google_sheets_client
from src.utils.logger import get_logger


class GoogleSheetsDataSync:
    """Google Sheets データ同期クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_logger("google_sheets_sync")
        self.client = google_sheets_client
    
    def setup_spreadsheet_structure(self, spreadsheet_title: str = "Amazon EC Tool") -> Optional[str]:
        """
        スプレッドシート構造をセットアップ
        
        Args:
            spreadsheet_title: スプレッドシートのタイトル
            
        Returns:
            スプレッドシートID
        """
        try:
            # スプレッドシートを作成
            spreadsheet_id = self.client.create_spreadsheet(spreadsheet_title)
            
            if not spreadsheet_id:
                self.logger.error("スプレッドシートの作成に失敗しました")
                return None
            
            # スプレッドシートを開く
            spreadsheet = self.client.open_spreadsheet(spreadsheet_id)
            
            if not spreadsheet:
                self.logger.error("スプレッドシートを開けませんでした")
                return None
            
            # 各ワークシートを作成
            self._create_product_master_sheet(spreadsheet)
            self._create_price_history_sheet(spreadsheet)
            self._create_stock_management_sheet(spreadsheet)
            self._create_analysis_dashboard_sheet(spreadsheet)
            
            self.logger.info("スプレッドシート構造のセットアップが完了しました")
            return spreadsheet_id
            
        except Exception as e:
            self.logger.error(f"スプレッドシート構造セットアップエラー: {e}")
            return None
    
    def _create_product_master_sheet(self, spreadsheet):
        """商品マスターシートを作成"""
        try:
            worksheet = self.client.create_worksheet(spreadsheet, "商品マスター")
            
            if worksheet:
                # ヘッダーを設定
                headers = [
                    'ASIN', '商品タイトル', 'ブランド', 'カテゴリ', '現在価格', 
                    '元価格', '割引率(%)', '在庫状況', '評価', 'レビュー数', 
                    '画像URL', '最終更新日時'
                ]
                
                self.client.format_headers(worksheet, headers)
                
        except Exception as e:
            self.logger.error(f"商品マスターシート作成エラー: {e}")
    
    def _create_price_history_sheet(self, spreadsheet):
        """価格履歴シートを作成"""
        try:
            worksheet = self.client.create_worksheet(spreadsheet, "価格履歴")
            
            if worksheet:
                # ヘッダーを設定
                headers = [
                    '日付', 'ASIN', '商品タイトル', '価格', '価格変動', 
                    '変動率(%)', '割引率(%)', '更新日時'
                ]
                
                self.client.format_headers(worksheet, headers)
                
        except Exception as e:
            self.logger.error(f"価格履歴シート作成エラー: {e}")
    
    def _create_stock_management_sheet(self, spreadsheet):
        """在庫管理シートを作成"""
        try:
            worksheet = self.client.create_worksheet(spreadsheet, "在庫管理")
            
            if worksheet:
                # ヘッダーを設定
                headers = [
                    'ASIN', '商品タイトル', 'ブランド', '在庫状況', '在庫カテゴリ',
                    '最終確認日時', 'アラート'
                ]
                
                self.client.format_headers(worksheet, headers)
                
        except Exception as e:
            self.logger.error(f"在庫管理シート作成エラー: {e}")
    
    def _create_analysis_dashboard_sheet(self, spreadsheet):
        """分析ダッシュボードシートを作成"""
        try:
            worksheet = self.client.create_worksheet(spreadsheet, "分析ダッシュボード")
            
            if worksheet:
                # ヘッダーを設定
                headers = [
                    '分析項目', '値', '単位', '更新日時'
                ]
                
                self.client.format_headers(worksheet, headers)
                
        except Exception as e:
            self.logger.error(f"分析ダッシュボードシート作成エラー: {e}")
    
    def sync_product_data(self, product_data: List[Dict]):
        """
        商品データを同期
        
        Args:
            product_data: 商品データリスト
        """
        try:
            if not self.client.is_connected():
                self.logger.error("Google Sheets API に接続されていません")
                return
            
            # スプレッドシートを開く
            spreadsheet = self.client.open_spreadsheet()
            
            if not spreadsheet:
                self.logger.error("スプレッドシートを開けませんでした")
                return
            
            # 商品マスターシートを取得
            worksheet = spreadsheet.worksheet("商品マスター")
            
            if not worksheet:
                self.logger.error("商品マスターシートが見つかりません")
                return
            
            # データを2次元配列に変換
            data_rows = []
            for product in product_data:
                row = [
                    product.get('asin', ''),
                    product.get('title', ''),
                    product.get('brand', ''),
                    '',  # カテゴリ（後で追加）
                    product.get('current_price', 0),
                    product.get('original_price', 0),
                    product.get('discount_rate', 0),
                    product.get('availability', ''),
                    product.get('rating', 0),
                    product.get('review_count', 0),
                    product.get('image_url', ''),
                    product.get('processed_at', '')
                ]
                data_rows.append(row)
            
            # 既存データをクリア（ヘッダー以外）
            if len(data_rows) > 0:
                worksheet.clear()
                self.client.format_headers(worksheet, [
                    'ASIN', '商品タイトル', 'ブランド', 'カテゴリ', '現在価格', 
                    '元価格', '割引率(%)', '在庫状況', '評価', 'レビュー数', 
                    '画像URL', '最終更新日時'
                ])
                
                # データを追加
                self.client.append_rows(worksheet, data_rows)
            
            self.logger.info(f"商品データを同期しました: {len(product_data)}件")
            
        except Exception as e:
            self.logger.error(f"商品データ同期エラー: {e}")
    
    def sync_price_history(self, price_history: List[Dict]):
        """
        価格履歴を同期
        
        Args:
            price_history: 価格履歴データリスト
        """
        try:
            if not self.client.is_connected():
                self.logger.error("Google Sheets API に接続されていません")
                return
            
            # スプレッドシートを開く
            spreadsheet = self.client.open_spreadsheet()
            
            if not spreadsheet:
                self.logger.error("スプレッドシートを開けませんでした")
                return
            
            # 価格履歴シートを取得
            worksheet = spreadsheet.worksheet("価格履歴")
            
            if not worksheet:
                self.logger.error("価格履歴シートが見つかりません")
                return
            
            # データを2次元配列に変換
            data_rows = []
            for record in price_history:
                row = [
                    record.get('date', ''),
                    record.get('asin', ''),
                    record.get('title', ''),
                    record.get('price', 0),
                    record.get('price_change', 0),
                    record.get('change_percentage', 0),
                    record.get('discount_rate', 0),
                    record.get('processed_at', '')
                ]
                data_rows.append(row)
            
            # データを追加
            if data_rows:
                self.client.append_rows(worksheet, data_rows)
            
            self.logger.info(f"価格履歴を同期しました: {len(price_history)}件")
            
        except Exception as e:
            self.logger.error(f"価格履歴同期エラー: {e}")
    
    def sync_stock_data(self, stock_data: List[Dict]):
        """
        在庫データを同期
        
        Args:
            stock_data: 在庫データリスト
        """
        try:
            if not self.client.is_connected():
                self.logger.error("Google Sheets API に接続されていません")
                return
            
            # スプレッドシートを開く
            spreadsheet = self.client.open_spreadsheet()
            
            if not spreadsheet:
                self.logger.error("スプレッドシートを開けませんでした")
                return
            
            # 在庫管理シートを取得
            worksheet = spreadsheet.worksheet("在庫管理")
            
            if not worksheet:
                self.logger.error("在庫管理シートが見つかりません")
                return
            
            # データを2次元配列に変換
            data_rows = []
            for stock in stock_data:
                # 在庫カテゴリを判定
                availability = stock.get('availability', '').lower()
                if '在庫' in availability and 'なし' not in availability:
                    stock_category = '在庫あり'
                elif '在庫' in availability and 'なし' in availability:
                    stock_category = '在庫切れ'
                elif '予約' in availability:
                    stock_category = '予約商品'
                else:
                    stock_category = '不明'
                
                # アラートを判定
                alert = ''
                if stock_category == '在庫切れ':
                    alert = '在庫切れアラート'
                elif stock_category == '予約商品':
                    alert = '予約商品アラート'
                
                row = [
                    stock.get('asin', ''),
                    stock.get('title', ''),
                    stock.get('brand', ''),
                    stock.get('availability', ''),
                    stock_category,
                    stock.get('processed_at', ''),
                    alert
                ]
                data_rows.append(row)
            
            # 既存データをクリア（ヘッダー以外）
            if len(data_rows) > 0:
                worksheet.clear()
                self.client.format_headers(worksheet, [
                    'ASIN', '商品タイトル', 'ブランド', '在庫状況', '在庫カテゴリ',
                    '最終確認日時', 'アラート'
                ])
                
                # データを追加
                self.client.append_rows(worksheet, data_rows)
            
            self.logger.info(f"在庫データを同期しました: {len(stock_data)}件")
            
        except Exception as e:
            self.logger.error(f"在庫データ同期エラー: {e}")
    
    def update_analysis_dashboard(self, price_analysis: Dict, stock_analysis: Dict):
        """
        分析ダッシュボードを更新
        
        Args:
            price_analysis: 価格分析結果
            stock_analysis: 在庫分析結果
        """
        try:
            if not self.client.is_connected():
                self.logger.error("Google Sheets API に接続されていません")
                return
            
            # スプレッドシートを開く
            spreadsheet = self.client.open_spreadsheet()
            
            if not spreadsheet:
                self.logger.error("スプレッドシートを開けませんでした")
                return
            
            # 分析ダッシュボードシートを取得
            worksheet = spreadsheet.worksheet("分析ダッシュボード")
            
            if not worksheet:
                self.logger.error("分析ダッシュボードシートが見つかりません")
                return
            
            # 分析データを準備
            analysis_data = []
            current_time = datetime.now().isoformat()
            
            # 価格分析データ
            if price_analysis:
                price_stats = price_analysis.get('price_statistics', {})
                current_stats = price_stats.get('current_price', {})
                
                analysis_data.extend([
                    ['総レコード数', price_analysis.get('total_records', 0), '件', current_time],
                    ['現在価格最小値', current_stats.get('min', 0), '円', current_time],
                    ['現在価格最大値', current_stats.get('max', 0), '円', current_time],
                    ['現在価格平均値', round(current_stats.get('mean', 0), 2), '円', current_time],
                    ['割引商品数', price_analysis.get('discount_analysis', {}).get('total_discounted_items', 0), '件', current_time]
                ])
            
            # 在庫分析データ
            if stock_analysis:
                stock_summary = stock_analysis.get('stock_status_summary', {})
                
                analysis_data.extend([
                    ['総商品数', stock_analysis.get('total_items', 0), '件', current_time],
                    ['在庫あり商品数', stock_summary.get('in_stock', 0), '件', current_time],
                    ['在庫切れ商品数', stock_summary.get('out_of_stock', 0), '件', current_time],
                    ['予約商品数', stock_summary.get('pre_order', 0), '件', current_time],
                    ['在庫率', f"{stock_summary.get('in_stock', 0) / stock_summary.get('total', 1) * 100:.1f}", '%', current_time]
                ])
            
            # 既存データをクリア（ヘッダー以外）
            if analysis_data:
                worksheet.clear()
                self.client.format_headers(worksheet, [
                    '分析項目', '値', '単位', '更新日時'
                ])
                
                # データを追加
                self.client.append_rows(worksheet, analysis_data)
            
            self.logger.info("分析ダッシュボードを更新しました")
            
        except Exception as e:
            self.logger.error(f"分析ダッシュボード更新エラー: {e}")


# グローバルデータ同期インスタンス
google_sheets_sync = GoogleSheetsDataSync() 
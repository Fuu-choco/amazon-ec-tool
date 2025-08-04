"""
データエクスポートモジュール
分析結果をCSV、Excel、JSON形式でエクスポートする機能を提供
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.utils.logger import get_logger


class DataExporter:
    """データエクスポートクラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_logger("data_exporter")
    
    def export_to_csv(self, data: List[Dict], filepath: str, encoding: str = 'utf-8-sig'):
        """
        データをCSVファイルにエクスポート
        
        Args:
            data: エクスポートするデータ
            filepath: 出力ファイルパス
            encoding: エンコーディング
        """
        try:
            if not data:
                self.logger.warning("エクスポートするデータがありません")
                return
            
            # DataFrameに変換
            df = pd.DataFrame(data)
            
            # ディレクトリを作成
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # CSVファイルに出力
            df.to_csv(filepath, index=False, encoding=encoding)
            
            self.logger.info(f"CSVエクスポート完了: {filepath} ({len(data)}件)")
            
        except Exception as e:
            self.logger.error(f"CSVエクスポートエラー: {e}")
    
    def export_to_excel(self, data_dict: Dict[str, List[Dict]], filepath: str):
        """
        データをExcelファイルにエクスポート
        
        Args:
            data_dict: シート名とデータの辞書
            filepath: 出力ファイルパス
        """
        try:
            if not data_dict:
                self.logger.warning("エクスポートするデータがありません")
                return
            
            # ディレクトリを作成
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # ExcelWriterを作成
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                for sheet_name, data in data_dict.items():
                    if data:
                        df = pd.DataFrame(data)
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        self.logger.info(f"シート '{sheet_name}' に {len(data)}件 エクスポート")
            
            self.logger.info(f"Excelエクスポート完了: {filepath}")
            
        except Exception as e:
            self.logger.error(f"Excelエクスポートエラー: {e}")
    
    def export_price_analysis(self, price_data: List[Dict], analysis_result: Dict, filepath: str):
        """
        価格分析結果をエクスポート
        
        Args:
            price_data: 価格データ
            analysis_result: 分析結果
            filepath: 出力ファイルパス
        """
        try:
            # 複数のシートに分けてエクスポート
            excel_data = {
                '商品価格データ': price_data,
                '価格統計': self._format_price_statistics(analysis_result),
                '価格変動': self._format_price_changes(analysis_result),
                '割引分析': self._format_discount_analysis(analysis_result)
            }
            
            self.export_to_excel(excel_data, filepath)
            
        except Exception as e:
            self.logger.error(f"価格分析エクスポートエラー: {e}")
    
    def export_stock_analysis(self, stock_data: List[Dict], analysis_result: Dict, filepath: str):
        """
        在庫分析結果をエクスポート
        
        Args:
            stock_data: 在庫データ
            analysis_result: 分析結果
            filepath: 出力ファイルパス
        """
        try:
            # 複数のシートに分けてエクスポート
            excel_data = {
                '在庫データ': stock_data,
                '在庫状況サマリー': self._format_stock_summary(analysis_result),
                'ブランド別分析': self._format_brand_analysis(analysis_result),
                '在庫アラート': self._format_stock_alerts(analysis_result)
            }
            
            self.export_to_excel(excel_data, filepath)
            
        except Exception as e:
            self.logger.error(f"在庫分析エクスポートエラー: {e}")
    
    def _format_price_statistics(self, analysis_result: Dict) -> List[Dict]:
        """価格統計をフォーマット"""
        try:
            price_stats = analysis_result.get('price_statistics', {})
            formatted_data = []
            
            for price_type in ['current_price', 'original_price']:
                stats = price_stats.get(price_type, {})
                formatted_data.append({
                    '価格タイプ': price_type,
                    '最小値': stats.get('min', 0),
                    '最大値': stats.get('max', 0),
                    '平均値': stats.get('mean', 0),
                    '中央値': stats.get('median', 0)
                })
            
            return formatted_data
            
        except Exception as e:
            self.logger.error(f"価格統計フォーマットエラー: {e}")
            return []
    
    def _format_price_changes(self, analysis_result: Dict) -> List[Dict]:
        """価格変動をフォーマット"""
        try:
            price_changes = analysis_result.get('price_changes', [])
            formatted_data = []
            
            for change in price_changes:
                formatted_data.append({
                    '日付': change.get('date', ''),
                    'ASIN': change.get('asin', ''),
                    '前回価格': change.get('previous_price', 0),
                    '現在価格': change.get('current_price', 0),
                    '価格変動': change.get('price_change', 0),
                    '変動率(%)': change.get('price_change_percentage', 0),
                    '経過日数': change.get('days_since_previous', 0)
                })
            
            return formatted_data
            
        except Exception as e:
            self.logger.error(f"価格変動フォーマットエラー: {e}")
            return []
    
    def _format_discount_analysis(self, analysis_result: Dict) -> List[Dict]:
        """割引分析をフォーマット"""
        try:
            discount_analysis = analysis_result.get('discount_analysis', {})
            formatted_data = []
            
            # 基本統計
            stats = discount_analysis.get('discount_rate_statistics', {})
            formatted_data.append({
                '項目': '割引率統計',
                '最小値(%)': stats.get('min', 0),
                '最大値(%)': stats.get('max', 0),
                '平均値(%)': stats.get('mean', 0)
            })
            
            # カテゴリ別
            categories = discount_analysis.get('discount_categories', {})
            formatted_data.append({
                '項目': '小割引(10%以下)',
                '件数': categories.get('small_discount', 0)
            })
            formatted_data.append({
                '項目': '中割引(10-30%)',
                '件数': categories.get('medium_discount', 0)
            })
            formatted_data.append({
                '項目': '大割引(30%以上)',
                '件数': categories.get('large_discount', 0)
            })
            
            return formatted_data
            
        except Exception as e:
            self.logger.error(f"割引分析フォーマットエラー: {e}")
            return []
    
    def _format_stock_summary(self, analysis_result: Dict) -> List[Dict]:
        """在庫状況サマリーをフォーマット"""
        try:
            stock_summary = analysis_result.get('stock_status_summary', {})
            formatted_data = []
            
            formatted_data.append({
                '項目': '在庫あり',
                '件数': stock_summary.get('in_stock', 0)
            })
            formatted_data.append({
                '項目': '在庫切れ',
                '件数': stock_summary.get('out_of_stock', 0)
            })
            formatted_data.append({
                '項目': '予約商品',
                '件数': stock_summary.get('pre_order', 0)
            })
            formatted_data.append({
                '項目': '発送可能',
                '件数': stock_summary.get('shipping_available', 0)
            })
            formatted_data.append({
                '項目': '不明',
                '件数': stock_summary.get('unknown', 0)
            })
            
            return formatted_data
            
        except Exception as e:
            self.logger.error(f"在庫サマリーフォーマットエラー: {e}")
            return []
    
    def _format_brand_analysis(self, analysis_result: Dict) -> List[Dict]:
        """ブランド別分析をフォーマット"""
        try:
            brand_analysis = analysis_result.get('brand_analysis', {})
            formatted_data = []
            
            for brand, data in brand_analysis.items():
                formatted_data.append({
                    'ブランド': brand,
                    '総商品数': data.get('total_items', 0),
                    '在庫あり': data.get('in_stock', 0),
                    '在庫切れ': data.get('out_of_stock', 0),
                    '予約商品': data.get('pre_order', 0),
                    '在庫率(%)': data.get('availability_rate', 0)
                })
            
            return formatted_data
            
        except Exception as e:
            self.logger.error(f"ブランド分析フォーマットエラー: {e}")
            return []
    
    def _format_stock_alerts(self, analysis_result: Dict) -> List[Dict]:
        """在庫アラートをフォーマット"""
        try:
            stock_alerts = analysis_result.get('stock_alerts', [])
            formatted_data = []
            
            for alert in stock_alerts:
                formatted_data.append({
                    'アラートタイプ': alert.get('type', ''),
                    'ASIN': alert.get('asin', ''),
                    '商品タイトル': alert.get('title', ''),
                    'ブランド': alert.get('brand', ''),
                    '在庫状況': alert.get('availability', ''),
                    'アラートメッセージ': alert.get('alert_message', '')
                })
            
            return formatted_data
            
        except Exception as e:
            self.logger.error(f"在庫アラートフォーマットエラー: {e}")
            return []
    
    def generate_summary_report(self, price_analysis: Dict, stock_analysis: Dict) -> str:
        """
        サマリーレポートを生成
        
        Args:
            price_analysis: 価格分析結果
            stock_analysis: 在庫分析結果
            
        Returns:
            レポート文字列
        """
        try:
            report = []
            report.append("=== データ分析サマリーレポート ===")
            report.append(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 価格分析サマリー
            if price_analysis:
                report.append("\n--- 価格分析サマリー ---")
                report.append(f"総レコード数: {price_analysis.get('total_records', 0)}件")
                
                price_stats = price_analysis.get('price_statistics', {})
                if price_stats:
                    current_stats = price_stats.get('current_price', {})
                    report.append(f"現在価格範囲: ¥{current_stats.get('min', 0):,} 〜 ¥{current_stats.get('max', 0):,}")
                
                discount_analysis = price_analysis.get('discount_analysis', {})
                if discount_analysis:
                    report.append(f"割引商品数: {discount_analysis.get('total_discounted_items', 0)}件")
            
            # 在庫分析サマリー
            if stock_analysis:
                report.append("\n--- 在庫分析サマリー ---")
                report.append(f"総商品数: {stock_analysis.get('total_items', 0)}件")
                
                stock_summary = stock_analysis.get('stock_status_summary', {})
                if stock_summary:
                    in_stock = stock_summary.get('in_stock', 0)
                    total = stock_summary.get('total', 0)
                    if total > 0:
                        availability_rate = (in_stock / total) * 100
                        report.append(f"在庫率: {availability_rate:.1f}%")
                
                stock_alerts = stock_analysis.get('stock_alerts', [])
                if stock_alerts:
                    report.append(f"在庫アラート: {len(stock_alerts)}件")
            
            return "\n".join(report)
            
        except Exception as e:
            self.logger.error(f"サマリーレポート生成エラー: {e}")
            return "サマリーレポート生成に失敗しました"


# グローバルデータエクスポートインスタンス
data_exporter = DataExporter() 
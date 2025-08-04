"""
価格変動分析モジュール
商品価格の変動を分析・可視化する機能を提供
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from src.utils.logger import get_logger


class PriceAnalyzer:
    """価格変動分析クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_logger("price_analyzer")
    
    def analyze_price_changes(self, price_history: List[Dict]) -> Dict:
        """
        価格変動を分析
        
        Args:
            price_history: 価格履歴データ
            
        Returns:
            価格変動分析結果
        """
        try:
            if not price_history:
                return {}
            
            # DataFrameに変換
            df = pd.DataFrame(price_history)
            df['date'] = pd.to_datetime(df['processed_at'])
            df = df.sort_values('date')
            
            analysis_result = {
                'total_records': len(df),
                'date_range': {
                    'start': df['date'].min().isoformat(),
                    'end': df['date'].max().isoformat()
                },
                'price_statistics': self._calculate_price_statistics(df),
                'price_changes': self._calculate_price_changes(df),
                'discount_analysis': self._analyze_discounts(df),
                'trend_analysis': self._analyze_trends(df)
            }
            
            self.logger.info(f"価格変動分析完了: {len(df)}件")
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"価格変動分析エラー: {e}")
            return {}
    
    def _calculate_price_statistics(self, df: pd.DataFrame) -> Dict:
        """価格統計を計算"""
        try:
            current_prices = df['current_price'].dropna()
            original_prices = df['original_price'].dropna()
            
            return {
                'current_price': {
                    'min': float(current_prices.min()) if len(current_prices) > 0 else 0,
                    'max': float(current_prices.max()) if len(current_prices) > 0 else 0,
                    'mean': float(current_prices.mean()) if len(current_prices) > 0 else 0,
                    'median': float(current_prices.median()) if len(current_prices) > 0 else 0
                },
                'original_price': {
                    'min': float(original_prices.min()) if len(original_prices) > 0 else 0,
                    'max': float(original_prices.max()) if len(original_prices) > 0 else 0,
                    'mean': float(original_prices.mean()) if len(original_prices) > 0 else 0,
                    'median': float(original_prices.median()) if len(original_prices) > 0 else 0
                }
            }
        except Exception as e:
            self.logger.error(f"価格統計計算エラー: {e}")
            return {}
    
    def _calculate_price_changes(self, df: pd.DataFrame) -> List[Dict]:
        """価格変動を計算"""
        try:
            changes = []
            
            # 時系列でソート
            df_sorted = df.sort_values('date')
            
            for i in range(1, len(df_sorted)):
                current = df_sorted.iloc[i]
                previous = df_sorted.iloc[i-1]
                
                # 価格変動を計算
                price_change = current['current_price'] - previous['current_price']
                price_change_percentage = 0
                
                if previous['current_price'] > 0:
                    price_change_percentage = (price_change / previous['current_price']) * 100
                
                change_record = {
                    'date': current['date'].isoformat(),
                    'asin': current['asin'],
                    'previous_price': float(previous['current_price']),
                    'current_price': float(current['current_price']),
                    'price_change': float(price_change),
                    'price_change_percentage': round(price_change_percentage, 2),
                    'days_since_previous': (current['date'] - previous['date']).days
                }
                
                changes.append(change_record)
            
            return changes
            
        except Exception as e:
            self.logger.error(f"価格変動計算エラー: {e}")
            return []
    
    def _analyze_discounts(self, df: pd.DataFrame) -> Dict:
        """割引分析"""
        try:
            # 割引率が0より大きい商品を抽出
            discounted_items = df[df['discount_rate'] > 0]
            
            return {
                'total_discounted_items': len(discounted_items),
                'discount_rate_statistics': {
                    'min': float(discounted_items['discount_rate'].min()) if len(discounted_items) > 0 else 0,
                    'max': float(discounted_items['discount_rate'].max()) if len(discounted_items) > 0 else 0,
                    'mean': float(discounted_items['discount_rate'].mean()) if len(discounted_items) > 0 else 0
                },
                'discount_categories': {
                    'small_discount': len(discounted_items[discounted_items['discount_rate'] <= 10]),
                    'medium_discount': len(discounted_items[(discounted_items['discount_rate'] > 10) & (discounted_items['discount_rate'] <= 30)]),
                    'large_discount': len(discounted_items[discounted_items['discount_rate'] > 30])
                }
            }
            
        except Exception as e:
            self.logger.error(f"割引分析エラー: {e}")
            return {}
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict:
        """価格トレンド分析"""
        try:
            # 最新のデータを取得
            latest_data = df.sort_values('date').tail(10)
            
            if len(latest_data) < 2:
                return {'trend': 'insufficient_data'}
            
            # 価格トレンドを計算
            price_trend = latest_data['current_price'].pct_change().mean()
            
            trend_direction = 'stable'
            if price_trend > 0.05:
                trend_direction = 'increasing'
            elif price_trend < -0.05:
                trend_direction = 'decreasing'
            
            return {
                'trend_direction': trend_direction,
                'trend_strength': abs(price_trend),
                'recent_price_change': float(latest_data['current_price'].iloc[-1] - latest_data['current_price'].iloc[0])
            }
            
        except Exception as e:
            self.logger.error(f"トレンド分析エラー: {e}")
            return {}
    
    def detect_price_alerts(self, current_data: List[Dict], threshold: float = 10.0) -> List[Dict]:
        """
        価格アラートを検出
        
        Args:
            current_data: 現在の価格データ
            threshold: アラート閾値（%）
            
        Returns:
            アラートリスト
        """
        try:
            alerts = []
            
            for item in current_data:
                # 割引率が閾値を超える場合
                if item.get('discount_rate', 0) >= threshold:
                    alert = {
                        'type': 'discount_alert',
                        'asin': item['asin'],
                        'title': item['title'],
                        'current_price': item['current_price'],
                        'original_price': item['original_price'],
                        'discount_rate': item['discount_rate'],
                        'alert_message': f"大幅割引: {item['discount_rate']}%OFF"
                    }
                    alerts.append(alert)
                
                # 価格が大幅に上昇した場合
                if item.get('price_change_percentage', 0) >= threshold:
                    alert = {
                        'type': 'price_increase_alert',
                        'asin': item['asin'],
                        'title': item['title'],
                        'price_change_percentage': item['price_change_percentage'],
                        'alert_message': f"価格上昇: {item['price_change_percentage']}%UP"
                    }
                    alerts.append(alert)
            
            self.logger.info(f"価格アラート検出: {len(alerts)}件")
            return alerts
            
        except Exception as e:
            self.logger.error(f"価格アラート検出エラー: {e}")
            return []
    
    def generate_price_report(self, analysis_result: Dict) -> str:
        """
        価格分析レポートを生成
        
        Args:
            analysis_result: 分析結果
            
        Returns:
            レポート文字列
        """
        try:
            report = []
            report.append("=== 価格分析レポート ===")
            report.append(f"分析期間: {analysis_result.get('date_range', {}).get('start', 'N/A')} 〜 {analysis_result.get('date_range', {}).get('end', 'N/A')}")
            report.append(f"総レコード数: {analysis_result.get('total_records', 0)}件")
            
            # 価格統計
            price_stats = analysis_result.get('price_statistics', {})
            if price_stats:
                report.append("\n--- 価格統計 ---")
                current_stats = price_stats.get('current_price', {})
                report.append(f"現在価格 - 最小: ¥{current_stats.get('min', 0):,}, 最大: ¥{current_stats.get('max', 0):,}, 平均: ¥{current_stats.get('mean', 0):,.0f}")
            
            # 割引分析
            discount_analysis = analysis_result.get('discount_analysis', {})
            if discount_analysis:
                report.append("\n--- 割引分析 ---")
                report.append(f"割引商品数: {discount_analysis.get('total_discounted_items', 0)}件")
                discount_cats = discount_analysis.get('discount_categories', {})
                report.append(f"小割引(10%以下): {discount_cats.get('small_discount', 0)}件")
                report.append(f"中割引(10-30%): {discount_cats.get('medium_discount', 0)}件")
                report.append(f"大割引(30%以上): {discount_cats.get('large_discount', 0)}件")
            
            # トレンド分析
            trend_analysis = analysis_result.get('trend_analysis', {})
            if trend_analysis:
                report.append("\n--- 価格トレンド ---")
                report.append(f"トレンド方向: {trend_analysis.get('trend_direction', 'unknown')}")
                report.append(f"トレンド強度: {trend_analysis.get('trend_strength', 0):.2f}")
            
            return "\n".join(report)
            
        except Exception as e:
            self.logger.error(f"レポート生成エラー: {e}")
            return "レポート生成に失敗しました"


# グローバル価格分析インスタンス
price_analyzer = PriceAnalyzer() 
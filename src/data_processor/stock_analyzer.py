"""
在庫分析モジュール
商品在庫状況を分析・監視する機能を提供
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from src.utils.logger import get_logger


class StockAnalyzer:
    """在庫分析クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_logger("stock_analyzer")
    
    def analyze_stock_status(self, stock_data: List[Dict]) -> Dict:
        """
        在庫状況を分析
        
        Args:
            stock_data: 在庫データ
            
        Returns:
            在庫分析結果
        """
        try:
            if not stock_data:
                return {}
            
            # DataFrameに変換
            df = pd.DataFrame(stock_data)
            df['date'] = pd.to_datetime(df['processed_at'])
            df = df.sort_values('date')
            
            analysis_result = {
                'total_items': len(df),
                'stock_status_summary': self._analyze_stock_status(df),
                'availability_trends': self._analyze_availability_trends(df),
                'stock_alerts': self._detect_stock_alerts(df),
                'brand_analysis': self._analyze_by_brand(df)
            }
            
            self.logger.info(f"在庫分析完了: {len(df)}件")
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"在庫分析エラー: {e}")
            return {}
    
    def _analyze_stock_status(self, df: pd.DataFrame) -> Dict:
        """在庫状況の概要を分析"""
        try:
            # 在庫状況をカテゴリ化
            def categorize_availability(availability):
                availability_lower = str(availability).lower()
                if '在庫' in availability_lower and 'なし' not in availability_lower:
                    return 'in_stock'
                elif '在庫' in availability_lower and 'なし' in availability_lower:
                    return 'out_of_stock'
                elif '予約' in availability_lower:
                    return 'pre_order'
                elif '発送' in availability_lower:
                    return 'shipping_available'
                else:
                    return 'unknown'
            
            df['stock_category'] = df['availability'].apply(categorize_availability)
            
            # カテゴリ別集計
            status_counts = df['stock_category'].value_counts().to_dict()
            
            return {
                'in_stock': status_counts.get('in_stock', 0),
                'out_of_stock': status_counts.get('out_of_stock', 0),
                'pre_order': status_counts.get('pre_order', 0),
                'shipping_available': status_counts.get('shipping_available', 0),
                'unknown': status_counts.get('unknown', 0),
                'total': len(df)
            }
            
        except Exception as e:
            self.logger.error(f"在庫状況分析エラー: {e}")
            return {}
    
    def _analyze_availability_trends(self, df: pd.DataFrame) -> Dict:
        """在庫状況のトレンドを分析"""
        try:
            # 日付別の在庫状況を集計
            daily_status = df.groupby(['date', 'stock_category']).size().unstack(fill_value=0)
            
            # 最新の状況
            latest_date = df['date'].max()
            latest_status = df[df['date'] == latest_date]['stock_category'].value_counts().to_dict()
            
            # 前回との比較
            previous_date = latest_date - timedelta(days=1)
            previous_status = df[df['date'] == previous_date]['stock_category'].value_counts().to_dict()
            
            # 変化を計算
            changes = {}
            for category in ['in_stock', 'out_of_stock', 'pre_order']:
                current = latest_status.get(category, 0)
                previous = previous_status.get(category, 0)
                changes[category] = current - previous
            
            return {
                'latest_status': latest_status,
                'previous_status': previous_status,
                'changes': changes,
                'latest_date': latest_date.isoformat(),
                'previous_date': previous_date.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"在庫トレンド分析エラー: {e}")
            return {}
    
    def _detect_stock_alerts(self, df: pd.DataFrame) -> List[Dict]:
        """在庫アラートを検出"""
        try:
            alerts = []
            
            # 最新のデータを取得
            latest_data = df.sort_values('date').groupby('asin').tail(1)
            
            for _, item in latest_data.iterrows():
                # 在庫切れアラート
                if item['stock_category'] == 'out_of_stock':
                    alert = {
                        'type': 'out_of_stock',
                        'asin': item['asin'],
                        'title': item['title'],
                        'brand': item['brand'],
                        'availability': item['availability'],
                        'alert_message': f"在庫切れ: {item['title']}"
                    }
                    alerts.append(alert)
                
                # 予約商品アラート
                elif item['stock_category'] == 'pre_order':
                    alert = {
                        'type': 'pre_order',
                        'asin': item['asin'],
                        'title': item['title'],
                        'brand': item['brand'],
                        'availability': item['availability'],
                        'alert_message': f"予約商品: {item['title']}"
                    }
                    alerts.append(alert)
            
            self.logger.info(f"在庫アラート検出: {len(alerts)}件")
            return alerts
            
        except Exception as e:
            self.logger.error(f"在庫アラート検出エラー: {e}")
            return []
    
    def _analyze_by_brand(self, df: pd.DataFrame) -> Dict:
        """ブランド別在庫分析"""
        try:
            # ブランド別の在庫状況を集計
            brand_analysis = {}
            
            for brand in df['brand'].unique():
                if pd.isna(brand) or brand == '':
                    continue
                
                brand_data = df[df['brand'] == brand]
                brand_status = brand_data['stock_category'].value_counts().to_dict()
                
                brand_analysis[brand] = {
                    'total_items': len(brand_data),
                    'in_stock': brand_status.get('in_stock', 0),
                    'out_of_stock': brand_status.get('out_of_stock', 0),
                    'pre_order': brand_status.get('pre_order', 0),
                    'availability_rate': (brand_status.get('in_stock', 0) / len(brand_data)) * 100 if len(brand_data) > 0 else 0
                }
            
            return brand_analysis
            
        except Exception as e:
            self.logger.error(f"ブランド別分析エラー: {e}")
            return {}
    
    def generate_stock_report(self, analysis_result: Dict) -> str:
        """
        在庫分析レポートを生成
        
        Args:
            analysis_result: 分析結果
            
        Returns:
            レポート文字列
        """
        try:
            report = []
            report.append("=== 在庫分析レポート ===")
            report.append(f"総商品数: {analysis_result.get('total_items', 0)}件")
            
            # 在庫状況サマリー
            stock_summary = analysis_result.get('stock_status_summary', {})
            if stock_summary:
                report.append("\n--- 在庫状況サマリー ---")
                report.append(f"在庫あり: {stock_summary.get('in_stock', 0)}件")
                report.append(f"在庫切れ: {stock_summary.get('out_of_stock', 0)}件")
                report.append(f"予約商品: {stock_summary.get('pre_order', 0)}件")
                report.append(f"発送可能: {stock_summary.get('shipping_available', 0)}件")
                
                # 在庫率を計算
                total = stock_summary.get('total', 0)
                in_stock = stock_summary.get('in_stock', 0)
                if total > 0:
                    availability_rate = (in_stock / total) * 100
                    report.append(f"在庫率: {availability_rate:.1f}%")
            
            # 在庫アラート
            stock_alerts = analysis_result.get('stock_alerts', [])
            if stock_alerts:
                report.append("\n--- 在庫アラート ---")
                for alert in stock_alerts:
                    report.append(f"• {alert['alert_message']}")
            
            # ブランド別分析
            brand_analysis = analysis_result.get('brand_analysis', {})
            if brand_analysis:
                report.append("\n--- ブランド別分析 ---")
                for brand, data in brand_analysis.items():
                    report.append(f"{brand}: {data['in_stock']}件在庫 / {data['total_items']}件総数 ({data['availability_rate']:.1f}%)")
            
            return "\n".join(report)
            
        except Exception as e:
            self.logger.error(f"在庫レポート生成エラー: {e}")
            return "在庫レポート生成に失敗しました"
    
    def predict_stock_shortage(self, stock_history: List[Dict], days_ahead: int = 7) -> List[Dict]:
        """
        在庫不足を予測
        
        Args:
            stock_history: 在庫履歴データ
            days_ahead: 予測日数
            
        Returns:
            予測結果リスト
        """
        try:
            predictions = []
            
            # 時系列データを分析
            df = pd.DataFrame(stock_history)
            df['date'] = pd.to_datetime(df['processed_at'])
            
            # 商品別の在庫状況変化を分析
            for asin in df['asin'].unique():
                item_data = df[df['asin'] == asin].sort_values('date')
                
                if len(item_data) < 2:
                    continue
                
                # 最近の在庫状況変化を分析
                recent_data = item_data.tail(5)
                out_of_stock_count = len(recent_data[recent_data['stock_category'] == 'out_of_stock'])
                
                # 在庫切れが増加傾向の場合
                if out_of_stock_count >= 3:
                    prediction = {
                        'asin': asin,
                        'title': item_data.iloc[-1]['title'],
                        'brand': item_data.iloc[-1]['brand'],
                        'prediction': 'likely_shortage',
                        'confidence': min(out_of_stock_count / 5 * 100, 100),
                        'reason': f"過去5回中{out_of_stock_count}回在庫切れ",
                        'predicted_date': (datetime.now() + timedelta(days=days_ahead)).isoformat()
                    }
                    predictions.append(prediction)
            
            self.logger.info(f"在庫不足予測: {len(predictions)}件")
            return predictions
            
        except Exception as e:
            self.logger.error(f"在庫不足予測エラー: {e}")
            return []


# グローバル在庫分析インスタンス
stock_analyzer = StockAnalyzer() 
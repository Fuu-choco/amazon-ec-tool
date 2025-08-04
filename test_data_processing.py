#!/usr/bin/env python3
"""
データ処理機能テストスクリプト
価格分析、在庫分析、データエクスポート機能をテスト
"""

import sys
import os
import json
from datetime import datetime, timedelta

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_processor.price_analyzer import price_analyzer
from data_processor.stock_analyzer import stock_analyzer
from data_processor.data_exporter import data_exporter
from utils.logger import logger


def generate_test_price_data():
    """テスト用価格データを生成"""
    test_data = []
    
    # 過去7日間のデータを生成
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        
        # 複数の商品データ
        for j in range(3):
            base_price = 1000 + (j * 500)
            discount = (i % 3) * 10  # 0%, 10%, 20%の割引
            current_price = base_price * (1 - discount / 100)
            
            test_data.append({
                'asin': f'B08N5WRWNW{j}',
                'title': f'テスト商品{j+1}',
                'brand': f'テストブランド{j+1}',
                'current_price': current_price,
                'original_price': base_price,
                'discount_rate': discount,
                'currency': 'JPY',
                'availability': '在庫あり',
                'rating': 4.0 + (j * 0.5),
                'review_count': 100 + (j * 50),
                'image_url': f'https://example.com/image{j}.jpg',
                'processed_at': date.isoformat()
            })
    
    return test_data


def generate_test_stock_data():
    """テスト用在庫データを生成"""
    test_data = []
    
    # 複数の商品の在庫データ
    stock_statuses = ['在庫あり', '在庫切れ', '予約商品', '発送可能']
    
    for i in range(10):
        status = stock_statuses[i % len(stock_statuses)]
        
        test_data.append({
            'asin': f'B08N5WRWNW{i}',
            'title': f'テスト商品{i+1}',
            'brand': f'テストブランド{(i % 3) + 1}',
            'current_price': 1000 + (i * 100),
            'original_price': 1200 + (i * 100),
            'discount_rate': (i % 4) * 5,
            'currency': 'JPY',
            'availability': status,
            'rating': 4.0 + (i * 0.1),
            'review_count': 50 + (i * 10),
            'image_url': f'https://example.com/image{i}.jpg',
            'processed_at': datetime.now().isoformat()
        })
    
    return test_data


def test_price_analysis():
    """価格分析機能のテスト"""
    print("=== 価格分析機能テスト ===")
    
    # テストデータを生成
    test_data = generate_test_price_data()
    print(f"テストデータ生成: {len(test_data)}件")
    
    # 価格分析を実行
    analysis_result = price_analyzer.analyze_price_changes(test_data)
    
    if analysis_result:
        print("✓ 価格分析完了")
        print(f"  総レコード数: {analysis_result.get('total_records', 0)}件")
        
        # 価格統計を表示
        price_stats = analysis_result.get('price_statistics', {})
        if price_stats:
            current_stats = price_stats.get('current_price', {})
            print(f"  現在価格 - 最小: ¥{current_stats.get('min', 0):,}, 最大: ¥{current_stats.get('max', 0):,}")
        
        # 割引分析を表示
        discount_analysis = analysis_result.get('discount_analysis', {})
        if discount_analysis:
            print(f"  割引商品数: {discount_analysis.get('total_discounted_items', 0)}件")
        
        # レポートを生成
        report = price_analyzer.generate_price_report(analysis_result)
        print("\n--- 価格分析レポート ---")
        print(report)
        
    else:
        print("✗ 価格分析失敗")
    
    print()


def test_stock_analysis():
    """在庫分析機能のテスト"""
    print("=== 在庫分析機能テスト ===")
    
    # テストデータを生成
    test_data = generate_test_stock_data()
    print(f"テストデータ生成: {len(test_data)}件")
    
    # 在庫分析を実行
    analysis_result = stock_analyzer.analyze_stock_status(test_data)
    
    if analysis_result:
        print("✓ 在庫分析完了")
        print(f"  総商品数: {analysis_result.get('total_items', 0)}件")
        
        # 在庫状況サマリーを表示
        stock_summary = analysis_result.get('stock_status_summary', {})
        if stock_summary:
            print(f"  在庫あり: {stock_summary.get('in_stock', 0)}件")
            print(f"  在庫切れ: {stock_summary.get('out_of_stock', 0)}件")
            print(f"  予約商品: {stock_summary.get('pre_order', 0)}件")
        
        # 在庫アラートを表示
        stock_alerts = analysis_result.get('stock_alerts', [])
        if stock_alerts:
            print(f"  在庫アラート: {len(stock_alerts)}件")
            for alert in stock_alerts[:3]:  # 最初の3件のみ表示
                print(f"    • {alert['alert_message']}")
        
        # レポートを生成
        report = stock_analyzer.generate_stock_report(analysis_result)
        print("\n--- 在庫分析レポート ---")
        print(report)
        
    else:
        print("✗ 在庫分析失敗")
    
    print()


def test_data_export():
    """データエクスポート機能のテスト"""
    print("=== データエクスポート機能テスト ===")
    
    # テストデータを生成
    price_data = generate_test_price_data()
    stock_data = generate_test_stock_data()
    
    # 価格分析を実行
    price_analysis = price_analyzer.analyze_price_changes(price_data)
    
    # 在庫分析を実行
    stock_analysis = stock_analyzer.analyze_stock_status(stock_data)
    
    # CSVエクスポートテスト
    csv_file = "data/processed/test_price_data.csv"
    data_exporter.export_to_csv(price_data, csv_file)
    
    # Excelエクスポートテスト
    excel_file = "data/processed/test_analysis.xlsx"
    data_exporter.export_price_analysis(price_data, price_analysis, excel_file)
    data_exporter.export_stock_analysis(stock_data, stock_analysis, excel_file)
    
    # サマリーレポート生成
    summary_report = data_exporter.generate_summary_report(price_analysis, stock_analysis)
    print("\n--- サマリーレポート ---")
    print(summary_report)
    
    print("✓ データエクスポート完了")
    print(f"  CSVファイル: {csv_file}")
    print(f"  Excelファイル: {excel_file}")
    print()


def test_price_alerts():
    """価格アラート機能のテスト"""
    print("=== 価格アラート機能テスト ===")
    
    # テストデータを生成（大幅割引を含む）
    test_data = generate_test_price_data()
    
    # 大幅割引のテストデータを追加
    test_data.append({
        'asin': 'B08N5WRWNW999',
        'title': '大幅割引商品',
        'brand': 'テストブランド',
        'current_price': 500,
        'original_price': 2000,
        'discount_rate': 75.0,  # 75%割引
        'currency': 'JPY',
        'availability': '在庫あり',
        'rating': 4.5,
        'review_count': 200,
        'image_url': 'https://example.com/image999.jpg',
        'processed_at': datetime.now().isoformat()
    })
    
    # 価格アラートを検出
    alerts = price_analyzer.detect_price_alerts(test_data, threshold=10.0)
    
    if alerts:
        print(f"✓ 価格アラート検出: {len(alerts)}件")
        for alert in alerts:
            print(f"  • {alert['alert_message']}")
    else:
        print("✗ 価格アラート検出: なし")
    
    print()


def test_stock_predictions():
    """在庫予測機能のテスト"""
    print("=== 在庫予測機能テスト ===")
    
    # テスト用在庫履歴データを生成
    stock_history = []
    
    # 過去10日間のデータを生成
    for i in range(10):
        date = datetime.now() - timedelta(days=i)
        
        # 在庫切れが増加傾向の商品
        if i < 5:
            status = '在庫切れ' if i >= 3 else '在庫あり'
        else:
            status = '在庫あり'
        
        stock_history.append({
            'asin': 'B08N5WRWNW001',
            'title': '在庫不足予測商品',
            'brand': 'テストブランド',
            'availability': status,
            'processed_at': date.isoformat()
        })
    
    # 在庫不足を予測
    predictions = stock_analyzer.predict_stock_shortage(stock_history)
    
    if predictions:
        print(f"✓ 在庫不足予測: {len(predictions)}件")
        for prediction in predictions:
            print(f"  • {prediction['title']}: {prediction['confidence']:.1f}%確信度")
    else:
        print("✗ 在庫不足予測: なし")
    
    print()


def main():
    """メイン関数"""
    print("データ処理機能テスト")
    print("=" * 50)
    
    # 各テストを実行
    test_price_analysis()
    test_stock_analysis()
    test_data_export()
    test_price_alerts()
    test_stock_predictions()
    
    print("=" * 50)
    print("✓ データ処理機能テスト完了！")
    print("\n次のステップ:")
    print("1. Google Sheets連携の実装")
    print("2. 自動化機能の実装")
    print("3. 定期実行機能の実装")


if __name__ == "__main__":
    main() 
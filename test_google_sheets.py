#!/usr/bin/env python3
"""
Google Sheets連携テストスクリプト
Google Sheets API接続とデータ同期機能をテスト
"""

import sys
import os
from datetime import datetime, timedelta

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from google_sheets.client import google_sheets_client
from google_sheets.data_sync import google_sheets_sync
from data_processor.amazon_data_processor import amazon_data_processor
from utils.logger import logger


def test_google_sheets_connection():
    """Google Sheets API接続テスト"""
    print("=== Google Sheets API接続テスト ===")
    
    # 接続状態を確認
    if google_sheets_client.is_connected():
        print("✓ Google Sheets API接続: 成功")
        
        # 設定を確認
        config = google_sheets_client.config
        print(f"認証ファイル: {config.get('credentials_file', '未設定')}")
        print(f"スプレッドシートID: {config.get('spreadsheet_id', '未設定')}")
        
    else:
        print("✗ Google Sheets API接続: 失敗")
        print("\n設定が必要です:")
        print("1. Google Cloud Consoleでプロジェクトを作成")
        print("2. Google Sheets APIを有効化")
        print("3. サービスアカウントを作成")
        print("4. 認証キー（JSON）をダウンロード")
        print("5. credentials.jsonとして保存")
    
    print()


def test_spreadsheet_creation():
    """スプレッドシート作成テスト"""
    print("=== スプレッドシート作成テスト ===")
    
    try:
        # テスト用スプレッドシートを作成
        spreadsheet_id = google_sheets_sync.setup_spreadsheet_structure("Amazon EC Tool Test")
        
        if spreadsheet_id:
            print(f"✓ スプレッドシート作成: 成功 (ID: {spreadsheet_id})")
            print("作成されたワークシート:")
            print("  • 商品マスター")
            print("  • 価格履歴")
            print("  • 在庫管理")
            print("  • 分析ダッシュボード")
            
            # 設定ファイルを更新
            update_config_with_spreadsheet_id(spreadsheet_id)
            
        else:
            print("✗ スプレッドシート作成: 失敗")
            
    except Exception as e:
        print(f"✗ スプレッドシート作成エラー: {e}")
    
    print()


def test_data_sync():
    """データ同期テスト"""
    print("=== データ同期テスト ===")
    
    try:
        # テストデータを生成
        test_product_data = generate_test_product_data()
        test_stock_data = generate_test_stock_data()
        
        print(f"テストデータ生成: 商品{len(test_product_data)}件, 在庫{len(test_stock_data)}件")
        
        # 商品データを同期
        google_sheets_sync.sync_product_data(test_product_data)
        
        # 在庫データを同期
        google_sheets_sync.sync_stock_data(test_stock_data)
        
        print("✓ データ同期: 成功")
        
    except Exception as e:
        print(f"✗ データ同期エラー: {e}")
    
    print()


def test_analysis_dashboard():
    """分析ダッシュボードテスト"""
    print("=== 分析ダッシュボードテスト ===")
    
    try:
        # テスト用分析データを生成
        price_analysis = {
            'total_records': 10,
            'price_statistics': {
                'current_price': {
                    'min': 1000,
                    'max': 5000,
                    'mean': 2500
                }
            },
            'discount_analysis': {
                'total_discounted_items': 3
            }
        }
        
        stock_analysis = {
            'total_items': 10,
            'stock_status_summary': {
                'in_stock': 7,
                'out_of_stock': 1,
                'pre_order': 2,
                'total': 10
            }
        }
        
        # 分析ダッシュボードを更新
        google_sheets_sync.update_analysis_dashboard(price_analysis, stock_analysis)
        
        print("✓ 分析ダッシュボード更新: 成功")
        
    except Exception as e:
        print(f"✗ 分析ダッシュボード更新エラー: {e}")
    
    print()


def generate_test_product_data():
    """テスト用商品データを生成"""
    test_data = []
    
    for i in range(5):
        test_data.append({
            'asin': f'B08N5WRWNW{i}',
            'title': f'テスト商品{i+1}',
            'brand': f'テストブランド{(i % 3) + 1}',
            'current_price': 1000 + (i * 500),
            'original_price': 1200 + (i * 500),
            'discount_rate': (i % 4) * 10,
            'currency': 'JPY',
            'availability': '在庫あり' if i % 2 == 0 else '在庫切れ',
            'rating': 4.0 + (i * 0.2),
            'review_count': 50 + (i * 20),
            'image_url': f'https://example.com/image{i}.jpg',
            'processed_at': datetime.now().isoformat()
        })
    
    return test_data


def generate_test_stock_data():
    """テスト用在庫データを生成"""
    test_data = []
    
    stock_statuses = ['在庫あり', '在庫切れ', '予約商品', '発送可能']
    
    for i in range(5):
        test_data.append({
            'asin': f'B08N5WRWNW{i}',
            'title': f'テスト商品{i+1}',
            'brand': f'テストブランド{(i % 3) + 1}',
            'current_price': 1000 + (i * 200),
            'original_price': 1200 + (i * 200),
            'discount_rate': (i % 3) * 5,
            'currency': 'JPY',
            'availability': stock_statuses[i % len(stock_statuses)],
            'rating': 4.0 + (i * 0.1),
            'review_count': 30 + (i * 10),
            'image_url': f'https://example.com/image{i}.jpg',
            'processed_at': datetime.now().isoformat()
        })
    
    return test_data


def update_config_with_spreadsheet_id(spreadsheet_id):
    """設定ファイルにスプレッドシートIDを更新"""
    try:
        # .envファイルを更新
        env_file = '.env'
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                lines = f.readlines()
            
            # SPREADSHEET_IDの行を更新または追加
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('SPREADSHEET_ID='):
                    lines[i] = f'SPREADSHEET_ID={spreadsheet_id}\n'
                    updated = True
                    break
            
            if not updated:
                lines.append(f'SPREADSHEET_ID={spreadsheet_id}\n')
            
            with open(env_file, 'w') as f:
                f.writelines(lines)
            
            print(f"✓ 設定ファイルを更新しました: SPREADSHEET_ID={spreadsheet_id}")
            
    except Exception as e:
        print(f"設定ファイル更新エラー: {e}")


def test_config_validation():
    """設定検証テスト"""
    print("=== 設定検証テスト ===")
    
    # 必要な環境変数をチェック
    required_vars = [
        'GOOGLE_SHEETS_CREDENTIALS_FILE',
        'SPREADSHEET_ID'
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
            if var == 'GOOGLE_SHEETS_CREDENTIALS_FILE':
                print(f"  {var}=credentials.json")
            else:
                print(f"  {var}=実際の値")
    else:
        print("✓ すべての環境変数が設定されています")
    
    print()


def main():
    """メイン関数"""
    print("Google Sheets連携テスト")
    print("=" * 50)
    
    # 各テストを実行
    test_config_validation()
    test_google_sheets_connection()
    test_spreadsheet_creation()
    test_data_sync()
    test_analysis_dashboard()
    
    print("=" * 50)
    print("✓ Google Sheets連携テスト完了！")
    print("\n次のステップ:")
    print("1. 実際のGoogle Cloud Project設定")
    print("2. サービスアカウントキーの設定")
    print("3. 自動化機能の実装")
    print("4. 定期実行機能の実装")


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
基本機能テストスクリプト
設定管理とログ機能の動作確認
"""

import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.config import config_manager
from utils.logger import logger


def test_config():
    """設定管理機能のテスト"""
    print("=== 設定管理機能テスト ===")
    
    # 設定値を取得
    amazon_config = config_manager.get_amazon_config()
    google_config = config_manager.get_google_sheets_config()
    data_config = config_manager.get_data_processing_config()
    
    print(f"Amazon設定: {amazon_config}")
    print(f"Google設定: {google_config}")
    print(f"データ処理設定: {data_config}")
    
    # 個別の設定値を取得
    batch_size = config_manager.get('data_processing.batch_size', 100)
    print(f"バッチサイズ: {batch_size}")
    
    print("✓ 設定管理機能テスト完了\n")


def test_logger():
    """ログ機能のテスト"""
    print("=== ログ機能テスト ===")
    
    # 各レベルのログを出力
    logger.debug("これはデバッグメッセージです")
    logger.info("これは情報メッセージです")
    logger.warning("これは警告メッセージです")
    logger.error("これはエラーメッセージです")
    
    print("✓ ログ機能テスト完了\n")


def test_directory_structure():
    """ディレクトリ構造の確認"""
    print("=== ディレクトリ構造確認 ===")
    
    required_dirs = [
        'src',
        'src/amazon_api',
        'src/data_processor', 
        'src/google_sheets',
        'src/utils',
        'tests',
        'data',
        'data/raw',
        'data/processed',
        'logs',
        'config',
        'docs'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
        else:
            print(f"✓ {dir_path}")
    
    if missing_dirs:
        print(f"✗ 不足しているディレクトリ: {missing_dirs}")
    else:
        print("✓ すべてのディレクトリが存在します")
    
    print()


def test_files():
    """必要なファイルの確認"""
    print("=== ファイル確認 ===")
    
    required_files = [
        'requirements.txt',
        'config/config.yaml',
        'env.template',
        'src/__init__.py',
        'src/utils/__init__.py',
        'src/utils/config.py',
        'src/utils/logger.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✓ {file_path}")
    
    if missing_files:
        print(f"✗ 不足しているファイル: {missing_files}")
    else:
        print("✓ すべてのファイルが存在します")
    
    print()


def main():
    """メイン関数"""
    print("Amazon EC Tool - 基本機能テスト")
    print("=" * 50)
    
    # 各テストを実行
    test_directory_structure()
    test_files()
    test_config()
    test_logger()
    
    print("=" * 50)
    print("✓ 基本機能テスト完了！")
    print("\n次のステップ:")
    print("1. 必要なライブラリをインストール: pip install -r requirements.txt")
    print("2. 環境変数を設定: cp env.template .env")
    print("3. Amazon API認証情報を設定")
    print("4. Google Sheets API認証情報を設定")


if __name__ == "__main__":
    main() 
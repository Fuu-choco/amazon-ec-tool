"""
ログ管理モジュール
アプリケーション全体のログ機能を提供
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional
from .config import config_manager


class Logger:
    """ログ管理クラス"""
    
    def __init__(self, name: str = "amazon_ec_tool"):
        """
        初期化
        
        Args:
            name: ロガー名
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """ロガーの設定"""
        # ログ設定を取得
        log_config = config_manager.get_logging_config()
        
        # ログレベルを設定
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        self.logger.setLevel(log_level)
        
        # 既存のハンドラーをクリア
        self.logger.handlers.clear()
        
        # フォーマッターを作成
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # コンソールハンドラーを追加
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # ファイルハンドラーを追加（設定されている場合）
        log_file = log_config.get('file')
        if log_file:
            # ログディレクトリを作成
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # ローテーティングファイルハンドラーを作成
            max_size = log_config.get('max_size', 10 * 1024 * 1024)  # 10MB
            backup_count = log_config.get('backup_count', 5)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_size,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """デバッグログを出力"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """情報ログを出力"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告ログを出力"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """エラーログを出力"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """重大エラーログを出力"""
        self.logger.critical(message)
    
    def exception(self, message: str):
        """例外ログを出力（スタックトレース付き）"""
        self.logger.exception(message)


# グローバルロガーインスタンス
logger = Logger()


def get_logger(name: Optional[str] = None) -> Logger:
    """
    ロガーを取得
    
    Args:
        name: ロガー名（Noneの場合はデフォルトロガー）
        
    Returns:
        ロガーインスタンス
    """
    if name:
        return Logger(name)
    return logger 
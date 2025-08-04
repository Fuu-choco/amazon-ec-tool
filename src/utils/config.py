"""
設定管理モジュール
環境変数とYAML設定ファイルを読み込む機能を提供
"""

import os
import yaml
from dotenv import load_dotenv
from typing import Dict, Any


class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        初期化
        
        Args:
            config_path: 設定ファイルのパス
        """
        self.config_path = config_path
        self.config = {}
        self._load_config()
    
    def _load_config(self):
        """設定ファイルと環境変数を読み込む"""
        # 環境変数を読み込み
        load_dotenv()
        
        # YAML設定ファイルを読み込み
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file)
        
        # 環境変数を設定に反映
        self._replace_env_vars()
    
    def _replace_env_vars(self):
        """設定内の環境変数を実際の値に置換"""
        def replace_in_dict(d: Dict[str, Any]) -> Dict[str, Any]:
            for key, value in d.items():
                if isinstance(value, dict):
                    d[key] = replace_in_dict(value)
                elif isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                    env_var = value[2:-1]  # ${VAR} -> VAR
                    d[key] = os.getenv(env_var, value)
            return d
        
        self.config = replace_in_dict(self.config)
    
    def get(self, key: str, default=None):
        """
        設定値を取得
        
        Args:
            key: 設定キー（ドット区切りでネストしたキーを指定可能）
            default: デフォルト値
            
        Returns:
            設定値
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_amazon_config(self) -> Dict[str, str]:
        """Amazon API設定を取得"""
        return self.config.get('amazon', {})
    
    def get_google_sheets_config(self) -> Dict[str, str]:
        """Google Sheets API設定を取得"""
        return self.config.get('google_sheets', {})
    
    def get_data_processing_config(self) -> Dict[str, Any]:
        """データ処理設定を取得"""
        return self.config.get('data_processing', {})
    
    def get_scheduling_config(self) -> Dict[str, int]:
        """スケジューリング設定を取得"""
        return self.config.get('scheduling', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """ログ設定を取得"""
        return self.config.get('logging', {})


# グローバル設定インスタンス
config_manager = ConfigManager() 
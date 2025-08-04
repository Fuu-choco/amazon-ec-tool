"""
Google Sheets API クライアント
スプレッドシートの作成・更新・データ反映機能を提供
"""

import os
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import Dict, List, Optional, Any
from src.utils.config import config_manager
from src.utils.logger import get_logger


class GoogleSheetsClient:
    """Google Sheets API クライアント"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_logger("google_sheets")
        self.config = config_manager.get_google_sheets_config()
        self.credentials = None
        self.service = None
        self.gc = None
        self._setup_client()
    
    def _setup_client(self):
        """クライアントの設定"""
        try:
            credentials_file = self.config.get('credentials_file')
            
            if not credentials_file or not os.path.exists(credentials_file):
                self.logger.warning(f"認証ファイルが見つかりません: {credentials_file}")
                return
            
            # 認証情報を読み込み
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            self.credentials = Credentials.from_service_account_file(
                credentials_file, scopes=scopes
            )
            
            # Google Sheets API サービスを作成
            self.service = build('sheets', 'v4', credentials=self.credentials)
            
            # gspreadクライアントを作成
            self.gc = gspread.authorize(self.credentials)
            
            self.logger.info("Google Sheets API クライアントを設定しました")
            
        except Exception as e:
            self.logger.error(f"Google Sheets API クライアント設定エラー: {e}")
    
    def create_spreadsheet(self, title: str) -> Optional[str]:
        """
        新しいスプレッドシートを作成
        
        Args:
            title: スプレッドシートのタイトル
            
        Returns:
            スプレッドシートID
        """
        try:
            if not self.gc:
                self.logger.error("Google Sheets API クライアントが設定されていません")
                return None
            
            # スプレッドシートを作成
            spreadsheet = self.gc.create(title)
            
            self.logger.info(f"スプレッドシートを作成しました: {title} (ID: {spreadsheet.id})")
            return spreadsheet.id
            
        except Exception as e:
            self.logger.error(f"スプレッドシート作成エラー: {e}")
            return None
    
    def open_spreadsheet(self, spreadsheet_id: str = None):
        """
        スプレッドシートを開く
        
        Args:
            spreadsheet_id: スプレッドシートID（Noneの場合は設定ファイルから取得）
            
        Returns:
            スプレッドシートオブジェクト
        """
        try:
            if not self.gc:
                self.logger.error("Google Sheets API クライアントが設定されていません")
                return None
            
            # スプレッドシートIDを取得
            if not spreadsheet_id:
                spreadsheet_id = self.config.get('spreadsheet_id')
            
            if not spreadsheet_id:
                self.logger.error("スプレッドシートIDが設定されていません")
                return None
            
            # スプレッドシートを開く
            spreadsheet = self.gc.open_by_key(spreadsheet_id)
            
            self.logger.info(f"スプレッドシートを開きました: {spreadsheet.title}")
            return spreadsheet
            
        except Exception as e:
            self.logger.error(f"スプレッドシートを開くエラー: {e}")
            return None
    
    def create_worksheet(self, spreadsheet, title: str, rows: int = 1000, cols: int = 26):
        """
        ワークシートを作成
        
        Args:
            spreadsheet: スプレッドシートオブジェクト
            title: ワークシートのタイトル
            rows: 行数
            cols: 列数
            
        Returns:
            ワークシートオブジェクト
        """
        try:
            worksheet = spreadsheet.add_worksheet(title=title, rows=rows, cols=cols)
            
            self.logger.info(f"ワークシートを作成しました: {title}")
            return worksheet
            
        except Exception as e:
            self.logger.error(f"ワークシート作成エラー: {e}")
            return None
    
    def update_cells(self, worksheet, data: List[List], start_cell: str = 'A1'):
        """
        セルを更新
        
        Args:
            worksheet: ワークシートオブジェクト
            data: 更新するデータ（2次元配列）
            start_cell: 開始セル
        """
        try:
            # データを更新
            worksheet.update(start_cell, data)
            
            self.logger.info(f"セルを更新しました: {start_cell} から {len(data)}行")
            
        except Exception as e:
            self.logger.error(f"セル更新エラー: {e}")
    
    def append_rows(self, worksheet, data: List[List]):
        """
        行を追加
        
        Args:
            worksheet: ワークシートオブジェクト
            data: 追加するデータ（2次元配列）
        """
        try:
            # 行を追加
            worksheet.append_rows(data)
            
            self.logger.info(f"行を追加しました: {len(data)}行")
            
        except Exception as e:
            self.logger.error(f"行追加エラー: {e}")
    
    def clear_worksheet(self, worksheet):
        """
        ワークシートをクリア
        
        Args:
            worksheet: ワークシートオブジェクト
        """
        try:
            worksheet.clear()
            self.logger.info("ワークシートをクリアしました")
            
        except Exception as e:
            self.logger.error(f"ワークシートクリアエラー: {e}")
    
    def format_headers(self, worksheet, headers: List[str]):
        """
        ヘッダー行をフォーマット
        
        Args:
            worksheet: ワークシートオブジェクト
            headers: ヘッダーリスト
        """
        try:
            # ヘッダー行を更新
            worksheet.update('A1', [headers])
            
            # ヘッダー行をフォーマット（太字、背景色など）
            worksheet.format('A1:Z1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8}
            })
            
            self.logger.info("ヘッダー行をフォーマットしました")
            
        except Exception as e:
            self.logger.error(f"ヘッダーフォーマットエラー: {e}")
    
    def get_all_values(self, worksheet) -> List[List]:
        """
        すべての値を取得
        
        Args:
            worksheet: ワークシートオブジェクト
            
        Returns:
            すべての値（2次元配列）
        """
        try:
            values = worksheet.get_all_values()
            self.logger.info(f"値を取得しました: {len(values)}行")
            return values
            
        except Exception as e:
            self.logger.error(f"値取得エラー: {e}")
            return []
    
    def find_cell_by_value(self, worksheet, value: str) -> Optional[str]:
        """
        値でセルを検索
        
        Args:
            worksheet: ワークシートオブジェクト
            value: 検索する値
            
        Returns:
            セル位置（例: 'A1'）
        """
        try:
            cell = worksheet.find(value)
            if cell:
                return cell.address
            return None
            
        except Exception as e:
            self.logger.error(f"セル検索エラー: {e}")
            return None
    
    def is_connected(self) -> bool:
        """
        接続状態を確認
        
        Returns:
            接続状態
        """
        return self.gc is not None and self.service is not None


# グローバルGoogle Sheetsクライアントインスタンス
google_sheets_client = GoogleSheetsClient() 
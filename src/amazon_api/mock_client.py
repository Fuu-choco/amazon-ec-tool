"""
Amazon API モッククライアント
審査期間中の開発用にモックデータを提供
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.utils.logger import get_logger


class MockAmazonAPIClient:
    """Amazon API モッククライアント"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_logger("mock_amazon_api")
        self.mock_data = self._load_mock_data()
        
    def _load_mock_data(self) -> Dict:
        """モックデータを読み込み"""
        return {
            "search_results": [
                {
                    "ASIN": "B08N5WRWNW",
                    "ItemInfo": {
                        "Title": {
                            "DisplayValue": "Apple iPhone 14 Pro 128GB ディープパープル"
                        },
                        "ByLineInfo": {
                            "Brand": {
                                "DisplayValue": "Apple"
                            }
                        },
                        "Features": {
                            "DisplayValues": [
                                "A16 Bionicチップ搭載",
                                "ProRAW写真撮影対応",
                                "Always-Onディスプレイ"
                            ]
                        }
                    },
                    "Offers": {
                        "CurrentPrice": {
                            "Amount": 149800,
                            "Currency": "JPY"
                        },
                        "ListPrice": {
                            "Amount": 159800,
                            "Currency": "JPY"
                        },
                        "Availability": {
                            "Message": "在庫あり"
                        }
                    },
                    "CustomerReviews": {
                        "Rating": 4.5,
                        "ReviewCount": 1250
                    },
                    "Images": {
                        "Primary": {
                            "Large": {
                                "URL": "https://m.media-amazon.com/images/I/71T5nKVYorL._AC_SL1500_.jpg"
                            }
                        }
                    }
                },
                {
                    "ASIN": "B09G9HD6PD",
                    "ItemInfo": {
                        "Title": {
                            "DisplayValue": "Sony WH-1000XM4 ワイヤレスノイズキャンセリングヘッドホン"
                        },
                        "ByLineInfo": {
                            "Brand": {
                                "DisplayValue": "Sony"
                            }
                        },
                        "Features": {
                            "DisplayValues": [
                                "30時間バッテリー",
                                "マルチポイント接続",
                                "タッチコントロール"
                            ]
                        }
                    },
                    "Offers": {
                        "CurrentPrice": {
                            "Amount": 29800,
                            "Currency": "JPY"
                        },
                        "ListPrice": {
                            "Amount": 39800,
                            "Currency": "JPY"
                        },
                        "Availability": {
                            "Message": "在庫あり"
                        }
                    },
                    "CustomerReviews": {
                        "Rating": 4.3,
                        "ReviewCount": 890
                    },
                    "Images": {
                        "Primary": {
                            "Large": {
                                "URL": "https://m.media-amazon.com/images/I/71o8Q5XJS5L._AC_SL1500_.jpg"
                            }
                        }
                    }
                },
                {
                    "ASIN": "B08F7PTF54",
                    "ItemInfo": {
                        "Title": {
                            "DisplayValue": "Nintendo Switch 有機ELモデル ホワイト"
                        },
                        "ByLineInfo": {
                            "Brand": {
                                "DisplayValue": "Nintendo"
                            }
                        },
                        "Features": {
                            "DisplayValues": [
                                "7インチ有機ELディスプレイ",
                                "約4.5-9時間バッテリー",
                                "Joy-Conコントローラー付属"
                            ]
                        }
                    },
                    "Offers": {
                        "CurrentPrice": {
                            "Amount": 37980,
                            "Currency": "JPY"
                        },
                        "ListPrice": {
                            "Amount": 37980,
                            "Currency": "JPY"
                        },
                        "Availability": {
                            "Message": "在庫あり"
                        }
                    },
                    "CustomerReviews": {
                        "Rating": 4.7,
                        "ReviewCount": 2100
                    },
                    "Images": {
                        "Primary": {
                            "Large": {
                                "URL": "https://m.media-amazon.com/images/I/71i+TPP7LzL._AC_SL1500_.jpg"
                            }
                        }
                    }
                }
            ],
            "item_details": {
                "B08N5WRWNW": {
                    "ASIN": "B08N5WRWNW",
                    "ItemInfo": {
                        "Title": {
                            "DisplayValue": "Apple iPhone 14 Pro 128GB ディープパープル"
                        },
                        "ByLineInfo": {
                            "Brand": {
                                "DisplayValue": "Apple"
                            }
                        },
                        "Features": {
                            "DisplayValues": [
                                "A16 Bionicチップ搭載",
                                "ProRAW写真撮影対応",
                                "Always-Onディスプレイ",
                                "5G対応",
                                "MagSafe充電対応"
                            ]
                        },
                        "ProductInfo": {
                            "ItemDimensions": {
                                "Height": {
                                    "Value": 147.5,
                                    "Units": "millimeters"
                                },
                                "Length": {
                                    "Value": 71.5,
                                    "Units": "millimeters"
                                },
                                "Width": {
                                    "Value": 7.85,
                                    "Units": "millimeters"
                                },
                                "Weight": {
                                    "Value": 206,
                                    "Units": "grams"
                                }
                            }
                        }
                    },
                    "Offers": {
                        "CurrentPrice": {
                            "Amount": 149800,
                            "Currency": "JPY"
                        },
                        "ListPrice": {
                            "Amount": 159800,
                            "Currency": "JPY"
                        },
                        "Availability": {
                            "Message": "在庫あり"
                        },
                        "PriceHistory": [
                            {"date": "2024-01-01", "price": 159800},
                            {"date": "2024-01-15", "price": 154800},
                            {"date": "2024-02-01", "price": 149800}
                        ]
                    },
                    "CustomerReviews": {
                        "Rating": 4.5,
                        "ReviewCount": 1250,
                        "ReviewDetails": {
                            "FiveStar": {"Percentage": 65},
                            "FourStar": {"Percentage": 20},
                            "ThreeStar": {"Percentage": 10},
                            "TwoStar": {"Percentage": 3},
                            "OneStar": {"Percentage": 2}
                        }
                    },
                    "Images": {
                        "Primary": {
                            "Large": {
                                "URL": "https://m.media-amazon.com/images/I/71T5nKVYorL._AC_SL1500_.jpg"
                            }
                        },
                        "Secondary": [
                            {
                                "Large": {
                                    "URL": "https://m.media-amazon.com/images/I/71T5nKVYorL._AC_SL1500_.jpg"
                                }
                            }
                        ]
                    }
                }
            }
        }
    
    def search_items(self, keywords: str, search_index: str = "All", item_count: int = 10) -> Dict:
        """
        商品検索を実行（モック）
        
        Args:
            keywords: 検索キーワード
            search_index: 検索インデックス
            item_count: 取得件数
            
        Returns:
            検索結果
        """
        try:
            self.logger.info(f"モック商品検索を実行: {keywords}")
            
            # キーワードに基づいてフィルタリング
            filtered_results = []
            for item in self.mock_data["search_results"]:
                title = item["ItemInfo"]["Title"]["DisplayValue"].lower()
                brand = item["ItemInfo"]["ByLineInfo"]["Brand"]["DisplayValue"].lower()
                keywords_lower = keywords.lower()
                
                if any(keyword in title or keyword in brand for keyword in keywords_lower.split()):
                    filtered_results.append(item)
            
            # 件数制限
            filtered_results = filtered_results[:item_count]
            
            # レート制限シミュレーション
            time.sleep(0.1)
            
            result = {
                "SearchResult": {
                    "Items": filtered_results,
                    "TotalResultCount": len(filtered_results),
                    "SearchIndex": search_index
                }
            }
            
            self.logger.info(f"モック検索成功: {len(filtered_results)}件")
            return result
            
        except Exception as e:
            self.logger.error(f"モック商品検索エラー: {e}")
            return {"SearchResult": {"Items": []}}
    
    def get_items(self, asins: List[str]) -> Dict:
        """
        商品詳細情報を取得（モック）
        
        Args:
            asins: ASINリスト
            
        Returns:
            商品詳細情報
        """
        try:
            self.logger.info(f"モック商品詳細取得: {len(asins)}件")
            
            items = []
            for asin in asins:
                if asin in self.mock_data["item_details"]:
                    items.append(self.mock_data["item_details"][asin])
            
            # レート制限シミュレーション
            time.sleep(0.1)
            
            result = {
                "ItemsResult": {
                    "Items": items,
                    "TotalResultCount": len(items)
                }
            }
            
            self.logger.info(f"モック商品詳細取得成功: {len(items)}件")
            return result
            
        except Exception as e:
            self.logger.error(f"モック商品詳細取得エラー: {e}")
            return {"ItemsResult": {"Items": []}}
    
    def get_similar_items(self, asin: str, item_count: int = 10) -> Dict:
        """
        類似商品を取得（モック）
        
        Args:
            asin: 商品ASIN
            item_count: 取得件数
            
        Returns:
            類似商品情報
        """
        try:
            self.logger.info(f"モック類似商品取得: {asin}")
            
            # 類似商品のモックデータ
            similar_items = self.mock_data["search_results"][:item_count]
            
            # レート制限シミュレーション
            time.sleep(0.1)
            
            result = {
                "SimilarItemsResult": {
                    "Items": similar_items,
                    "TotalResultCount": len(similar_items)
                }
            }
            
            self.logger.info(f"モック類似商品取得成功: {len(similar_items)}件")
            return result
            
        except Exception as e:
            self.logger.error(f"モック類似商品取得エラー: {e}")
            return {"SimilarItemsResult": {"Items": []}}
    
    def rate_limit_delay(self, seconds: float = 1.0):
        """
        レート制限対応のための遅延（モック）
        
        Args:
            seconds: 遅延秒数
        """
        time.sleep(seconds)
        self.logger.debug(f"モックレート制限対応: {seconds}秒遅延")


# グローバルモッククライアントインスタンス
mock_amazon_client = MockAmazonAPIClient() 
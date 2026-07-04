# app/tools.py
import os
import logging
import requests
import json
from typing import Optional, Dict, Any, List
from crewai_tools import BaseTool

logger = logging.getLogger(__name__)

class BoardDataFetcherTool(BaseTool):
    """Fetches card data, comments, and activity from a Trello board."""
    
    name: str = "Trello Board Data Fetcher"
    description: str = "Fetches card data, comments, and activity from a Trello board."
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('TRELLO_API_KEY')
        self.api_token = os.getenv('TRELLO_API_TOKEN')
        self.board_id = os.getenv('TRELLO_BOARD_ID')
        self.base_url = os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')
        
        if not self.api_key or not self.api_token or not self.board_id:
            logger.warning("⚠️ Trello credentials not fully configured. Using fallback data.")
    
    def _run(self) -> Dict:
        """Fetch all cards from the specified Trello board."""
        try:
            url = f"{self.base_url}/1/boards/{self.board_id}/cards"
            
            query = {
                'key': self.api_key,
                'token': self.api_token,
                'fields': 'name,idList,due,dateLastActivity,labels,desc',
                'attachments': 'true',
                'actions': 'commentCard',
                'members': 'true'
            }
            
            response = requests.get(url, params=query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Fetched {len(data)} cards from Trello")
                return {"status": "success", "data": data}
            else:
                logger.error(f"❌ Trello API error: {response.status_code}")
                return self._get_fallback_data()
                
        except Exception as e:
            logger.error(f"❌ Error fetching Trello data: {str(e)}")
            return self._get_fallback_data()
    
    def _get_fallback_data(self) -> Dict:
        """Return fallback data in case of API failure"""
        fallback_data = [
            {
                'id': '66c3bfed69b473b8fe9d922e',
                'name': 'Analysis of results from CSV',
                'idList': '66c308f676b057fdfbd5fdb3',
                'due': None,
                'dateLastActivity': '2024-08-19T21:58:05.062Z',
                'labels': [],
                'desc': 'Analyze the CSV results and prepare summary',
                'attachments': [],
                'actions': []
            },
            {
                'id': '66c3c002bb1c337f3fdf1563',
                'name': 'Approve the planning',
                'idList': '66c308f676b057fdfbd5fdb3',
                'due': '2024-08-16T21:58:00.000Z',
                'dateLastActivity': '2024-08-19T21:58:57.697Z',
                'labels': [{'id': '66c305ea10ea602ee6e03d47', 'name': 'Urgent', 'color': 'red'}],
                'desc': 'Review and approve the project planning document',
                'attachments': [],
                'actions': [
                    {
                        'id': '66c3c021f3c1bb157028f53d',
                        'type': 'commentCard',
                        'date': '2024-08-19T21:58:57.683Z',
                        'data': {'text': 'This was harder than expected, need more time'}
                    }
                ]
            },
            {
                'id': '66c3bff4a25b398ef1b6de78',
                'name': 'Scaffold of the initial app UI',
                'idList': '66c3bfdfb851ad9ff7eee159',
                'due': None,
                'dateLastActivity': '2024-08-19T21:58:12.210Z',
                'labels': [],
                'desc': 'Create the basic UI structure for the application',
                'attachments': [],
                'actions': []
            },
            {
                'id': '66c3bffdb06faa1e69216c6f',
                'name': 'Planning of the project',
                'idList': '66c3bfe3151c01425f366f4c',
                'due': None,
                'dateLastActivity': '2024-08-19T21:58:21.081Z',
                'labels': [],
                'desc': 'Create detailed project plan with timelines',
                'attachments': [],
                'actions': []
            }
        ]
        return {"status": "fallback", "data": fallback_data}


class CardDataFetcherTool(BaseTool):
    """Fetches detailed data for a specific Trello card."""
    
    name: str = "Trello Card Data Fetcher"
    description: str = "Fetches detailed card data from a Trello board."
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('TRELLO_API_KEY')
        self.api_token = os.getenv('TRELLO_API_TOKEN')
        self.base_url = os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')
    
    def _run(self, card_id: str) -> Dict:
        """Fetch detailed data for a specific card."""
        try:
            url = f"{self.base_url}/1/cards/{card_id}"
            query = {
                'key': self.api_key,
                'token': self.api_token,
                'fields': 'name,desc,due,idList,labels,members,dateLastActivity',
                'actions': 'commentCard,updateCard',
                'attachments': 'true'
            }
            
            response = requests.get(url, params=query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Fetched card data for {card_id}")
                return {"status": "success", "data": data}
            else:
                logger.error(f"❌ Error fetching card {card_id}: {response.status_code}")
                return {"status": "error", "error": "Failed to fetch card data"}
                
        except Exception as e:
            logger.error(f"❌ Error fetching card: {str(e)}")
            return {"status": "error", "error": str(e)}


class BoardListFetcherTool(BaseTool):
    """Fetches all lists from a Trello board."""
    
    name: str = "Trello Board List Fetcher"
    description: str = "Fetches all lists from a Trello board."
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv('TRELLO_API_KEY')
        self.api_token = os.getenv('TRELLO_API_TOKEN')
        self.board_id = os.getenv('TRELLO_BOARD_ID')
        self.base_url = os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')
    
    def _run(self) -> Dict:
        """Fetch all lists from the board."""
        try:
            url = f"{self.base_url}/1/boards/{self.board_id}/lists"
            query = {
                'key': self.api_key,
                'token': self.api_token,
                'fields': 'name,id'
            }
            
            response = requests.get(url, params=query, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Fetched {len(data)} lists from Trello")
                return {"status": "success", "data": data}
            else:
                logger.error(f"❌ Error fetching lists: {response.status_code}")
                return {"status": "error", "data": []}
                
        except Exception as e:
            logger.error(f"❌ Error fetching lists: {str(e)}")
            return {"status": "error", "data": []}
# app/tools.py
import os
import logging
import requests
import json
from typing import Optional, Dict, Any, List
from crewai_tools import tool

logger = logging.getLogger(__name__)

def _get_trello_fallback_data() -> Dict:
    """Return fallback data in case of Trello API failure"""
    # This is a helper function, not a tool
    return {
        "status": "fallback",
        "data": [
            {'id': '66c3bfed69b473b8fe9d922e', 'name': 'Analysis of results from CSV', 'idList': '66c308f676b057fdfbd5fdb3', 'due': None, 'dateLastActivity': '2024-08-19T21:58:05.062Z', 'labels': [], 'desc': 'Analyze the CSV results and prepare summary', 'attachments': [], 'actions': []},
            {'id': '66c3c002bb1c337f3fdf1563', 'name': 'Approve the planning', 'idList': '66c308f676b057fdfbd5fdb3', 'due': '2024-08-16T21:58:00.000Z', 'dateLastActivity': '2024-08-19T21:58:57.697Z', 'labels': [{'id': '66c305ea10ea602ee6e03d47', 'name': 'Urgent', 'color': 'red'}], 'desc': 'Review and approve the project planning document', 'attachments': [], 'actions': [{'id': '66c3c021f3c1bb157028f53d', 'type': 'commentCard', 'date': '2024-08-19T21:58:57.683Z', 'data': {'text': 'This was harder than expected, need more time'}}]},
            {'id': '66c3bff4a25b398ef1b6de78', 'name': 'Scaffold of the initial app UI', 'idList': '66c3bfdfb851ad9ff7eee159', 'due': None, 'dateLastActivity': '2024-08-19T21:58:12.210Z', 'labels': [], 'desc': 'Create the basic UI structure for the application', 'attachments': [], 'actions': []},
            {'id': '66c3bffdb06faa1e69216c6f', 'name': 'Planning of the project', 'idList': '66c3bfe3151c01425f366f4c', 'due': None, 'dateLastActivity': '2024-08-19T21:58:21.081Z', 'labels': [], 'desc': 'Create detailed project plan with timelines', 'attachments': [], 'actions': []}
        ]
    }

@tool("Trello Board Data Fetcher")
def board_data_fetcher_tool() -> Dict:
    """Fetches card data, comments, and activity from a Trello board."""
    api_key = os.getenv('TRELLO_API_KEY')
    api_token = os.getenv('TRELLO_API_TOKEN')
    board_id = os.getenv('TRELLO_BOARD_ID')
    base_url = os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')

    if not all([api_key, api_token, board_id]):
        logger.warning("⚠️ Trello credentials not fully configured. Using fallback data.")
        return _get_trello_fallback_data()

    try:
        url = f"{base_url}/1/boards/{board_id}/cards"
        query = {
            'key': api_key,
            'token': api_token,
            'fields': 'name,idList,due,dateLastActivity,labels,desc',
            'attachments': 'true',
            'actions': 'commentCard',
            'members': 'true'
        }
        response = requests.get(url, params=query, timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info(f"✅ Fetched {len(data)} cards from Trello")
        return {"status": "success", "data": data}
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Trello API error: {e}")
        return _get_trello_fallback_data()
    except Exception as e:
        logger.error(f"❌ Error fetching Trello data: {str(e)}")
        return _get_trello_fallback_data()

@tool("Trello Card Data Fetcher")
def card_data_fetcher_tool(card_id: str) -> Dict:
    """Fetches detailed data for a specific Trello card."""
    api_key = os.getenv('TRELLO_API_KEY')
    api_token = os.getenv('TRELLO_API_TOKEN')
    base_url = os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')

    if not all([api_key, api_token]):
        logger.error("❌ Trello credentials not configured for card fetching.")
        return {"status": "error", "error": "Trello credentials not configured."}

    try:
        url = f"{base_url}/1/cards/{card_id}"
        query = {
            'key': api_key,
            'token': api_token,
            'fields': 'name,desc,due,idList,labels,members,dateLastActivity',
            'actions': 'commentCard,updateCard',
            'attachments': 'true'
        }
        response = requests.get(url, params=query, timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info(f"✅ Fetched card data for {card_id}")
        return {"status": "success", "data": data}
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error fetching card {card_id}: {e}")
        return {"status": "error", "error": f"Failed to fetch card data: {e}"}
    except Exception as e:
        logger.error(f"❌ Error fetching card: {str(e)}")
        return {"status": "error", "error": str(e)}

@tool("Trello Board List Fetcher")
def board_list_fetcher_tool() -> Dict:
    """Fetches all lists from a Trello board."""
    api_key = os.getenv('TRELLO_API_KEY')
    api_token = os.getenv('TRELLO_API_TOKEN')
    board_id = os.getenv('TRELLO_BOARD_ID')
    base_url = os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')

    if not all([api_key, api_token, board_id]):
        logger.error("❌ Trello credentials not configured for list fetching.")
        return {"status": "error", "data": []}

    try:
        url = f"{base_url}/1/boards/{board_id}/lists"
        query = {'key': api_key, 'token': api_token, 'fields': 'name,id'}
        response = requests.get(url, params=query, timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info(f"✅ Fetched {len(data)} lists from Trello")
        return {"status": "success", "data": data}
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error fetching lists: {e}")
        return {"status": "error", "data": []}
    except Exception as e:
        logger.error(f"❌ Error fetching lists: {str(e)}")
        return {"status": "error", "data": []}
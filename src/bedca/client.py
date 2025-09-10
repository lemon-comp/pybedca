"""BEDCA API client implementation."""

import xml.etree.ElementTree as ET
from typing import List
import requests

from .models import FoodPreview
from .query import get_all_foods_query, get_food_by_id_query


class BedcaClient:
    """Client for interacting with the BEDCA API."""

    BASE_URL = "https://www.bedca.net/bdpub/procquery.php"

    def __init__(self):
        """Initialize the BEDCA client."""
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "text/xml",
            "User-Agent": "Python-pybedca",
            "Origin": "https://www.bedca.net",
            "Referer": "https://www.bedca.net/bdpub/index.php",
        }

    def get_all_foods(self) -> List[FoodPreview]:
        """Get all food products from BEDCA.

        Returns:
            List[Food]: A list of FoodPreview objects containing basic information about each food item.
        """
        payload = get_all_foods_query()

        response = self.session.post(self.BASE_URL, headers=self.headers, data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        root = ET.fromstring(response.text)
        
        return [
            FoodPreview(
                id=food.findtext("f_id"),
                name_es=food.findtext("f_ori_name"),
                name_en=food.findtext("f_eng_name"),
            )
            for food in root.findall("food")
        ]

    def get_food_by_id(self, food_id: int) -> ET.Element:
        """Get detailed information about a specific food by its ID.
        
        Args:
            food_id: The ID of the food to fetch.
            
        Returns:
            ET.Element: The raw XML response as an ElementTree for further processing.
            
        Raises:
            requests.HTTPError: If the request fails.
        """
        payload = get_food_by_id_query(food_id)
        
        response = self.session.post(self.BASE_URL, headers=self.headers, data=payload)
        response.raise_for_status()
        
        return ET.fromstring(response.text)

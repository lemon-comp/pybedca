"""BEDCA API client implementation."""

import xml.etree.ElementTree as ET
from typing import List
import requests

from .models import FoodPreview
from .query import get_all_foods_query


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

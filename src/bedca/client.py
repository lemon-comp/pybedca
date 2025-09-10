"""BEDCA API client implementation."""

from typing import List
import xml.etree.ElementTree as ET

import requests

from .query import BedcaQueryBuilder
from .models import FoodPreview, Food
from .parser import parse_food_response
from .enums import Languages, BedcaRelation, BedcaAttribute


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
        query = (
            BedcaQueryBuilder(level=1)
            .select(
                BedcaAttribute.ID,
                BedcaAttribute.SPANISH_NAME,
                BedcaAttribute.ENGLISH_NAME,
                BedcaAttribute.ORIGIN,
            )
            .where(BedcaAttribute.ORIGIN, BedcaRelation.EQUAL, "BEDCA")
            .order(BedcaAttribute.SPANISH_NAME)
            .build()
        )

        response = self.session.post(self.BASE_URL, headers=self.headers, data=query)
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

    def search_food_by_name(self, search_query: str, language: Languages = Languages.ES) -> List[FoodPreview]:
        """Get all food products from BEDCA.

        Returns:
            List[Food]: A list of FoodPreview objects containing basic information about each food item.
        """
        search_attribute = BedcaAttribute.SPANISH_NAME if language == Languages.ES else BedcaAttribute.ENGLISH_NAME
        query = (
            BedcaQueryBuilder(level=1)
            .select(
                BedcaAttribute.ID,
                BedcaAttribute.SPANISH_NAME,
                BedcaAttribute.ENGLISH_NAME,
                BedcaAttribute.ORIGIN,
            )
            .where(search_attribute, BedcaRelation.LIKE, search_query)
            .where(BedcaAttribute.ORIGIN, BedcaRelation.EQUAL, "BEDCA")
            .order(search_attribute)
            .build()
        )

        response = self.session.post(self.BASE_URL, headers=self.headers, data=query)
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

    def get_food_by_id(self, food_id: int) -> Food:
        """Get detailed information about a specific food by its ID.
        
        Args:
            food_id: The ID of the food to fetch.
            
        Returns:
            ET.Element: The raw XML response as an ElementTree for further processing.
            
        Raises:
            requests.HTTPError: If the request fails.
        """
        query =  (
            BedcaQueryBuilder(level=2)
            .select(
                *[attr for attr in BedcaAttribute]  # Select all attributes
            )
            .where(BedcaAttribute.ID, BedcaRelation.EQUAL, str(food_id))
            .order(BedcaAttribute.COMPONENT_GROUP_ID)
            .build()
        )

        response = self.session.post(self.BASE_URL, headers=self.headers, data=query)
        response.raise_for_status()
        
        return parse_food_response(response.text)

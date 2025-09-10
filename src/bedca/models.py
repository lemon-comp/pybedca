"""Models for the BEDCA API client."""

from dataclasses import dataclass


@dataclass
class FoodPreview:
    """Represents a food item in the BEDCA database."""
    id: str
    name_es: str
    name_en: str

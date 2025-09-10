"""Models for the BEDCA API client."""

from dataclasses import dataclass
from typing import Dict, Optional

from .enums import BedcaComponent


@dataclass
class FoodValue:
    """Represents a nutritional value for a food component."""
    component: BedcaComponent
    value: float | str  # str for cases like 'trace'
    unit: str


@dataclass
class FoodNutrients:
    """Contains all nutritional values for a food item."""
    # Proximales
    alcohol: FoodValue
    energy: FoodValue
    fat: FoodValue
    protein: FoodValue
    water: FoodValue

    # Hidratos de Carbono
    carbohydrate: FoodValue
    fiber: FoodValue

    # Grasas
    monounsaturated_fat: FoodValue
    polyunsaturated_fat: FoodValue
    saturated_fat: FoodValue
    cholesterol: FoodValue

    # Vitaminas
    vitamin_a: FoodValue
    vitamin_d: FoodValue
    vitamin_e: FoodValue
    folate: FoodValue
    niacin: FoodValue
    riboflavin: FoodValue
    thiamin: FoodValue
    vitamin_b12: FoodValue
    vitamin_b6: FoodValue
    vitamin_c: FoodValue

    # Minerales
    calcium: FoodValue
    iron: FoodValue
    potassium: FoodValue
    magnesium: FoodValue
    sodium: FoodValue
    phosphorus: FoodValue
    iodide: FoodValue
    selenium: FoodValue
    zinc: FoodValue


@dataclass
class FoodPreview:
    """Represents a food item in the BEDCA database."""
    id: str
    name_es: str
    name_en: str


@dataclass
class Food:
    """Represents a complete food item with all its nutritional values."""
    id: str
    name_es: str
    name_en: str
    scientific_name: Optional[str]
    nutrients: FoodNutrients
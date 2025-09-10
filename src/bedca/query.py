"""Query builder for BEDCA API."""

from enum import StrEnum
from xml.dom import minidom
from typing import List, Optional
import xml.etree.ElementTree as ET


class BedcaAttribute(StrEnum):
    """Attributes available in BEDCA API."""
    
    ID = "f_id"
    SPANISH_NAME = "f_ori_name"
    ENGLISH_NAME = "f_eng_name"
    LANGUAL = "langual"
    ORIGIN = "f_origen"
    EDIBLE_PORTION = "edible_portion"


class BedcaRelation(StrEnum):
    """Relation types for BEDCA query conditions."""
    
    EQUAL = "EQUAL"
    LIKE = "LIKE"
    BEGINS_WITH = "BEGINW"


class BedcaQueryBuilder:
    """Builder for BEDCA API queries."""
    
    def __init__(self):
        """Initialize the query builder."""
        self.root = ET.Element("foodquery")
        
        # Add default type level
        type_elem = ET.SubElement(self.root, "type")
        type_elem.set("level", "1")
        
        # Initialize selection element
        self.selection = ET.SubElement(self.root, "selection")
        
        # Always add the BEDCA origin condition
        self.where(BedcaAttribute.ORIGIN, BedcaRelation.EQUAL, "BEDCA")
    
    def select(self, *attributes: BedcaAttribute) -> "BedcaQueryBuilder":
        """Add attributes to select in the query.
        
        Args:
            *attributes: The attributes to select.
            
        Returns:
            self: The query builder instance for method chaining.
        """
        for attr in attributes:
            attribute = ET.SubElement(self.selection, "atribute")
            attribute.set("name", attr)
        return self

    def where(self, attribute: BedcaAttribute, relation: BedcaRelation, value: str) -> "BedcaQueryBuilder":
        """Add a condition to the query.
        
        Args:
            attribute: The attribute to filter on.
            relation: The type of relation to use.
            value: The value to compare against.
            
        Returns:
            self: The query builder instance for method chaining.
        """
        condition = ET.SubElement(self.root, "condition")
        
        # Add attribute
        cond1 = ET.SubElement(condition, "cond1")
        attr1 = ET.SubElement(cond1, "atribute1")
        attr1.set("name", attribute)
        
        # Add relation
        rel = ET.SubElement(condition, "relation")
        rel.set("type", relation)
        
        # Add value
        cond3 = ET.SubElement(condition, "cond3")
        cond3.text = value
        
        return self

    def order(self, attribute: BedcaAttribute, ascending: bool = True) -> "BedcaQueryBuilder":
        """Set the order for the query results.
        
        Args:
            attribute: The attribute to order by.
            ascending: Whether to order in ascending order (default: True).
            
        Returns:
            self: The query builder instance for method chaining.
        """
        order = ET.SubElement(self.root, "order")
        order.set("ordtype", "ASC" if ascending else "DESC")
        
        attr3 = ET.SubElement(order, "atribute3")
        attr3.set("name", attribute)
        
        return self

    def build(self) -> str:
        """Build the XML query string.
        
        Returns:
            str: The XML query string with proper formatting.
        """        
        # Convert the ElementTree to a string with proper indentation
        xml_str = ET.tostring(self.root, encoding='unicode')
        
        # Add proper indentation
        pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ", encoding="utf-8")
        return pretty_xml.decode('utf-8')


def get_all_foods_query() -> str:
    """Get the query to fetch all foods from BEDCA.
    
    Returns:
        str: The XML query string.
    """
    return (
        BedcaQueryBuilder()
        .select(
            BedcaAttribute.ID,
            BedcaAttribute.SPANISH_NAME,
            BedcaAttribute.LANGUAL,
            BedcaAttribute.ENGLISH_NAME,
            BedcaAttribute.ORIGIN,
            BedcaAttribute.EDIBLE_PORTION
        )
        .order(BedcaAttribute.SPANISH_NAME)
        .build()
    )


if __name__ == "__main__":
    print(get_all_foods_query())

"""Query builder for BEDCA API."""

from enum import StrEnum
from xml.dom import minidom
from typing import List, Optional
import xml.etree.ElementTree as ET


class BedcaAttribute(StrEnum):
    """Attributes available in BEDCA API."""
    
    # Food attributes
    ID = "f_id"
    SPANISH_NAME = "f_ori_name"
    ENGLISH_NAME = "f_eng_name"
    SCIENTIFIC_NAME = "sci_name"
    LANGUAL = "langual"
    FOODEX_CODE = "foodexcode"
    MAIN_LEVEL_CODE = "mainlevelcode"
    CODE_LEVEL_1 = "codlevel1"
    NAME_LEVEL_1 = "namelevel1"
    CODE_SUBLEVEL = "codsublevel"
    CODE_LEVEL_2 = "codlevel2"
    NAME_LEVEL_2 = "namelevel2"
    DESCRIPTION_ES = "f_des_esp"
    DESCRIPTION_EN = "f_des_ing"
    PHOTO = "photo"
    EDIBLE_PORTION = "edible_portion"
    ORIGIN = "f_origen"
    PUBLIC = "publico"
    
    # Component attributes
    COMPONENT_ID = "c_id"
    COMPONENT_NAME_ES = "c_ori_name"
    COMPONENT_NAME_EN = "c_eng_name"
    EURNAME = "eur_name"
    COMPONENT_GROUP_ID = "componentgroup_id"
    GLOSSARY_ES = "glos_esp"
    GLOSSARY_EN = "glos_ing"
    GROUP_NAME_ES = "cg_descripcion"
    GROUP_NAME_EN = "cg_description"
    BEST_LOCATION = "best_location"
    VALUE_UNIT = "v_unit"
    MOEX = "moex"
    STANDARD_DEVIATION = "stdv"
    MIN_VALUE = "min"
    MAX_VALUE = "max"
    N_VALUE = "v_n"
    UNIT_ID = "u_id"
    UNIT_NAME_ES = "u_descripcion"
    UNIT_NAME_EN = "u_description"
    VALUE_TYPE = "value_type"
    VALUE_TYPE_DESC_ES = "vt_descripcion"
    VALUE_TYPE_DESC_EN = "vt_description"
    MEASURE_UNIT_ID = "mu_id"
    MEASURE_UNIT_DESC_ES = "mu_descripcion"
    MEASURE_UNIT_DESC_EN = "mu_description"
    REFERENCE_ID = "ref_id"
    CITATION = "citation"
    ACQUISITION_TYPE_ES = "at_descripcion"
    ACQUISITION_TYPE_EN = "at_description"
    PUBLICATION_TYPE_ES = "pt_descripcion"
    PUBLICATION_TYPE_EN = "pt_description"
    METHOD_ID = "method_id"
    METHOD_TYPE_ES = "mt_descripcion"
    METHOD_TYPE_EN = "mt_description"
    METHOD_DESC_ES = "m_descripcion"
    METHOD_DESC_EN = "m_description"
    METHOD_NAME_ES = "m_nom_esp"
    METHOD_NAME_EN = "m_nom_ing"
    METHOD_HEADER_ES = "mhd_descripcion"
    METHOD_HEADER_EN = "mhd_description"


class BedcaRelation(StrEnum):
    """Relation types for BEDCA query conditions."""
    
    EQUAL = "EQUAL"
    LIKE = "LIKE"
    BEGINS_WITH = "BEGINW"


class BedcaQueryBuilder:
    """Builder for BEDCA API queries."""
    
    def __init__(self, level: int = 1):
        """Initialize the query builder.
        
        Args:
            level: The type level of the query (1 for basic food list, 2 for detailed food info)
        """
        self.root = ET.Element("foodquery")
        
        # Add type level
        type_elem = ET.SubElement(self.root, "type")
        type_elem.set("level", str(level))
        
        # Initialize selection element
        self.selection = ET.SubElement(self.root, "selection")
        
        # Always add the public condition for detailed queries
        if level == 2:
            self.where(BedcaAttribute.PUBLIC, BedcaRelation.EQUAL, "1")
    
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
        # Convert the ElementTree to a string
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
        BedcaQueryBuilder(level=1)
        .select(
            BedcaAttribute.ID,
            BedcaAttribute.SPANISH_NAME,
            BedcaAttribute.LANGUAL,
            BedcaAttribute.ENGLISH_NAME,
            BedcaAttribute.ORIGIN,
            BedcaAttribute.EDIBLE_PORTION
        )
        .where(BedcaAttribute.ORIGIN, BedcaRelation.EQUAL, "BEDCA")
        .order(BedcaAttribute.SPANISH_NAME)
        .build()
    )


def get_food_by_id_query(food_id: int) -> str:
    """Get the query to fetch detailed food information from BEDCA by ID.
    
    Args:
        food_id: The ID of the food to fetch.
        
    Returns:
        str: The XML query string.
    """
    return (
        BedcaQueryBuilder(level=2)
        .select(
            *[attr for attr in BedcaAttribute]  # Select all attributes
        )
        .where(BedcaAttribute.ID, BedcaRelation.EQUAL, str(food_id))
        .order(BedcaAttribute.COMPONENT_GROUP_ID)
        .build()
    )


if __name__ == "__main__":
    print(get_all_foods_query())

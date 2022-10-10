from dataclasses import dataclass
from typing import List

@dataclass
class Item():
    """Class for creating an item spec"""
    name: str
    unit_price: float
    weight_kg: float
    length: int
    width: int
    height: int
    qty: int = 1

    @property
    def total_cost(self) -> float:
        return self.unit_price * self.qty

@dataclass
class Parcel():
    parcel: List[Item]
    etsy_reference: str
    
    @property
    def total_parcel_cost(self) -> float:
        cost = 0
        for item in self.parcel:
            cost = cost+item.total_cost
        return cost
    
    @property
    def total_items(self) -> float:
        qty = 0
        for item in self.parcel:
            qty = qty+item.qty
        return qty
    
    @property
    def weight_kg(self) -> float:
        weight = 0
        for item in self.parcel:
            weight = weight+item.weight_kg*item.qty
        return weight
    
    @property
    def dimensions(self) -> float:
        length = max([item.length for item in self.parcel])
        width = max([item.width for item in self.parcel])
        height = 0
        for item in self.parcel:
            height = height+item.height*item.qty
        return length, width, height
    
    @property
    def contents(self) -> str:
        return ", ".join([item.name for item in self.parcel])
from pydantic import BaseModel
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ItemModel(BaseModel):
    item_name: str = Field(description="Name of the purchased item.")
    item_quantity: float = Field(description="Quantity of the purchased item.")
    item_quantity_units: str = Field(description="Quantity units of the purchased item. Can be either g for grams, kg for kilograms, ml for milliliters, l for liters, num for number of items.")
    item_discount: Optional[float] = Field(description="Discount applied to the item, if any. this must be monetary value.")
    item_price: float = Field(description="Normal price of the item before any discounts are applied.")

class CartModel(BaseModel):
    timestamp: datetime = Field(description="Date and time of sale.")
    store_name: str = Field(description="The name of the store where purchase was made.")
    currency: str = Field(description="Currency of transaction in ISO format.")
    purchase_total: float = Field(description="Total purchase value on the receipt.")
    purchase_total_tax: float = Field(description="Tax for the total purchase listed on the receipt in currency.")
    items: List[ItemModel] = Field(description="Tax for the total purchase listed on the receipt in currency.")
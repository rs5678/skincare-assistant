from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date as date_type

class SkinLogEntry(BaseModel):
    date: date_type
    symptoms: List[str] = Field(min_length=1)
    severity: int = Field(ge=1, le=5)
    products_used: List[str]
    notes: Optional[str] = None

class IngredientFact(BaseModel):
    ingredient_name: str
    category: str
    effects: Optional[List[str]] = None
    warnings: Optional[str] = None
    
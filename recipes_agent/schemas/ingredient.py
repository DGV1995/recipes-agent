from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    qty: float
    uom: str

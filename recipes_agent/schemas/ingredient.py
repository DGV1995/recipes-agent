from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    qty: int
    uom: str

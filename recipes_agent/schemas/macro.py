from pydantic import BaseModel


class Macro(BaseModel):
    qty: int
    uom: str

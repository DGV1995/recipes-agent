from pydantic import BaseModel

from recipes_agent.schemas.ingredient import Ingredient
from recipes_agent.schemas.macro import Macro


class Recipe(BaseModel):
    name: str
    category: str
    types: list[str]
    cooking_time: int
    ingredients: list[Ingredient]
    instructions: list[str]
    macros: dict[str, Macro]

from typing import Optional, TypedDict  # noqa: F401

from langchain_core.messages import BaseMessage


class RecipeBatchState(TypedDict):
    messages: list[BaseMessage]
    recipe_tasks: list[str]
    current_index: int

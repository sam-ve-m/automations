from typing import Any, List

from pydantic import BaseModel


class Graph(BaseModel):
    title: str
    plot_data: dict
    registers: int
    interactions: Any


class GraphSample(BaseModel):
    sample: List[dict]
    possible_fields: List[str]

from pydantic import BaseModel


class RequestExcel(BaseModel):
    representation: str
    highlights: dict


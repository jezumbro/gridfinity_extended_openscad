from pydantic import BaseModel, Field


class Tolerance(BaseModel):
    diameter: float = 0.25
    height: float = 0.5


class Configuration(BaseModel):
    tolerance: Tolerance = Field(default_factory=Tolerance)
    stackable: bool = True
    rows: int | None = None
    columns: int | None = None
    height: int | None = None
    per_row_height: bool = False

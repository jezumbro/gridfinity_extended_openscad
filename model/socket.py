import abc

from pydantic import AliasChoices, BaseModel, Field


class Tolerance(abc.ABC):
    @abc.abstractmethod
    def add_tolerance(self, tolerance: float) -> None: ...


class Socket(BaseModel, Tolerance):
    height: float
    diameter: float = Field(..., validation_alias=AliasChoices("diameter", "d1"))
    name: str

    @property
    def radius(self) -> float:
        return self.diameter / 2

    def add_tolerance(self, tolerance: float):
        self.diameter += tolerance


class MultiLevelSocket(Socket, Tolerance):
    small_diameter: float = Field(
        ..., validation_alias=AliasChoices("small_diameter", "d2")
    )
    transition_length: float = Field(
        ..., validation_alias=AliasChoices("transition_length", "transition")
    )
    offset: float

    @property
    def small_radius(self) -> float:
        return self.small_diameter / 2

    def add_tolerance(self, tolerance: float):
        super().add_tolerance(tolerance)
        self.small_diameter += tolerance

import abc

from pydantic import AliasChoices, BaseModel, Field


class Tolerance(abc.ABC):
    @abc.abstractmethod
    def add_diameter_tolerance(self, tolerance: float) -> None: ...
    def add_height_tolerance(self, tolerance: float) -> None: ...


class Socket(BaseModel, Tolerance):
    height: float
    diameter: float = Field(..., validation_alias=AliasChoices("diameter", "d1"))
    name: str

    @property
    def radius(self) -> float:
        return self.diameter / 2

    def add_diameter_tolerance(self, tolerance: float):
        self.diameter += tolerance

    def add_height_tolerance(self, tolerance: float) -> None:
        self.height += tolerance

    def __hash__(self):
        return hash((self.diameter, self.height, self.name))

    def __eq__(self, other) -> bool:
        if not type(other) == Socket:
            return False
        other: Socket
        return (
            self.diameter == other.diameter
            and self.height == other.height
            and self.name == other.name
        )


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

    def add_height_tolerance(self, tolerance: float):
        super().add_height_tolerance(tolerance)
        self.offset += tolerance * 0.5

    def add_diameter_tolerance(self, tolerance: float):
        super().add_diameter_tolerance(tolerance)
        self.small_diameter += tolerance

    def __hash__(self):
        return hash(
            (self.diameter, self.height, self.name, self.small_diameter, self.offset)
        )

    def __eq__(self, other):
        if not type(other) == MultiLevelSocket:
            return False
        other: MultiLevelSocket
        return (
            self.diameter == other.diameter
            and self.height == other.height
            and self.small_diameter == other.small_diameter
            and self.name == other.name
        )

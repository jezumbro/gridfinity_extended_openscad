from dataclasses import dataclass
from typing import Optional


@dataclass
class Socket:
    height: float
    diameter: float
    name: Optional[str]

    @property
    def radius(self) -> float:
        return self.diameter / 2

@dataclass
class MultiLevelSocket(Socket):
    small_diameter: float
    transition_length: float
    offset: float

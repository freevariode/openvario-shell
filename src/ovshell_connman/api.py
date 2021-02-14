import enum
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Sequence

from typing_extensions import Protocol


class ConnmanState(enum.Enum):
    UNKNOWN = "unknown"
    OFFLINE = "offline"
    IDLE = "idle"
    READY = "ready"
    ONLINE = "online"


class ConnmanServiceState(enum.Enum):
    IDLE = "idle"
    FAILURE = "failure"
    ASSOCIATION = "association"
    CONFIGURATION = "configuration"
    READY = "ready"
    DISCONNECT = "disconnect"
    ONLINE = "online"


@dataclass
class ConnmanTechnology:
    path: str
    name: str
    type: str
    connected: bool
    powered: bool


@dataclass
class ConnmanService:
    path: str
    auto_connect: bool
    favorite: bool
    name: str
    security: List[str]
    state: ConnmanServiceState
    strength: int
    type: str


class ConnmanManager(Protocol):
    technologies: Sequence[ConnmanTechnology]

    @abstractmethod
    async def setup(self) -> None:
        pass

    @abstractmethod
    def teardown(self) -> None:
        pass

    @abstractmethod
    def list_services(self) -> Sequence[ConnmanService]:
        pass

    @abstractmethod
    def on_service_property_changed(
        self, service: ConnmanService, handler: Callable[[ConnmanService], None]
    ) -> None:
        pass

    @abstractmethod
    def off_service_property_changed(
        self, service: ConnmanService, handler: Callable[[ConnmanService], None]
    ) -> None:
        pass

    @abstractmethod
    async def connect(self, service: ConnmanService) -> None:
        pass

    @abstractmethod
    async def remove(self, service: ConnmanService) -> None:
        pass

    @abstractmethod
    async def disconnect(self, service: ConnmanService) -> None:
        pass

    @abstractmethod
    async def power(self, tech: ConnmanTechnology, on: bool) -> None:
        pass

    @abstractmethod
    def on_technologies_changed(self, handler: Callable[[], None]) -> None:
        pass

    @abstractmethod
    def on_services_changed(self, handler: Callable[[], None]) -> None:
        pass

    @abstractmethod
    async def scan_all(self) -> int:
        pass

    @abstractmethod
    def get_state(self) -> ConnmanState:
        pass


class Canceled(Exception):
    pass


class ConnmanAgent(Protocol):
    """Interface for connman agent

    See https://git.kernel.org/pub/scm/network/connman/connman.git/tree/doc/agent-api.txt
    """

    @abstractmethod
    def report_error(self, service: ConnmanService, error: str) -> None:
        pass

    @abstractmethod
    async def request_input(
        self, service: ConnmanService, fields: Dict[str, Dict[str, str]]
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def cancel(self) -> None:
        pass

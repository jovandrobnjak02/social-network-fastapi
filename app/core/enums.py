import enum

class Role(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class ConnectionStatus(enum.Enum):
    REQUESTED = "REQUESTED"
    CONNECTED = "CONNECTED"
    NOT_CONNECTED = "NOT CONNECTED"
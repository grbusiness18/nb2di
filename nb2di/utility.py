from functools import wraps
from enum import Enum


class PortKind(Enum):
    INPUT = "input"
    OUTPUT = "output"


class ContentType(Enum):
    MESSAGE = "message"
    ARTIFACT = "message.artifact"
    STRING = "string"
    ANY = "any.*"
    BLOB = "blob"
    INT64 = "int64"
    UINT64 = "uint64"
    FLOAT64 = "float64"
    BYTE = "byte"
    STREAM = "stream"
    UNKNOWN = "unknown"


def validate_di(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        self.validate_di_mode_is_on()
        method_output = method(self, *method_args, **method_kwargs)
        return method_output
    return _impl

from .utility import PortKind, ContentType
#from .port import Port
import nb2di.port as nb

class ConnectionTemplateSourceToTarget:
    def __init__(self, src: nb.Port, tgt: nb.Port):

        if not isinstance(src, nb.Port) and not isinstance(tgt, nb.Port):
            raise Exception("Invalid Connection Template")

        self.src = src
        self.tgt = tgt


class ConnectionTemplate:
    def __init__(self, port: nb.Port):
        if not isinstance(port, nb.Port):
            raise Exception("Invalid Operator: src_operator")
        self.target_port = port


class PortTemplate:
    def __init__(self, name: str, kind: PortKind=None, content_type: ContentType=None, target: ConnectionTemplate=None):
        self.name = name
        self.kind = kind
        if content_type is not None and not isinstance(content_type, ContentType):
            raise Exception("Invalid Argument Type for ContentType")

        if target is not None and not isinstance(target, ConnectionTemplate):
            raise Exception("Invalid Argument Type for connection")

        self.content_type = content_type
        self.target = target

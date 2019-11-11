from .utility import PortKind, ContentType
from sapdi.internal.modeler.port_info import PortInfo
from .connections import ConnectionHandlerWithPort
from jq import jq


class Port(object):

    def __init__(self, cxt,  name: str, kind: PortKind, contenttype: ContentType=None):
        self.port_context = cxt
        self.name = name
        self.kind = kind
        self.contenttype = contenttype
        self.connection = ConnectionHandlerWithPort(self)

    def delete(self):
        from .template import PortTemplate
        self.port_context.delete_port(PortTemplate(self.name))


class Ports(object):
    def __init__(self, opr):
        from .operator import Operator

        if not isinstance(opr, Operator):
            raise Exception("Invalid Operator Instance")

        self.inports  = PortContext(opr, PortKind.INPUT)
        self.outports = PortContext(opr, PortKind.OUTPUT)


class PortContext(object):
    def __init__(self, operator, kind: PortKind):
        from .operator import Operator
        if not isinstance(operator, Operator):
            raise Exception("Invalid Operator Instance")

        self.kind = kind
        self.operator = operator
        for p in self.get_ports():
            self.add_ports_class_attrib(p)

    def add_ports_class_attrib(self, p):
        setattr(self, p.name, Port(self, p.name, self.kind))

    def delete_ports_class_attrib(self, p):
        try:
            delattr(self, p.name)
        except AttributeError:
            pass

    def add_port(self, port):
        from .template import PortTemplate
        if not isinstance(port, PortTemplate):
            raise Exception("Invalid port instance")

        if self.check_port_already_exists(port.name, self.kind):
            raise Exception("Port '{}' already exists".format(port.name))

        pi = PortInfo(name=port.name, type_=port.content_type)
        if self.kind == PortKind.INPUT:
            self.operator.operator.operatorinfo.add_inport(port=pi)
        else:
            self.operator.operator.operatorinfo.add_outport(port=pi)

        self.add_ports_class_attrib(pi)

        if port.target:
            self.add_connection(pi.name, connection=port.target)

    def add_connection(self, port_name, connection):
        try:
            pc = getattr(self, port_name)
            pc.connection.add_connections([connection])
        except AttributeError:
            raise Exception("Invalid Port")

    def delete_connection(self, port_name, connection):
        try:
            pc = getattr(self, port_name)
            pc.connection.delete_connections([connection])
        except AttributeError:
            raise Exception("Invalid Port")

    def delete_port(self, port):
        if self.kind == PortKind.INPUT:
            self.operator.operator.operatorinfo.delete_inport(port.name)
        else:
            self.operator.operator.operatorinfo.delete_outport(port.name)
        self.delete_ports_class_attrib(port)

        if port.target:
            self.delete_connection(port.name, connection=port.target)

    def list_port(self):
        if self.kind == PortKind.INPUT:
            return self.get_inports()
        else:
            return self.get_outports()

    def check_port_already_exists(self, port_name: str, port_kind: PortKind):
        port_exists = False
        inports = [ip.name for ip in self.get_inports()]
        outports = [op.name for op in self.get_outports()]
        if port_kind == PortKind.INPUT:
            if port_name in inports:
                port_exists = True
        else:
            if port_name in outports:
                port_exists = True
        return port_exists

    def get_ports(self):
        if self.kind == PortKind.INPUT:
            return self.get_inports()
        else:
            return self.get_outports()

    def get_inports(self):
        return self.operator.operator.operatorinfo.inports

    def get_outports(self):
        return self.operator.operator.operatorinfo.outports

    def get_connections(self):
        g = self.get_graph().to_json()
        if 'connections' in g:
            return g['connections']
        else:
            return []

    def get_ports_for_operator(self, kind: PortKind = PortKind.INPUT):
        connections = self.get_connections()
        if not connections:
            return []

        port_type = 'src'
        if kind == PortKind.INPUT:
            port_type = 'tgt'
        else:
            port_type = 'src'

        trns = '.[] | select(&1.process == "&2")'.replace("&1", "." + port_type).replace("&2", self.instance_id)
        try:
            cops = jq(trns).transform(connections, multiple_output=True)
            ports = [cop[port_type]['port'] for cop in cops]
            return ports
        except:
            return []
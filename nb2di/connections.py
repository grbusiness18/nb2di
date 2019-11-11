from .context import Context
from .utility import PortKind
from jq import jq


class ConnectionHandlerWithPort(Context):
    def __init__(self, port):
        from .port import Port
        super().__init__()
        if not isinstance(port, Port):
            raise Exception("Invalid Port Instance")
        self.source_port = port

    def add_connection(self, p: object):
        from .port import Port
        if not isinstance(p, Port):
            raise Exception("Invalid connection instance")
        g = self.get_graph()
        g.add_connection(self.source_port.port_context.operator.operator,
                         self.source_port.name, p.port_context.operator.operator, p.name)

    def delete_connection(self, p: object):
        from .port import Port
        if not isinstance(p, Port):
            raise Exception("Invalid connection instance")
        g = self.get_graph()
        g.delete_connection(self.source_port.port_context.operator.operator, self.source_port.name, p.port_context.operator.operator, p.target_port.name)

    def get_connections(self):
        g = self.get_graph().to_json()
        if 'connections' in g:
            return g['connections']
        else:
            return []

    def get_connections_operator(self):
        output = []
        con = self.jq_transformation_for_connection(PortKind.INPUT, self.source_port.port_context.operator.instance_id)
        if con:
            output.extend(con)

        con = self.jq_transformation_for_connection(PortKind.OUTPUT, self.source_port.port_context.operator.instance_id)
        if con:
            output.extend(con)
        return output

    def get_connections_operator_port(self):
        output = []
        con = self.jq_transformation_for_connection(PortKind.INPUT, self.source_port.port_context.operator.instance_id, self.source_port.name)
        if con:
            output.extend(con)

        con = self.jq_transformation_for_connection(PortKind.OUTPUT, self.source_port.port_context.operator.instance_id,self.source_port.name)
        if con:
            output.extend(con)
        return output

    def jq_transformation_for_connection(self, kind: PortKind, opr_name: str, port_name: str=None):
        port_type = 'src'
        if kind == PortKind.INPUT:
            port_type = 'tgt'
        else:
            port_type = 'src'

        trns = '.[] | select(&1.process == "&2")'.replace("&1", "." + port_type).replace("&2", opr_name)

        if port_name:
            trns = '.[] | select(&1.process == "&2" and &1.port == "&3)'.replace("&1", "." + port_type)
            trns = trns.replace("&2", opr_name).replace("&3", port_name)

        try:
            cops = jq(trns).transform(self.get_connections(), multiple_output=True)
            return cops
        except:
            return []


class ConnectionHandler(Context):

    def __init__(self, src_port, tgt_port):
        from .port import Port
        super().__init__()
        if not isinstance(src_port, Port):
            raise Exception("Invalid Port Instance")
        if not isinstance(tgt_port, Port):
            raise Exception("Invalid Port Instance")

        self.source_port = src_port
        self.target_port = tgt_port

    def add_connections(self):
        g = self.get_graph()
        g.add_connection(self.source_port.port_context.operator.operator, self.source_port.name, self.target_port.port_context.operator.operator, self.target_port.name)

    def delete_connections(self):
        g = self.get_graph()
        g.delete_connection(self.source_port.port_context.operator.operator, self.source_port.port_context.name, self.target_port.port_context.operator.operator, self.target_port.name)


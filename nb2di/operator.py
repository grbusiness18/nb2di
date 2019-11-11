from .context import Context
from .utility import PortKind
from .template import PortTemplate
from jq import jq
import re
from .port import Ports


class Operator(Context):
    def __init__(self, instance_id: str = None, component_name: str = None, create_ports: list=[]):
        super().__init__()
        if instance_id is None and component_name is None:
            raise Exception("Please Provide instance ID or Component Name")

        self.instance_id = None
        self.component_name = None
        self.operator = None
        self.ports = None

        if instance_id is not None:
            self.instance_id = instance_id
            self.get_existing_operator()

        if instance_id is None and component_name is not None:
            self.component_name = component_name
            self.create_new_operator()

        self.set_ports_context()

        if create_ports:
            self.create_new_ports(create_ports)

    def set_ports_context(self):
        self.ports = Ports(self)

    def get_existing_operator(self):
        self.operator = self.get_operator()
        self.component_name = self.operator.operatorinfo.component_name

    def get_operator(self):
        self.check_operator_in_graph()
        self.operator = self.get_graph().operators[self.instance_id]
        return self.operator

    def check_operator_in_graph(self):
        if self.instance_id not in self.get_graph().operators.keys():
            raise Exception("Invalid Operator {} instance name".format(self.instance_id))

    def validate_component_name(self):
        rex = re.compile(r'.*' + self.component_name, re.IGNORECASE)
        if len(list(filter(rex.match, self.get_operator_names()))) == 0:
            raise Exception("Invalid Component Name of Operator")

    def generate_instance_name(self):
        opr_inst_name = None
        if self.instance_id:
            opr_inst_name = self.instance_id
        else:
            opr_inst_name = self.component_name.rsplit('.', 1)[1]

        rex = re.compile(r'.*' + opr_inst_name, re.IGNORECASE)
        operator_count = len(list(filter(rex.match, list(self.get_graph().operators.keys()))))

        if operator_count == 0:
            opr_inst_name = opr_inst_name + "1"
        else:
            opr_inst_name = opr_inst_name + str(operator_count + 1)

        return opr_inst_name

    def create_new_operator(self):
        self.validate_component_name()
        self.operator = self.get_model_manager().create_operator(instance_name=self.generate_instance_name(),
                                                                 operatorinfo=self.get_operator_info(
                                                                     self.component_name))
        self.instance_id = self.operator.instance_name
        self.get_graph().add_operator(self.operator)

    def create_new_ports(self, ports: list=[]):
        for p in ports:
            if not isinstance(p, PortTemplate):
                raise Exception("Invalid Port Template")
            if p.kind == PortKind.INPUT:
                self.ports.inports.add_port(p)
            else:
                self.ports.outports.add_port(p)

    def delete_ports(self, ports: list=[]):
        for p in ports:
            if not isinstance(p, PortTemplate):
                raise Exception("Invalid Port Template")
            if p.kind == PortKind.INPUT:
                self.ports.inports.delete_port(p)
            else:
                self.ports.outport.delete_port(p)

    def is_operator_scriptable(self):
        opi = self.get_operator_info(self.component_name)
        if not 'script' in opi.get_config().keys():
            raise Exception("Operator {} is not scriptable".format(opi.component))

    def add_code_to_operator(self, code: str, fn_name: str):
        self.is_operator_scriptable()
        inports = self.get_ports_for_operator()
        callback_code = None
        if len(inports) == 1:
            callback_code = 'api.set_port_callback("{}", {})'.format(inports[0], fn_name)

        if len(inports) > 1:
            port_string = None
            for p in inports:
                if port_string:
                    port_string = port_string + ", " + '"{}"'.format(p)
                else:
                    port_string = '"{}"'.format(p)
            port_string = '[ ' + port_string + ' ]'
            callback_code = 'api.set_port_callback(&1, {})'.replace("&1", port_string).format(fn_name)

        if callback_code:
            code = code + '\n' + callback_code

        self.get_graph().operators[self.operator.instance_name].config['script'] = code

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





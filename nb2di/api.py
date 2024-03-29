from .operator import Operator
#from .connections import
from .template import ConnectionTemplateSourceToTarget
from .context import Context
from .pipeline import Pipeline
from .utility import validate_di
from .connections import ConnectionHandler
import inspect


class ApiLog(object):
    def __init__(self):
        self.info = lambda *args, **kwargs: print("Info: Arguments {} \nKeyed-Arguments {}".format(args, kwargs))
        self.warn = lambda *args, **kwargs: print("Warn: Arguments {} \nKeyed-Arguments {}".format(args, kwargs))
        self.error = lambda *args, **kwargs: print("Error: Arguments {} \nKeyed-Arguments {}".format(args, kwargs))
        self.debug = lambda *args, **kwargs: print("Debug: Arguments {} \nKeyed-Arguments {}".format(args, kwargs))


class Api(Context):
    def __init__(self):
        super().__init__()
        self.send = lambda *args, **kwargs: print("Send: Arguments {} \nKeyed-Arguments {}".format(args, kwargs))
        self.Message = lambda *args, **kwargs: print("Message: Arguments {} \nKeyed-Arguments {}".format(args, kwargs))
        self.logger = ApiLog()

    def operator(self, instance_id: str=None, component_name: str=None, ports: list=[]):
        def wrapper(fn):
            def inner_wrapper(*args, **kwargs):
                code = inspect.getsource(fn).split('\n', 1)[1]
                fn_name = fn.__name__
                if not self.get_di_mode():
                    ret = fn(*args, **kwargs)
                    return ret
                else:
                    opr = Operator(instance_id=instance_id, component_name=component_name, create_ports=ports)
                    opr.add_code_to_operator(code, fn_name)
                    opr.save_graph()
            return inner_wrapper
        return wrapper

    @validate_di
    def add_port_to_operator(self, instance_id: str, ports: list=[]):
        opr = Operator(instance_id=instance_id)
        opr.create_new_ports(ports=ports)
        opr.save_graph()

    @validate_di
    def add_connections_to_port(self, connections: list=[]):
        for c in connections:
            if not isinstance(c, ConnectionTemplateSourceToTarget):
                raise Exception("Invalid Connection Instances")
            ch = ConnectionHandler(c.src, c.tgt)
            ch.add_connections()
            ch.save_graph()

    def create_pipeline(self, name: str=None, desc: str=None, template: str=None):
        self.set_di_mode_on(ignore_validation=True)
        p = Pipeline(name=name, desc=desc, template=template)
        return p.pipeline_id

    @validate_di
    def get_operator_component_name(self, name: str = None):
        return self.get_operator_names(name)

    @validate_di
    def get_pipeline_template_name(self, name: str = None):
        return self.get_pipeline_templates(name)

    @validate_di
    def get_current_pipeline_id(self):
        pipeline = self.get_pipeline()
        return pipeline.id, pipeline.name

   # @validate_di
    def set_pipeline_by_id(self, value: str):
        pipeline = self.set_pipeline_byid(value)
        return pipeline.id, pipeline.name

    @validate_di
    def get_pipeline_operator_list(self):
        return self.get_graph_operators_list()

    @validate_di
    def execute_pipeline(self):
        self.di_context.execute()


api = Api()
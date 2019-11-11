import logging
from .di import DICONTEXT

log = logging.getLogger('di_logger')


class Context:
    def __init__(self):
        self.di_context = DICONTEXT

    def get_graph(self):
        return self.di_context.get_graph()

    def get_pipeline_templates(self, name: str=None):
        return self.di_context.get_pipeline_templates(name)

    def get_operator_names(self, name: str=None):
        return self.di_context.get_operator_names(name)

    def get_operator_info(self, component_name: str):
        return self.di_context.get_operator_info(component_name)

    def get_pipeline(self):
        return self.di_context.get_current_pipeline()

    def get_model_manager(self):
        return self.di_context.MODEL_MANAGER

    def get_di(self):
        return self.di_context.DI

    def get_di_mode(self):
        return self.di_context.get_di_mode()

    def get_all_pipelines_in_current_scenario(self):
        return self.di_context.list_pipelines_in_current_scenario()

    def set_pipeline_byid(self, value: str):
        return self.di_context.set_pipeline_by_id(value)

    def validate_di_mode_is_on(self):
        self.di_context.validate_di_mode()

    def set_di_mode_on(self, ignore_validation: bool=True):
        self.di_context.set_di_mode_on(ignore_validation)

    def set_di_mode_off(self):
        self.di_context.set_di_mode_off()

    def get_graph_operators_list(self):
        return list(self.get_graph().to_json()['processes'].keys())

    def save_graph(self, fetch_graph: bool=False, execute_graph: bool=False):
        self.di_context.get_graph(fetch_graph).save()
        if execute_graph:
            self.execute()

    def execute(self):
        self.di_context.execute()
from sapdi.internal.di_client import DIClient
from sapdi.internal.modeler.graph import Graph
from sapdi.scenario.scenario import Scenario
from sapdi.scenario.pipeline import Pipeline
from dotenv import load_dotenv, find_dotenv
import sapdi as di
import logging
import os
import re
import time
from datetime import datetime

log = logging.getLogger('di_logger')


class DiManager(object):
    def __init__(self):
        self.PIPELINE = None
        self.SCENARIO = None
        self.MODEL_MANAGER = None
        self.GRAPH = None
        self.DI = None
        self.OPERATOR_NAMES = []
        self.PIPELINE_TEMPLATES = []
        self.DI_MODE = False
        self.__set_di_context()

    def __set_di_context(self):
        s = di.get_current_scenario()
        try:
            if s.name:
                self.set_scenario_by_id(scenario_id=s.id)
        except AttributeError:
            self.di_connect()

        self.set_defaults()

    def di_connect(self):
        print("connecting to DI...")
        load_dotenv(find_dotenv())
        start = time.time()
        di.connect(url=os.environ['DI_CLUSTER_URL'],
                   tenant=os.environ['DI_TENANT'],
                   username=os.environ['DI_USERNAME'],
                   password=os.environ['DI_PASSWORD'])

        print("connected in {} seconds".format(time.time() - start))

        if 'DI_SCENARIO_ID' in os.environ:
            self.set_scenario_by_id(os.environ['DI_SCENARIO_ID'])
            di.set_current_scenario(self.SCENARIO)
            log.warning("Current Scenario : {}".format(self.SCENARIO.name))
        else:
            raise Exception("Scenario can't be EMPTY. Use Env.Variable DI_SCENARIO_ID to set it.")

        if 'DI_PIPELINE_ID' in os.environ:
            self.set_pipeline_by_id(pipeline_id=os.environ['DI_PIPELINE_ID'])
        else:
            log.warning("Please Set/Create Pipeline ID.")

    def set_defaults(self):
        self.set_model_manager()
        self.set_di()
        self.set_pipeline_template_names()
        self.set_operator_names()

    def set_model_manager(self):
        self.MODEL_MANAGER = DIClient.getInstance().getModelerManager()

    def set_di(self):
        self.DI = di

    def set_pipeline_template_names(self):
        self.PIPELINE_TEMPLATES = [x["name"] for x in di.list_pipeline_templates()]

    def set_operator_names(self):
        self.OPERATOR_NAMES = [x.name for x in DIClient.getInstance().getModelerManager().repo.list_operators()]

    def set_graph(self):
        start = time.time()
        if not isinstance(self.PIPELINE, Pipeline):
            raise Exception("Invalid Pipeline")
        self.GRAPH = DIClient.getInstance().getModelerManager().find_graph("{}".format("com.sap.dsp." + self.PIPELINE.id))
        #print(traceback.print_stack())
        print("Current DI Pipeline Set {}".format(time.time() - start))

    def set_scenario(self, scenario: Scenario):
        if not isinstance(scenario, Scenario):
            raise Exception("Invalid Scenario Object")
        self.SCENARIO = DiManager.get_scenario_by_id(scenario.id)

    def set_scenario_by_id(self, scenario_id:str):
        scenario = DiManager.get_scenario_by_id(scenario_id)
        self.set_scenario(scenario)

    @staticmethod
    def get_scenario_by_id(scenario_id: str):
        return di.scenario.Scenario.get(scenario_id=scenario_id)

    def set_pipeline(self, pipeline: Pipeline):
        if not isinstance(pipeline, Pipeline):
            raise Exception("Invalid Pipeline Object")
        self.PIPELINE = DiManager.get_pipeline_by_id(pipeline.id)
        self.set_graph()

    def set_pipeline_by_id(self, pipeline_id: str):
        pipeline = DiManager.get_pipeline_by_id(pipeline_id)
        self.set_pipeline(pipeline)
        return pipeline

    @staticmethod
    def get_pipeline_by_id(pipeline_id: str):
        return di.get_pipeline(pipeline_id=pipeline_id)

    def get_pipeline_templates(self, name: str=None):
        if name:
            rex = re.compile(r'.*' + name, re.IGNORECASE)
            return list(filter(rex.match, self.PIPELINE_TEMPLATES))
        else:
            return self.PIPELINE_TEMPLATES

    def get_operator_names(self, name: str=None):
        if name:
            rex = re.compile(r'.*' + name, re.IGNORECASE)
            return list(filter(rex.match, self.OPERATOR_NAMES))
        else:
            return self.OPERATOR_NAMES

    def get_graph(self, fetch: bool=False):
        if fetch:
            self.GRAPH = DIClient.getInstance().getModelerManager().find_graph(
                "{}".format("com.sap.dsp." + self.PIPELINE.id))

        return self.GRAPH

    def list_pipelines_in_current_scenario(self):
        return self.DI.list_pipelines()

    def get_operator_info(self, component_name: str):
        return self.MODEL_MANAGER.find_operator_info(component_name=component_name)

    def get_current_pipeline(self):
        return self.PIPELINE

    def get_di_mode(self):
        return self.DI_MODE

    def execute(self):
        pipeline = self.get_current_pipeline()
        #try:
        version = di.create_version()
        print(pipeline, version)
        desc = "Generated Conf {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        print(desc)
        conf = di.scenario.Configuration.create(desc, [], pipeline, version)
        print(conf)
        pipeline.execute(conf)
        #except:
         #   print("Unable to Execute Pipeline: {} . Error Occurred".format(pipeline.id))

    def set_di_mode_on(self, ignore_validation: bool=False):
        log.warning("Setting DI Mode to ON")
        if not ignore_validation and self.PIPELINE is None:
            raise Exception('Pipeline is invalid/Empty. Please set the pipeline')
        self.DI_MODE = True
        # log.warning("Current Pipeline '{}'".format(self.get_current_pipeline().name))

    def set_di_mode_off(self):
        self.DI_MODE = False

    def validate_di_mode(self):
        if not self.get_di_mode():
            raise Exception("Di Mode is OFF.")


DICONTEXT = DiManager()

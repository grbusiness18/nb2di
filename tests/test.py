from nb2di import Operator, ConnectionTemplateSourceToTarget
from nb2di import PortTemplate, PortKind, ContentType
from nb2di import api

def test():
    #api.create_pipeline()
    api.set_pipeline_by_id('d71ea8cb-6cbf-45fe-8ab3-e172d653844c')
    # create port template
    python_opr_port = PortTemplate(name="test", kind=PortKind.OUTPUT, content_type=ContentType.MESSAGE)

    # create python operator
    python_opr = Operator(component_name="com.sap.system.python3Operator", create_ports=[python_opr_port])
    metrics_opr = Operator(component_name="com.sap.ml.submitMetrics")

    # create port template
    terminator_opr_port = PortTemplate(name="stop", kind=PortKind.INPUT, content_type=ContentType.ANY)

    terminator_opr = Operator(component_name="com.sap.util.graphTerminator", create_ports=[terminator_opr_port])

    python_opr.ports.outports.test.connection.add_connection(metrics_opr.ports.inports.metrics)

    metrics_opr.ports.outports.response.connection.add_connection(terminator_opr.ports.inports.stop)

    python_opr.save_graph(execute_graph=True)

test()
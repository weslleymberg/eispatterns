import unittest
from should_dsl import should
from ludibrio import Dummy
from domain.node.node import Node
from domain.movement.movement import Movement
from domain.movement.process import Process
from domain.movement.transformation import Transformation
from configurator.statemachine.configuration import ProcessTemplate
from domain.resource.operation import operation
from domain.supportive.association_error import AssociationError
#from configurator.fluidity import StateMachineTemplate
#from fluidity import state, transition


class ProcessSpec(unittest.TestCase):

    def setUp(self):
        self.a_client = Node()
        self.the_company = Node()
        self.a_process = Process()
        self.a_process.set_source(self.the_company)
        self.a_process.set_destination(self.a_client)
        self.a_processing_unit = Node()
        self.a_movement = Movement()
        self.a_movement.set_source(self.a_processing_unit)
        self.a_movement.set_destination(self.a_processing_unit)

    def it_inserts_a_movement(self):
        #should not work
        non_movement = "I am not a Movement"
        (self.a_process.insert_movement, 'Ops!',non_movement) |should| throw(AssociationError)
        #test doubles won't work given type checking rules, using classic
        self.a_process.insert_movement('A movement', self.a_movement)
        self.a_process.movements |should| contain('A movement')

    def it_inserts_a_node(self):
        #should not work
        non_node = "I am not a Node"
        (self.a_process.insert_node, 'Ops!', non_node) |should| throw(AssociationError)
        #test doubles won't work given type checking rules, using classic
        self.a_process.insert_node('A company processing unit', self.a_processing_unit)
        self.a_process.nodes |should| contain('A company processing unit')

'''
    def it_configures_itself_from_a_template(self):
        template = type('object', (object,), {})()
        template.states = [1, 2]
        transformations = [Transformation(), Transformation()]
        template.transformations = transformations
        process = Process()
        process.configure(template)
        process.template |should| equal_to(template)
        process.states |should| equal_to([1, 2])
        process.transformations |should| equal_to(transformations)

    def it_adds_a_transformation_from_template_as_a_movement(self):
        class CreditAnalyst(object):
            def create_loan(self): pass
        template = ProcessTemplate(initial_state='start')
        template.transformation('Create Loan',action=CreditAnalyst.create_loan)
        process = Process()
        process.configure(template)
        process.movements['Create Loan'] |should| equal_to(template.transformations[0])
'''


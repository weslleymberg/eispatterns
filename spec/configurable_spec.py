import unittest
from should_dsl import should
from ludibrio import Stub
from domain.configurable import Configurable

class ConfigurableSpec(unittest.TestCase):

    def setUp(self):
        self.configurable = Configurable()

    def it_defines_a_todo_method(self):
        #todo is just a protocol
        self.configurable.todo() |should| equal_to(self.configurable.tag)

    def it_obtains_a_configuration(self):
        #Stubs a configuration object
        with Stub() as configuration:
            configuration.mask >> 'a mask'
            configuration.version >> 'a version'
        #expected_configuration_attributes is defined only in subclasses, forced below
        self.configurable.expected_configuration_attributes = ['mask','version']
        self.configurable.configure(configuration)
        self.configurable.configuration.mask |should| equal_to('a mask')
        self.configurable.configuration.version |should| equal_to('a version')
        #resource.configuration |should| be(configuration)

    def it_defines_a_tag(self):
        #first method's scenario
        self.configurable.define_tag()
        self.configurable.tag |should| equal_to(0)
        #second method's scenario
        self.configurable.define_tag(10)
        self.configurable.tag |should| equal_to(10)

import unittest
from should_dsl import should
import eispatterns_examples.bank_system.decorators.credit_analyst_decorator
import eispatterns_examples.bank_system.resources
from configurator.documenter import Documenter
import configurator.rule_checker_imports
import configurator.documenter_imports

class DocumenterSpec(unittest.TestCase):

    def setUp(self):
        self.documenter = Documenter()

    def it_finds_classes(self):
        #a decorator module, which imports two other decorator modules
        self.documenter.find_classes(eispatterns_examples.bank_system.decorators.credit_analyst_decorator)
        self.documenter |should| have(3).decorators
        #a resource module
        self.documenter.work_items = []
        self.documenter.find_classes(eispatterns_examples.bank_system.resources.loan)
        self.documenter |should| have(2).work_items
        #a imports module
        self.documenter.decorators = []
        self.documenter.work_items = []
        self.documenter.find_classes(configurator.documenter_imports)
        self.documenter |should| have(4).decorators
        self.documenter |should| have(2).work_items

    def it_gets_decorators_operations(self):
        self.documenter.find_classes(configurator.documenter_imports)
        self.documenter.get_decorators_operations()
<<<<<<< HEAD
        self.documenter |should| have(8).operations
=======
        self.documenter |should| have(6).operations
>>>>>>> cb5b2b83d411acb1e9fa7f289880d67621a0bc2e

    def it_gets_work_items_documentations(self):
        self.documenter.find_classes(configurator.documenter_imports)
        self.documenter.get_work_items_documentations()
        self.documenter |should| have(2).work_items_documentations

    def it_searches_a_term(self):
        self.documenter.find_classes(configurator.documenter_imports)
        self.documenter.get_work_items_documentations()
        self.documenter.get_decorators_operations()
        self.documenter.search_term('loan')
<<<<<<< HEAD
        #3 @operations from credit_analyst_decorator, loan_request.__doc__, loan.__doc__
=======
        #4 @operations from credit_analyst_decorator, loan_request.__doc__, loan.__doc__
>>>>>>> cb5b2b83d411acb1e9fa7f289880d67621a0bc2e
        self.documenter.found |should| have(6).items
        self.documenter.search_term('xxxx')
        self.documenter.found |should| have(0).item


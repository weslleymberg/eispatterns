#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from should_dsl import should
from domain.node.person import Person
from domain.supportive.association_error import AssociationError
from bank_system.decorators.client_decorator import ClientDecorator


class ClientDecoratorsSpec(unittest.TestCase):

    def setUp(self):
        self.an_client_decorator = ClientDecorator()
        self.an_client = Person()

    def it_decorates_a_person(self):
        #should work
        self.an_client_decorator.decorate(self.an_client)
        self.an_client_decorator.decorated |should| be(self.an_client)
        self.an_client |should| have(1).decorators
        #should fail
        non_person = 'I am not a person'
        (self.an_client_decorator.decorate, non_person) |should| throw(AssociationError)

    def it_generates_a_register(self):
        self.an_client_decorator.generate_register('1234 5 - 6')
        self.an_client_decorator.register |should| equal_to('1234 5 - 6')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from should_dsl import should
from domain.base.decorator import Decorator
from domain.node.person import Person
from domain.resource.operation import operation
from domain.supportive.rule import rule
from domain.supportive.association_error import AssociationError


class ClientDecorator(Decorator):
    '''A general porpuse Client decorator'''

    def __init__(self):
        Decorator.__init__(self)
        self.description = "Supplies the basis for representing clients"

    def generate_register(self, register):
        ''' generates de register number for the client'''
        self.register = register

    def decorate(self, decorated):
        try:
            ClientDecorator.rule_should_be_person_instance(decorated)
        except:
            raise AssociationError('Person instance expected, instead % s passed' % type(decorated))
        self.decorated = decorated
        self.decorated.decorators[self.__doc__] = self
    @classmethod
    @rule('association')

    def rule_should_be_person_instance(self, decorated):
        ''' Decorated object should be a Person '''
        decorated |should| be_instance_of(Person)

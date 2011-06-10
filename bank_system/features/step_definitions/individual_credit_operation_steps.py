# -*- coding: utf-8 -*-
from lettuce import step, world
from should_dsl import should
from domain.node.person import Person
from domain.node.machine import Machine
from domain.movement.process import Process
from domain.movement.transformation import Transformation
from domain.movement.transportation import Transportation
from bank_system.decorators.credit_analyst_decorator import CreditAnalystDecorator
from bank_system.decorators.bank_account_decorator import BankAccountDecorator
from bank_system.decorators.employee_decorator import EmployeeDecorator
from fluidity.machine import StateMachine, state, transition, InvalidTransition
from extreme_fluidity.xfluidity import StateMachineConfigurator
from loan_process_template import LoanProcess

#
# ATTENTION: you can't run more than one example, otherwise Fluidity will return
# an error of type InvalidTransition: Cannot change from new_state to new_state
# since after the first example the machine changes its state
#


#Scenario Individual Customer asks for loan
@step(u'Given I am a registered Credit Analyst')

def given_i_am_a_registered_credit_analyst(step):
     world.a_person = Person()
     an_employee_decorator = EmployeeDecorator()
     an_employee_decorator.decorate(world.a_person)
     world.credit_analyst = CreditAnalystDecorator('09876-5')
     world.credit_analyst.decorate(world.a_person)

@step(u'And an individual customer with account number (.+) asks for a personal loan')
def and_an_individual_customer_with_account_number_account_number_asks_for_a_personal_loan(step, account_number):
    world.a_machine = Machine()
    world.account = BankAccountDecorator(account_number)
    world.account.average_credit = 2501
    world.account.decorate(world.a_machine)

@step(u'And the loan request is of (.+)')
def and_the_loan_request_is_of_desired_value(step, desired_value):
    #GUI action
    pass

@step(u'When I confirm the loan request')
def when_i_confirm_the_loan_request(step):
    #GUI action which will start the whole process
    pass

@step(u'Then a new loan request with the (.+) and (.+) is created')
def then_a_new_loan_request_with_the_account_number_and_desired_value_is_created(step, account_number, desired_value):
    #Processes are nodes that use the company as the source node, and the client as destination
    world.the_company = Machine()
    world.a_client = Person()
    #now the business process starts to be assembled
    world.an_individual_credit_operation = Process('Individual Customer Credit Operation')
    world.an_individual_credit_operation.set_source(world.the_company)
    world.an_individual_credit_operation.set_destination(world.a_client)
    #configures the process using a template state machine
    template = LoanProcess()
    configurator = StateMachineConfigurator(template)
    configurator.configure(world.an_individual_credit_operation)
    #configures the loan request creation
    the_movement = world.an_individual_credit_operation.configure_activity(world.credit_analyst.decorated, world.credit_analyst.decorated, world.an_individual_credit_operation.create_loan_request, CreditAnalystDecorator.create_loan_request)
    #runs the loan request creation
    the_movement.context = world.an_individual_credit_operation.run_activity(the_movement, world.credit_analyst, world.account, desired_value)
    world.an_individual_credit_operation.current_state() |should| equal_to('request_created')
    world.an_individual_credit_operation.movements |should| contain(the_movement.activity.__name__)

@step(u'And the new loan request is associated to the Credit Analyst')
def and_the_new_loan_request_is_associated_to_the_credit_analyst(step):
    #... this association is done during loan creation, just checking
    world.a_person.input_area[world.account.number].analyst |should| be(world.credit_analyst)

#Scenario Credit Analyst analyses the individual customer loan request
@step(u'And there is a loan request of account (.+) with desired value (.+) to be analysed')
def and_there_is_a_loan_request_of_account_account_number_with_desired_value_desired_value_to_be_analysed(step, account_number, desired_value):
    #(a)the process is already in the right state, however, Lettuce cleans the objects, thus:
    world.credit_analyst.create_loan_request(world.account, int(desired_value))

@step(u'When I pick to analyse the loan request of account (.+)')
def when_i_pick_to_analyse_the_loan_request_of_account_account_number(step, account_number):
    #configure
    the_movement = world.an_individual_credit_operation.configure_activity(world.credit_analyst.decorated, world.credit_analyst.decorated, world.an_individual_credit_operation.analyst_select_request, CreditAnalystDecorator.analyse)
    #run
    the_movement.context = world.an_individual_credit_operation.run_activity(the_movement, world.credit_analyst, world.account.number)
    world.an_individual_credit_operation.current_state() |should| equal_to('request_analyzed')
    #checks
    #(a) if everything is ok the loan request was stored in the Node's output_area
    world.credit_analyst.decorated.output_area |should| contain(account_number)

@step(u'Then the loan request for account (.+) has the decision (.+)')
def then_the_loan_request_for_account_account_number_has_the_decision_decision(step, account_number, decision):
    #Lettuce sends u'False', thus using eval() to convert it into boolean
    world.credit_analyst.decorated.output_area[account_number].approved |should| equal_to(eval(decision))

#Scenario Approved loan request
@step(u'And there is an approved loan request of value (.+) for account (.+)')
def and_there_is_an_approved_loan_request_of_value_value_for_account_account_number(step, value, account_number):
    #prepare the context for this scenario
    #directly creating a loan request (same problem of (a) - maybe it is the case of developing an specific tool)
    world.credit_analyst.create_loan_request(world.account, value)
    #forces the loan request approval and its transfer to the output_area
    world.credit_analyst.decorated.input_area[world.account.number].approved = True
    world.credit_analyst.decorated.transfer(world.account.number, 'input', 'output')
    world.credit_analyst.decorated.output_area |should| contain(world.account.number)

@step(u'When I pick and perfom this loan')
def when_i_pick_and_perfom_this_loan(step):
    #pick
    loan_request = world.credit_analyst.decorated.output_area[world.account.number]
    #configure
    the_movement = world.an_individual_credit_operation.configure_activity(world.credit_analyst.decorated, world.credit_analyst.decorated, world.an_individual_credit_operation.loan_accepted, CreditAnalystDecorator.create_loan)
    #run
    the_movement.context = world.an_individual_credit_operation.run_activity(the_movement, world.credit_analyst, loan_request)
    #checks
    world.an_individual_credit_operation.current_state() |should| equal_to('loan_created')
    #datetime is used to generate the key, thus I cannot access the newly created loan through its key
    #the only way to check is: output_area must have at least the loan_request and the newly created loan
    world.credit_analyst.decorated.output_area.values() |should| have(2).itens

@step(u'Then a loan of value (.+) for account (.+) is generated')
def then_a_loan_of_value_value_for_account_account_number_is_generated(step, value, account_number):
    #not solved yet:
    #transportations needs a different treatment - and should be implemented by the decorator
    #

    #moves the loan to the processing area of the account
    world.move_loan_to_account = Transportation('Moves new loan to the account')
    world.move_loan_to_account.set_source(world.credit_analyst.decorated)
    world.move_loan_to_account.set_destination(world.account.decorated)
    #picks the loan by its type - no way to know its key here
    for item in world.credit_analyst.decorated.output_area.values():
        if item.__class__.__name__ == 'Loan':
            break
    world.move_loan_to_account.perform(item.datetime)
    world.account.decorated.input_area |should| contain(item.datetime)

@step(u'And the loan_request is moved to the account (.+) historic')
def and_the_loan_request_is_moved_to_the_account_account_number_historic(step, account_number):
    #not solved yet:
    #transportations needs a different treatment - and should be implemented by the decorator
    #

    #creates the movement
    world.move_loan_request_to_account = Transportation('Move loan request to account historic')
    world.move_loan_request_to_account.set_source(world.credit_analyst.decorated)
    world.move_loan_request_to_account.set_destination(world.account.decorated)
    #insert the movement into the business process
    world.an_individual_credit_operation.insert_movement(world.move_loan_request_to_account.name, world.move_loan_request_to_account)
    #perform! (world.account.number is the loan request key)
    world.an_individual_credit_operation.movements[world.move_loan_request_to_account.name].perform(world.account.number)
    #moves from the input area to the log area
    world.account.decorated.transfer(world.account.number,'input','log')
    world.account.decorated.log_area |should| have(1).loan_request

#Scenario Refused loan request
@step(u'And there is a refused loan request of value (.+) for account (.+)')
def and_there_is_a_refused_loan_request_of_value_value_for_account_account_number(step, desired_value, account_number):
    #directly creating a loan request (I really need BLDD to avoid this...)
    world.credit_analyst.create_loan_request(world.account, int(desired_value))
    #forces the loan request approval and its transfer to the output_area
    world.credit_analyst.decorated.input_area[world.account.number].approved = False
    world.credit_analyst.decorated.transfer(world.account.number, 'input', 'output')
    world.credit_analyst.decorated.output_area |should| contain(world.account.number)

@step(u'When When I pick this loan request')
def when_when_i_pick_this_loan_request(step):
    #GUI code goes here
    pass

@step(u'Then the loan_request is moved to the account (.+) historic')
def then_the_loan_request_is_moved_to_the_account_account_number_historic(step, account_number):
    step.then(u'And the loan_request is moved to the account (.+) historic')


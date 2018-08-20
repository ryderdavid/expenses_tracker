"""
Ryder Cobean
CS 521
Final Project - Expenses Tracker

Test program to test code in expenses_tracker


Created on Sun Aug  5 10:17:09 2018

@author: Ryder Cobean
"""

import pandas as pd
from expenses_tracker import update_spender_records
from expenses_tracker import print_spender_data
from expenses_tracker import print_payback_instructions
from Spender import Spender
import os
from validation_logic import get_file, get_int, validate_data


def update_spender_records(expenses_df):
    """Each time this runs, it has been passed a new dataframe of expenses
    to add to the spenders' records. It iterates over the new spending
    records, looking for Spender names and expenses. When it finds a record
    with a new spender name, it instantiates them as a new member of the
    Spender class, and saves them into the dictionary of spenders by their
    name as a key, with the corresponding first found transaction as the
    initializing balance. For any records for existing spenders, it calls
    an increment method to add the found value for the transaction to the
    corresponding spender object's balance attribute. This is implemented
    via pandas, which handles the excel spreadsheet as an iterable
    dataframe."""
    for index, row in expenses_df.iterrows():

        name = row['Spender']
        amount = row['Amount']

        # check the keylist for spender name. If found name not already
        # in dictionary, instantiate new Spender member with starting
        # balance of their first transaction
        # also, track number of transactions found for recordkeeping
        if name not in spenders.keys():
            spenders.update({name: Spender(name, s_bal = amount)})
            Spender.increment_num_spenders()
            Spender.increment_num_transactions()

        # if the name in this row's spender column is already there, process
        # that line's data instead, and increment that Spender's balance
        # also, count number of transactions for recordkeeping
        elif name in spenders.keys():
            Spender.increment_spender_balance(spenders[name], amount)
            Spender.increment_num_transactions()

        # finally, add the amount found on this line to the total spending
        # for all spenders in the class-level attribute total_spending
        Spender.increment_total_spending(amount)

    # get average spending (total transactions / number of spenders)
    Spender.set_avg_spending()

    # in case run before, reset the names of who owes and who is owed
    # before re-populating based on the latest spending data
    Spender.clear_owed_spenders()
    Spender.clear_owing_spenders()

    # iterate through each Spender member, and set its deviation (distance
    # from the average). If positive deviation, they are owed that money;
    # if negative, they owe that money to others.
    for name in spenders.keys():
        spenders[name].set_spender_deviation()

        # if deviation positive, add to set of 'owed' names
        if spenders[name].get_spender_deviation() > 0:
            Spender.add_owed_spender(name)

        # if negative, add to set of 'owers' names
        elif spenders[name].get_spender_deviation() < 0:
            Spender.add_owing_spender(name)


def print_spender_data():
    """Reports out the current spending data."""
    print('\nSPENDER DATA\n==============')
    print('Total spending: ${:,.2f} across {} transactions'
          .format(Spender.get_total_spending(),
                  Spender.get_num_transactions()))
    print('Average spending across {} spenders: ${:,.2f}'
          .format(Spender.get_num_spenders(), Spender.get_avg_spending()),
          end = '\n')

    for name in spenders.keys():
        print('')
        print(spenders[name])

def print_payback_instructions():
    """The below prints out instructions for all Spender members who were
    added to the 'owers' set of names - those with negative deviations from
    the average spending. This function iterates through each Spender member
    whose name was added to the owers list, gets their deviation, and
    divides it by the number of Spender members whose names were added to
    the 'owed' set of names. Thus, each ower is to pay an equal amount of
    what they owe to each Spender member who is owed. The conditions in the
    function govern proper syntax depending on how many are in each list."""
    num_owed = len(Spender.get_owed_spenders())

    print('\nPAYBACK INSTRUCTIONS\n======================')

    if num_owed > 0:
        for ower_name in Spender.get_owing_spenders():
            print(ower_name, end = ': pay ')

            for index, owed_name in enumerate(Spender.get_owed_spenders()):
                pay_to_each = (abs(spenders[ower_name]
                                   .get_spender_deviation()) / num_owed)

                if num_owed == 1:
                    print(owed_name + ' ${:,.2f}'.format(pay_to_each))
                elif num_owed == 2:
                    if not index == num_owed - 1:
                        print(owed_name, end = ' ')
                    else:
                        print('and ' + owed_name + ' ${:,.2f} each'
                              .format(pay_to_each))
                elif num_owed > 2:
                    if not index == num_owed - 1:
                        print(owed_name, end = ', ')
                    else:
                        print('and ' + owed_name + ' ${:,.2f} each'
                              .format(pay_to_each))
    else:
        print('Nobody owes anyone anything! Even Steven!')

if __name__ == "__main__":
    spenders = {}

    # I cannot run assertions on code here without trouble - any function that
    # has a print statement cannot silence it, so it appears that an error
    # message that would be desired is instead printing in the test program.
    # because this would be confusing, I am commenting out these test assertions
    # but showing my attempt. I tried extensively at coming up with ways to test
    # all the validation schemes and while there was ample documentation,
    # much of this seems above me until I take the QA/testing course. As an
    # alternative to testing the program's ability to catch intentionally bad
    # input files, I will test that the attributes loaded into the class
    # members from a CORRECTLY formatted simple file do indeed work and produce
    # predicted values in the attributes.
    #
    # Further, I cannot in my test program import the functions from the
    # expenses_tracker.py driver program - this only seems to work when I have
    # them here in this test program. Recognize it would be better to import
    # than to copy that code over here, but want to actually test its
    # functionality.
    #
    # proves that program catches bad column data
    #
    # file = 'expenses_bad_columns.xlsx'
    # badcol_df = pd.read_excel(file)
    #
    # assert validate_data(badcol_df) is False, 'Erroneously allowing bad data'
    #
    # file = 'expenses_nofloat.xlsx'
    # badvalues_df = pd.read_excel(file)
    #
    # assert validate_data(badvalues_df) is ValueError, 'Erroneously allowing non-floats'


    file = 'test_record.xlsx'
    df = pd.read_excel(file)

    assert not validate_data(df) is False, 'Erroneously disallowing good data'

    try:
        update_spender_records(df)
    except NameError:
        raise AssertionError('Dataframe not found.')


    # total in spreadsheet is 100 + 10 + 100 + 10 + 80 = 300.0; test for that
    assert Spender.get_total_spending() == 300.0

    # test that class is reading names from file correctly
    assert spenders['Ladybug'].get_spender_name() == 'Ladybug'

    # test member balances:
    assert spenders['Ladybug'].get_spender_balance() == 20.0
    assert spenders['Parrot'].get_spender_balance() == 200.0
    assert spenders['Octopus'].get_spender_balance() == 80.0

    # test number of spenders
    assert Spender.get_num_spenders() == 3

    # test number of transactions
    assert Spender.get_num_transactions() == 5

    # test avg transactions; 300 total / 3 spenders should = 100.0
    assert Spender.get_avg_spending() == 100.0

    # test Ladybug's deviation - if Ladybug only spent $20, then it is $80.0
    # below average -- should return -80.0
    assert spenders['Ladybug'].get_spender_deviation() == -80.0

    # check population of owed spenders - the update_spender_records() method
    # generates a set of names of any spender that spent OVER the average -
    # meaning positive deviation attribute. Should only be Parrot with $200.00.
    assert Spender.get_owed_spenders() == {'Parrot'}

    # now check for owers - same but should contain underspenders, Ladybug and
    # Octopus
    assert Spender.get_owing_spenders() == {'Octopus', 'Ladybug'}

    print('All tests passed OK - attributes contain expected values.')

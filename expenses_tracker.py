#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ryder Cobean
CS 521
Final Project - Expenses Tracker

Driver program for Expenses Tracker for roommates, couples, or teams.

Program Depends on two files: validation_logic.py, and Spender.py, which should
be in same directory as expenses_tracker.py. Also, the program will ask the 
user to provide the filename for an Excel (.xlsx) spreadsheet located in the 
working directory of the program. At a minimum, the spreadsheet needs to have
column headers labeled "Amount" and "Spender", with each record containing the
name of the Spender in the Spender column (Spelling and case-sensitive), and
a dollar and cents (##.##) value in the Amount column. Any number of users may 
input their own data, so a household does not need to keep one centralized 
spreadsheet - this will crunch everyone's numbers and cacluate who owes what.

NOTE: depends on third part module pandas, more info at 
https://pandas.pydata.org/. To install:
    
    Cross platform: Easiest way to install is by installing is to install it as
    part of the Anaconda data analysis python distribution, Available at 
    https://www.anaconda.com/download
    
    Platform specific, plain Python methods:
    
    Windows:
        Run "py -m pip install pandas" from command line
    macOS: 
        First install Python 3.4+, then,
        from Terminal, "pip install pandas"
    Ubuntu 18.04:
        From Terminal,
        "sudo apt-get install python3-pip"
        "pip3 install pandas"
        

Created on Sun Aug  5 10:17:09 2018

@author: Ryder Cobean
"""

import pandas as pd
from validation_logic import get_file, get_int, validate_data
from Spender import Spender

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

    def menu():
        while True:
            print('\n1: Add expenses from file')
            print('2: Show spender information')
            print('3: Get payback instructions')
            print('4: Exit')
            menu_choice = get_int('Enter a choice: ')

            if menu_choice == 1:
                # validate file existence and extension before moving on
                file = get_file('xlsx')
                expenses_df = pd.read_excel(file)
                # validate proper formatting of xlsx file before moving on
                if validate_data(expenses_df) is False:
                    pass
                else:  # if good, process the data into the program
                    update_spender_records(expenses_df)
                    print('\nUpdated records with {} added transactions.'
                          .format(expenses_df.shape[0]))
                continue
            elif menu_choice == 2:
                print_spender_data()
                continue
            elif menu_choice == 3:
                print_payback_instructions()
                continue
            elif menu_choice == 4:
                break
            elif menu_choice == 0:
                for name in spenders.keys():
                    print(repr(spenders[name]))
            else:
                print('Please choose an option from 1 to 4.')


    menu()
    print('\nProgram exiting. Goodbye.')

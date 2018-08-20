# expenses_tracker
Python Expenses Tracker for Roommates
       Final Project – Expenses Tracker that Reads Microsoft Excel Spreadsheets

## Preparation
This program depends on pandas, a data analysis package available for Python. More information on pandas is available at https://pandas.pydata.org/. It also requires xlrd, to handle Excel files. To install:

- Cross platform: Easiest way to install is by installing is to install it as part of the Anaconda data analysis python distribution, 
    Available at https://www.anaconda.com/download.
- Platform specific, plain Python methods:
  + Windows: Run "py -m pip install pandas" “ py -m pip install xlrd from command line”
  + macOS: First install Python 3.4+, then, from Terminal, "pip3 install pandas" “pip3 install xlrd”
  + Ubuntu 18.04: From Terminal, "sudo apt-get install python3-pip"; "pip3 install pandas" “pip3 install xlrd”

## Function
In short, the program takes in records of spending on behalf of a group undertaken by members of it, gets the total amount each individual spent, gets the total the whole group spent, and determines based on how many members what the average spending was. From there, it identifies who owes money by how much below the average they are, and who is owed money, based on how much their spending balance exceeds the average. The program then prints this information and can also provide instructions to the members in debt on how much to pay to each member who is owed money.

The program takes as input spreadsheets with, at a minimum, a header with at least two columns labeled “Spender” and “Amount”, with “Spender” being a transaction’s spender (spelling and capitalization matters, and each Spender must have a unique name), and dollar amounts (cents are also OK) listed under each “Amount.” 

When the user opens the program, the following menu is displayed:

1: Add expenses from file 
2: Show spender information 
3: Get payback instructions 
4: Exit 
Enter a choice:

The user’s first step is to invoke the file loader by choosing option 1. They will then be prompted to provide the filename of an .xlsx file containing expenses data. The file must be located in the working directory of the program, and must end with ‘.xlsx’. The program will run validation on the file’s location (existence), its extension, and its column and data formatting. 

The user’s first step is to invoke the file loader by choosing option 1. They will then be prompted to provide the filename of an .xlsx file containing expenses data. The file must be located in the working directory of the program, and must end with ‘.xlsx’. The program will run validation on the file’s location (existence), its extension, and its column and data formatting. 

Once through, it iterates over its contents, and does the following things:
- When it sees a new spender, it creates a new Spender object tied to that spender’s name in a dictionary data structure, like {‘Parrot’: Spender(), ‘Octopus’: Spender(), ….}, and initializes the spender’s starting balance as the first transaction seen. It also adds that transaction to a class-level attribute, Spender.total_spending.
- For every recurring instance of an already added spender, it increments that spender’s balance and the total amount spent by all by the amount found.
- Once all data is in, it updates a class level attribute that tracks the average amount spent by each spender, and calculates how much below the average each spender is (how much that person owes) or how much above it they are (how much they are owed). Selecting Option 2 from the menu will print this information off to the user:

The user can keep inputting spreadsheets (to mimic the idea that perhaps each roommate is keeping their own tracker), and the program will keep crunching the averages and update the debts and instructions each time an excel file is fed into it.

## Dependencies:
- xlrd, for XLSX file import: https://pypi.org/project/xlrd/
- pandas, for processing data from XLSX files. https://pandas.pydata.org/

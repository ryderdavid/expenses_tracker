"""
Ryder Cobean
CS 521
Final Project - Expenses Tracker

Spender Class
"""


class Spender:
    """A member of the household who spends money on communal items, and is
    either owed or owes money to other compared to what would have been an even
    split."""

    num_transactions = 0
    total_spending = 0.0
    avg_spending = 0.0
    num_spenders = 0

    __owed_spenders = set()
    __owing_spenders = set()

    # class level accessors
    @classmethod
    def get_avg_spending(self):
        return self.avg_spending

    @classmethod
    def get_owed_spenders(self):
        return self.__owed_spenders

    @classmethod
    def get_owing_spenders(self):
        return self.__owing_spenders

    @classmethod
    def get_num_spenders(self):
        return self.num_spenders

    @classmethod
    def get_num_transactions(self):
        return self.num_transactions

    @classmethod
    def get_total_spending(self):
        return self.total_spending

    # class level mutators
    @classmethod
    def set_avg_spending(self):
        self.avg_spending = self.total_spending / self.num_spenders

    @classmethod
    def set_num_transactions(self, amt):
        self.num_transactions = amt

    @classmethod
    def increment_num_spenders(self):
        self.num_spenders += 1

    @classmethod
    def increment_num_transactions(self):
        self.num_transactions += 1

    @classmethod
    def increment_total_spending(self, amt):
        self.total_spending += amt

    @classmethod
    def add_owed_spender(self, name):
        self.__owed_spenders.add(name)

    @classmethod
    def add_owing_spender(self, name):
        self.__owing_spenders.add(name)

    @classmethod
    def clear_owed_spenders(self):
        self.__owed_spenders.clear()

    @classmethod
    def clear_owing_spenders(self):
        self.__owing_spenders.clear()

    def __init__(self, s_name, s_bal = 0.0, s_dev = 0.0):
        self.__name = s_name
        self.__balance = s_bal
        self.__deviation = s_dev

    def __str__(self):
        balinfo = str('Spender: ' + self.__name + '\n'
                      'Transaction balance: ${:,.2f}'.format(self.__balance))
        if self.__deviation < 0:
            return str(balinfo + '\n'+ self.__name + ' owes: ${:,.2f}'
                       .format(abs(self.__deviation)))
        elif self.__deviation > 0:
            return str(balinfo + '\n'+ self.__name + ' is owed: ${:,.2f}'
                       .format(abs(self.__deviation)))
        else:
            return balinfo

    def __repr__(self):
        return str({"self.__balance": self.__balance,
                    "self.__name": self.__name,
                    "self.total_spending": self.total_spending,
                    "self.num_spenders": self.num_spenders,
                    "self.num_transactions": self.num_transactions,
                    "self.avg_spending": self.avg_spending,
                    "self.__deviation": self.__deviation,
                    "self.__owed_spenders": repr(self.__owed_spenders),
                    "self.__owing_spenders": repr(self.__owing_spenders)})

    def increment_spender_balance(self, amt):
        self.__balance += amt

    def get_spender_name(self):
        return self.__name

    def get_spender_balance(self):
        return self.__balance

    def get_spender_deviation(self):
        return self.__deviation

    def set_spender_balance(self, amt):
        self.__balance = amt

    def set_spender_deviation(self):
        """This compares the spender's balance of spending (self.__balance)
        with the average spending for all spenders (a class method stored in
        each instantiation as self.avg_spending). A negative deviation means
        the spender spent less than the average and owes the other spenders;
        a positive deviation means that the spender spent more than the average
        and is due some money back."""
        self.__deviation = self.__balance - self.avg_spending

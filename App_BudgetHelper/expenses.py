from App_BudgetHelper.AbstractData import *


class ExpenseKeys(AbstractKeys):
    NAME = AbstractObjCommonKeys.NAME
    VALUE = 'Value'
    FREQUENCY = 'Frequency'
    ACCOUNT = 'Account'

    all_keys = [
        NAME,
        VALUE,
        FREQUENCY,
        ACCOUNT
    ]

    required_keys = [
        NAME,
        VALUE,
        FREQUENCY,
    ]


class ExpenseIndices(AbstractIndices):
    NAME = 0
    VALUE = 1
    FREQUENCY = 2
    # ACCOUNT = 3

    all_indices = [
        NAME,
        VALUE,
        FREQUENCY,
        # ACCOUNT,
    ]


class ExpenseFrequencies:
    WEEKLY = 'Weekly'
    BI_WEEKLY = 'Bi-Weekly'
    MONTHLY = 'Monthly'
    YEARLY = 'Yearly'

    all_frequencies = [
        MONTHLY,
        BI_WEEKLY,
        YEARLY,
        WEEKLY,
    ]


class Expense(AbstractDictBasedDataObject):
    object_name = "Expense"
    keys = ExpenseKeys
    idxs = ExpenseIndices

    frequencies = ExpenseFrequencies

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def default_values(self):
        self[self.keys.ACCOUNT] = self.get(self.keys.ACCOUNT, None)

    def get_yearly_value(self):
        frequency = self[self.keys.FREQUENCY]
        value = float(self[self.keys.VALUE])
        if frequency == self.frequencies.YEARLY:
            return value
        elif frequency == self.frequencies.MONTHLY:
            return value * 12
        elif frequency == self.frequencies.BI_WEEKLY:
            return value * 26
        elif frequency == self.frequencies.WEEKLY:
            return value * 52


test_expense_dict = {
    Expense.keys.NAME: "Test Expense",
    Expense.keys.VALUE: 500,
    Expense.keys.FREQUENCY: Expense.frequencies.MONTHLY,
}
test_expense = Expense(**test_expense_dict)
test_expense_list = []
for x in range(5):
    index = x+1
    test_expense_dict = {
        Expense.keys.NAME: "Test Expense {}".format(str(index)),
        Expense.keys.VALUE: index * 5,
        Expense.keys.FREQUENCY: Expense.frequencies.MONTHLY,
    }
    test_expense_list.append(Expense(**test_expense_dict))


if __name__ == '__main__':
    print(test_expense)

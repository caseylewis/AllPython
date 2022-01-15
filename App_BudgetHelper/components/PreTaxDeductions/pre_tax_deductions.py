from App_BudgetHelper.AbstractData import *


class PreTaxDeductionKeys(AbstractKeys):
    NAME = AbstractObjCommonKeys.NAME
    VALUE = 'Value'
    PRIORITY = 'Priority'
    TYPE = 'Type'

    all_keys = [
        NAME,
        VALUE,
        PRIORITY,
        TYPE,
    ]

    required_keys = [
        NAME,
        VALUE,
        PRIORITY,
        TYPE,
    ]


class PreTaxDeductionIndices(AbstractIndices):
    NAME = 0
    VALUE = 1
    PRIORITY = 2
    TYPE = 3

    all_indices = [
        NAME,
        VALUE,
        PRIORITY,
        TYPE,
    ]


class PreTaxDeductionTypes:
    PERCENTAGE = '%'
    FIXED = 'Fixed'

    all = [
        PERCENTAGE,
        FIXED,
    ]


class PreTaxDeduction(AbstractDictBasedDataObject):
    object_name = "Pre Tax Deduction"
    keys = PreTaxDeductionKeys
    idxs = PreTaxDeductionIndices

    types = PreTaxDeductionTypes

    # NAME
    @property
    def name(self):
        return self[self.keys.NAME]

    @name.setter
    def name(self, val):
        self[self.keys.NAME] = val

    # VALUE
    @property
    def value(self):
        return self[self.keys.VALUE]

    @value.setter
    def value(self, val):
        self[self.keys.VALUE] = val

    # TYPE
    @property
    def type(self):
        return self[self.keys.TYPE]

    @type.setter
    def type(self, val):
        self[self.keys.TYPE] = val

    # PRIORITY
    @property
    def priority(self):
        return self[self.keys.PRIORITY]

    @priority.setter
    def priority(self, val):
        self[self.keys.PRIORITY] = val

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def default_values(self):
        self[self.keys.PRIORITY] = self.get(self.keys.PRIORITY, None)


test_pre_tax_deduction_dict = {
    PreTaxDeduction.keys.NAME: "401k",
    PreTaxDeduction.keys.VALUE: 6,
    PreTaxDeduction.keys.TYPE: PreTaxDeductionTypes.PERCENTAGE,
    PreTaxDeduction.keys.PRIORITY: 1,
}
test_pre_tax_deduction = PreTaxDeduction(**test_pre_tax_deduction_dict)
test_pre_tax_deduction_list = []
for x in range(5):
    index = x+1
    test_expense_dict = {
        PreTaxDeduction.keys.NAME: "Test Deduction {}".format(str(index)),
        PreTaxDeduction.keys.VALUE: index * 50,
        PreTaxDeduction.keys.TYPE: PreTaxDeductionTypes.FIXED,
        PreTaxDeduction.keys.PRIORITY: 1,
    }
    test_pre_tax_deduction_list.append(PreTaxDeduction(**test_expense_dict))


if __name__ == '__main__':
    print(test_pre_tax_deduction)

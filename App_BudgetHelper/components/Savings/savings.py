from App_BudgetHelper.AbstractData import *


class SavingKeys(AbstractKeys):
    NAME = AbstractObjCommonKeys.NAME
    VALUE = 'Value'
    TYPE = 'Type'

    all_keys = [
        NAME,
        VALUE,
        TYPE,
    ]

    required_keys = [
        NAME,
        VALUE,
        TYPE,
    ]


class SavingIndices(AbstractIndices):
    NAME = 0
    VALUE = 1
    TYPE = 2

    all_indices = [
        NAME,
        VALUE,
        TYPE,
    ]


class SavingTypes:
    PERCENTAGE = '%'
    FIXED = 'Fixed'

    all = [
        PERCENTAGE,
        FIXED,
    ]


class Saving(AbstractDictBasedDataObject):
    object_name = "Saving"
    keys = SavingKeys
    idxs = SavingIndices

    types = SavingTypes

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def default_values(self):
        pass
        # self[self.keys.PRIORITY] = self.get(self.keys.PRIORITY, None)


test_saving_dict = {
    Saving.keys.NAME: "Standard Saving",
    Saving.keys.VALUE: 10,
    Saving.keys.TYPE: SavingTypes.PERCENTAGE,
}
test_saving = Saving(**test_saving_dict)
test_saving_list = []
for x in range(5):
    index = x+1
    test_expense_dict = {
        Saving.keys.NAME: "Test Saving {}".format(str(index)),
        Saving.keys.VALUE: index * 50,
        Saving.keys.TYPE: SavingTypes.FIXED,
    }
    test_saving_list.append(Saving(**test_expense_dict))


if __name__ == '__main__':
    print(test_saving)

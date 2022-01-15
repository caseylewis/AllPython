from App_BudgetHelper.components.PreTaxDeductions.pre_tax_deductions import *
from Libs.GuiLib.gui_abstracts import *


class PreTaxDeductionCard(AbstractCard):
    class cols:
        NAME = 0
        VALUE = 1
        PRIORITY = 2
        BTNS = 3
    _c = cols

    def __init__(self, root, pre_tax_deduction: PreTaxDeduction,
                 on_delete_by_name_func=None,
                 on_edit_by_name_func=None):
        super().__init__(root, pre_tax_deduction)
        self.grid_columnconfigure(self._c.NAME, weight=1)
        self.grid_columnconfigure(self._c.VALUE, weight=1)
        self.grid_columnconfigure(self._c.PRIORITY, weight=0)
        self.grid_columnconfigure(self._c.BTNS, weight=0)

        # CALLBACK FUNCTIONS
        self.on_delete_by_name_callback = on_delete_by_name_func
        self.on_edit_by_name_callback = on_edit_by_name_func

        pad = 10

        self._name_lbl = StandardLabel(self, pre_tax_deduction.name, width=10)
        self._name_lbl.grid(row=0, column=self._c.NAME, rowspan=2, sticky='nsew', pady=(pad, pad), padx=(pad, pad))

        self._value_lbl = StandardLabel(self, '', width=6)
        self._value_lbl.grid(row=0, column=self._c.VALUE, rowspan=2, sticky='nsew', pady=(pad, pad), padx=(0, 0))
        self.__set_value(pre_tax_deduction)

        self._priority_lbl = StandardLabel(self, pre_tax_deduction.priority, width=2)
        self._priority_lbl.grid(row=0, column=self._c.PRIORITY, rowspan=2, sticky='nsew', pady=(pad, pad), padx=(pad, 0))

        self._edit_btn = StandardButton(self, 'Edit', command=lambda: self.__handle_edit_btn())
        self._edit_btn.grid(row=0, column=self._c.BTNS, sticky='nsew', pady=(pad, 0), padx=(pad, pad))

        self._delete_btn = DeleteButton(self, command=lambda: self.__handle_delete_btn())
        self._delete_btn.grid(row=1, column=self._c.BTNS, sticky='nsew', pady=(pad, pad), padx=(pad, pad))


    def __handle_edit_btn(self):
        if self.on_edit_by_name_callback is not None:
            self.on_edit_by_name_callback(self.key())

    def __handle_delete_btn(self):
        if self.on_delete_by_name_callback is not None:
            self.on_delete_by_name_callback(self.key())

    def __set_value(self, object):
        if object.type == PreTaxDeductionTypes.FIXED:
            self._value_lbl.set("${}".format(object.value))
        elif object.type == PreTaxDeductionTypes.PERCENTAGE:
            self._value_lbl.set("{}%".format(object.value))

    def update_from_object(self, object):
        self.__set_value(object)
        # self._value_lbl['text'] = object.value
        # self._type_lbl['text'] = object.type
        self._priority_lbl['text'] = object.priority


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def output_name(name):
        print(name)

    pre_tax_deduction = test_pre_tax_deduction
    test_card = PreTaxDeductionCard(root, pre_tax_deduction,
                                    on_delete_by_name_func=output_name,
                                    on_edit_by_name_func=output_name)
    test_card.grid(row=0, column=0, sticky='nsew')

    root.mainloop()

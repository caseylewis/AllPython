from App_BudgetHelper.components.PreTaxDeductions.pre_tax_deductions import *
from Libs.GuiLib.gui_abstracts import *


class PreTaxDeductionForm(AbstractEditFrame):
    def __init__(self, root, on_add_func=None, on_update_func=None):
        super().__init__(root, PreTaxDeduction, on_add_func, on_update_func)

    def set_entries(self):
        for key, idx in zip(self.object_type.keys.required_keys, self.object_type.idxs.all_indices):
            if key == PreTaxDeduction.keys.TYPE:
                entry = StandardDropdown(self._input_frame, PreTaxDeduction.types.all)
            else:
                entry = StandardEntry(self._input_frame)
            entry.grid(row=idx, column=1, sticky=grid_style.sticky.all, pady=grid_style.pad.pady_std, padx=0)
            self._entry_dict[key] = entry


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def on_add(obj):
        print('printing', obj.name)
        test_form.change_to_add_mode()

    def on_update(obj):
        print(obj.name)
        test_form.change_to_add_mode()

    test_form = PreTaxDeductionForm(root, on_add_func=on_add, on_update_func=on_update)
    test_form.change_to_update_mode(test_pre_tax_deduction)
    test_form.grid(row=0, column=0, sticky='nsew')

    root.mainloop()

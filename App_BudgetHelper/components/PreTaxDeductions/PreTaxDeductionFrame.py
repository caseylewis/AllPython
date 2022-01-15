from App_BudgetHelper.components.PreTaxDeductions.PreTaxDeductionForm import *
from App_BudgetHelper.components.PreTaxDeductions.PreTaxDeductionCard import *
from Libs.GuiLib.gui_abstracts import *


class PreTaxDeductionFrame(AbstractObjectFrame):
    def __init__(self, root, on_add_func, on_update_func, on_delete_by_name_func, on_edit_by_name_func):
        super().__init__(root, "Pre Tax Deductions", PreTaxDeductionForm, PreTaxDeductionCard,
                         on_add_func=on_add_func,
                         on_update_func=on_update_func,
                         on_delete_by_name_func=on_delete_by_name_func,
                         on_edit_by_name_func=on_edit_by_name_func)


if __name__ == '__main__':
    root = Tk()
    root.config(bg=FRAME_BG_STANDARD)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def get_object_from_list_by_name(obj_name, obj_list):
        for obj in obj_list:
            if obj.name == obj_name:
                return obj

    # TEST FOR OBJECT FRAME
    def add_object(obj):
        test_object_list.append(obj)
        frame.add_object(obj)
        frame.object_edit_frame.clear_entries()

    def update_obj(new_obj):
        old_obj = get_object_from_list_by_name(new_obj.name, test_object_list)
        old_obj.copy_from(new_obj)
        frame.update_object(new_obj)

    def delete_obj_by_name(obj_name):
        frame.delete_object_by_name(obj_name)

    def edit_obj_by_name(obj_name):
        obj = get_object_from_list_by_name(obj_name, test_object_list)
        frame.edit_object(obj)

    # SPECIFIC TO THIS FRAME
    def arrow_by_name(direction, obj_name):
        print(direction, obj_name)

    test_object_list = [test_pre_tax_deduction]
    frame = PreTaxDeductionFrame(root,
                         on_add_func=add_object,
                         on_update_func=update_obj,
                         on_delete_by_name_func=delete_obj_by_name,
                         on_edit_by_name_func=edit_obj_by_name)
    frame.populate_objects(test_object_list)

    # GRID WHICHEVER FRAME
    frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()

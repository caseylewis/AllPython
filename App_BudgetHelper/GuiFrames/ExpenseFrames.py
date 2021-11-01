from Libs.GuiLib.gui_helpers import *
from App_BudgetHelper.AbstractFrames import *
from App_BudgetHelper.expenses import *


class ExpenseEditFrame(AbstractEditFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, Expense, *args, **kwargs)

    def set_entries(self):
        for key, idx in zip(self.object_type.keys.all_keys, self.object_type.idxs.all_indices):
            if key == Expense.keys.FREQUENCY:
                entry = DropdownPlus(self._input_frame, Expense.frequencies.all_frequencies, **style_dropdown)
            else:
                entry = EntryPlus(self._input_frame, **style_entry)
            entry.grid(row=idx, column=1, **grid_entry)
            self._entry_dict[key] = entry


class ExpenseViewFrame(AbstractViewFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, Expense, *args, **kwargs)


class ExpenseFrame(ContentFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, "Expenses", *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        class ExpenseFrameRowIndices:
            EDIT_FRAME = 0
            VIEW_FRAME = 1
            # LOGGER = 2
        self._expense_frame_idxs = ExpenseFrameRowIndices
        self.view_port.grid_columnconfigure(0, weight=1)
        self.view_port.grid_columnconfigure(1, weight=0)
        self.view_port.grid_columnconfigure(2, weight=1)
        self.view_port.grid_rowconfigure(self._expense_frame_idxs.EDIT_FRAME, weight=0)
        self.view_port.grid_rowconfigure(self._expense_frame_idxs.VIEW_FRAME, weight=1)
        # self.view_port.grid_rowconfigure(self._expense_frame_idxs.LOGGER, weight=0)

        # ACCOUNT EDIT FRAME
        self.expense_edit_frame = ExpenseEditFrame(self.view_port, **style_frame_primary)
        self.expense_edit_frame.grid(row=self._expense_frame_idxs.EDIT_FRAME, column=1, **grid_frame_primary)

        # ACCOUNT VIEW FRAME
        self.expense_view_frame = ExpenseViewFrame(self.view_port, on_edit_func=self.__edit_expense, **style_frame_primary)
        self.expense_view_frame.grid(row=self._expense_frame_idxs.VIEW_FRAME, column=0, columnspan=3, **grid_frame_primary)

        # # LOGGER
        # self._logger = LoggerPlus(self.view_port, **style_logger)
        # self._logger.grid(row=self._expense_frame_idxs.LOGGER, column=0, columnspan=3, **grid_logger)

    def handle_close(self):
        # self._accounts_json_manager.export_data(self._accounts_list)
        return

    def __edit_expense(self, expense):
        self.expense_edit_frame.change_to_update_mode(expense)


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    frame = ExpenseEditFrame(root)

    frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()

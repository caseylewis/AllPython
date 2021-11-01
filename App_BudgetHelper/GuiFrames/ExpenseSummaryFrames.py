from Libs.GuiLib.gui_helpers import *
from App_BudgetHelper.expenses import *


class ExpenseSummaryFrame(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        # TITLE
        self._title = Label(self, text="Account Expense Map", **style_lbl_title)
        self._title.grid(row=0, column=0, **grid_frame_primary)

        # ACTION FRAME
        self._action_frame = Frame(self, **style_frame_primary)
        self._action_frame.grid(row=1, column=0, **grid_frame_primary)
        self._action_frame.grid_columnconfigure(0, weight=1)
        self._action_frame.grid_columnconfigure(1, weight=1)

        # TOTAL EXPENSES
        self._total_expenses_lbl = Label(self._action_frame, text="Total Expenses", **style_lbl)
        self._total_expenses_lbl.grid(row=0, column=0, **grid_lbl)

        self._total_expenses_display = Label(self._action_frame, **style_lbl)
        self._total_expenses_display.grid(row=0, column=1, **grid_lbl)

        # TOTAL YEARLY
        self._total_yearly_lbl = Label(self._action_frame, text="Total Yearly", **style_lbl)
        self._total_yearly_lbl.grid(row=1, column=0, **grid_lbl)

        self._total_yearly_display = Label(self._action_frame, **style_lbl)
        self._total_yearly_display.grid(row=1, column=1, **grid_lbl)

        # TOTAL MONTHLY
        self._total_monthly_lbl = Label(self._action_frame, text="Total Monthly", **style_lbl)
        self._total_monthly_lbl.grid(row=2, column=0, **grid_lbl)

        self._total_monthly_display = Label(self._action_frame, **style_lbl)
        self._total_monthly_display.grid(row=2, column=1, **grid_lbl)

        # TOTAL SEMI MONTHLY
        self._total_semi_monthly_lbl = Label(self._action_frame, text="Total Semi-Monthly", **style_lbl)
        self._total_semi_monthly_lbl.grid(row=3, column=0, **grid_lbl)

        self._total_semi_monthly_display = Label(self._action_frame, **style_lbl)
        self._total_semi_monthly_display.grid(row=3, column=1, **grid_lbl)

    def update_expense_summary(self, expenses_list):
        print("UPDATE EXPENSE SUMMARY")
        # TOTAL EXPENSES
        expense_count = len(expenses_list)
        self._total_expenses_display['text'] = "{}".format(expense_count)

        # YEARLY
        total_yearly = 0
        for expense in expenses_list:
            expense_yearly = expense.get_yearly_value()
            total_yearly += expense_yearly
        self._total_yearly_display['text'] = "{:.2f}".format(total_yearly)

        # MONTHLY
        total_monthly = total_yearly / 12
        self._total_monthly_display['text'] = "{:.2f}".format(total_monthly)

        # SEMI MONTHLY
        total_semi_monthly = total_monthly / 2
        self._total_semi_monthly_display['text'] = "{:.2f}".format(total_semi_monthly)


class ExpenseSummary(ContentFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, "Expense Summary", *args, **kwargs)
        self.view_port.grid_columnconfigure(0, weight=1)
        self.view_port.grid_columnconfigure(1, weight=1)
        self.view_port.grid_columnconfigure(2, weight=1)
        self.view_port.grid_rowconfigure(0, weight=0)
        self.view_port.grid_rowconfigure(1, weight=1)

        self.expense_summary_frame = ExpenseSummaryFrame(self.view_port, **style_frame_primary)
        self.expense_summary_frame.grid(row=0, column=1, columnspan=1, **grid_frame_primary)

    def handle_close(self):
        return

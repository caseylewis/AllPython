from Libs.GuiLib.gui_helpers import *
from App_BudgetHelper.accounts import *
from App_BudgetHelper.expenses import *


class AccountExpenseMapFrame(Frame):
    default_account_option = "Select Account"

    class AvailableExpenseKeys:
        FRAME = 'frame'
        NAME_LBL = 'name_lbl'
        ASSIGN_BTN = 'assign_btn'
        all_keys = [
            FRAME,
            NAME_LBL,
            ASSIGN_BTN
        ]
    _available_expense_keys = AvailableExpenseKeys

    class AccountExpenseKeys:
        FRAME = 'frame'
        NAME_LBL = 'name_lbl'
        UNASSIGN_BTN = 'unassign_btn'
        all_keys = [
            FRAME,
            NAME_LBL,
            UNASSIGN_BTN
        ]
    _account_expense_keys = AccountExpenseKeys

    style_btn_delete = copy_dict(style_btn)
    style_btn_delete['width'] = 3

    def __init__(self, root, on_assign_func=None, on_unassign_func=None, on_account_changed_func=None, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        self.on_assign_callback = on_assign_func
        self.on_unassign_callback = on_unassign_func
        self.on_account_changed_callback = on_account_changed_func

        # TITLE
        self._title = Label(self, text="Account Expense Map", **style_lbl_title)
        self._title.grid(row=0, column=0, **grid_frame_primary)

        # ACTION FRAME
        self._action_frame = Frame(self, **style_frame_primary)
        self._action_frame.grid(row=1, column=0, **grid_frame_primary)
        self._action_frame.grid_columnconfigure(0, weight=1)
        self._action_frame.grid_columnconfigure(1, weight=1)

        # ACCOUNT DROPDOWN
        self._account_dropdown = DropdownPlus(self._action_frame, **style_dropdown)
        self._account_dropdown.on_change_func = self.__handle_account_dropdown_changed
        self._account_dropdown.grid(row=0, column=0, **grid_dropdown)

        # ACCOUNT EXPENSE SCROLLFRAME
        self._account_expense_scrollframe = ScrollFrame(self._action_frame, hide_scroll_bar=True, width=600, **style_frame_primary)
        self._account_expense_scrollframe.grid(row=1, column=0, **grid_frame_primary)
        self._account_expense_scrollframe.view_port.grid_columnconfigure(0, weight=1)
        self._account_expense_row_list = []
        self._next_account_expense_index = 0

        # AVAILABLE EXPENSE LABEL
        self._available_expense_lbl = Label(self._action_frame, text="Available Expenses", **style_lbl)
        self._available_expense_lbl.grid(row=0, column=1, **grid_lbl)

        # AVAILABLE EXPENSE SCROLLFRAME
        self._available_expense_scrollframe = ScrollFrame(self._action_frame, hide_scroll_bar=True, width=600, **style_frame_primary)
        self._available_expense_scrollframe.grid(row=1, column=1, **grid_frame_primary)
        self._available_expense_scrollframe.view_port.grid_columnconfigure(0, weight=1)
        self._available_expense_row_list = []
        self._next_available_expense_index = 0

    def __handle_account_dropdown_changed(self):
        if self.on_account_changed_callback is not None:
            self.on_account_changed_callback()

    def __handle_assign_btn(self, expense_name):
        active_account = self._account_dropdown.get()
        if active_account != self.default_account_option:
            if self.on_assign_callback is not None:
                self.on_assign_callback(expense_name, active_account)

    def __handle_unassign_btn(self, expense_name):
        if self._account_dropdown.get() != self.default_account_option:
            if self.on_unassign_callback is not None:
                self.on_unassign_callback(expense_name)

    def get_available_expense_name_from_index(self, index):
        return self._available_expense_row_list[index]['name_lbl']['text']

    def __get_account_expense_name_from_index(self, index):
        return self._account_expense_row_list[index]['name_lbl']['text']

    def set_active_account_to_none(self):
        self._account_dropdown.set(self.default_account_option)

    def get_active_account_name(self):
        return self._account_dropdown.get()

    def delete_account_option(self, account):
        self._account_dropdown.remove_option(account[Account.keys.NAME])

    def populate_accounts(self, accounts_list):
        options_list = [self.default_account_option]
        for account in accounts_list:
            options_list.append(account[Account.keys.NAME])
        self._account_dropdown.set_options(options_list)

    def add_account(self, account):
        self._account_dropdown.add_option(account[Account.keys.NAME])

    def populate_expenses(self, expenses_list):
        for expense in expenses_list:
            if expense[Expense.keys.ACCOUNT] is None:
                self.append_to_available_expense_list(expense)

    def __get_index_of_account_expense(self, expense_name):
        for index, row_dict in enumerate(self._account_expense_row_list):
            if expense_name == row_dict[self._account_expense_keys.NAME_LBL]['text']:
                return index

    def unassign_expense_from_account(self, expense):
        # GET THE INDEX TO DELETE BY
        delete_index = self.__get_index_of_account_expense(expense)

        account_expense_delete_row = self._account_expense_row_list[delete_index]
        # DESTROY EVERY CHILD WIDGET
        account_expense_delete_row[self._account_expense_keys.NAME_LBL].grid_remove()
        account_expense_delete_row[self._account_expense_keys.NAME_LBL].destroy()
        account_expense_delete_row[self._account_expense_keys.UNASSIGN_BTN].grid_remove()
        account_expense_delete_row[self._account_expense_keys.UNASSIGN_BTN].destroy()

        # DESTROY FRAME
        account_expense_frame = account_expense_delete_row[self._available_expense_keys.FRAME]
        account_expense_frame.grid_remove()
        account_expense_frame.destroy()
        self._account_expense_row_list.pop(delete_index)
        self._next_account_expense_index -= 1

    def __get_index_of_available_expense(self, expense_name):
        for idx, row_dict in enumerate(self._available_expense_row_list):
            if row_dict[self._available_expense_keys.NAME_LBL]['text'] == expense_name:
                return idx

    def remove_expense_from_account_by_name(self, expense_name):
        delete_index = self.__get_index_of_account_expense(expense_name)
        self.account_expense_list_remove_expense_from_account_by_index(delete_index)

    def remove_expense_from_available_by_name(self, expense_name):
        delete_index = self.__get_index_of_available_expense(expense_name)
        self.available_expense_list_remove_expense_by_index(delete_index)

    # AVAILABLE EXPENSE LIST
    def available_expense_list_remove_expense_by_index(self, delete_index):
        available_expense_delete_row = self._available_expense_row_list[delete_index]
        available_expense_frame = available_expense_delete_row[self._available_expense_keys.FRAME]
        # DESTROY EVERY CHILD WIDGET OF FRAME
        for child in available_expense_frame.grid_slaves():
            child.grid_remove()
            child.destroy()

        # DESTROY FRAME
        available_expense_frame.grid_remove()
        available_expense_frame.destroy()
        self._available_expense_row_list.pop(delete_index)
        self._next_available_expense_index -= 1

    def __available_expense_list_get_index_of_expense(self, expense):
        for index, row_dict in enumerate(self._available_expense_row_list):
            if expense[Expense.keys.NAME] == row_dict[self._available_expense_keys.NAME_LBL]['text']:
                return index

    def append_to_expense_list(self, expense, expense_list, scrollframe_view_port, button_func, button_text, btn_key):
        expense_name = expense[Expense.keys.NAME]
        available_expense_dict = {}

        print(scrollframe_view_port.grid_size())

        # FRAME
        expense_frame = Frame(scrollframe_view_port, **style_frame_primary)
        expense_frame.grid(**grid_frame_primary)
        expense_frame.grid_columnconfigure(0, weight=1)
        expense_frame.grid_columnconfigure(1, weight=0)
        available_expense_dict['frame'] = expense_frame

        # NAME LABEL
        expense_name_lbl = Label(expense_frame, text=expense_name, **style_lbl)
        expense_name_lbl.grid(row=0, column=0, **grid_lbl)
        available_expense_dict['name_lbl'] = expense_name_lbl

        # BUTTON
        expense_action_btn = Button(expense_frame, text=button_text, command=lambda x=expense_name: button_func(x), **self.style_btn_delete)
        expense_action_btn.grid(row=0, column=1, **grid_btn)
        available_expense_dict[btn_key] = expense_action_btn

        expense_list.append(available_expense_dict)

    def append_to_available_expense_list(self, expense):
        self.append_to_expense_list(expense, self._available_expense_row_list, self._available_expense_scrollframe.view_port, self.__handle_assign_btn, "[+]", self._available_expense_keys.ASSIGN_BTN)
        # expense_name = expense[Expense.keys.NAME]
        # print('add available expense', expense_name)
        # available_expense_dict = {}
        # available_expense_frame = Frame(self._available_expense_scrollframe.view_port, **style_frame_primary)
        # available_expense_frame.grid(**grid_frame_primary)
        # available_expense_frame.grid_columnconfigure(0, weight=1)
        # available_expense_frame.grid_columnconfigure(1, weight=0)
        # available_expense_dict['frame'] = available_expense_frame
        #
        # expense_name_lbl = Label(available_expense_frame, text=expense_name, **style_lbl)
        # expense_name_lbl.grid(row=0, column=0, **grid_lbl)
        # available_expense_dict['name_lbl'] = expense_name_lbl
        #
        # expense_assign_btn = Button(available_expense_frame, text='[+]', command=lambda x=expense_name: self.__handle_assign_btn(x), **self.style_btn_delete)
        # expense_assign_btn.grid(row=0, column=1, **grid_btn)
        # available_expense_dict['assign_btn'] = expense_assign_btn
        #
        # self._available_expense_row_list.append(available_expense_dict)
        # self._next_available_expense_index += 1

    def append_to_account_expense_list(self, expense):
        expense_name = expense[Expense.keys.NAME]
        print('adding expense to account', expense_name)
        account_expense_dict = {}
        account_expense_frame = Frame(self._account_expense_scrollframe.view_port, **style_frame_primary)
        account_expense_frame.grid(row=self._next_account_expense_index, column=0, **grid_frame_primary)
        account_expense_frame.grid_columnconfigure(0, weight=1)
        account_expense_frame.grid_columnconfigure(1, weight=0)
        account_expense_dict[self._account_expense_keys.FRAME] = account_expense_frame

        expense_name_lbl = Label(account_expense_frame, text=expense_name, **style_lbl)
        expense_name_lbl.grid(row=0, column=0, **grid_lbl)
        account_expense_dict[self._account_expense_keys.NAME_LBL] = expense_name_lbl

        expense_unassign_btn = Button(account_expense_frame, text='[-]', command=lambda x=expense_name: self.__handle_unassign_btn(x), **self.style_btn_delete)
        expense_unassign_btn.grid(row=0, column=1, **grid_btn)
        account_expense_dict[self._account_expense_keys.UNASSIGN_BTN] = expense_unassign_btn

        self._account_expense_row_list.append(account_expense_dict)
        self._next_account_expense_index += 1

    def account_expense_list_clear(self):
        print("Clearing account/expense list")
        for row_dict in self._account_expense_row_list:
            account_expense_frame = row_dict[self._account_expense_keys.FRAME]
            for child in account_expense_frame.grid_slaves():
                child.grid_remove()
                child.destroy()

            # DESTROY FRAME
            account_expense_frame.grid_remove()
            account_expense_frame.destroy()
            self._account_expense_row_list.remove(row_dict)
            self._next_account_expense_index -= 1

            # self.account_expense_list_remove_expense_from_account_by_index(idx)
        if self._account_expense_row_list != []:
            print("HAD TO CLEAR TWICE FOR SOME REASON")
            self.account_expense_list_clear()
        if self._next_account_expense_index != 0:
            print("INDEX WAS INCORRECT")

    # ACCOUNT EXPENSE LIST
    def account_expense_list_remove_expense_from_account_by_index(self, delete_index):
        account_expense_delete_row = self._account_expense_row_list[delete_index]
        account_expense_frame = account_expense_delete_row[self._account_expense_keys.FRAME]
        # DESTROY EVERY CHILD WIDGET
        for child in account_expense_frame.grid_slaves():
            child.grid_remove()
            child.destroy()

        # DESTROY FRAME
        account_expense_frame.grid_remove()
        account_expense_frame.destroy()
        self._account_expense_row_list.pop(delete_index)
        self._next_account_expense_index -= 1

    def account_expense_list_populate(self, expenses_list):
        print("POPULATING EXPENSE LIST")
        for expense in expenses_list:
            print(expense[Expense.keys.NAME])
            self.append_to_account_expense_list(expense)


class TotalsFrame(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # TOTALS TITLE
        self._totals_lbl_title = Label(self, text="Totals", **style_lbl)
        self._totals_lbl_title.grid(row=0, column=0, columnspan=2, **grid_lbl)

        # YEARLY
        self._total_yearly_lbl = Label(self, text="Yearly", **style_lbl)
        self._total_yearly_lbl.grid(row=1, column=0, **grid_lbl)

        self._total_yearly_display = Label(self, **style_lbl)
        self._total_yearly_display.grid(row=1, column=1, **grid_lbl)

        # MONTHLY
        self._total_monthly_lbl = Label(self, text="Monthly", **style_lbl)
        self._total_monthly_lbl.grid(row=2, column=0, **grid_lbl)

        self._total_monthly_display = Label(self, **style_lbl)
        self._total_monthly_display.grid(row=2, column=1, **grid_lbl)

        # SEMI MONTHLY
        self._total_semi_monthly_lbl = Label(self, text="Semi-Monthly", **style_lbl)
        self._total_semi_monthly_lbl.grid(row=3, column=0, **grid_lbl)

        self._total_semi_monthly_display = Label(self, **style_lbl)
        self._total_semi_monthly_display.grid(row=3, column=1, **grid_lbl)

    def clear_displays(self):
        for display in [
            self._total_yearly_display,
            self._total_monthly_display,
            self._total_semi_monthly_display,
        ]:
            display['text'] = ""

    def show_account_stats(self, expenses_list, account):
        print('SHOWING TOTAL STATS - [ {} ]'.format(account[Account.keys.NAME]))
        # SHOW TOTALS
        total_yearly = 0
        for expense in expenses_list:
            yearly_value = expense.get_yearly_value()
            total_yearly += float(yearly_value)
        self._total_yearly_display['text'] = "{:.2f}".format(total_yearly)

        total_monthly = total_yearly / 12
        self._total_monthly_display['text'] = "{:.2f}".format(total_monthly)

        total_semi_monthly = total_monthly / 2
        self._total_semi_monthly_display['text'] = "{:.2f}".format(total_semi_monthly)


class AccountInfoFrame(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # INFO TITLE
        self._info_lbl_title = Label(self, text="Account Info", **style_lbl)
        self._info_lbl_title.grid(row=0, column=0, columnspan=2, **grid_lbl)

        # ACCOUNT NUMBER
        self._account_number_lbl = Label(self, text="Account #", **style_lbl)
        self._account_number_lbl.grid(row=1, column=0, **grid_lbl)

        self._account_number_display = Label(self, **style_lbl)
        self._account_number_display.grid(row=1, column=1, **grid_lbl)

        # ROUTE NUMBER
        self._route_number_lbl = Label(self, text="Route #", **style_lbl)
        self._route_number_lbl.grid(row=2, column=0, **grid_lbl)

        self._route_number_display = Label(self, **style_lbl)
        self._route_number_display.grid(row=2, column=1, **grid_lbl)

        # DESCRIPTION
        self._description_lbl = Label(self, text="Description", **style_lbl)
        self._description_lbl.grid(row=3, column=0, **grid_lbl)

        self._description_display = Label(self, **style_lbl)
        self._description_display.grid(row=3, column=1, **grid_lbl)

    def show_info(self, account):
        account_number = account[Account.keys.ACC_NUM]
        self._account_number_display['text'] = account_number
        self._route_number_display['text'] = account[Account.keys.ROUT_NUM]
        self._description_display['text'] = account[Account.keys.DESC]

    def clear_displays(self):
        for display in [
            self._account_number_display,
            self._route_number_display,
            self._description_display,
        ]:
            display['text'] = ""


class AccountSummaryFrame(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # TITLE
        self._title = Label(self, text="Account Summary", **style_lbl_title)
        self._title.grid(row=0, column=0, **grid_frame_primary)

        # ACTION FRAME
        self._action_frame = Frame(self, **style_frame_primary)
        self._action_frame.grid(row=1, column=0, **grid_frame_primary)
        self._action_frame.grid_columnconfigure(0, weight=1)
        self._action_frame.grid_columnconfigure(1, weight=1)
        self._action_frame.grid_rowconfigure(0, weight=0)

        # TOTALS FRAME
        self.totals_frame = TotalsFrame(self._action_frame, **style_frame_primary)
        self.totals_frame.grid(row=0, column=0, **grid_frame_primary)

        # INFO FRAME
        self.info_frame = AccountInfoFrame(self._action_frame, **style_frame_primary)
        self.info_frame.grid(row=0, column=1, **grid_frame_primary)

    def clear_stats(self):
        print("clear stats")
        self.totals_frame.clear_displays()
        self.info_frame.clear_displays()

    def refresh_account_summary(self, account, expenses_list):
        self.clear_stats()
        self.totals_frame.show_account_stats(expenses_list, account)
        self.info_frame.show_info(account)


class AccountSummary(ContentFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, "Account Summary", *args, **kwargs)
        self.view_port.grid_columnconfigure(0, weight=1)
        self.view_port.grid_columnconfigure(1, weight=1)
        self.view_port.grid_columnconfigure(2, weight=1)
        self.view_port.grid_rowconfigure(0, weight=0)
        self.view_port.grid_rowconfigure(1, weight=1)

        self.account_expense_map_frame = AccountExpenseMapFrame(self.view_port, **style_frame_primary)
        self.account_expense_map_frame.grid(row=0, column=1, columnspan=1, **grid_frame_primary)

        self.account_summary_frame = AccountSummaryFrame(self.view_port, **style_frame_primary)
        self.account_summary_frame.grid(row=1, column=0, columnspan=3, **grid_frame_primary)

    def handle_close(self):
        return


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # DATA
    accounts_list = [test_account]
    test_expense_list[0][Expense.keys.ACCOUNT] = accounts_list[0][Account.keys.NAME]

    # DEBUGGING FUNCTION
    def output_expense_list():
        for expense in test_expense_list:
            account_name = expense[Expense.keys.ACCOUNT]
            account_name_output = account_name
            if account_name is None:
                account_name_output = "***"
            print("[ {} ] = [ {} ]".format(expense[Expense.keys.NAME], account_name_output))

    def get_object_by_name_from_list(object_name, object_list):
        for obj in object_list:
            if obj[AbstractObjCommonKeys.NAME] == object_name:
                return obj
        return None

    def get_expenses_of_account(account):
        expenses_list = []
        for expense in test_expense_list:
            if expense[Expense.keys.ACCOUNT] == account[Account.keys.NAME]:
                expenses_list.append(expense)
        return expenses_list


    def account_changed():
        print("ACCOUNT CHANGED")
        current_account_name = frame.account_expense_map_frame.get_active_account_name()
        # ACCOUNT EXPENSE MAP
        frame.account_expense_map_frame.account_expense_list_clear()
        frame.account_summary_frame.clear_stats()
        if current_account_name != frame.account_expense_map_frame.default_account_option:
            account = get_object_by_name_from_list(current_account_name, accounts_list)
            expenses_list = get_expenses_of_account(account)
            frame.account_expense_map_frame.account_expense_list_populate(expenses_list)
            print(current_account_name)
            # ACCOUNT SUMMARY
            frame.account_summary_frame.show_account_stats(expenses_list, account)

    def unassign_expense(expense_name):
        print("UNASSIGN ACCOUNT")
        print(expense_name)
        account_name = frame.account_expense_map_frame.get_active_account_name()
        account = get_object_by_name_from_list(account_name, accounts_list)
        expense = get_object_by_name_from_list(expense_name, test_expense_list)
        # UPDATE EXPENSE IN DATA
        expense[Expense.keys.ACCOUNT] = None

        # REMOVE EXPENSE FROM ACCOUNT LIST
        frame.account_expense_map_frame.remove_expense_from_account_by_name(expense_name)

        # ADD EXPENSE TO AVAILABLE LIST
        frame.account_expense_map_frame.append_to_available_expense_list(expense)

        # REFRESH ACCOUNT SUMMARY
        expenses_list = get_expenses_of_account(account)
        frame.account_summary_frame.refresh_account_summary(account, expenses_list)

    def assign_expense_to_account(expense_name, account_name):
        print("ASSIGN ACCOUNT")
        account = get_object_by_name_from_list(account_name, accounts_list)
        expense = get_object_by_name_from_list(expense_name, test_expense_list)
        # UPDATE EXPENSE IN DATA
        expense[Expense.keys.ACCOUNT] = account[Account.keys.NAME]

        # REMOVE EXPENSE FROM AVAILABLE LIST
        frame.account_expense_map_frame.remove_expense_from_available_by_name(expense_name)

        # ADD EXPENSE TO ACCOUNT LIST
        frame.account_expense_map_frame.append_to_account_expense_list(expense)

        # REFRESH ACCOUNT SUMMARY
        expenses_list = get_expenses_of_account(account)
        frame.account_summary_frame.refresh_account_summary(account, expenses_list)

        # OUTPUT EXPENSE LIST
        output_expense_list()

    # SUMMARY FRAME
    frame = AccountSummary(root, width=800, height=800, **style_frame_primary)
    frame.account_expense_map_frame.populate_accounts(accounts_list)
    frame.account_expense_map_frame.populate_expenses(test_expense_list)
    frame.account_expense_map_frame.on_assign_callback = assign_expense_to_account
    frame.account_expense_map_frame.on_unassign_callback = unassign_expense
    frame.account_expense_map_frame.on_account_changed_callback = account_changed

    frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()

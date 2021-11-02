from App_BudgetHelper.GuiFrames.AccountFrames import *
from App_BudgetHelper.GuiFrames.ExpenseFrames import *
from App_BudgetHelper.GuiFrames.AccountSummaryFrames import *
from App_BudgetHelper.GuiFrames.ExpenseSummaryFrames import *
from Libs.DataLib.json_helper import *
from Libs.OSLib.os_helper import *

app_data = StandardAppDirStruct(os.getcwd(), "BudgetHelper")

# JSON FILEPATHS
JSON_ACCOUNTS = '{}\\accounts.json'.format(app_data.data_dir)
JSON_EXPENSES = '{}\\expenses.json'.format(app_data.data_dir)


class BudgetHelper(NavigableTkFrame):

    class ContentFrameIndices:
        ACCOUNT = 0
        EXPENSE = 1
        SAVING = 2
        ACCOUNT_SUMMARY = 3
        EXPENSE_SUMMARY = 4
    _frame_idxs = ContentFrameIndices()

    def __init__(self, root):
        super().__init__(root)
        # CONFIGURE FRAME
        self.content_frame.config(width=800, height=800)
        self.content_frame.grid_propagate(0)
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.__handle_close())
        self.config(bg='black')
        self.set_nav_btn_style(**style_navbtn)

        # DEFINE ACCOUNT VARIABLES
        self._accounts_list = []
        self._accounts_json_manager = JsonManager(JSON_ACCOUNTS)
        self.__import_account_data()

        # DEFINE EXPENSE VARIABLES
        self._expenses_list = []
        self._expenses_json_manager = JsonManager(JSON_EXPENSES)
        self.__import_expense_data()

        # CONTENT FRAMES
        # ACCOUNTS
        self._accounts_frame = AccountFrame(self.content_frame, **style_frame_primary)
        self._accounts_frame.account_edit_frame.add_object_btn.config(command=lambda: self.__add_account())
        self._accounts_frame.account_edit_frame.update_object_btn.config(command=lambda: self.__update_account())
        self._accounts_frame.account_view_frame.on_delete_callback = self.__delete_account
        self.add_content_frame(self._frame_idxs.ACCOUNT, self._accounts_frame)
        # EXPENSES
        self._expenses_frame = ExpenseFrame(self.content_frame, **style_frame_primary)
        self._expenses_frame.expense_edit_frame.add_object_btn.config(command=lambda: self.__add_expense())
        self._expenses_frame.expense_edit_frame.update_object_btn.config(command=lambda: self.__update_expense())
        self._expenses_frame.expense_view_frame.on_delete_callback = self.__delete_expense
        self.add_content_frame(self._frame_idxs.EXPENSE, self._expenses_frame)
        # ACCOUNT SUMMARY
        self._account_summary_frame = AccountSummary(self.content_frame, **style_frame_primary)
        self._account_summary_frame.account_expense_map_frame.on_assign_callback = self.assign_expense_to_account
        self._account_summary_frame.account_expense_map_frame.on_unassign_callback = self.unassign_expense
        self._account_summary_frame.account_expense_map_frame.on_account_changed_callback = self.account_changed
        self.add_content_frame(self._frame_idxs.ACCOUNT_SUMMARY, self._account_summary_frame)
        # EXPENSE SUMMARY
        self._expense_summary_frame = ExpenseSummary(self.content_frame, **style_frame_primary)
        self.add_content_frame(self._frame_idxs.EXPENSE_SUMMARY, self._expense_summary_frame)

        # PUT DATA IN FRAMES
        self._accounts_frame.account_view_frame.populate_objects(self._accounts_list)
        self._expenses_frame.expense_view_frame.populate_objects(self._expenses_list)
        self._account_summary_frame.account_expense_map_frame.populate_accounts(self._accounts_list)
        self._account_summary_frame.account_expense_map_frame.populate_expenses(self._expenses_list)
        self._expense_summary_frame.expense_summary_frame.update_expense_summary(self._expenses_list)

        self.show_frame(self._frame_idxs.ACCOUNT)

    def __handle_close(self):
        self.__save_all_data()
        self.master.destroy()

    def __save_all_data(self):
        self._accounts_json_manager.export_data(self._accounts_list)
        self._expenses_json_manager.export_data(self._expenses_list)

    ####################################################################################################################
    # ACCOUNT RELATED FUNCTIONS
    def __import_account_data(self):
        raw_accounts = self._accounts_json_manager.import_data()
        # SORT ALPHABETICALLY
        sorted_list = sorted(raw_accounts, key=lambda d: d[AccountKeys.NAME])
        for raw_account in sorted_list:
            new_account = Account(**raw_account)
            self._accounts_list.append(new_account)

    def __check_account_exists(self, account: Account):
        for acc in self._accounts_list:
            if acc[AccountKeys.NAME] == account[AccountKeys.NAME]:
                return True
        return False

    def __add_account(self):
        # GET ACCOUNT FROM ENTRIES
        raw_account_dict = self._accounts_frame.account_edit_frame.get_object_from_entries()
        account = Account(**raw_account_dict)

        # DATA VALIDATION
        if self.__check_account_exists(account):
            return

        # GLOBAL ADD
        self._accounts_list.append(account)

        # ACCOUNT FRAME
        self._accounts_frame.account_view_frame.add_object(account)
        self._accounts_frame.account_edit_frame.clear_entries()

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.account_expense_map_frame.add_account(account)

    def __update_account(self):
        # GET ACCOUNT FROM ENTRIES
        update_account = self._accounts_frame.account_edit_frame.get_object_from_entries()

        # GLOBAL UPDATE
        for account in self._accounts_list:
            if account[AccountKeys.NAME] == update_account[AccountKeys.NAME]:
                self._accounts_list.remove(account)
                self._accounts_list.append(update_account)

        # UPDATE ACCOUNT FRAME
        self._accounts_frame.account_view_frame.update_object(update_account)
        self._accounts_frame.account_edit_frame.change_to_add_mode()

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.account_expense_map_frame.set_active_account_to_none()

    def __delete_account(self, delete_account: Account):
        # GLOBAL DELETE
        for account in self._accounts_list:
            if account[AccountKeys.NAME] == delete_account[AccountKeys.NAME]:
                self._accounts_list.remove(account)

        # ACCOUNT FRAME
        self._accounts_frame.account_view_frame.delete_object(delete_account)

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.account_expense_map_frame.delete_account_option(delete_account)
        for expense in self._expenses_list:
            if expense[Expense.keys.ACCOUNT] == delete_account[Account.keys.NAME]:
                expense[Expense.keys.ACCOUNT] = None
                self._account_summary_frame.account_expense_map_frame.append_to_available_expense_list(expense)

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.account_expense_map_frame.set_active_account_to_none()

    ####################################################################################################################
    # EXPENSE RELATED FUNCTIONS
    def __import_expense_data(self):
        raw_expenses = self._expenses_json_manager.import_data()
        # SORT ALPHABETICALLY
        sorted_list = sorted(raw_expenses, key=lambda d: d[ExpenseKeys.NAME])
        for raw_expense in sorted_list:
            new_expense = Expense(**raw_expense)
            self._expenses_list.append(new_expense)

    def __check_expense_exists(self, expense):
        for acc in self._expenses_list:
            if acc[ExpenseKeys.NAME] == expense[ExpenseKeys.NAME]:
                return True
        return False

    def __add_expense(self):
        # GET EXPENSE FROM ENTRIES
        raw_expense_dict = self._expenses_frame.expense_edit_frame.get_object_from_entries()
        expense = Expense(**raw_expense_dict)

        # DATA VALIDATION
        if self.__check_expense_exists(expense):
            return

        # GLOBAL ADD
        self._expenses_list.append(expense)

        # EXPENSE FRAME
        self._expenses_frame.expense_view_frame.add_object(expense)
        self._expenses_frame.expense_edit_frame.clear_entries()

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.account_expense_map_frame.append_to_available_expense_list(expense)

        # EXPENSE SUMMARY FRAME
        self._expense_summary_frame.expense_summary_frame.update_expense_summary(self._expenses_list)

    def __update_expense(self):
        # GET EXPENSE FROM ENTRIES
        entry_expense = self._expenses_frame.expense_edit_frame.get_object_from_entries()

        # GET EXPENSE FROM DATA
        update_expense = self.get_object_by_name_from_list(entry_expense[Expense.keys.NAME], self._expenses_list)
        # ENTRY WON'T HAVE ACCOUNT NAME, SO ADD IT BEFORE COPYING OVER
        entry_expense[Expense.keys.ACCOUNT] = update_expense[Expense.keys.ACCOUNT]
        update_expense.copy_from(entry_expense)

        # UPDATE EXPENSE FRAME
        self._expenses_frame.expense_view_frame.update_object(update_expense)
        self._expenses_frame.expense_edit_frame.change_to_add_mode()

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.account_expense_map_frame.set_active_account_to_none()

        # EXPENSE SUMMARY FRAME
        self._expense_summary_frame.expense_summary_frame.update_expense_summary(self._expenses_list)

    def __delete_expense(self, delete_expense: Expense):
        # GLOBAL DELETE
        expense = self.get_object_by_name_from_list(delete_expense[Expense.keys.NAME], self._expenses_list)
        expense_name = expense[Expense.keys.NAME]
        # for expense in self._expenses_list:
        #     if expense[ExpenseKeys.NAME] == delete_expense[ExpenseKeys.NAME]:
        self._expenses_list.remove(expense)

        # EXPENSE FRAME
        self._expenses_frame.expense_view_frame.delete_object(expense)

        # REMOVE FROM AVAILABLE IF IT IS NOT ASSIGNED
        self._account_summary_frame.account_expense_map_frame.set_active_account_to_none()
        if expense[Expense.keys.ACCOUNT] is None:
            self._account_summary_frame.account_expense_map_frame.remove_expense_from_available_by_name(expense_name)

        # EXPENSE SUMMARY FRAME
        self._expense_summary_frame.expense_summary_frame.update_expense_summary(self._expenses_list)

    ####################################################################################################################
    # ACCOUNT SUMMARY RELATED FUNCTIONS
    @staticmethod
    def get_object_by_name_from_list(object_name, object_list):
        for obj in object_list:
            if obj[AbstractObjCommonKeys.NAME] == object_name:
                return obj
        return None

    def get_expenses_of_account(self, account):
        expenses_list = []
        for expense in self._expenses_list:
            if expense[Expense.keys.ACCOUNT] == account[Account.keys.NAME]:
                expenses_list.append(expense)
        return expenses_list

    def account_changed(self):
        print("ACCOUNT CHANGED")
        current_account_name = self._account_summary_frame.account_expense_map_frame.get_active_account_name()
        # ACCOUNT EXPENSE MAP
        self._account_summary_frame.account_expense_map_frame.account_expense_list_clear()
        self._account_summary_frame.account_summary_frame.clear_stats()
        if current_account_name != self._account_summary_frame.account_expense_map_frame.default_account_option:
            account = self.get_object_by_name_from_list(current_account_name, self._accounts_list)
            expenses_list = self.get_expenses_of_account(account)
            self._account_summary_frame.account_expense_map_frame.account_expense_list_populate(expenses_list)
            print(current_account_name)
            # ACCOUNT SUMMARY
            self._account_summary_frame.account_summary_frame.refresh_account_summary(account, expenses_list)

    def unassign_expense(self, expense_name):
        print("UNASSIGN ACCOUNT")
        print(expense_name)
        account_name = self._account_summary_frame.account_expense_map_frame.get_active_account_name()
        account = self.get_object_by_name_from_list(account_name, self._accounts_list)
        expense = self.get_object_by_name_from_list(expense_name, self._expenses_list)
        # UPDATE EXPENSE IN DATA
        expense[Expense.keys.ACCOUNT] = None

        # REMOVE EXPENSE FROM ACCOUNT LIST
        self._account_summary_frame.account_expense_map_frame.remove_expense_from_account_by_name(expense_name)

        # ADD EXPENSE TO AVAILABLE LIST
        self._account_summary_frame.account_expense_map_frame.append_to_available_expense_list(expense)

        # REFRESH ACCOUNT SUMMARY
        expenses_list = self.get_expenses_of_account(account)
        self._account_summary_frame.account_summary_frame.refresh_account_summary(account, expenses_list)

    def assign_expense_to_account(self, expense_name, account_name):
        print("ASSIGN ACCOUNT")
        account = self.get_object_by_name_from_list(account_name, self._accounts_list)
        expense = self.get_object_by_name_from_list(expense_name, self._expenses_list)
        # UPDATE EXPENSE IN DATA
        expense[Expense.keys.ACCOUNT] = account[Account.keys.NAME]

        # REMOVE EXPENSE FROM AVAILABLE LIST
        self._account_summary_frame.account_expense_map_frame.remove_expense_from_available_by_name(expense_name)

        # ADD EXPENSE TO ACCOUNT LIST
        self._account_summary_frame.account_expense_map_frame.append_to_account_expense_list(expense)

        # REFRESH ACCOUNT SUMMARY
        expenses_list = self.get_expenses_of_account(account)
        self._account_summary_frame.account_summary_frame.refresh_account_summary(account, expenses_list)

    ####################################################################################################################
    # EXPENSE SUMMARY RELATED FUNCTIONS
    def update_expense_summary(self):
        self._expense_summary_frame.expense_summary_frame.update_expense_summary(self._expenses_list)


if __name__ == '__main__':
    root = Tk()
    root.title("Budget Helper")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # # TEST ACCOUNTEDITFRAME
    # def on_submit():
    #     print(frame.get_entries())
    #     frame.clear_entries()
    # frame = AccountEditFrame(root, on_submit_func=lambda: on_submit())
    # frame.edit_account(test_account)

    # # TEST ACCOUNTVIEWFRAME
    # frame = AccountViewFrame(root, **style_frame_primary)
    # frame.populate_accounts([test_account])

    # # TEST ACCOUNT FRAME
    # frame = AccountFrame(root)

    # TEST BUDGETHELPER
    frame = BudgetHelper(root)

    frame.grid(row=0, column=0, sticky='nsew')
        
    root.mainloop()

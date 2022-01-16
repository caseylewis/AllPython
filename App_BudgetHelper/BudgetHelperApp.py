import yaml

from App_BudgetHelper.components.AccountSummary.AccountSummaryFrame import *
from App_BudgetHelper.components.Accounts.AccountFrame import *
from App_BudgetHelper.components.ExpenseSummary.ExpenseSummaryFrame import *
from App_BudgetHelper.components.Expenses.ExpenseFrame import *
from App_BudgetHelper.components.PaymentOverview.PaymentOverviewFrame import *
from App_BudgetHelper.components.PreTaxDeductions.PreTaxDeductionFrame import *
from App_BudgetHelper.components.Savings.SavingFrame import *
from App_BudgetHelper.config import *
from Libs.DataLib.json_helper import *
from Libs.GuiLib.gui_majors import *
from Libs.GuiLib.gui_styles import *
from Libs.OSLib.os_helper import *


class BudgetHelper(NavigableTkFrame):
    app_data = StandardAppDirStruct(os.getcwd(), "BudgetHelper")
    # JSON DATA
    accounts_json = JsonManager(os.path.join(app_data.data_dir, 'accounts.json'))
    expenses_json = JsonManager(os.path.join(app_data.data_dir, 'expenses.json'))
    savings_json = JsonManager(os.path.join(app_data.data_dir, 'savings.json'))
    pre_tax_deductions_json = JsonManager(os.path.join(app_data.data_dir, 'pre_tax_deductions.json'))
    # YAML DATA
    config_yaml = os.path.join(app_data.data_dir, 'config.yml')
    payment_info_yaml = os.path.join(app_data.data_dir, 'payment_info.yml')

    class ContentFrameIndices:
        ACCOUNT = 0
        EXPENSE = 1
        SAVING = 2
        PRE_TAX_DEDUCTION = 3
        ACCOUNT_SUMMARY = 4
        EXPENSE_SUMMARY = 5
        PAYMENT_OVERVIEW = 6

    _frame_idxs = ContentFrameIndices()

    def __init__(self, root):
        super().__init__(root)
        # CONFIGURE FRAME
        self.content_frame.config(width=800, height=800)
        self.content_frame.grid_propagate(0)
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.__handle_close())
        self.config(bg='black')
        self.set_nav_btn_style(**style_navbtn)

        # DEFINE CONFIG VARIABLES
        self._config_dict = {}
        self.__import_config_data()

        # DEFINE ACCOUNT VARIABLES
        self._accounts_list = []
        self.__import_account_data()

        # DEFINE EXPENSE VARIABLES
        self._expenses_list = []
        self.__import_expense_data()

        # DEFINE SAVING VARIABLES
        self._savings_list = []
        self.__import_saving_data()

        # DEFINE PRE TAX DEDUCTION VARIABLES
        self._pre_tax_deductions_list = []
        self.__import_pre_tax_deduction_data()

        # DEFINE PAYMENT OVERVIEW VARIABLES
        self._payment_dict = {}
        self.__import_payment_data()

        # CONTENT FRAMES
        # ACCOUNTS
        self._accounts_frame = AccountFrame(self.content_frame,
                                            hide_scrollbars=self._config_dict[KEY_HIDE_SCROLLBARS],
                                            on_add_func=self.__add_account,
                                            on_update_func=self.__update_account,
                                            on_edit_by_name_func=self.__edit_account_by_name,
                                            on_delete_by_name_func=self.__delete_account_by_name)
        self.add_content_frame(self._frame_idxs.ACCOUNT, self._accounts_frame)
        # EXPENSES
        self._expenses_frame = ExpenseFrame(self.content_frame,
                                            hide_scrollbars=self._config_dict[KEY_HIDE_SCROLLBARS],
                                            on_add_func=self.__add_expense,
                                            on_update_func=self.__update_expense,
                                            on_edit_by_name_func=self.__edit_expense_by_name,
                                            on_delete_by_name_func=self.__delete_expense_by_name)
        self.add_content_frame(self._frame_idxs.EXPENSE, self._expenses_frame)
        # SAVINGS
        self._savings_frame = SavingFrame(self.content_frame,
                                          hide_scrollbars=self._config_dict[KEY_HIDE_SCROLLBARS],
                                          on_add_func=self.__add_saving,
                                          on_update_func=self.__update_saving,
                                          on_edit_by_name_func=self.__edit_saving_by_name,
                                          on_delete_by_name_func=self.__delete_saving_by_name)
        self.add_content_frame(self._frame_idxs.SAVING, self._savings_frame)
        # PRE TAX DEDUCTIONS
        self._pre_tax_deductions_frame = PreTaxDeductionFrame(self.content_frame,
                                                              hide_scrollbars=self._config_dict[KEY_HIDE_SCROLLBARS],
                                                              on_add_func=self.__add_pre_tax_deduction,
                                                              on_update_func=self.__update_pre_tax_deduction,
                                                              on_edit_by_name_func=self.__edit_deduction_by_name,
                                                              on_delete_by_name_func=self.__delete_deduction_by_name)
        self.add_content_frame(self._frame_idxs.PRE_TAX_DEDUCTION, self._pre_tax_deductions_frame)
        # ACCOUNT SUMMARY
        self._account_summary_frame = AccountSummaryFrame(self.content_frame,
                                                          hide_scrollbars=self._config_dict[KEY_HIDE_SCROLLBARS],
                                                          on_assign_by_name_func=self.__assign_to_account,
                                                          on_unassign_by_name_func=self.__unassign_from_account,
                                                          on_account_name_changed_func=self.__account_changed)
        self.add_content_frame(self._frame_idxs.ACCOUNT_SUMMARY, self._account_summary_frame)
        # EXPENSE SUMMARY
        self._expense_summary_frame = ExpenseSummaryFrame(self.content_frame)
        self.add_content_frame(self._frame_idxs.EXPENSE_SUMMARY, self._expense_summary_frame)
        # PAYMENT OVERVIEW
        self._payment_overview_frame = PaymentOverviewFrame(self.content_frame, self._payment_dict,
                                                            hide_scrollbars=self._config_dict[KEY_HIDE_SCROLLBARS],
                                                            on_payment_info_changed_func=self.__payment_info_changed)
        self.add_content_frame(self._frame_idxs.PAYMENT_OVERVIEW, self._payment_overview_frame)

        # PUT DATA IN FRAMES
        self._accounts_frame.populate_objects(self._accounts_list)
        self._expenses_frame.populate_objects(self._expenses_list)
        self._savings_frame.populate_objects(self._savings_list)
        self._pre_tax_deductions_frame.populate_objects(self._pre_tax_deductions_list)
        self._account_summary_frame.populate_objects(self._accounts_list, self._expenses_list)
        self._expense_summary_frame.update_expense_summary(self._expenses_list)
        self.__update_payment_overview()

        self.show_frame(self._frame_idxs.ACCOUNT)

    def __handle_close(self):
        self.__save_all_data()
        self.master.destroy()

    def __save_all_data(self):
        self.__export_config_data()
        self.accounts_json.export_data(self._accounts_list)
        self.expenses_json.export_data(self._expenses_list)
        self.savings_json.export_data(self._savings_list)
        self.pre_tax_deductions_json.export_data(self._pre_tax_deductions_list)
        self.__export_payment_data()

    @staticmethod
    def get_object_by_name_from_list(object_name, object_list):
        for obj in object_list:
            if obj[AbstractObjCommonKeys.NAME] == object_name:
                return obj
        return None

    ####################################################################################################################
    # GENERAL OBJECT FUNCTIONS
    @staticmethod
    def __data_import_simple_object(object_json, object_type, object_list):
        raw_objects = object_json.import_data()
        # SORT ALPHABETICALLY
        sorted_list = sorted(raw_objects, key=lambda d: d[object_type.keys.NAME])
        for raw_object in sorted_list:
            new_object = object_type(**raw_object)
            object_list.append(new_object)

    @staticmethod
    def __data_check_object_exists(object_list, object_type, object_to_check):
        for obj in object_list:
            if obj[object_type.keys.NAME] == object_to_check[object_type.keys.NAME]:
                return True
        return False

    def __data_add_object(self, object_to_add, object_type, object_list):
        # DATA VALIDATION
        if self.__data_check_object_exists(object_list, object_type, object_to_add):
            return
        # GLOBAL ADD
        object_list.append(object_to_add)

    def __data_update_object(self, object_list, object_to_update):
        old_object = self.get_object_by_name_from_list(object_to_update.name, object_list)
        old_object.copy_from(object_to_update)

    def __data_delete_object_by_name(self, object_list, object_name):
        delete_object = self.get_object_by_name_from_list(object_name, object_list)
        object_list.remove(delete_object)

    ####################################################################################################################
    # GUI SHARED OBJECT FUNCTIONS
    @staticmethod
    def __gui_add_simple_object(object_to_add, object_frame):
        object_frame.add_object(object_to_add)
        object_frame.clear_entries()

    @staticmethod
    def __gui_update_simple_object(object_to_update, object_frame):
        object_frame.update_object(object_to_update)

    def __gui_edit_object_by_name(self, object_list, object_name, object_frame):
        edit_object = self.get_object_by_name_from_list(object_name, object_list)
        object_frame.edit_object(edit_object)

    @staticmethod
    def __gui_delete_object_by_name(object_name, object_frame):
        object_frame.delete_object_by_name(object_name)

    ####################################################################################################################
    # IMPORTS
    def __import_account_data(self):
        self.__data_import_simple_object(self.accounts_json, Account, self._accounts_list)

    def __import_expense_data(self):
        self.__data_import_simple_object(self.expenses_json, Expense, self._expenses_list)

    def __import_saving_data(self):
        self.__data_import_simple_object(self.savings_json, Saving, self._savings_list)

    def __import_pre_tax_deduction_data(self):
        self.__data_import_simple_object(self.pre_tax_deductions_json, PreTaxDeduction, self._pre_tax_deductions_list)

    def __import_config_data(self):
        # ENSURE FILE EXISTS
        file_create(self.config_yaml)
        # IMPORT FROM CONFIG YAML
        with open(self.config_yaml, 'r') as file:
            config_dict = yaml.safe_load(file)
            file.close()

        if config_dict is not None:
            self._config_dict = config_dict
            print(self._config_dict)
        else:
            self._config_dict[KEY_HIDE_SCROLLBARS] = True

    def __import_payment_data(self):
        # ENSURE FILE EXISTS
        file_create(self.payment_info_yaml)
        # IMPORT FROM PAYMENT INFO YAML
        with open(self.payment_info_yaml, 'r') as file:
            payment_dict = yaml.safe_load(file)
            file.close()

        if payment_dict is not None:
            self._payment_dict = payment_dict
        else:
            self._payment_dict[KEY_SALARY] = 50000
            self._payment_dict[KEY_PAY_FREQUENCY] = PayFrequencies.SEMI_MONTHLY

    # EXPORTS
    def __export_config_data(self):
        with open(self.config_yaml, 'w') as file:
            yaml.dump(self._config_dict, file)

    def __export_payment_data(self):
        with open(self.payment_info_yaml, 'w') as file:
            yaml.dump(self._payment_dict, file)

    # ADD
    def __add_account(self, account):
        # DATA ADD
        self.__data_add_object(account, Account, self._accounts_list)
        # GUI SIMPLE ADD
        self.__gui_add_simple_object(account, self._accounts_frame)

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.add_account(account)

    def __add_expense(self, expense):
        # DATA ADD
        self.__data_add_object(expense, Expense, self._expenses_list)
        # GUI SIMPLE ADD
        self.__gui_add_simple_object(expense, self._expenses_frame)

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.add_available_expense(expense)

        # EXPENSE SUMMARY FRAME
        self._expense_summary_frame.update_expense_summary(self._expenses_list)

        # PAYMENT OVERVIEW FRAME
        self.__update_payment_overview()

    def __add_saving(self, saving):
        # DATA ADD
        self.__data_add_object(saving, Saving, self._savings_list)
        # GUI SIMPLE ADD
        self.__gui_add_simple_object(saving, self._savings_frame)

        # PAYMENT OVERVIEW FRAME
        self.__update_payment_overview()

    def __add_pre_tax_deduction(self, pre_tax_deduction):
        # DATA ADD
        self.__data_add_object(pre_tax_deduction, PreTaxDeduction, self._pre_tax_deductions_list)
        # GUI SIMPLE ADD
        self.__gui_add_simple_object(pre_tax_deduction, self._pre_tax_deductions_frame)

        # PAYMENT OVERVIEW FRAME
        self.__update_payment_overview()

    # UPDATE
    def __update_account(self, new_account):
        # DATA UPDATE
        self.__data_update_object(self._accounts_list, new_account)
        # GUI UPDATE OBJECT
        self.__gui_update_simple_object(new_account, self._accounts_frame)

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.set_active_account_to_none()

    def __update_expense(self, new_expense):
        # BEFORE UPDATING, MUST COPY OVER ACCOUNT
        old_expense = self.get_object_by_name_from_list(new_expense.name, self._expenses_list)
        new_expense.account = old_expense.account
        # DATA UPDATE
        self.__data_update_object(self._expenses_list, new_expense)
        # GUI UPDATE OBJECT
        self.__gui_update_simple_object(new_expense, self._expenses_frame)

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.set_active_account_to_none()

        # EXPENSE SUMMARY FRAME
        self._expense_summary_frame.update_expense_summary(self._expenses_list)

        # PAYMENT OVERVIEW FRAME
        self.__update_payment_overview()

    def __update_saving(self, new_saving):
        # DATA UPDATE
        self.__data_update_object(self._savings_list, new_saving)
        # GUI UPDATE OBJECT
        self.__gui_update_simple_object(new_saving, self._savings_frame)

        # PAYMENT OVERVIEW FRAME
        self.__update_payment_overview()

    def __update_pre_tax_deduction(self, new_pre_tax_deduction):
        # DATA UPDATE
        self.__data_update_object(self._pre_tax_deductions_list, new_pre_tax_deduction)
        # GUI UPDATE OBJECT
        self.__gui_update_simple_object(new_pre_tax_deduction, self._pre_tax_deductions_frame)

        # PAYMENT OVERVIEW FRAME
        self.__update_payment_overview()

    # EDIT
    def __edit_account_by_name(self, account_name):
        # DATA EDIT
        self.__gui_edit_object_by_name(self._accounts_list, account_name, self._accounts_frame)

    def __edit_expense_by_name(self, expense_name):
        # GUI EDIT
        self.__gui_edit_object_by_name(self._expenses_list, expense_name, self._expenses_frame)

    def __edit_saving_by_name(self, saving_name):
        # GUI EDIT
        self.__gui_edit_object_by_name(self._savings_list, saving_name, self._savings_frame)

    def __edit_deduction_by_name(self, deduction_name):
        # GUI EDIT
        self.__gui_edit_object_by_name(self._pre_tax_deductions_list, deduction_name, self._pre_tax_deductions_frame)

    # DELETE
    def __delete_account_by_name(self, account_name):
        # BEFORE NORMAL DATA AND GUI FUNCTION, MUST GET INFO
        delete_account = self.get_object_by_name_from_list(account_name, self._accounts_list)

        # DATA DELETE
        self.__data_delete_object_by_name(self._accounts_list, account_name)
        # GUI DELETE OBJECT
        self.__gui_delete_object_by_name(account_name, self._accounts_frame)

        # ACCOUNT SUMMARY FRAME
        self._account_summary_frame.set_active_account_to_none()
        self._account_summary_frame.delete_account_option(delete_account)
        for expense in self._expenses_list:
            if expense.account == delete_account.name:
                expense.account = None
                self._account_summary_frame.add_available_expense(expense)

    def __delete_expense_by_name(self, expense_name):
        # BEFORE NORMAL DATA AND GUI FUNCTION, MUST GET INFO
        delete_expense = self.get_object_by_name_from_list(expense_name, self._expenses_list)

        # DATA DELETE
        self.__data_delete_object_by_name(self._expenses_list, expense_name)
        # GUI DELETE OBJECT
        self.__gui_delete_object_by_name(expense_name, self._expenses_frame)

        # ACCOUNT SUMMARY FRAME
        # # REMOVE FROM AVAILABLE IF IT IS NOT ASSIGNED
        self._account_summary_frame.set_active_account_to_none()
        if delete_expense.account is None:
            self._account_summary_frame.remove_available_expense(delete_expense)

        # EXPENSE SUMMARY FRAME
        self._expense_summary_frame.update_expense_summary(self._expenses_list)

        # PAYMENT OVERVIEW FRAME
        self.__update_payment_overview()

    def __delete_saving_by_name(self, saving_name):
        # DATA DELETE
        self.__data_delete_object_by_name(self._savings_list, saving_name)
        # GUI DELETE OBJECT
        self.__gui_delete_object_by_name(saving_name, self._savings_frame)

        # PAYMENT OVERVIEW FRAME
        self.__update_payment_overview()

    def __delete_deduction_by_name(self, deduction_name):
        # DATA DELETE
        self.__data_delete_object_by_name(self._expenses_list, deduction_name)
        # GUI DELETE OBJECT
        self.__gui_delete_object_by_name(deduction_name, self._expenses_frame)

        # PAYMENT OVERVIEW FRAME
        self.__update_payment_overview()

    ####################################################################################################################
    # ACCOUNT SUMMARY RELATED FUNCTIONS
    def __get_expenses_of_account(self, account):
        account_expenses_list = []
        for expense in self._expenses_list:
            if expense.account == account.name:
                account_expenses_list.append(expense)
        return account_expenses_list

    def __assign_to_account(self, expense_name):
        active_account = self._account_summary_frame.get_active_account_name()
        if active_account != self._account_summary_frame.default_account_option:
            expense = self.get_object_by_name_from_list(expense_name, self._expenses_list)
            expense.account = active_account
            self._account_summary_frame.add_account_expense(expense)
            self._account_summary_frame.remove_available_expense(expense)
            # UPDATE ACCOUNT VALUES
            self.__account_values_changed_by_name(self._account_summary_frame.get_active_account_name())

    def __unassign_from_account(self, expense_name):
        expense = self.get_object_by_name_from_list(expense_name, self._expenses_list)
        expense.account = None
        self._account_summary_frame.add_available_expense(expense)
        self._account_summary_frame.remove_account_expense(expense)
        # UPDATE ACCOUNT VALUES
        self.__account_values_changed_by_name(self._account_summary_frame.get_active_account_name())

    def __account_changed(self):
        active_account_name = self._account_summary_frame.get_active_account_name()
        self._account_summary_frame.clear_data()
        if active_account_name != self._account_summary_frame.default_account_option:
            active_account = self.get_object_by_name_from_list(active_account_name, self._accounts_list)
            account_expense_list = self.__get_expenses_of_account(active_account)
            self._account_summary_frame.populate_account_expense_scrollframe(account_expense_list)
            # UPDATE ACCOUNT VALUES
            self.__account_values_changed_by_name(active_account.name)

    def __account_values_changed_by_name(self, account_name):
        account = self.get_object_by_name_from_list(account_name, self._accounts_list)
        account_expense_list = self.__get_expenses_of_account(account)
        self._account_summary_frame.refresh_account_info(account_expense_list, account)

    ####################################################################################################################
    # EXPENSE SUMMARY RELATED FUNCTIONS

    ####################################################################################################################
    def __update_payment_overview(self):
        self._payment_overview_frame.update_payment_overview(self._payment_dict, self._expenses_list, self._pre_tax_deductions_list, self._savings_list)

    # PAYMENT OVERVIEW RELATED FUNCTIONS
    def __payment_info_changed(self, payment_dict):
        self._payment_dict = payment_dict
        self.__update_payment_overview()


if __name__ == '__main__':
    root = Tk()
    root.title("Budget Helper")
    root.config(bg='black')
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

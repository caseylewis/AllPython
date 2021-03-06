from App_BudgetHelper.components.Expenses.expenses import *
from App_BudgetHelper.components.PaymentOverview.PayFrequencies import *
from App_BudgetHelper.components.PaymentOverview.PaymentEntryFrame import KEY_SALARY, KEY_PAY_FREQUENCY, \
    get_pay_divisor_by_pay_frequency
from App_BudgetHelper.components.PaymentOverview.TaxBrackets import calculate_federal_taxes_owed, calculate_fica_owed
from App_BudgetHelper.components.PreTaxDeductions.pre_tax_deductions import *
from App_BudgetHelper.components.Savings.savings import *
from Libs.GuiLib.gui_standards import *


class PaymentBreakdownFrame(StandardFrame):
    def __init__(self, root, hide_scrollbars=True):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # TITLE
        self._title = TitleLabel(self, "Pay Breakdown")
        self._title.grid(row=0, column=0, columnspan=3, **TitleLabel.grid_args)

        # SCROLLFRAME
        self._content_scrollframe = ScrollFramePlus(self, hide_scrollbar=hide_scrollbars, bg=FRAME_BG_STANDARD)
        self._content_scrollframe.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=0, padx=0)
        self._content_scrollframe.view_port.grid_columnconfigure(0, weight=1)
        self._content_scrollframe.view_port.grid_columnconfigure(1, weight=1)
        self._content_scrollframe.view_port.grid_columnconfigure(2, weight=1)

        # PAYMENT INFO DISPLAY
        class cols:
            LBL = 0
            DISPLAY = 1

        class rows:
            SALARY_HEADER = 0
            SALARY = 1
            PAY_FREQ = 2
            PAY_HEADER = 3
            GROSS = 4
            NET = 5
            DED_HEADER = 6
            PRE_TAX = 7
            FED_TAX = 8
            FICA_TAX = 9
            DISCLAIMER = 10
        c = cols()
        r = rows()

        self._payment_info_frame = StandardFrame(self._content_scrollframe.view_port)
        self._payment_info_frame.grid(row=1, column=1, **StandardFrame.grid_args)
        self._payment_info_frame.grid_columnconfigure(0, weight=1)
        self._payment_info_frame.grid_columnconfigure(1, weight=1)

        # SALARY
        self._salary_header = StandardLabel(self._payment_info_frame, "Salary", **StandardLabel.header_args)
        self._salary_header.grid(row=r.SALARY_HEADER, column=0, columnspan=2, **StandardLabel.grid_args)

        self._salary_lbl = StandardLabel(self._payment_info_frame, "Salary")
        self._salary_lbl.grid(row=r.SALARY, column=c.LBL, **StandardLabel.grid_args)

        self._salary_display = StandardLabel(self._payment_info_frame, "", **StandardLabel.decimal_args)
        self._salary_display.grid(row=r.SALARY, column=c.DISPLAY, **StandardLabel.grid_args)

        self._pay_freq_lbl = StandardLabel(self._payment_info_frame, "Pay Frequency")
        self._pay_freq_lbl.grid(row=r.PAY_FREQ, column=c.LBL, **StandardLabel.grid_args)

        self._pay_freq_display = StandardLabel(self._payment_info_frame, "")
        self._pay_freq_display.grid(row=r.PAY_FREQ, column=c.DISPLAY, **StandardLabel.grid_args)

        # PAYCHECK
        self._paycheck_header = StandardLabel(self._payment_info_frame, "Paycheck", **StandardLabel.header_args)
        self._paycheck_header.grid(row=r.PAY_HEADER, column=0, columnspan=2, **StandardLabel.grid_args)

        self._gross_paycheck_lbl = StandardLabel(self._payment_info_frame, "Gross Paycheck")
        self._gross_paycheck_lbl.grid(row=r.GROSS, column=c.LBL, **StandardLabel.grid_args)

        self._gross_paycheck_display = StandardLabel(self._payment_info_frame, "", **StandardLabel.decimal_args)
        self._gross_paycheck_display.grid(row=r.GROSS, column=c.DISPLAY, **StandardLabel.grid_args)

        self._net_paycheck_lbl = StandardLabel(self._payment_info_frame, "Net Paycheck")
        self._net_paycheck_lbl.grid(row=r.NET, column=c.LBL, **StandardLabel.grid_args)

        self._net_paycheck_display = StandardLabel(self._payment_info_frame, "", **StandardLabel.decimal_args)
        self._net_paycheck_display.grid(row=r.NET, column=c.DISPLAY, **StandardLabel.grid_args)

        # DEDUCTIONS
        self._deductions_header = StandardLabel(self._payment_info_frame, "Deductions", **StandardLabel.header_args)
        self._deductions_header.grid(row=r.DED_HEADER, column=0, columnspan=2, **StandardLabel.grid_args)

        self._pre_tax_deductions_lbl = StandardLabel(self._payment_info_frame, "Pre Tax Deductions")
        self._pre_tax_deductions_lbl.grid(row=r.PRE_TAX, column=c.LBL, **StandardLabel.grid_args)

        self._pre_tax_deductions_display = StandardLabel(self._payment_info_frame, "", **StandardLabel.decimal_args)
        self._pre_tax_deductions_display.grid(row=r.PRE_TAX, column=c.DISPLAY, **StandardLabel.grid_args)

        self._federal_taxes_lbl = StandardLabel(self._payment_info_frame, "*Federal Taxes")
        self._federal_taxes_lbl.grid(row=r.FED_TAX, column=c.LBL, **StandardLabel.grid_args)

        self._federal_taxes_display = StandardLabel(self._payment_info_frame, "", **StandardLabel.decimal_args)
        self._federal_taxes_display.grid(row=r.FED_TAX, column=c.DISPLAY, **StandardLabel.grid_args)

        self._fica_taxes_lbl = StandardLabel(self._payment_info_frame, "*FICA Taxes")
        self._fica_taxes_lbl.grid(row=r.FICA_TAX, column=c.LBL, **StandardLabel.grid_args)

        self._fica_taxes_display = StandardLabel(self._payment_info_frame, "", **StandardLabel.decimal_args)
        self._fica_taxes_display.grid(row=r.FICA_TAX, column=c.DISPLAY, **StandardLabel.grid_args)

        # tax_disclaimer = "* Tax calculations are approximate and based on 2022 tax brackets found here: https://www.nerdwallet.com/article/taxes/federal-income-tax-brackets"
        # self._tax_disclaimer = StandardLabel(self._payment_info_frame, tax_disclaimer)
        # self._tax_disclaimer.grid(row=r.DISCLAIMER, column=0, columnspan=2, **StandardLabel.grid_args)

        # EXPENSE/LEFTOVER DISPLAY
        self._expense_leftover_display_frame = StandardFrame(self._content_scrollframe.view_port)
        self._expense_leftover_display_frame.grid(row=2, column=0, columnspan=3, **StandardFrame.grid_args)
        self._expense_leftover_display_frame.grid_columnconfigure(0, weight=0)
        self._expense_leftover_display_frame.grid_columnconfigure(1, weight=1)
        self._expense_leftover_display_frame.grid_columnconfigure(2, weight=1)

        r_header = 0
        r_expenses = 1
        r_savings = 2
        r_left = 3
        # HEADER ROW
        self._blank_lbl = StandardLabel(self._expense_leftover_display_frame, "", **StandardLabel.header_args)
        self._blank_lbl.grid(row=r_header, column=0, **StandardLabel.grid_args)

        self._amount_per_check_lbl = StandardLabel(self._expense_leftover_display_frame, "Amount/Check", **StandardLabel.header_args)
        self._amount_per_check_lbl.grid(row=r_header, column=1, **StandardLabel.grid_args)

        self._percent_of_check_lbl = StandardLabel(self._expense_leftover_display_frame, "% of Check", **StandardLabel.header_args)
        self._percent_of_check_lbl.grid(row=r_header, column=2, **StandardLabel.grid_args)

        # EXPENSES ROW
        self._expenses_lbl = StandardLabel(self._expense_leftover_display_frame, "Expenses", **StandardLabel.header_args)
        self._expenses_lbl.grid(row=r_expenses, column=0, **StandardLabel.grid_args)

        self._expense_amount_display = StandardLabel(self._expense_leftover_display_frame, "", **StandardLabel.decimal_args)
        self._expense_amount_display.grid(row=r_expenses, column=1, **StandardLabel.grid_args)

        self._expense_percent_display = StandardLabel(self._expense_leftover_display_frame, "", **StandardLabel.decimal_args)
        self._expense_percent_display.grid(row=r_expenses, column=2, **StandardLabel.grid_args)

        # SAVINGS ROW
        self._savings_lbl = StandardLabel(self._expense_leftover_display_frame, "Savings", **StandardLabel.header_args)
        self._savings_lbl.grid(row=r_savings, column=0, **StandardLabel.grid_args)

        self._saving_amount_display = StandardLabel(self._expense_leftover_display_frame, "", **StandardLabel.decimal_args)
        self._saving_amount_display.grid(row=r_savings, column=1, **StandardLabel.grid_args)

        self._saving_percent_display = StandardLabel(self._expense_leftover_display_frame, "", **StandardLabel.decimal_args)
        self._saving_percent_display.grid(row=r_savings, column=2, **StandardLabel.grid_args)

        # LEFTOVER ROW
        self._leftover_lbl = StandardLabel(self._expense_leftover_display_frame, "Leftover", **StandardLabel.header_args)
        self._leftover_lbl.grid(row=r_left, column=0, **StandardLabel.grid_args)

        self._leftover_amount_display = StandardLabel(self._expense_leftover_display_frame, "", **StandardLabel.decimal_args)
        self._leftover_amount_display.grid(row=r_left, column=1, **StandardLabel.grid_args)

        self._leftover_percent_display = StandardLabel(self._expense_leftover_display_frame, "", **StandardLabel.decimal_args)
        self._leftover_percent_display.grid(row=r_left, column=2, **StandardLabel.grid_args)

    @staticmethod
    def __get_total_pre_tax_deductions(gross_pay, pre_tax_deductions_list):
        total_deductions = 0
        post_deduction_pay = gross_pay
        highest_priority = 0

        # MAKE A SPARE LIST TO MUTATE
        temp_deductions_list = []
        for deduction in pre_tax_deductions_list:
            temp_deductions_list.append(deduction)

        # GET HIGHEST PRIORITY FOR RANGE
        for deduction in pre_tax_deductions_list:
            if int(deduction.priority) > highest_priority:
                highest_priority = int(deduction.priority)
        # ITERATE THROUGH PRIORITIES
        for priority in range(highest_priority+1):
            for deduction in temp_deductions_list:
                deduction_priority = int(deduction.priority)
                deduction_value = float(deduction.value)
                if deduction_priority == priority:
                    # PERCENTAGE
                    if deduction.type == PreTaxDeductionTypes.PERCENTAGE:
                        deduction_value = float(deduction_value / 100) * post_deduction_pay
                    # FIXED
                    elif deduction.type == PreTaxDeductionTypes.FIXED:
                        deduction_value = deduction_value
                    # SUBTRACT POST DEDUCTION PAY AND REMOVE DEDUCTION FROM LIST
                    post_deduction_pay -= deduction_value
                    total_deductions += deduction_value
                    temp_deductions_list.remove(deduction)

        return post_deduction_pay, total_deductions

    def update_breakdown(self, payment_dict, expenses_list, pre_tax_deductions_list, savings_list):
        salary = float(payment_dict[KEY_SALARY])
        pay_frequency = payment_dict[KEY_PAY_FREQUENCY]
        # GET YEAR DIVISOR BASED ON PAY FREQUENCY
        year_divisor = get_pay_divisor_by_pay_frequency(pay_frequency)

        gross_paycheck = float(salary / year_divisor)
        post_deduction_paycheck, pre_tax_deductions_per_paycheck = self.__get_total_pre_tax_deductions(gross_paycheck, pre_tax_deductions_list)
        fica_tax_per_paycheck = calculate_fica_owed(gross_paycheck)
        yearly_taxable = (post_deduction_paycheck - fica_tax_per_paycheck) * year_divisor
        federal_tax_per_year, tax_bracket = calculate_federal_taxes_owed(yearly_taxable)
        federal_tax_per_paycheck = federal_tax_per_year / year_divisor
        net_paycheck = post_deduction_paycheck - federal_tax_per_paycheck - fica_tax_per_paycheck

        # CALCULATE YEARLY EXPENSES TO DIVIDE BY YEAR DIVISOR
        yearly_expenses = 0
        for expense in expenses_list:
            yearly_expenses += expense.get_yearly_value()
        expenses_per_paycheck = yearly_expenses / year_divisor

        # CALCULATE SAVINGS
        savings_per_paycheck = 0
        for saving in savings_list:
            saving_value = float(saving.value)
            saving_type = saving.type
            if saving_type == SavingTypes.PERCENTAGE:
                savings_per_paycheck += net_paycheck * (saving_value / 100)
            elif saving_type == SavingTypes.FIXED:
                savings_per_paycheck += saving_value

        # UPDATE PAYMENT INFO DISPLAY
        self._salary_display.set_decimal(salary)
        self._pay_freq_display.set(pay_frequency)

        # GROSS PAYCHECK
        self._gross_paycheck_display.set_decimal(gross_paycheck)

        # NET PAYCHECK
        self._net_paycheck_display.set_decimal(net_paycheck)

        # PRE TAX DEDUCTIONS
        self._pre_tax_deductions_display.set_decimal(pre_tax_deductions_per_paycheck)

        # FEDERAL TAX
        self._federal_taxes_display.set_decimal(federal_tax_per_paycheck)

        # FICA TAX
        self._fica_taxes_display.set_decimal(fica_tax_per_paycheck)

        # CALCULATE LEFTOVER
        leftover = net_paycheck - expenses_per_paycheck

        # SET AMOUNTS
        self._expense_amount_display.set_decimal(expenses_per_paycheck)
        self._saving_amount_display.set_decimal(savings_per_paycheck)
        self._leftover_amount_display.set_decimal(leftover)

        # CALCULATE PERCENTAGES
        expense_percentage = float(float(expenses_per_paycheck) / float(net_paycheck)) * 100
        saving_percentage = float(float(savings_per_paycheck) / float(net_paycheck)) * 100
        leftover_percentage = 100 - expense_percentage - saving_percentage

        # SET PERCENTAGES
        self._expense_percent_display.set_percentage(expense_percentage)
        self._saving_percent_display.set_percentage(saving_percentage)
        self._leftover_percent_display.set_percentage(leftover_percentage)


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    payment_dict = {
        KEY_SALARY: 50000,
        KEY_PAY_FREQUENCY: PayFrequencies.SEMI_MONTHLY
    }

    def on_submit(payment_dict):
        for key, value in payment_dict.items():
            print(key, value)

    frame = PaymentBreakdownFrame(root)
    frame.grid(row=0, column=0, sticky=grid_style.sticky.all)
    frame.update_breakdown(payment_dict, test_expense_list, test_pre_tax_deduction_list)

    root.mainloop()

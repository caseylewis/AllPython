

__MEDICARE_RATE = 0.0145
__SOCIAL_SECURITY_RATE = 0.062
FICA_RATE = __MEDICARE_RATE + __SOCIAL_SECURITY_RATE


class FederalTaxBracket:
    def __init__(self, rate, low, high, previous_bracket_sum):
        self.rate = rate
        self.low = low
        self.high = high
        self.previous_bracket_sum = previous_bracket_sum


__tax_bracket_list = [
    FederalTaxBracket(10, 1, 10275, 0),
    FederalTaxBracket(12, 10276, 41775, 1027.5),
    FederalTaxBracket(22, 41776, 89075, 4807.5),
    FederalTaxBracket(24, 89076, 170050, 15213.5),
    FederalTaxBracket(32, 170051, 215950, 34647.5),
    FederalTaxBracket(35, 215951, 539900, 49335.5),
    FederalTaxBracket(37, 539901, 10000000, 162718),
]


def calculate_fica_owed(gross_salary):
    _fica_tax = gross_salary * FICA_RATE
    return _fica_tax


def calculate_federal_taxes_owed(taxable_yearly_salary):
    _federal_taxes = 0
    _tax_bracket = None

    for bracket in __tax_bracket_list:
        if bracket.low <= taxable_yearly_salary <= bracket.high:
            _federal_taxes = ((taxable_yearly_salary - bracket.low - 1) * (bracket.rate / 100)) + bracket.previous_bracket_sum
            _tax_bracket = bracket
    return _federal_taxes, _tax_bracket


if __name__ == '__main__':
    _fica_tax = calculate_fica_owed(110000)
    _federal_taxes, _bracket = calculate_federal_taxes_owed(89619.44)
    print(_federal_taxes, _fica_tax, _bracket.rate)

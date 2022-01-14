

FICA_RATE = 0.0765


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


def calculate_taxes_owed(gross_salary):
    federal_taxes = 0
    fica_taxes = gross_salary * FICA_RATE
    tax_bracket = None

    for bracket in __tax_bracket_list:
        if bracket.low <= gross_salary <= bracket.high:
            federal_taxes = ((gross_salary - bracket.low - 1) * (bracket.rate / 100)) + bracket.previous_bracket_sum
            tax_bracket = bracket

    return federal_taxes, fica_taxes, tax_bracket


if __name__ == '__main__':
    _federal_taxes, _fica_tax, _bracket = calculate_taxes_owed(100000)
    print(_federal_taxes, _fica_tax, _bracket.rate)

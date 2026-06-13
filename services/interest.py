from models.inputs import InterestType, InvestmentInputs


def calculate_gross_amount(inputs: InvestmentInputs) -> tuple[float, float]:
    principal = inputs.principal
    rate = inputs.annual_rate / 100.0
    years = inputs.years

    if inputs.interest_type == InterestType.SIMPLE:
        gross_amount = principal * (1 + rate * years)
    else:
        gross_amount = principal * ((1 + rate) ** years)

    gross_interest = gross_amount - principal
    return gross_amount, gross_interest


def calculate_net(inputs: InvestmentInputs) -> dict[str, float]:
    gross_amount, gross_interest = calculate_gross_amount(inputs)
    tax_rate = inputs.tax_rate / 100.0
    fee_rate = inputs.fee_rate / 100.0
    net_interest = gross_interest * (1 - tax_rate - fee_rate)
    net_amount = inputs.principal + net_interest

    return {
        "gross_amount": gross_amount,
        "gross_interest": gross_interest,
        "net_interest": net_interest,
        "net_amount": net_amount,
    }

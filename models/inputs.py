from dataclasses import dataclass
from enum import Enum


class InterestType(str, Enum):
    SIMPLE = "Simple"
    COMPOUND = "Compound"


@dataclass
class InvestmentInputs:
    principal: float
    annual_rate: float
    years: float
    tax_rate: float
    fee_rate: float
    interest_type: InterestType

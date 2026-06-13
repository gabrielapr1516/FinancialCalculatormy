from PyQt5.QtGui import QDoubleValidator


def positive_double_validator(decimals: int = 2) -> QDoubleValidator:
    validator = QDoubleValidator(0.0, 1e12, decimals)
    validator.setNotation(QDoubleValidator.StandardNotation)
    return validator

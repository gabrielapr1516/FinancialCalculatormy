# Calculadora financiera (PyQt5)

App sencilla y modular para calcular rendimiento neto usando interes simple o interes compuesto.

## Requisitos
- Python 3.9+

## Instalacion
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar
```bash
python app.py
```

## Formulas
- Interes simple: monto bruto = P * (1 + r * t)
- Interes compuesto: monto bruto = P * (1 + r) ^ t
- Interes bruto = monto bruto - P
- Interes neto = interes bruto * (1 - impuesto - gastos)
- Monto neto = P + interes neto

Donde:
- P = capital inicial
- r = tasa anual (decimal)
- t = tiempo en anos
- impuesto y gastos = porcentajes (decimales)

## Notas
- Impuesto y gastos son opcionales; si se dejan vacios se asumen 0%.
- Si impuesto + gastos superan 100%, el interes neto puede ser negativo.

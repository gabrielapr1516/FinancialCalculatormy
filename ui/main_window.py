# ui/main_window.py
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QTabWidget,
)

from models.inputs import InterestType, InvestmentInputs
from services.interest import calculate_net
from utils.validators import positive_double_validator

# ─── Paleta de Colores Estilizada ─────────────────────────────────────────
BG_DARK      = "#090D16"
BG_CARD      = "#111622"
BG_INPUT     = "#1A2030"
BORDER       = "#263147"
BORDER_FOCUS = "#4DA6FF"
ACCENT       = "#4DA6FF"
ACCENT2      = "#47D16D"
TEXT_PRIMARY = "#F0F3F8"
TEXT_MUTED   = "#7E8C9F"
TEXT_LABEL   = "#BDC9DB"
RESULT_BG    = "#0A1424"
RESULT_CARD  = "#142136"
GOLD         = "#FFD043"


def _build_style(s: float) -> str:
    """Genera el stylesheet escalado al factor *s*."""
    def p(val: int) -> int:
        return max(1, round(val * s))

    return f"""
QMainWindow, QWidget#root {{
    background-color: {BG_DARK};
}}

/* ── Estilo de las Pestañas (Tabs) ── */
QTabWidget::panel {{
    border: 1px solid {BORDER};
    background-color: {BG_DARK};
    border-radius: {p(8)}px;
    top: -1px;
}}
QTabBar::tab {{
    background-color: {BG_INPUT};
    color: {TEXT_MUTED};
    border: 1px solid {BORDER};
    border-bottom: none;
    border-top-left-radius: {p(6)}px;
    border-top-right-radius: {p(6)}px;
    padding: {p(8)}px {p(16)}px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 600;
    font-size: {p(13)}px;
    margin-right: {p(4)}px;
}}
QTabBar::tab:selected {{
    background-color: {BG_CARD};
    color: {ACCENT};
    border-color: {BORDER};
    border-bottom: 2px solid {ACCENT};
}}
QTabBar::tab:hover:!selected {{
    background-color: #222B3D;
    color: {TEXT_PRIMARY};
}}

QFrame#card {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: {p(14)}px;
}}
QLabel#app_title {{
    color: {TEXT_PRIMARY};
    font-size: {p(24)}px;
    font-weight: 700;
    font-family: 'Segoe UI', sans-serif;
}}
QLabel#app_subtitle {{
    color: {TEXT_MUTED};
    font-size: {p(13)}px;
    font-family: 'Segoe UI', sans-serif;
}}
QLabel#section_title {{
    color: {ACCENT};
    font-size: {p(11)}px;
    font-weight: 700;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 1.8px;
}}
QLabel#field_label {{
    color: {TEXT_LABEL};
    font-size: {p(13)}px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 600;
    min-width: {p(130)}px;
}}
QLineEdit {{
    background-color: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: {p(8)}px;
    color: {TEXT_PRIMARY};
    font-size: {p(14)}px;
    padding: {p(9)}px {p(14)}px;
}}
QLineEdit:focus {{
    border: 1px solid {BORDER_FOCUS};
    background-color: #151B2B;
}}
QLineEdit:hover {{ border-color: #3B4B6E; }}
QLineEdit::placeholder {{ color: #4E5D78; font-style: italic; }}

QComboBox {{
    background-color: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: {p(8)}px;
    color: {TEXT_PRIMARY};
    font-size: {p(14)}px;
    padding: {p(9)}px {p(14)}px;
}}
QComboBox:hover {{ border-color: #3B4B6E; }}
QComboBox:focus {{ border: 1px solid {BORDER_FOCUS}; }}
QComboBox::drop-down {{ border: none; width: {p(28)}px; }}
QComboBox::down-arrow {{
    image: none;
    border-left: {p(4)}px solid transparent;
    border-right: {p(4)}px solid transparent;
    border-top: {p(5)}px solid {TEXT_MUTED};
    margin-right: {p(10)}px;
}}
QComboBox QAbstractItemView {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER};
    color: {TEXT_PRIMARY};
    selection-background-color: #1A2A45;
    outline: none;
}}

QPushButton#calc_btn {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2575FC, stop:1 #6A11CB);
    color: white;
    border: none;
    border-radius: {p(8)}px;
    font-size: {p(14)}px;
    font-weight: 600;
    padding: {p(11)}px {p(30)}px;
}}
QPushButton#calc_btn:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3B82F6, stop:1 #7C3AED);
}}
QPushButton#clear_btn {{
    background-color: transparent;
    color: {TEXT_MUTED};
    border: 1px solid {BORDER};
    border-radius: {p(8)}px;
    font-size: {p(13)}px;
    padding: {p(10)}px {p(22)}px;
}}
QPushButton#clear_btn:hover {{
    color: {TEXT_PRIMARY};
    border-color: #4A5B7C;
    background-color: {BG_INPUT};
}}

QFrame#result_panel {{
    background-color: {RESULT_BG};
    border: 1px solid #16263F;
    border-radius: {p(14)}px;
}}
QFrame#metric_card {{
    background-color: {RESULT_CARD};
    border: 1px solid #1C304E;
    border-radius: {p(10)}px;
}}
QLabel#metric_value {{ font-size: {p(21)}px; font-weight: 700; color: {TEXT_PRIMARY}; }}
QLabel#metric_value_accent {{ font-size: {p(26)}px; font-weight: 700; color: {ACCENT2}; }}
QLabel#metric_label {{ color: {TEXT_MUTED}; font-size: {p(11)}px; font-weight: 700; letter-spacing: 0.8px; }}
QLabel#metric_badge {{
    color: {GOLD};
    font-size: {p(10)}px;
    font-weight: 700;
    background-color: rgba(255, 208, 67, 0.1);
    border: 1px solid rgba(255, 208, 67, 0.2);
    border-radius: {p(4)}px;
    padding: {p(2)}px {p(8)}px;
}}
QFrame#separator {{ background-color: #161F30; max-height: 1px; }}
"""

def _shadow() -> QGraphicsDropShadowEffect:
    fx = QGraphicsDropShadowEffect()
    fx.setBlurRadius(20)
    fx.setOffset(0, 6)
    fx.setColor(QColor(0, 0, 0, 102))
    return fx

class MetricCard(QFrame):
    def __init__(self, label: str, accent: bool = False, badge: str = "") -> None:
        super().__init__()
        self.setObjectName("metric_card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        self._label = QLabel(label.upper())
        self._label.setObjectName("metric_label")

        self._value = QLabel("—")
        self._value.setObjectName("metric_value_accent" if accent else "metric_value")

        layout.addWidget(self._label)
        layout.addWidget(self._value)

        if badge:
            badge_lbl = QLabel(badge.upper())
            badge_lbl.setObjectName("metric_badge")
            badge_lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addWidget(badge_lbl)

    def set_value(self, text: str) -> None:
        self._value.setText(text)


class MainWindow(QMainWindow):
    def __init__(self, screen_geometry=None, screen_dpi: float = 96.0) -> None:
        super().__init__()
        self._scale = max(0.85, min(2.5, screen_dpi / 96.0))
        self._screen_geo = screen_geometry
        self.setWindowTitle("Software de Ingeniería y Finanzas")
        self.setStyleSheet(_build_style(self._scale))
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("root")
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(16)

        # ── Encabezado Principal ────────────────────────────────────────────
        header = QHBoxLayout()
        icon_lbl = QLabel("📊")
        icon_lbl.setStyleSheet("font-size: 32px;")
        
        title_col = QVBoxLayout()
        title = QLabel("Panel de Control General")
        title.setObjectName("app_title")
        subtitle = QLabel("Módulos independientes de simulación científica y análisis analítico")
        subtitle.setObjectName("app_subtitle")
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        header.addWidget(icon_lbl)
        header.addLayout(title_col)
        header.addStretch()
        root_layout.addLayout(header)

        # ── Contenedor de Pestañas (TabWidget) ──────────────────────────────
        self.tabs = QTabWidget()
        
        # Instanciar las pestañas
        finance_tab = QWidget()
        graphic_tab = QWidget()
        
        self.tabs.addTab(finance_tab, "💰 Calculadora Financiera")
        self.tabs.addTab(graphic_tab, "🌡️ Diagrama Termodinámico P-V")
        
        # Armar contenido de cada pestaña
        self._setup_finance_tab(finance_tab)
        self._setup_graphic_tab(graphic_tab)
        
        root_layout.addWidget(self.tabs)
        self.setCentralWidget(root)

        # Escalar tamaño de ventana
        if self._screen_geo is not None:
            sw, sh = self._screen_geo.width(), self._screen_geo.height()
            self.setGeometry(self._screen_geo.x() + (sw - int(sw*0.6))//2,
                             self._screen_geo.y() + (sh - int(sh*0.8))//2,
                             int(sw * 0.6), int(sh * 0.8))
        else:
            self.resize(800, 680)

    def _setup_finance_tab(self, container: QWidget) -> None:
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(16)

        # Formulario
        form_card = QFrame()
        form_card.setObjectName("card")
        form_card.setGraphicsEffect(_shadow())
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(20, 16, 20, 16)
        
        sec_lbl = QLabel("PARÁMETROS DE INVERSIÓN")
        sec_lbl.setObjectName("section_title")
        form_layout.addWidget(sec_lbl)

        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(12)

        self.principal_input = QLineEdit()
        self.principal_input.setPlaceholderText("Ej: 10000.00")
        self.principal_input.setValidator(positive_double_validator(2))

        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText("Ej: 7.5")
        self.rate_input.setValidator(positive_double_validator(4))

        self.years_input = QLineEdit()
        self.years_input.setPlaceholderText("Ej: 3")
        self.years_input.setValidator(positive_double_validator(2))

        self.tax_input = QLineEdit()
        self.tax_input.setPlaceholderText("Ej: 10 (Opcional)")
        self.tax_input.setValidator(positive_double_validator(2))

        self.fee_input = QLineEdit()
        self.fee_input.setPlaceholderText("Ej: 1 (Opcional)")
        self.fee_input.setValidator(positive_double_validator(2))

        self.interest_type = QComboBox()
        self.interest_type.addItems([InterestType.SIMPLE.value, InterestType.COMPOUND.value])

        fields = [
            ("Capital inicial ($)", self.principal_input, 0, 0),
            ("Tasa anual (%)",      self.rate_input,      0, 2),
            ("Tiempo (años)",       self.years_input,     1, 0),
            ("Tipo de interés",     self.interest_type,   1, 2),
            ("Impuesto (%)",        self.tax_input,       2, 0),
            ("Gastos (%)",          self.fee_input,       2, 2),
        ]

        for label_text, widget, row, col in fields:
            lbl = QLabel(label_text)
            lbl.setObjectName("field_label")
            grid.addWidget(lbl, row, col)
            grid.addWidget(widget, row, col + 1)

        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)
        form_layout.addLayout(grid)
        layout.addWidget(form_card)

        # Botones
        btn_row = QHBoxLayout()
        self.clear_btn = QPushButton("Limpiar campos")
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.clicked.connect(self._on_clear)
        self.calculate_button = QPushButton("Calcular Análisis →")
        self.calculate_button.setObjectName("calc_btn")
        self.calculate_button.clicked.connect(self._on_calculate)
        btn_row.addStretch()
        btn_row.addWidget(self.clear_btn)
        btn_row.addWidget(self.calculate_button)
        layout.addLayout(btn_row)

        # Panel Resultados
        self.result_panel = QFrame()
        self.result_panel.setObjectName("result_panel")
        res_layout = QVBoxLayout(self.result_panel)
        
        res_header = QHBoxLayout()
        res_sec = QLabel("MÉTRICAS DEL ANÁLISIS")
        res_sec.setObjectName("section_title")
        self.result_status = QLabel("Esperando parámetros...")
        self.result_status.setObjectName("result_status")
        res_header.addWidget(res_sec)
        res_header.addStretch()
        res_header.addWidget(self.result_status)
        res_layout.addLayout(res_header)

        metrics_grid = QGridLayout()
        self.card_net_amount = MetricCard("Monto Neto Total", accent=True, badge="Rendimiento")
        self.card_net_int    = MetricCard("Interés Neto Real", accent=False)
        self.card_gross_amt  = MetricCard("Monto Bruto Base", accent=False)
        self.card_gross_int  = MetricCard("Interés Bruto Acum.", accent=False)

        metrics_grid.addWidget(self.card_net_amount, 0, 0)
        metrics_grid.addWidget(self.card_net_int,    0, 1)
        metrics_grid.addWidget(self.card_gross_amt,  1, 0)
        metrics_grid.addWidget(self.card_gross_int,  1, 1)
        res_layout.addLayout(metrics_grid)
        layout.addWidget(self.result_panel)

    def _setup_graphic_tab(self, container: QWidget) -> None:
        """Renderiza e incrusta el gráfico dinámico de Matplotlib (grafic.py)."""
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)

        # Crear figura de Matplotlib con fondo adaptado a la UI
        fig = Figure(figsize=(8, 5), facecolor=BG_CARD)
        canvas = FigureCanvas(fig)
        canvas.setGraphicsEffect(_shadow())
        
        ax = fig.add_subplot(111)
        ax.set_facecolor(BG_INPUT)

        # Lógica de grafic.py integrada
        V1, P1 = 2.066, 150
        V2, P2 = 0.540, 750
        V3, P3 = 0.413, 750

        # Trayectorias
        n = 1.2
        V_12 = np.linspace(V1, V2, 100)
        P_12 = (P1 * (V1 ** n)) / (V_12 ** n)

        V_23 = np.linspace(V2, V3, 100)
        P_23 = np.full_like(V_23, P2)

        V_31 = np.linspace(V3, V1, 100)
        P_31 = (P1 * V1) / V_31

        # Dibujar líneas con colores brillantes aptos para modo oscuro
        ax.plot(V_12, P_12, color="#58A6FF", linewidth=2.5, label=r'1 $\rightarrow$ 2: C. Politrópica ($n=1.2$)')
        ax.plot(V_23, P_23, color="#FF7B72", linewidth=2.5, label=r'2 $\rightarrow$ 3: E. Isobárico')
        ax.plot(V_31, P_31, color="#3FB950", linewidth=2.5, label=r'3 $\rightarrow$ 1: E. Isotérmica')
        ax.plot([V1, V2, V3], [P1, P2, P3], 'o', color=TEXT_PRIMARY, markersize=7)

        # Etiquetas de estados adaptadas al modo oscuro
        bbox_style = dict(boxstyle='round,pad=0.4', fc=BG_CARD, ec=BORDER, alpha=0.95)
        ax.text(V1 + 0.05, P1 - 40, 'Estado 1\n(2.066 m³, 150 kPa)', color=TEXT_PRIMARY, fontsize=10, fontweight='bold', bbox=bbox_style)
        ax.text(V2 + 0.05, P2 + 30, 'Estado 2\n(0.540 m³, 750 kPa)', color=TEXT_PRIMARY, fontsize=10, fontweight='bold', bbox=bbox_style)
        ax.text(V3 - 0.05, P3 + 30, 'Estado 3\n(0.413 m³, 750 kPa)', color=TEXT_PRIMARY, fontsize=10, fontweight='bold', ha='right', bbox=bbox_style)

        # Flechas directrices
        for V_arr, P_arr, col in [(V_12, P_12, '#58A6FF'), (V_23, P_23, '#FF7B72'), (V_31, P_31, '#3FB950')]:
            ax.annotate('', xy=(V_arr[50], P_arr[50]), xytext=(V_arr[49], P_arr[49]),
                        arrowprops=dict(arrowstyle="->", color=col, lw=2.5))

        # Estilizar títulos y ejes del gráfico
        ax.set_title('Diagrama P-V: Ciclo Termodinámico (Problema 3)', color=TEXT_PRIMARY, fontsize=13, fontweight='bold', pad=12)
        ax.set_xlabel('Volumen (m³)', color=TEXT_LABEL, fontsize=11)
        ax.set_ylabel('Presión (kPa)', color=TEXT_LABEL, fontsize=11)
        
        ax.tick_params(colors=TEXT_MUTED, labelsize=10)
        ax.set_xlim(0.2, 2.4)
        ax.set_ylim(0, 950)
        ax.grid(True, linestyle='--', color=BORDER, alpha=0.5)
        
        # Leyenda estilizada
        leg = ax.legend(loc='lower left', fontsize=10, facecolor=BG_CARD, edgecolor=BORDER)
        for text in leg.get_texts():
            text.set_color(TEXT_PRIMARY)

        layout.addWidget(canvas)

    # ── Métodos de Lógica Financiera ──────────────────────────────────────────
    def _on_calculate(self) -> None:
        principal = self._parse_required(self.principal_input, "Capital inicial")
        if principal is None: return
        rate = self._parse_required(self.rate_input, "Tasa anual")
        if rate is None: return
        years = self._parse_required(self.years_input, "Tiempo")
        if years is None: return

        tax_rate = self._parse_optional(self.tax_input)
        fee_rate = self._parse_optional(self.fee_input)

        interest_type = InterestType.SIMPLE if self.interest_type.currentText() == InterestType.SIMPLE.value else InterestType.COMPOUND

        inputs = InvestmentInputs(principal=principal, annual_rate=rate, years=years, tax_rate=tax_rate, fee_rate=fee_rate, interest_type=interest_type)
        result = calculate_net(inputs)

        def fmt(v: float) -> str: return f"$ {v:,.2f}"

        self.card_net_amount.set_value(fmt(result["net_amount"]))
        self.card_net_int.set_value(fmt(result["net_interest"]))
        self.card_gross_amt.set_value(fmt(result["gross_amount"]))
        self.card_gross_int.set_value(fmt(result["gross_interest"]))

        self.result_status.setText(f"Interés {'Simple' if interest_type == InterestType.SIMPLE else 'Compuesto'} · {years:.1f} Año(s)")
        self.result_status.setStyleSheet(f"color: {ACCENT2}; font-size: 13px; font-weight: 600;")
        self._pulse_panel()

    def _pulse_panel(self) -> None:
        self.result_panel.setStyleSheet(f"QFrame#result_panel {{ background-color: {RESULT_BG}; border: 1.5px solid {ACCENT2}; border-radius: 14px; }}")
        QTimer.singleShot(350, lambda: self.result_panel.setStyleSheet(f"QFrame#result_panel {{ background-color: {RESULT_BG}; border: 1px solid #16263F; border-radius: 14px; }}"))

    def _on_clear(self) -> None:
        for field in (self.principal_input, self.rate_input, self.years_input, self.tax_input, self.fee_input):
            field.clear()
        self.interest_type.setCurrentIndex(0)
        for card in (self.card_net_amount, self.card_net_int, self.card_gross_amt, self.card_gross_int):
            card.set_value("—")
        self.result_status.setText("Esperando parámetros...")
        self.result_status.setStyleSheet("")

    def _parse_required(self, field: QLineEdit, label: str) -> float | None:
        text = field.text().strip().replace(",", ".")
        if not text:
            self._show_error(f"El campo '{label}' es requerido.")
            return None
        try:
            value = float(text)
        except ValueError:
            self._show_error(f"'{label}' debe ser un número válido.")
            return None
        return value

    def _parse_optional(self, field: QLineEdit) -> float:
        text = field.text().strip().replace(",", ".")
        try:
            return float(text) if text else 0.0
        except ValueError:
            return 0.0

    def _show_error(self, message: str) -> None:
        msg = QMessageBox(self)
        msg.setWindowTitle("Error de Validación")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.setStyleSheet(f"QMessageBox {{ background-color: {BG_CARD}; color: {TEXT_PRIMARY}; }} QMessageBox QLabel {{ color: {TEXT_PRIMARY}; }} QPushButton {{ background-color: {BG_INPUT}; color: {TEXT_PRIMARY}; border: 1px solid {BORDER}; padding: 6px 20px; }}")
        msg.exec_()
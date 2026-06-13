# Calculadora de Ingeniería y Finanzas (PyQt5)

Aplicación de escritorio avanzada con arquitectura modular, diseñada para el análisis financiero y la visualización de datos científicos.

## 🚀 Mejoras Implementadas
- **Arquitectura Multimódulo:** Estructura organizada que separa lógica de negocio, modelos de datos y capa de presentación.
- **Interfaz Premium (UX):** Diseño moderno en modo oscuro con hojas de estilo personalizadas (QSS) y escalado dinámico por DPI.
- **Visualización Científica:** Integración nativa de diagramas termodinámicos (Ciclo P-V) usando el motor de renderizado de `Matplotlib`.
- **Feedback Dinámico:** Animaciones de respuesta visual en el panel de resultados tras cada cálculo.

## 🛠️ Tecnologías
- **Python 3.9+**
- **PyQt5:** Para la interfaz gráfica de usuario.
- **Matplotlib:** Para la generación de gráficos de ingeniería.
- **NumPy:** Para procesamiento de datos científicos.

## Instalación
```bash
python -m venv .venv
# En Windows:
.venv\Scripts\activate
# En Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt

import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. Definición de los Estados (V en m³, P en kPa)
# ==========================================
V1, P1 = 2.066, 150
V2, P2 = 0.540, 750
V3, P3 = 0.413, 750

# ==========================================
# 2. Generación de las trayectorias
# ==========================================
# Proceso 1 -> 2: Compresión politrópica (P * V^1.2 = C)
n = 1.2
C12 = P1 * (V1 ** n)
V_12 = np.linspace(V1, V2, 100)
P_12 = C12 / (V_12 ** n)

# Proceso 2 -> 3: Enfriamiento isobárico (P = constante)
V_23 = np.linspace(V2, V3, 100)
P_23 = np.full_like(V_23, P2)

# Proceso 3 -> 1: Expansión isotérmica (P * V = C)
# (Usamos P1*V1 como constante, que es aproximadamente igual a P3*V3)
C31 = P1 * V1 
V_31 = np.linspace(V3, V1, 100)
P_31 = C31 / V_31

# ==========================================
# 3. Configuración del Gráfico
# ==========================================
plt.figure(figsize=(9, 6))

# Dibujar las líneas de los procesos
plt.plot(V_12, P_12, 'b-', linewidth=2, label=r'1 $\rightarrow$ 2: Compresión Politrópica ($n=1.2$)')
plt.plot(V_23, P_23, 'r-', linewidth=2, label=r'2 $\rightarrow$ 3: Enfriamiento Isobárico')
plt.plot(V_31, P_31, 'g-', linewidth=2, label=r'3 $\rightarrow$ 1: Expansión Isotérmica')

# Marcar los estados exactos con puntos
plt.plot([V1, V2, V3], [P1, P2, P3], 'ko', markersize=6)

# Etiquetas de los estados (con fondo para mejorar legibilidad)
label_box = dict(boxstyle='round,pad=0.3', fc='white', ec='#222222', alpha=0.9)
plt.text(V1 + 0.12, P1 - 25, 'Estado 1\n(2.066 m³, 150 kPa)', fontsize=12, fontweight='bold', va='top', bbox=label_box)
plt.text(V2 + 0.18, P2 + 45, 'Estado 2\n(0.540 m³, 750 kPa)', fontsize=12, fontweight='bold', ha='left', bbox=label_box)
plt.text(V3 - 0.22, P3 + 45, 'Estado 3\n(0.413 m³, 750 kPa)', fontsize=12, fontweight='bold', ha='right', bbox=label_box)

# Añadir flechas indicadoras de dirección
# Flecha 1->2 (Aproximadamente a la mitad del array)
mid_12 = 50
plt.annotate('', xy=(V_12[mid_12], P_12[mid_12]), xytext=(V_12[mid_12-1], P_12[mid_12-1]),
             arrowprops=dict(arrowstyle="->", color='blue', lw=2))

# Flecha 2->3
mid_23 = 50
plt.annotate('', xy=(V_23[mid_23], P_23[mid_23]), xytext=(V_23[mid_23-1], P_23[mid_23-1]),
             arrowprops=dict(arrowstyle="->", color='red', lw=2))

# Flecha 3->1
mid_31 = 50
plt.annotate('', xy=(V_31[mid_31], P_31[mid_31]), xytext=(V_31[mid_31-1], P_31[mid_31-1]),
             arrowprops=dict(arrowstyle="->", color='green', lw=2))

# Formato de los ejes y leyenda
plt.title('Diagrama P-V: Ciclo Termodinámico (Problema 3)', fontsize=14, pad=15)
plt.xlabel('Volumen (m³)', fontsize=12)
plt.ylabel('Presión (kPa)', fontsize=12)
plt.xlim(0.2, 2.4)
plt.ylim(0, 900)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(loc='lower left', fontsize=11)

plt.tight_layout()
plt.show()
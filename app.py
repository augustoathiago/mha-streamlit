import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(
    page_title="Movimento Harmônico Amortecido",
    layout="centered"
)

st.title("Simulação: Movimento Harmônico Amortecido (MHA)")
st.markdown(
    """
    Explore os diferentes regimes de amortecimento ajustando os parâmetros do sistema.
    """
)

# -------------------------
# Sliders
# -------------------------
phi = st.slider("Fase inicial φ (rad)", 0.0, 2*np.pi, 0.5, 0.1)
b = st.slider("Coeficiente de amortecimento b (kg/s)", 0.1, 10.0, 1.0, 0.1)
m = st.slider("Massa m (kg)", 0.1, 10.0, 1.0, 0.1)
y0 = st.slider("Posição inicial y₀ (m)", 0.1, 5.0, 1.0, 0.1)
k = st.slider("Constante elástica k (N/m)", 1.0, 50.0, 10.0, 1.0)

# -------------------------
# Cálculos
# -------------------------
omega0 = np.sqrt(k/m)
gamma = b / (2*m)

if gamma < omega0:
    # Subamortecido (MHA)
    omega = np.sqrt(omega0**2 - gamma**2)
    T = 2*np.pi / omega
    t = np.linspace(0, 10*T, 2000)
    y = y0 * np.exp(-gamma*t) * np.sin(omega*t + phi)

    tipo = "Movimento Harmônico Amortecido (Subamortecido)"
    eq_str = f"y(t) = {y0:.2f} · e^(-{gamma:.2f}t) · sen({omega:.2f}t + {phi:.2f})"

elif math.isclose(gamma, omega0, rel_tol=1e-3):
    # Criticamente amortecido
    t = np.linspace(0, 10, 2000)
    y = y0 * np.exp(-gamma*t)

    omega = 0
    T = np.inf
    tipo = "Movimento Criticamente Amortecido"
    eq_str = f"y(t) = {y0:.2f} · e^(-{gamma:.2f}t)"

else:
    # Superamortecido
    t = np.linspace(0, 10, 2000)
    y = y0 * np.exp(-gamma*t)

    omega = 0
    T = np.inf
    tipo = "Movimento Superamortecido"
    eq_str = f"y(t) = {y0:.2f} · e^(-{gamma:.2f}t)"

# -------------------------
# Gráfico
# -------------------------
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, y, label=tipo)
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Deslocamento y(t) (m)")
ax.set_title(tipo)
ax.grid(True)
ax.legend()

st.pyplot(fig)

# -------------------------
# Informações
# -------------------------
st.subheader("Parâmetros e resultados")
st.markdown(f"""
- **ω₀** = {omega0:.2f} rad/s  
- **γ** = {gamma:.2f} rad/s  
- **ω** = {omega:.2f} rad/s  
- **Período T** = {"∞" if T == np.inf else f"{T:.2f} s"}  
- **Equação:**  
  {eq_str}
""")

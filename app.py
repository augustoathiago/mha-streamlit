import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Oscilador Mecânico",
    layout="centered"
)

# =========================================================
# LOGO
# =========================================================
st.image("logo_maua.png", use_container_width=True)

# =========================================================
# TÍTULO
# =========================================================
st.title("Oscilador Mecânico")

st.markdown(
    """
    **Escolha os valores do coeficiente de amortecimento, da massa e da constante elástica
    para observar os diferentes comportamentos: movimento harmônico simples,
    movimento harmônico subamortecido, movimento criticamente amortecido
    e movimento superamortecido.**
    """
)

# =========================================================
# PARÂMETROS DO SISTEMA
# =========================================================
st.header("Parâmetros do sistema")

col1, col2 = st.columns(2)

with col1:
    b = st.number_input("Coeficiente de amortecimento b (kg/s)", 0.0, 10.0, 1.0, 0.01)
    m = st.number_input("Massa m (kg)", 0.01, 10.0, 1.0, 0.01)
    k = st.number_input("Constante elástica k (N/m)", 0.01, 50.0, 10.0, 0.01)

with col2:
    b = st.slider("b (kg/s)", 0.0, 10.0, float(b), 0.01)
    m = st.slider("m (kg)", 0.01, 10.0, float(m), 0.01)
    k = st.slider("k (N/m)", 0.01, 50.0, float(k), 0.1)

gamma = b / (2 * m)
omega0 = math.sqrt(k / m)

gamma_r = float(f"{gamma:.3g}")
omega0_r = float(f"{omega0:.3g}")

# =========================================================
# GRANDEZAS DERIVADAS
# =========================================================
st.subheader("Grandezas derivadas")

st.latex(r"\gamma = \frac{b}{2m}")
st.latex(r"\omega_0 = \sqrt{\frac{k}{m}}")

st.markdown(f"""
- **Fator de amortecimento γ** = {gamma_r} rad/s  
- **Frequência angular natural ω₀** = {omega0_r} rad/s
""")

# =========================================================
# CLASSIFICAÇÃO
# =========================================================
st.header("Classificação do movimento")

if gamma_r == 0:
    regime = "MHS"
    st.success("Movimento Harmônico Simples (γ = 0)")

elif gamma_r < omega0_r:
    regime = "sub"
    st.info("Movimento Harmônico Subamortecido (γ < ω₀)")

elif gamma_r == omega0_r:
    regime = "critico"
    st.warning("Movimento Criticamente Amortecido (γ = ω₀)")

else:
    regime = "super"
    st.error("Movimento Superamortecido (γ > ω₀)")

# =========================================================
# SOLUÇÕES
# =========================================================
st.header("Equações do movimento")

t = np.linspace(0, 20, 4000)

# ======================= MHS ==============================
if regime == "MHS":
    A = st.slider("Amplitude A (m)", 0.0, 5.0, 1.0, 0.01)
    fase = st.slider("Constante de fase (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = A*np.sin(omega0_r*t + fase)
    v = A*omega0_r*np.cos(omega0_r*t + fase)
    a = -A*omega0_r**2*np.sin(omega0_r*t + fase)

    T = 2*np.pi / omega0_r
    f = 1 / T

    st.subheader("Grandezas temporais (MHS)")
    st.latex(r"T = \frac{2\pi}{\omega_0}")
    st.latex(r"f = \frac{1}{T}")

    st.markdown(f"""
    - **Período T** = {T:.3g} s  
    - **Frequência f** = {f:.3g} Hz
    """)

# =================== SUBAMORTECIDO ========================
elif regime == "sub":
    omega = math.sqrt(omega0_r**2 - gamma_r**2)

    C = st.slider("Constante C (m)", 0.0, 5.0, 1.0, 0.01)
    fase = st.slider("Constante de fase (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = C*np.exp(-gamma_r*t)*np.sin(omega*t + fase)
    v = (
        C*omega*np.exp(-gamma_r*t)*np.cos(omega*t + fase)
        - C*gamma_r*np.exp(-gamma_r*t)*np.sin(omega*t + fase)
    )
    a = (
        C*(gamma_r**2 - omega**2)*np.exp(-gamma_r*t)*np.sin(omega*t + fase)
        - 2*C*gamma_r*omega*np.exp(-gamma_r*t)*np.cos(omega*t + fase)
    )

    T = 2*np.pi / omega
    f = 1 / T

    st.subheader("Grandezas temporais (subamortecido)")
    st.latex(r"\omega = \sqrt{\omega_0^2 - \gamma^2}")
    st.latex(r"T = \frac{2\pi}{\omega}")
    st.latex(r"f = \frac{1}{T}")

    st.markdown(f"""
    - **Frequência angular ω** = {omega:.3g} rad/s  
    - **Pseudoperíodo T** = {T:.3g} s  
    - **Frequência f** = {f:.3g} Hz
    """)

# =================== CRÍTICO ==============================
elif regime == "critico":
    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m/s)", -5.0, 5.0, 0.0, 0.01)

    y = (a0 + b0*t)*np.exp(-gamma_r*t)
    v = (b0 - gamma_r*(a0 + b0*t))*np.exp(-gamma_r*t)
    a = (gamma_r**2*(a0 + b0*t) - 2*gamma_r*b0)*np.exp(-gamma_r*t)

# =================== SUPERAMORTECIDO ======================
else:
    alpha = math.sqrt(gamma_r**2 - omega0_r**2)

    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m)", -5.0, 5.0, 1.0, 0.01)

    y = (
        a0*np.exp((alpha-gamma_r)*t)
        + b0*np.exp(-(alpha+gamma_r)*t)
    )
    v = (
        a0*(alpha-gamma_r)*np.exp((alpha-gamma_r)*t)
        - b0*(alpha+gamma_r)*np.exp(-(alpha+gamma_r)*t)
    )
    a = (
        a0*(alpha-gamma_r)**2*np.exp((alpha-gamma_r)*t)
        + b0*(alpha+gamma_r)**2*np.exp(-(alpha+gamma_r)*t)
    )

# =========================================================
# ENERGIAS
# =========================================================
K = 0.5*m*v**2
U = 0.5*k*y**2
E = K + U

# =========================================================
# GRÁFICOS
# =========================================================
st.header("Gráficos")

fig, axs = plt.subplots(4, 1, figsize=(8, 14), sharex=True)

def plot(ax, data, label):
    ax.plot(t, data, linewidth=2)
    ax.axhline(0, color="black", linewidth=1.2)
    ax.set_ylabel(label)
    ax.grid(True, alpha=0.3)

plot(axs[0], y, "y (m)")
plot(axs[1], v, "v (m/s)")
plot(axs[2], a, "a (m/s²)")

axs[3].plot(t, K, label="Energia Cinética")
axs[3].plot(t, U, label="Energia Potencial")
axs[3].plot(t, E, label="Energia Mecânica Total")
axs[3].set_ylabel("Energia (J)")
axs[3].set_xlabel("Tempo (s)")
axs[3].legend()
axs[3].grid(True, alpha=0.3)

st.pyplot(fig)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Oscilador Mecânico Física II",
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
# PARÂMETROS
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
# SOLUÇÕES TEMPORAIS
# =========================================================
t = np.linspace(0, 20, 4000)

st.header("Equações do movimento")

# ==================== SUBAMORTECIDO ======================
if regime == "sub":
    omega = math.sqrt(omega0_r**2 - gamma_r**2)
    omega_r = float(f"{omega:.3g}")

    C = st.slider("Constante C (m)", 0.0, 5.0, 1.0, 0.01)
    fase = st.slider("Constante de fase (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = C*np.exp(-gamma_r*t)*np.sin(omega_r*t + fase)
    v = (
        C*omega_r*np.exp(-gamma_r*t)*np.cos(omega_r*t + fase)
        - C*gamma_r*np.exp(-gamma_r*t)*np.sin(omega_r*t + fase)
    )

    coef_sin = C*(gamma_r**2 - omega_r**2)
    coef_cos = -2*C*gamma_r*omega_r

    a = (
        coef_sin*np.exp(-gamma_r*t)*np.sin(omega_r*t + fase)
        + coef_cos*np.exp(-gamma_r*t)*np.cos(omega_r*t + fase)
    )

    st.latex(
        rf"y(t)={C:.3g}e^{{-{gamma_r}t}}\sin({omega_r}t+{fase:.3g})"
    )
    st.latex(
        rf"v(t)={C*omega_r:.3g}e^{{-{gamma_r}t}}\cos({omega_r}t+{fase:.3g})"
        rf"-{C*gamma_r:.3g}e^{{-{gamma_r}t}}\sin({omega_r}t+{fase:.3g})"
    )
    st.latex(
        rf"a(t)={coef_sin:.3g}e^{{-{gamma_r}t}}\sin({omega_r}t+{fase:.3g})"
        rf"+{coef_cos:.3g}e^{{-{gamma_r}t}}\cos({omega_r}t+{fase:.3g})"
    )

# ======================= CRÍTICO =========================
elif regime == "critico":
    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m/s)", -5.0, 5.0, 0.0, 0.01)

    y = (a0 + b0*t)*np.exp(-gamma_r*t)
    v = (
        b0*np.exp(-gamma_r*t)
        - gamma_r*a0*np.exp(-gamma_r*t)
        - gamma_r*b0*t*np.exp(-gamma_r*t)
    )
    a = (
        gamma_r**2*a0*np.exp(-gamma_r*t)
        - 2*gamma_r*b0*np.exp(-gamma_r*t)
        + gamma_r**2*b0*t*np.exp(-gamma_r*t)
    )

    st.latex(
        rf"y(t)=({a0:.3g}+{b0:.3g}t)e^{{-{gamma_r}t}}"
    )
    st.latex(
        rf"v(t)={b0:.3g}e^{{-{gamma_r}t}}"
        rf"-{gamma_r*a0:.3g}e^{{-{gamma_r}t}}"
        rf"-{gamma_r*b0:.3g}t e^{{-{gamma_r}t}}"
    )
    st.latex(
        rf"a(t)={gamma_r**2*a0:.3g}e^{{-{gamma_r}t}}"
        rf"-{2*gamma_r*b0:.3g}e^{{-{gamma_r}t}}"
        rf"+{gamma_r**2*b0:.3g}t e^{{-{gamma_r}t}}"
    )

# ==================== SUPERAMORTECIDO ====================
else:
    alpha = math.sqrt(gamma_r**2 - omega0_r**2)
    alpha_r = float(f"{alpha:.3g}")

    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m)", -5.0, 5.0, 1.0, 0.01)

    y = (
        a0*np.exp((alpha_r-gamma_r)*t)
        + b0*np.exp(-(alpha_r+gamma_r)*t)
    )
    v = (
        a0*(alpha_r-gamma_r)*np.exp((alpha_r-gamma_r)*t)
        - b0*(alpha_r+gamma_r)*np.exp(-(alpha_r+gamma_r)*t)
    )
    a = (
        a0*(alpha_r-gamma_r)**2*np.exp((alpha_r-gamma_r)*t)
        + b0*(alpha_r+gamma_r)**2*np.exp(-(alpha_r+gamma_r)*t)
    )

    st.latex(
        rf"y(t)={a0:.3g}e^{{({alpha_r}-{gamma_r})t}}"
        rf"+{b0:.3g}e^{{-({alpha_r}+{gamma_r})t}}"
    )
    st.latex(
        rf"v(t)={a0*(alpha_r-gamma_r):.3g}e^{{({alpha_r}-{gamma_r})t}}"
        rf"-{b0*(alpha_r+gamma_r):.3g}e^{{-({alpha_r}+{gamma_r})t}}"
    )
    st.latex(
        rf"a(t)={a0*(alpha_r-gamma_r)**2:.3g}e^{{({alpha_r}-{gamma_r})t}}"
        rf"+{b0*(alpha_r+gamma_r)**2:.3g}e^{{-({alpha_r}+{gamma_r})t}}"
    )

# =========================================================
# ENERGIAS (sempre com v definido)
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

axs[3].plot(t, K, label="Energia Cinética", color="tab:blue")
axs[3].plot(t, U, label="Energia Potencial", color="tab:orange")
axs[3].plot(t, E, label="Energia Mecânica Total", color="tab:green")
axs[3].set_ylabel("Energia (J)")
axs[3].set_xlabel("Tempo (s)")
axs[3].legend()
axs[3].grid(True, alpha=0.3)

st.pyplot(fig)
``

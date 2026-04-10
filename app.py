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
# LOGO INSTITUCIONAL
# =========================================================
st.image("logo_maua.png", use_container_width=True)

# =========================================================
# TÍTULO E TEXTO INTRODUTÓRIO
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
- **γ = {gamma_r} rad/s**
- **ω₀ = {omega0_r} rad/s**
""")

# =========================================================
# CLASSIFICAÇÃO DO MOVIMENTO
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
st.header("Equações do movimento")

t = np.linspace(0, 20, 4000)

# =========================================================
# SUBAMORTECIDO
# =========================================================
if regime == "sub":
    omega = math.sqrt(omega0_r**2 - gamma_r**2)
    omega_r = float(f"{omega:.3g}")

    C = st.slider("Constante C (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = C*np.exp(-gamma_r*t)*np.sin(omega_r*t + phi)

    v = (
        C*omega_r*np.exp(-gamma_r*t)*np.cos(omega_r*t + phi)
        - C*gamma_r*np.exp(-gamma_r*t)*np.sin(omega_r*t + phi)
    )

    c_sin = C*(gamma_r**2 - omega_r**2)
    c_cos = -2*C*gamma_r*omega_r

    a = (
        c_sin*np.exp(-gamma_r*t)*np.sin(omega_r*t + phi)
        + c_cos*np.exp(-gamma_r*t)*np.cos(omega_r*t + phi)
    )

    st.latex(
        rf"y(t) = {C:.3g}e^{{-{gamma_r}t}}\sin({omega_r}t+{phi:.3g})"
    )
    st.latex(
        rf"v(t) = {C*omega_r:.3g}e^{{-{gamma_r}t}}\cos({omega_r}t+{phi:.3g})"
        rf" - {C*gamma_r:.3g}e^{{-{gamma_r}t}}\sin({omega_r}t+{phi:.3g})"
    )
    st.latex(
        rf"a(t) = {c_sin:.3g}e^{{-{gamma_r}t}}\sin({omega_r}t+{phi:.3g})"
        rf" + {c_cos:.3g}e^{{-{gamma_r}t}}\cos({omega_r}t+{phi:.3g})"
    )

# =========================================================
# MHS
# =========================================================
elif regime == "MHS":
    A = st.slider("Amplitude A (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = A*np.sin(omega0_r*t + phi)
    v = A*omega0_r*np.cos(omega0_r*t + phi)
    a = -A*omega0_r**2*np.sin(omega0_r*t + phi)

    st.latex(
        rf"y(t) = {A:.3g}\sin({omega0_r}t+{phi:.3g})"
    )
    st.latex(
        rf"v(t) = {A*omega0_r:.3g}\cos({omega0_r}t+{phi:.3g})"
    )
    st.latex(
        rf"a(t) = {-A*omega0_r**2:.3g}\sin({omega0_r}t+{phi:.3g})"
    )

# =========================================================
# ENERGIAS
# =========================================================
st.header("Energia do sistema")

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

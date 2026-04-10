import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(
    page_title="Oscilador Mecânico",
    layout="centered"
)

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
# 1. PARÂMETROS FUNDAMENTAIS
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

# três algarismos significativos
gamma_r = float(f"{gamma:.3g}")
omega0_r = float(f"{omega0:.3g}")

st.subheader("Grandezas derivadas")
st.latex(r"\gamma = \frac{b}{2m}")
st.latex(r"\omega_0 = \sqrt{\frac{k}{m}}")

st.markdown(f"""
- **γ = {gamma_r} rad/s**
- **ω₀ = {omega0_r} rad/s**
""")

# =========================================================
# 2. CLASSIFICAÇÃO DO MOVIMENTO
# =========================================================
st.header("Classificação do movimento")

if gamma_r == 0:
    regime = "MHS"
    st.success("γ = 0 → Movimento Harmônico Simples")
elif gamma_r == omega0_r:
    regime = "critico"
    st.warning("γ = ω₀ → Movimento Criticamente Amortecido")
elif gamma_r < omega0_r:
    regime = "sub"
    st.info("γ < ω₀ → Movimento Harmônico Subamortecido")
else:
    regime = "super"
    st.error("γ > ω₀ → Movimento Superamortecido")

# =========================================================
# 3. EQUAÇÕES DO MOVIMENTO
# =========================================================
st.header("Equações do movimento")

t = np.linspace(0, 20, 3000)

# ======================= SUBAMORTECIDO ===================
if regime == "sub":
    omega = math.sqrt(omega0_r**2 - gamma_r**2)
    omega_r = float(f"{omega:.3g}")

    C = st.slider("Constante C (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = C * np.exp(-gamma_r * t) * np.sin(omega_r * t + phi)

    v = C * np.exp(-gamma_r * t) * (
        omega_r * np.cos(omega_r * t + phi)
        - gamma_r * np.sin(omega_r * t + phi)
    )

    a = C * np.exp(-gamma_r * t) * (
        -omega_r**2 * np.sin(omega_r * t + phi)
        - 2 * gamma_r * omega_r * np.cos(omega_r * t + phi)
        + gamma_r**2 * np.sin(omega_r * t + phi)
    )

    st.subheader("Posição")
    st.latex(
        rf"y(t)={C:.3g}e^{{-{gamma_r}t}}\sin({omega_r}t+{phi:.3g})"
    )

    st.subheader("Velocidade")
    st.latex(
        rf"v(t)={C:.3g}e^{{-{gamma_r}t}}"
        rf"\left[{omega_r}\cos({omega_r}t+{phi:.3g})"
        rf"-{gamma_r}\sin({omega_r}t+{phi:.3g})\right]"
    )

    st.subheader("Aceleração")
    st.latex(
        rf"a(t)={C:.3g}e^{{-{gamma_r}t}}"
        rf"\left[-{omega_r**2:.3g}\sin({omega_r}t+{phi:.3g})"
        rf"-2({gamma_r})({omega_r})\cos({omega_r}t+{phi:.3g})"
        rf"+{gamma_r**2:.3g}\sin({omega_r}t+{phi:.3g})\right]"
    )

# ======================= CRÍTICO ==========================
elif regime == "critico":
    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m/s)", -5.0, 5.0, 0.0, 0.01)

    y = (a0 + b0 * t) * np.exp(-gamma_r * t)
    v = np.exp(-gamma_r * t) * (b0 - gamma_r * a0 - gamma_r * b0 * t)
    a = np.exp(-gamma_r * t) * (
        gamma_r**2 * a0 - 2 * gamma_r * b0 + gamma_r**2 * b0 * t
    )

    st.latex(
        rf"y(t)=({a0:.3g}+{b0:.3g}t)e^{{-{gamma_r}t}}"
    )
    st.latex(
        rf"v(t)=e^{{-{gamma_r}t}}\left[{b0:.3g}-{gamma_r}({a0:.3g}+{b0:.3g}t)\right]"
    )
    st.latex(
        rf"a(t)=e^{{-{gamma_r}t}}\left[{gamma_r**2:.3g}{a0:.3g}"
        rf"-2({gamma_r}){b0:.3g}+{gamma_r**2:.3g}{b0:.3g}t\right]"
    )

# ======================= SUPERAMORTECIDO ==================
elif regime == "super":
    alpha = math.sqrt(gamma_r**2 - omega0_r**2)
    alpha_r = float(f"{alpha:.3g}")

    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m)", -5.0, 5.0, 1.0, 0.01)

    y = np.exp(-gamma_r * t) * (
        a0 * np.exp(alpha_r * t) + b0 * np.exp(-alpha_r * t)
    )

    v = np.exp(-gamma_r * t) * (
        a0 * (alpha_r - gamma_r) * np.exp(alpha_r * t)
        - b0 * (alpha_r + gamma_r) * np.exp(-alpha_r * t)
    )

    a = np.exp(-gamma_r * t) * (
        a0 * (alpha_r - gamma_r)**2 * np.exp(alpha_r * t)
        + b0 * (alpha_r + gamma_r)**2 * np.exp(-alpha_r * t)
    )

    st.latex(
        rf"y(t)=e^{{-{gamma_r}t}}\left[{a0:.3g}e^{{{alpha_r}t}}"
        rf"+{b0:.3g}e^{{-{alpha_r}t}}\right]"
    )
    st.latex(
        rf"v(t)=e^{{-{gamma_r}t}}\left[{a0:.3g}({alpha_r}-{gamma_r})e^{{{alpha_r}t}}"
        rf"-{b0:.3g}({alpha_r}+{gamma_r})e^{{-{alpha_r}t}}\right]"
    )
    st.latex(
        rf"a(t)=e^{{-{gamma_r}t}}\left[{a0:.3g}({alpha_r}-{gamma_r})^2e^{{{alpha_r}t}}"
        rf"+{b0:.3g}({alpha_r}+{gamma_r})^2e^{{-{alpha_r}t}}\right]"
    )

# ======================= MHS ===============================
else:
    A = st.slider("Amplitude A (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = A * np.sin(omega0_r * t + phi)
    v = A * omega0_r * np.cos(omega0_r * t + phi)
    a = -A * omega0_r**2 * np.sin(omega0_r * t + phi)

    st.latex(
        rf"y(t)={A:.3g}\sin({omega0_r}t+{phi:.3g})"
    )
    st.latex(
        rf"v(t)={A:.3g}({omega0_r})\cos({omega0_r}t+{phi:.3g})"
    )
    st.latex(
        rf"a(t)=-{A:.3g}({omega0_r})^2\sin({omega0_r}t+{phi:.3g})"
    )

# =========================================================
# 4. GRÁFICOS
# =========================================================
st.header("Gráficos")

fig, axs = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

def plot_central(ax, t, data, ylabel):
    Amax = max(abs(data))
    ax.plot(t, data, linewidth=2)
    ax.axhline(0, color="black", linewidth=1.5)
    ax.set_ylim(-1.1*Amax, 1.1*Amax)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)

plot_central(axs[0], t, y, "y (m)")
plot_central(axs[1], t, v, "v (m/s)")
plot_central(axs[2], t, a, "a (m/s²)")

axs[2].set_xlabel("Tempo (s)")

st.pyplot(fig)

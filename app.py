import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(
    page_title="Oscilações Mecânicas – Amortecimento",
    layout="centered"
)

st.title("Oscilador Massa–Mola com Amortecimento")

# =========================================================
# 1. PARÂMETROS FUNDAMENTAIS
# =========================================================
st.header("Parâmetros do sistema")

st.markdown(
    """
    Você pode **usar os campos numéricos** para definir valores específicos  
    (especialmente úteis para o caso criticamente amortecido)  
    ou os **sliders** para exploração qualitativa.
    """
)

col1, col2 = st.columns(2)

with col1:
    b = st.number_input(
        "Constante de amortecimento b (kg/s)",
        min_value=0.0, value=1.0, step=0.01, format="%.5g"
    )
    m = st.number_input(
        "Massa m (kg)",
        min_value=0.01, value=1.0, step=0.01, format="%.5g"
    )
    k = st.number_input(
        "Constante elástica k (N/m)",
        min_value=0.01, value=10.0, step=0.01, format="%.5g"
    )

with col2:
    b = st.slider("b (kg/s)", 0.0, 10.0, float(b), 0.01)
    m = st.slider("m (kg)", 0.01, 10.0, float(m), 0.01)
    k = st.slider("k (N/m)", 0.01, 50.0, float(k), 0.1)

gamma = b / (2 * m)
omega0 = math.sqrt(k / m)

# Arredondamento para 3 algarismos significativos
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
# 3. EQUAÇÕES E PARÂMETROS
# =========================================================
st.header("Equação do movimento")

t = np.linspace(0, 20, 3000)

if regime == "sub":
    st.latex(r"y(t)=C\,e^{-\gamma t}\sin(\omega t+\phi)")
    omega = math.sqrt(omega0_r**2 - gamma_r**2)
    omega_r = float(f"{omega:.3g}")

    T = 2 * np.pi / omega
    f = 1 / T

    T_r = float(f"{T:.3g}")
    f_r = float(f"{f:.3g}")

    C = st.slider("Constante C (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = C * np.exp(-gamma_r * t) * np.sin(omega_r * t + phi)

    st.markdown(f"""
    - **ω = {omega_r} rad/s**
    - **Pseudoperíodo T = {T_r} s**
    - **Frequência f = {f_r} Hz**
    """)

    st.latex(
        rf"y(t)={C:.3g}e^{{-{gamma_r}t}}\sin({omega_r}t+{phi:.3g})"
    )

elif regime == "critico":
    st.latex(r"y(t)=(a+bt)e^{-\gamma t}")

    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m/s)", -5.0, 5.0, 0.0, 0.01)

    y = (a0 + b0 * t) * np.exp(-gamma_r * t)

    st.latex(
        rf"y(t)=({a0:.3g}+{b0:.3g}t)e^{{-{gamma_r}t}}"
    )

elif regime == "super":
    st.latex(
        r"y(t)=e^{-\gamma t}\left[a e^{\sqrt{\gamma^2-\omega_0^2}\,t}"
        r"+b e^{-\sqrt{\gamma^2-\omega_0^2}\,t}\right]"
    )

    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m)", -5.0, 5.0, 1.0, 0.01)

    alpha = math.sqrt(gamma_r**2 - omega0_r**2)
    alpha_r = float(f"{alpha:.3g}")

    y = np.exp(-gamma_r * t) * (
        a0 * np.exp(alpha_r * t) + b0 * np.exp(-alpha_r * t)
    )

    st.latex(
        rf"y(t)=e^{{-{gamma_r}t}}\left[{a0:.3g}e^{{{alpha_r}t}}"
        rf"+{b0:.3g}e^{{-{alpha_r}t}}\right]"
    )

else:  # MHS
    st.latex(r"y(t)=A\sin(\omega_0 t+\phi)")

    A = st.slider("Amplitude A (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    T = 2 * np.pi / omega0_r
    f = 1 / T

    T_r = float(f"{T:.3g}")
    f_r = float(f"{f:.3g}")

    y = A * np.sin(omega0_r * t + phi)

    st.markdown(f"""
    - **Período T = {T_r} s**
    - **Frequência f = {f_r} Hz**
    """)

    st.latex(
        rf"y(t)={A:.3g}\sin({omega0_r}t+{phi:.3g})"
    )

# =========================================================
# 4. GRÁFICOS (CENTRALIZADOS E COM EIXOS DESTACADOS)
# =========================================================
v = np.gradient(y, t)
a = np.gradient(v, t)

fig, axs = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

def plot_central(ax, t, data, ylabel):
    Amax = max(abs(data))
    ax.plot(t, data, linewidth=2)
    ax.axhline(0, color="black", linewidth=1.5)
    ax.set_ylim(-Amax*1.1, Amax*1.1)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)

plot_central(axs[0], t, y, "y (m)")
plot_central(axs[1], t, v, "v (m/s)")
plot_central(axs[2], t, a, "a (m/s²)")

axs[2].set_xlabel("Tempo (s)")

st.pyplot(fig)

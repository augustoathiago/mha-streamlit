import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(
    page_title="Oscilações Mecânicas",
    layout="centered"
)

st.title("Oscilador Mecânico")

# =========================================================
# 1. PARÂMETROS FUNDAMENTAIS
# =========================================================
st.header("Parâmetros do sistema")

col1, col2 = st.columns(2)

with col1:
    b = st.number_input("Constante de amortecimento b (kg/s)", 0.0, 10.0, 1.0, 0.01)
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

if regime == "sub":
    omega = math.sqrt(omega0_r**2 - gamma_r**2)
    omega_r = float(f"{omega:.3g}")

    T = 2 * np.pi / omega
    f = 1 / T

    C = st.slider("Constante C (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = C * np.exp(-gamma_r * t) * np.sin(omega_r * t + phi)

    st.latex(r"y(t)=C\,e^{-\gamma t}\sin(\omega t+\phi)")
    st.latex(
        rf"y(t)={C:.3g}e^{{-{gamma_r}t}}\sin({omega_r}t+{phi:.3g})"
    )

    st.subheader("Velocidade")
    st.latex(
        rf"v(t)={C:.3g}e^{{-{gamma_r}t}}"
        rf"\left[{omega_r}\cos({omega_r}t+{phi:.3g})"
        rf"-{gamma_r}\sin({omega_r}t+{phi:.3g})\right]"
    )

elif regime == "critico":
    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m/s)", -5.0, 5.0, 0.0, 0.01)

    y = (a0 + b0 * t) * np.exp(-gamma_r * t)

    st.latex(r"y(t)=(a+bt)e^{-\gamma t}")
    st.latex(
        rf"y(t)=({a0:.3g}+{b0:.3g}t)e^{{-{gamma_r}t}}"
    )

elif regime == "super":
    alpha = math.sqrt(gamma_r**2 - omega0_r**2)
    alpha_r = float(f"{alpha:.3g}")

    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m)", -5.0, 5.0, 1.0, 0.01)

    y = np.exp(-gamma_r * t) * (
        a0 * np.exp(alpha_r * t) + b0 * np.exp(-alpha_r * t)
    )

    st.latex(
        r"y(t)=e^{-\gamma t}\left[a e^{\sqrt{\gamma^2-\omega_0^2}\,t}"
        r"+b e^{-\sqrt{\gamma^2-\omega_0^2}\,t}\right]"
    )
    st.latex(
        rf"y(t)=e^{{-{gamma_r}t}}\left[{a0:.3g}e^{{{alpha_r}t}}"
        rf"+{b0:.3g}e^{{-{alpha_r}t}}\right]"
    )

else:  # MHS
    A = st.slider("Amplitude A (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = A * np.sin(omega0_r * t + phi)

    st.latex(r"y(t)=A\sin(\omega_0 t+\phi)")
    st.latex(
        rf"y(t)={A:.3g}\sin({omega0_r}t+{phi:.3g})"
    )

    st.subheader("Velocidade")
    st.latex(
        rf"v(t)={A:.3g}({omega0_r})\cos({omega0_r}t+{phi:.3g})"
    )

# =========================================================
# 4. VELOCIDADE E ACELERAÇÃO (SEM ARTEFATO)
# =========================================================
v = np.gradient(y, t)
a = -2 * gamma_r * v - (omega0_r**2) * y

st.subheader("Aceleração")
st.latex(
    rf"a(t)=-2({gamma_r})\,v(t)-({omega0_r})^2y(t)"
)

# =========================================================
# 5. GRÁFICOS CENTRALIZADOS
# =========================================================
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

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import time

st.set_page_config(
    page_title="Oscilações Mecânicas – Amortecimento",
    layout="centered"
)

st.title("Oscilador Massa–Mola com Amortecimento")

# =========================================================
# 1. PARÂMETROS FUNDAMENTAIS
# =========================================================
st.header("Parâmetros do sistema")

b = st.slider("Constante de amortecimento b (kg/s)", 0.0, 10.0, 1.0, 0.1)
m = st.slider("Massa m (kg)", 0.1, 10.0, 1.0, 0.1)
k = st.slider("Constante elástica k (N/m)", 0.1, 50.0, 10.0, 0.5)

gamma = b / (2 * m)
omega0 = math.sqrt(k / m)

st.subheader("Grandezas derivadas")
st.latex(r"\gamma = \frac{b}{2m}")
st.latex(r"\omega_0 = \sqrt{\frac{k}{m}}")

st.markdown(f"""
- **γ (fator de amortecimento)** = {gamma:.3f} rad/s  
- **ω₀ (frequência angular natural)** = {omega0:.3f} rad/s
""")

# =========================================================
# 2. CLASSIFICAÇÃO DO MOVIMENTO
# =========================================================
st.header("Classificação do movimento")

epsilon = 1e-3

if gamma == 0:
    regime = "MHS"
    st.success("γ = 0 → Movimento Harmônico Simples")
elif abs(gamma - omega0) < epsilon:
    regime = "critico"
    st.warning("γ = ω₀ → Movimento Criticamente Amortecido")
elif gamma < omega0:
    regime = "sub"
    st.info("γ < ω₀ → Movimento Harmônico Subamortecido")
else:
    regime = "super"
    st.error("γ > ω₀ → Movimento Superamortecido")

# =========================================================
# 3. EQUAÇÕES E PARÂMETROS DO REGIME
# =========================================================
st.header("Equações do movimento")

t = np.linspace(0, 20, 2000)

if regime == "sub":
    st.latex(r"y(t) = C e^{-\gamma t}\,\sin(\omega t + \phi)")
    omega = math.sqrt(omega0**2 - gamma**2)
    T = 2 * np.pi / omega
    f = 1 / T

    C = st.slider("Constante C (m)", 0.1, 5.0, 1.0, 0.1)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.1)

    y = C * np.exp(-gamma * t) * np.sin(omega * t + phi)

    st.markdown(f"""
    - **ω = {omega:.3f} rad/s**
    - **Pseudoperíodo T = {T:.3f} s**
    - **Frequência f = {f:.3f} Hz**
    """)

    st.latex(
        rf"y(t) = {C:.2f} e^{{-{gamma:.2f}t}} \sin({omega:.2f}t + {phi:.2f})"
    )

elif regime == "critico":
    st.latex(r"y(t) = (a + bt)e^{-\gamma t}")

    a = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.1)
    b_lin = st.slider("Constante b (m/s)", -5.0, 5.0, 0.0, 0.1)

    y = (a + b_lin * t) * np.exp(-gamma * t)

    st.latex(
        rf"y(t) = ({a:.2f} + {b_lin:.2f}t)e^{{-{gamma:.2f}t}}"
    )

elif regime == "super":
    st.latex(
        r"y(t)=e^{-\gamma t}\left[a e^{\sqrt{\gamma^2-\omega_0^2}t}"
        r"+ b e^{-\sqrt{\gamma^2-\omega_0^2}t}\right]"
    )

    a = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.1)
    b_sup = st.slider("Constante b (m)", -5.0, 5.0, 1.0, 0.1)

    alfa = math.sqrt(gamma**2 - omega0**2)
    y = np.exp(-gamma * t) * (a * np.exp(alfa * t) + b_sup * np.exp(-alfa * t))

    st.latex(
        rf"y(t)=e^{{-{gamma:.2f}t}}\left[{a:.2f}e^{{{alfa:.2f}t}}"
        rf"+{b_sup:.2f}e^{{-{alfa:.2f}t}}\right]"
    )

else:  # MHS
    st.latex(r"y(t) = A \sin(\omega_0 t + \phi)")

    A = st.slider("Amplitude A (m)", 0.1, 5.0, 1.0, 0.1)
    phi = st.slider("Fase φ (rad)", 0.0, 2*np.pi, 0.0, 0.1)

    T = 2 * np.pi / omega0
    f = 1 / T

    y = A * np.sin(omega0 * t + phi)

    st.markdown(f"""
    - **Período T = {T:.3f} s**
    - **Frequência f = {f:.3f} Hz**
    """)

    st.latex(
        rf"y(t) = {A:.2f}\sin({omega0:.2f}t + {phi:.2f})"
    )

# =========================================================
# 4. VELOCIDADE E ACELERAÇÃO
# =========================================================
v = np.gradient(y, t)
a = np.gradient(v, t)

st.header("Gráficos")

fig, ax = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

ax[0].plot(t, y)
ax[0].set_ylabel("y (m)")
ax[0].grid()

ax[1].plot(t, v)
ax[1].set_ylabel("v (m/s)")
ax[1].grid()

ax[2].plot(t, a)
ax[2].set_ylabel("a (m/s²)")
ax[2].set_xlabel("Tempo (s)")
ax[2].grid()

st.pyplot(fig)

# =========================================================
# 5. ANIMAÇÃO MASSA–MOLA
# =========================================================
st.header("Animação do sistema massa–mola")

if st.button("Reproduzir animação"):
    anim_placeholder = st.empty()

    for yi in y[::30]:
        fig2, ax2 = plt.subplots(figsize=(6, 2))
        ax2.plot([0, yi], [0, 0], linewidth=4)
        ax2.scatter(yi, 0, s=400)
        ax2.set_xlim(-5, 5)
        ax2.set_ylim(-1, 1)
        ax2.axis("off")
        anim_placeholder.pyplot(fig2)
        time.sleep(0.05)

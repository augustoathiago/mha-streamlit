import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# =========================================================
# CONFIGURAÇÃO
# =========================================================
st.set_page_config(page_title="Oscilador Mecânico", layout="centered")
st.image("logo_maua.png", use_container_width=True)

st.title("Oscilador Mecânico Física II")

st.markdown(
    """
    **Escolha os valores do coeficiente de amortecimento, da massa e da constante elástica
    para observar os diferentes comportamentos do oscilador mecânico.**
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

gamma = b / (2*m)
omega0 = math.sqrt(k/m)

gamma_r = float(f"{gamma:.3g}")
omega0_r = float(f"{omega0:.3g}")

# =========================================================
# GRANDEZAS
# =========================================================
st.subheader("Grandezas características")

st.markdown(f"""
- **Fator de amortecimento γ** = {gamma_r} rad/s  
- **Frequência angular natural ω₀** = {omega0_r} rad/s
""")

# =========================================================
# CLASSIFICAÇÃO
# =========================================================
st.header("Classificação do movimento")

if gamma_r == 0:
    regime = "mhs"
    st.success("γ = 0 → Movimento harmônico simples")

elif gamma_r < omega0_r:
    regime = "sub"
    st.info("γ < ω₀ → Movimento harmônico subamortecido")

elif gamma_r == omega0_r:
    regime = "critico"
    st.warning("γ = ω₀ → Movimento criticamente amortecido")

else:
    regime = "super"
    st.error("γ > ω₀ → Movimento superamortecido")

# =========================================================
# TEMPO
# =========================================================
t = np.linspace(0, 20, 4000)

st.header("Equações do movimento")

# =========================================================
# MHS
# =========================================================
if regime == "mhs":

    A = st.slider("Amplitude A (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Constante de fase (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = A*np.sin(omega0_r*t + phi)
    v = A*omega0_r*np.cos(omega0_r*t + phi)
    a = -A*(omega0_r**2)*np.sin(omega0_r*t + phi)

    w2 = omega0_r**2
    Aw = A*omega0_r

    st.latex(r"y(t)=A\sin(\omega_0t+\phi)")
    st.latex(rf"y(t)={A:.3g}\sin({omega0_r}t+{phi:.3g})")

    st.latex(r"v(t)=A\omega_0\cos(\omega_0t+\phi)")
    st.latex(rf"v(t)={Aw:.4f}\cos({omega0_r}t+{phi:.3g})")

    st.latex(r"a(t)=-A\omega_0^2\sin(\omega_0t+\phi)")
    st.latex(rf"a(t)=-{A*w2:.4f}\sin({omega0_r}t+{phi:.3g})")

# =========================================================
# SUBAMORTECIDO
# =========================================================
elif regime == "sub":

    omega = math.sqrt(omega0_r**2 - gamma_r**2)

    C = st.slider("Constante C (m)", 0.0, 5.0, 1.0, 0.01)
    phi = st.slider("Constante de fase (rad)", 0.0, 2*np.pi, 0.0, 0.01)

    y = C*np.exp(-gamma_r*t)*np.sin(omega*t+phi)
    v = C*np.exp(-gamma_r*t)*(omega*np.cos(omega*t+phi)-gamma_r*np.sin(omega*t+phi))
    a = C*np.exp(-gamma_r*t)*((gamma_r**2-omega**2)*np.sin(omega*t+phi)-2*gamma_r*omega*np.cos(omega*t+phi))

    A1 = gamma_r**2 - omega**2
    A2 = 2*gamma_r*omega

    st.latex(r"y(t)=Ce^{-\gamma t}\sin(\omega t+\phi)")
    st.latex(rf"y(t)={C:.3g}e^{{-{gamma_r}t}}\sin({omega:.4f}t+{phi:.3g})")

    st.latex(r"v(t)=Ce^{-\gamma t}[\omega\cos(\omega t+\phi)-\gamma\sin(\omega t+\phi)]")
    st.latex(rf"v(t)={C:.3g}e^{{-{gamma_r}t}}[{omega:.4f}\cos({omega:.4f}t+{phi:.3g})-{gamma_r}\sin({omega:.4f}t+{phi:.3g})]")

    st.latex(r"a(t)=Ce^{-\gamma t}[(\gamma^2-\omega^2)\sin(\omega t+\phi)-2\gamma\omega\cos(\omega t+\phi)]")
    st.latex(rf"a(t)={C:.3g}e^{{-{gamma_r}t}}[{A1:.4f}\sin({omega:.4f}t+{phi:.3g})-{A2:.4f}\cos({omega:.4f}t+{phi:.3g})]")

# =========================================================
# CRÍTICO
# =========================================================
elif regime == "critico":

    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m/s)", -5.0, 5.0, 0.0, 0.01)

    y = (a0+b0*t)*np.exp(-gamma_r*t)
    v = (b0-gamma_r*(a0+b0*t))*np.exp(-gamma_r*t)
    a = (gamma_r**2*(a0+b0*t)-2*gamma_r*b0)*np.exp(-gamma_r*t)

    g2 = gamma_r**2

    st.latex(r"y(t)=(a+bt)e^{-\gamma t}")
    st.latex(rf"y(t)=({a0:.3g}+{b0:.3g}t)e^{{-{gamma_r}t}}")

    st.latex(r"v(t)=[b-\gamma(a+bt)]e^{-\gamma t}")
    st.latex(rf"v(t)=({b0:.3g}-{gamma_r}({a0:.3g}+{b0:.3g}t))e^{{-{gamma_r}t}}")

    st.latex(r"a(t)=[\gamma^2(a+bt)-2\gamma b]e^{-\gamma t}")
    st.latex(rf"a(t)=({g2:.4f}({a0:.3g}+{b0:.3g}t)-{2*gamma_r*b0:.4f})e^{{-{gamma_r}t}}")

# =========================================================
# SUPERAMORTECIDO
# =========================================================
else:

    alpha = math.sqrt(gamma_r**2 - omega0_r**2)

    a0 = st.slider("Constante a (m)", -5.0, 5.0, 1.0, 0.01)
    b0 = st.slider("Constante b (m)", -5.0, 5.0, 1.0, 0.01)

    y = a0*np.exp((alpha-gamma_r)*t)+b0*np.exp(-(alpha+gamma_r)*t)
    v = a0*(alpha-gamma_r)*np.exp((alpha-gamma_r)*t)-b0*(alpha+gamma_r)*np.exp(-(alpha+gamma_r)*t)
    a = a0*(alpha-gamma_r)**2*np.exp((alpha-gamma_r)*t)+b0*(alpha+gamma_r)**2*np.exp(-(alpha+gamma_r)*t)

    r1 = alpha - gamma_r
    r2 = alpha + gamma_r

    st.latex(r"y(t)=ae^{(\alpha-\gamma)t}+be^{-(\alpha+\gamma)t}")
    st.latex(rf"y(t)={a0:.3g}e^{{{r1:.4f}t}}+{b0:.3g}e^{{-{r2:.4f}t}}")

    st.latex(r"v(t)=a(\alpha-\gamma)e^{(\alpha-\gamma)t}-b(\alpha+\gamma)e^{-(\alpha+\gamma)t}")
    st.latex(rf"v(t)={a0*r1:.4f}e^{{{r1:.4f}t}}-{b0*r2:.4f}e^{{-{r2:.4f}t}}")

    st.latex(r"a(t)=a(\alpha-\gamma)^2e^{(\alpha-\gamma)t}+b(\alpha+\gamma)^2e^{-(\alpha+\gamma)t}")
    st.latex(rf"a(t)={a0*r1*r1:.4f}e^{{{r1:.4f}t}}+{b0*r2*r2:.4f}e^{{-{r2:.4f}t}}")

# =========================================================
# ENERGIA
# =========================================================
K = 0.5*m*v**2
U = 0.5*k*y**2
E = K + U

# =========================================================
# GRÁFICOS
# =========================================================
st.header("Gráficos")

fig, axs = plt.subplots(4, 1, figsize=(8, 14), sharex=True)

axs[0].plot(t, y)
axs[1].plot(t, v)
axs[2].plot(t, a)
axs[3].plot(t, K, label="Energia cinética")
axs[3].plot(t, U, label="Energia potencial")
axs[3].plot(t, E, label="Energia mecânica total")

axs[3].legend()

for ax, label in zip(
    axs,
    ["y (m)", "v (m/s)", "a (m/s²)", "Energia (J)"]
):
    ax.set_ylabel(label)
    ax.grid(True)

axs[3].set_xlabel("Tempo (s)")
st.pyplot(fig)

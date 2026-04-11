import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Página
# --------------------------------------------------
st.set_page_config(
    page_title="Oscilador Mecânico – Física II",
    layout="wide"
)

# --------------------------------------------------
# Funções auxiliares
# --------------------------------------------------
def sig(x):
    if abs(x) < 1e-12:
        return 0.0
    return float(f"{x:.3g}")

def fs(x):
    return f"{sig(x)}"

# --------------------------------------------------
# Cabeçalho
# --------------------------------------------------
col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo_maua.png", use_container_width=True)
with col2:
    st.title("Oscilador Mecânico – Física II")
    st.markdown(
        "Escolha os valores do **coeficiente de amortecimento**, da **massa** e da "
        "**constante elástica** para observar os diferentes comportamentos do "
        "oscilador mecânico."
    )

st.divider()

# --------------------------------------------------
# Parâmetros iniciais
# --------------------------------------------------
st.header("Parâmetros iniciais do sistema")

c1, c2, c3 = st.columns(3)

with c1:
    b = st.slider("Coeficiente de amortecimento b (kg/s)", 0.0, 10.0, 0.0, 0.01)
    b = st.number_input("Valor numérico de b", 0.0, 10.0, b, 0.001)

with c2:
    m = st.slider("Massa m (kg)", 0.01, 10.0, 1.0, 0.01)
    m = st.number_input("Valor numérico de m", 0.01, 10.0, m, 0.001)

with c3:
    k = st.slider("Constante elástica k (N/m)", 0.01, 10.0, 1.0, 0.01)
    k = st.number_input("Valor numérico de k", 0.01, 10.0, k, 0.001)

# valores reais (não arredondados)
b_r, m_r, k_r = b, m, k

# --------------------------------------------------
# Parâmetros físicos
# --------------------------------------------------
gamma_r = b_r / (2 * m_r)
omega0_r = np.sqrt(k_r / m_r)

gamma = sig(gamma_r)
omega0 = sig(omega0_r)

# --------------------------------------------------
# Classificação do movimento (CORRIGIDA)
# --------------------------------------------------
st.divider()
st.header("Classificação do movimento")

st.latex(r"\gamma = \frac{b}{2m}")
st.latex(r"\omega_0 = \sqrt{\frac{k}{m}}")

st.markdown(
f"""
- **Coeficiente de amortecimento (γ)** = {gamma} rad/s  
- **Frequência angular natural (ω₀)** = {omega0} rad/s  
"""
)

if b_r == 0:
    movimento = "Movimento harmônico simples"
    cmp = "="
elif gamma_r < omega0_r:
    movimento = "Movimento harmônico subamortecido"
    cmp = "<"
elif np.isclose(gamma_r, omega0_r, rtol=1e-6):
    movimento = "Movimento criticamente amortecido"
    cmp = "="
else:
    movimento = "Movimento superamortecido"
    cmp = ">"

st.markdown(f"### γ {cmp} ω₀ → **{movimento}**")

# --------------------------------------------------
# Vetor temporal
# --------------------------------------------------
t = np.linspace(0, 20, 4000)

# --------------------------------------------------
# EQUAÇÕES DO MOVIMENTO
# --------------------------------------------------
st.divider()
st.header("Equações do movimento")

# ===================== MHS =====================
if movimento == "Movimento harmônico simples":
    A = st.slider("Amplitude A (m)", 0.01, 10.0, 1.0)
    phi = st.slider("Constante de fase φ (rad)", 0.0, 2*np.pi, 0.0)

    x = A * np.sin(omega0_r*t + phi)
    v = A * omega0_r * np.cos(omega0_r*t + phi)
    a = -A * omega0_r**2 * np.sin(omega0_r*t + phi)

    st.latex(r"x(t)=A\sin(\omega_0 t+\phi)")
    st.latex(fr"x(t)={fs(A)}\sin({fs(omega0)}t+{fs(phi)})")

    st.latex(r"v(t)=A\omega_0\cos(\omega_0 t+\phi)")
    st.latex(fr"v(t)={fs(A*omega0_r)}\cos({fs(omega0)}t+{fs(phi)})")

    st.latex(r"a(t)=-A\omega_0^2\sin(\omega_0 t+\phi)")
    st.latex(fr"a(t)={fs(-A*omega0_r**2)}\sin({fs(omega0)}t+{fs(phi)})")

# ================= SUBAMORTECIDO =================
elif movimento == "Movimento harmônico subamortecido":
    C = st.slider("Constante C (m)", 0.01, 10.0, 1.0)
    phi = st.slider("Constante de fase φ (rad)", 0.0, 2*np.pi, 0.0)

    omega_r = np.sqrt(omega0_r**2 - gamma_r**2)
    omega = sig(omega_r)

    x = C*np.exp(-gamma_r*t)*np.sin(omega_r*t + phi)
    v = C*np.exp(-gamma_r*t)*(
        omega_r*np.cos(omega_r*t + phi)
        - gamma_r*np.sin(omega_r*t + phi)
    )
    a = C*np.exp(-gamma_r*t)*(
        -(omega_r**2 + gamma_r**2)*np.sin(omega_r*t + phi)
        - 2*gamma_r*omega_r*np.cos(omega_r*t + phi)
    )

    st.latex(r"x(t)=Ce^{-\gamma t}\sin(\omega t+\phi)")
    st.latex(fr"x(t)={fs(C)}e^{{-{fs(gamma)}t}}\sin({fs(omega)}t+{fs(phi)})")

    st.latex(
        r"v(t)=Ce^{-\gamma t}[\omega\cos(\omega t+\phi)-\gamma\sin(\omega t+\phi)]"
    )
    st.latex(
        fr"v(t)={fs(C)}e^{{-{fs(gamma)}t}}"
        fr"[{fs(omega)}\cos({fs(omega)}t+{fs(phi)})"
        fr"-{fs(gamma)}\sin({fs(omega)}t+{fs(phi)})]"
    )

    st.latex(
        r"a(t)=Ce^{-\gamma t}"
        r"[-(\omega^2+\gamma^2)\sin(\omega t+\phi)-2\gamma\omega\cos(\omega t+\phi)]"
    )
    st.latex(
        fr"a(t)={fs(C)}e^{{-{fs(gamma)}t}}"
        fr"[{-fs(omega_r**2 + gamma_r**2)}\sin({fs(omega)}t+{fs(phi)})"
        fr"-{fs(2*gamma_r*omega_r)}\cos({fs(omega)}t+{fs(phi)})]"
    )

# ================= CRÍTICO =================
elif movimento == "Movimento criticamente amortecido":
    a0 = st.slider("Constante a (m)", 0.01, 10.0, 1.0)
    B = st.slider("Constante B (m/s)", -10.0, 10.0, 0.0)

    x = (a0 + B*t)*np.exp(-gamma_r*t)
    v = np.exp(-gamma_r*t)*(B - gamma_r*(a0 + B*t))
    a = np.exp(-gamma_r*t)*(gamma_r**2*(a0 + B*t) - 2*gamma_r*B)

# ================= SUPERAMORTECIDO =================
else:
    a0 = st.slider("Constante a (m)", 0.01, 10.0, 1.0)
    B = st.slider("Constante B (m)", 0.01, 10.0, 1.0)

    alpha = np.sqrt(gamma_r**2 - omega0_r**2)

    x = np.exp(-gamma_r*t)*(a0*np.exp(alpha*t) + B*np.exp(-alpha*t))
    v = np.exp(-gamma_r*t)*(
        (alpha - gamma_r)*a0*np.exp(alpha*t)
        -(alpha + gamma_r)*B*np.exp(-alpha*t)
    )
    a = np.exp(-gamma_r*t)*(
        (alpha - gamma_r)**2*a0*np.exp(alpha*t)
        +(alpha + gamma_r)**2*B*np.exp(-alpha*t)
    )

# --------------------------------------------------
# Gráficos
# --------------------------------------------------
st.divider()
st.header("Gráficos")

Ec = 0.5*m_r*v**2
Ep = 0.5*k_r*x**2
Em = Ec + Ep

fig, axs = plt.subplots(4, 1, figsize=(9, 13), sharex=True)

axs[0].plot(t, x)
axs[0].set_ylabel("x (m)")
axs[1].plot(t, v)
axs[1].set_ylabel("v (m/s)")
axs[2].plot(t, a)
axs[2].set_ylabel("a (m/s²)")
axs[3].plot(t, Ep, label="Potencial")
axs[3].plot(t, Ec, label="Cinética")
axs[3].plot(t, Em, label="Mecânica total")
axs[3].legend()
axs[3].set_ylabel("Energia (J)")

for ax in axs:
    ax.axhline(0, color="black", linewidth=2)
    ax.axvline(0, color="black", linewidth=2)
    ax.grid(True)

axs[-1].set_xlabel("Tempo (s)")
st.pyplot(fig)

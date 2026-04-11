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
        "Escolha os valores do **coeficiente de amortecimento**, da **massa** "
        "e da **constante elástica**."
    )

st.divider()

# --------------------------------------------------
# Parâmetros iniciais
# --------------------------------------------------
st.header("Parâmetros iniciais do sistema")

c1, c2, c3 = st.columns(3)

with c1:
    b = st.slider("Coeficiente de amortecimento b (kg/s)", 0.0, 10.0, 0.0, 0.01)

with c2:
    m = st.slider("Massa m (kg)", 0.01, 10.0, 1.0, 0.01)

with c3:
    k = st.slider("Constante elástica k (N/m)", 0.01, 10.0, 1.0, 0.01)

# valores reais
gamma_r = b / (2 * m)
omega0_r = np.sqrt(k / m)

# valores exibidos (3 AS)
gamma = sig(gamma_r)
omega0 = sig(omega0_r)

# --------------------------------------------------
# Classificação do movimento
# --------------------------------------------------
st.divider()
st.header("Classificação do movimento")

st.markdown(
f"""
- **Coeficiente de amortecimento (γ)** = {gamma} rad/s  
- **Frequência angular natural (ω₀)** = {omega0} rad/s  
"""
)

if b == 0:
    movimento = "Movimento harmônico simples"
    cmp = "="
elif gamma_r < omega0_r:
    movimento = "Movimento harmônico subamortecido"
    cmp = "<"
elif np.isclose(gamma_r, omega0_r, rtol=1e-8):
    movimento = "Movimento criticamente amortecido"
    cmp = "="
else:
    movimento = "Movimento superamortecido"
    cmp = ">"

st.markdown(f"### γ {cmp} ω₀ → **{movimento}**")

# --------------------------------------------------
# Tempo
# --------------------------------------------------
t = np.linspace(0, 20, 4000)

# --------------------------------------------------
# Equações do movimento
# --------------------------------------------------
st.divider()
st.header("Equações do movimento")

# ================= MHS =================
if movimento == "Movimento harmônico simples":
    A = st.slider("Amplitude A (m)", 0.01, 10.0, 1.0)
    phi = st.slider("Constante de fase φ (rad)", 0.0, 2*np.pi, 0.0)

    x = A*np.sin(omega0_r*t + phi)
    v = A*omega0_r*np.cos(omega0_r*t + phi)
    a = -A*omega0_r**2*np.sin(omega0_r*t + phi)

    st.latex(fr"x(t)={fs(A)}\sin({fs(omega0)}t+{fs(phi)})")
    st.latex(fr"v(t)={fs(A*omega0_r)}\cos({fs(omega0)}t+{fs(phi)})")
    st.latex(fr"a(t)={fs(-A*omega0_r**2)}\sin({fs(omega0)}t+{fs(phi)})")

# ============ SUBAMORTECIDO ============
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

    st.latex(fr"x(t)={fs(C)}e^{{-{fs(gamma)}t}}\sin({fs(omega)}t+{fs(phi)})")
    st.latex(
        fr"v(t)={fs(C)}e^{{-{fs(gamma)}t}}"
        fr"[{fs(omega)}\cos({fs(omega)}t+{fs(phi)})"
        fr"-{fs(gamma)}\sin({fs(omega)}t+{fs(phi)})]"
    )
    st.latex(
        fr"a(t)={fs(C)}e^{{-{fs(gamma)}t}}"
        fr"[{-fs(omega_r**2+gamma_r**2)}\sin({fs(omega)}t+{fs(phi)})"
        fr"-{fs(2*gamma_r*omega_r)}\cos({fs(omega)}t+{fs(phi)})]"
    )

# ========== CRITICAMENTE AMORTECIDO ==========
elif movimento == "Movimento criticamente amortecido":
    a0 = st.slider("Constante a (m)", 0.01, 10.0, 1.0)
    B = st.slider("Constante B (m/s)", -10.0, 10.0, 0.0)

    x = (a0+B*t)*np.exp(-gamma_r*t)
    v = np.exp(-gamma_r*t)*(B - gamma_r*(a0+B*t))
    a = np.exp(-gamma_r*t)*(gamma_r**2*(a0+B*t) - 2*gamma_r*B)

    st.latex(fr"x(t)=({fs(a0)}+{fs(B)}t)e^{{-{fs(gamma)}t}}")
    st.latex(
        fr"v(t)=e^{{-{fs(gamma)}t}}"
        fr"[{fs(B)}-{fs(gamma)}({fs(a0)}+{fs(B)}t)]"
    )
    st.latex(
        fr"a(t)=e^{{-{fs(gamma)}t}}"
        fr"[{fs(gamma_r**2)}({fs(a0)}+{fs(B)}t)-{fs(2*gamma_r*B)}]"
    )

# ============ SUPERAMORTECIDO ============
else:
    a0 = st.slider("Constante a (m)", 0.01, 10.0, 1.0)
    B = st.slider("Constante B (m)", 0.01, 10.0, 1.0)

    alpha = np.sqrt(gamma_r**2 - omega0_r**2)

    x = np.exp(-gamma_r*t)*(a0*np.exp(alpha*t)+B*np.exp(-alpha*t))
    v = np.exp(-gamma_r*t)*(
        (alpha-gamma_r)*a0*np.exp(alpha*t)
        -(alpha+gamma_r)*B*np.exp(-alpha*t)
    )
    a = np.exp(-gamma_r*t)*(
        (alpha-gamma_r)**2*a0*np.exp(alpha*t)
        +(alpha+gamma_r)**2*B*np.exp(-alpha*t)
    )

    st.latex(
        fr"x(t)=e^{{-{fs(gamma)}t}}"
        fr"[{fs(a0)}e^{{\sqrt{{{fs(gamma)}^2-{fs(omega0)}^2}}t}}"
        fr"+{fs(B)}e^{{-\sqrt{{{fs(gamma)}^2-{fs(omega0)}^2}}t}}]"
    )
    st.latex(
        fr"v(t)=e^{{-{fs(gamma)}t}}[\cdots]"
    )
    st.latex(
        fr"a(t)=e^{{-{fs(gamma)}t}}[\cdots]"
    )

# --------------------------------------------------
# Gráficos
# --------------------------------------------------
st.divider()
st.header("Gráficos")

Ec = 0.5*m*v**2
Ep = 0.5*k*x**2
Em = Ec + Ep

fig, axs = plt.subplots(4, 1, figsize=(9, 13), sharex=True)

axs[0].plot(t, x)
axs[1].plot(t, v)
axs[2].plot(t, a)
axs[3].plot(t, Ep, label="Potencial")
axs[3].plot(t, Ec, label="Cinética")
axs[3].plot(t, Em, label="Mecânica total")
axs[3].legend()

for ax in axs:
    ax.axhline(0, color="black", linewidth=2)
    ax.axvline(0, color="black", linewidth=2)
    ax.grid(True)

axs[-1].set_xlabel("Tempo (s)")
st.pyplot(fig)

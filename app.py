import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Configuração da página
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
        "e da **constante elástica** para observar os diferentes comportamentos "
        "do oscilador mecânico."
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

b, m, k = sig(b), sig(m), sig(k)

# --------------------------------------------------
# Classificação do movimento
# --------------------------------------------------
st.divider()
st.header("Classificação do movimento")

gamma = sig(b / (2 * m))
omega0 = sig(np.sqrt(k / m))

st.latex(r"\gamma = \frac{b}{2m}")
st.latex(r"\omega_0 = \sqrt{\frac{k}{m}}")

st.markdown(
f"""
- **Coeficiente de amortecimento (γ)** = {gamma} rad/s  
- **Frequência angular natural (ω₀)** = {omega0} rad/s  
"""
)

# ⚠️ ORDEM CORRETA – MHS SOMENTE SE γ = 0
if gamma == 0:
    movimento = "Movimento harmônico simples"
    cmp = "="
elif gamma < omega0:
    movimento = "Movimento harmônico subamortecido"
    cmp = "<"
elif gamma == omega0:
    movimento = "Movimento criticamente amortecido"
    cmp = "="
else:
    movimento = "Movimento superamortecido"
    cmp = ">"

st.markdown(f"### γ {cmp} ω₀  →  **{movimento}**")

# --------------------------------------------------
# Cálculos
# --------------------------------------------------
if movimento in [
    "Movimento harmônico simples",
    "Movimento harmônico subamortecido"
]:
    st.divider()
    st.header("Cálculos")

if movimento == "Movimento harmônico simples":
    T = sig(2 * np.pi / omega0)
    f = sig(1 / T)

    st.latex(r"T=\frac{2\pi}{\omega_0}")
    st.latex(r"f=\frac{1}{T}")

    st.markdown(
        f"""
- **Período (T)** = {T} s  
- **Frequência (f)** = {f} Hz  
"""
    )

elif movimento == "Movimento harmônico subamortecido":
    omega = sig(np.sqrt(omega0**2 - gamma**2))
    T = sig(2 * np.pi / omega)
    f = sig(1 / T)

    st.latex(r"\omega=\sqrt{\omega_0^2-\gamma^2}")
    st.latex(r"T=\frac{2\pi}{\omega}")
    st.latex(r"f=\frac{1}{T}")

    st.markdown(
        f"""
- **Frequência angular amortecida (ω)** = {omega} rad/s  
- **Pseudoperíodo (T)** = {T} s  
- **Frequência (f)** = {f} Hz  
"""
    )

# --------------------------------------------------
# Equações do movimento
# --------------------------------------------------
st.divider()
st.header("Equações do movimento")

t = np.linspace(0, 20, 3000)

# ===================== MHS =====================
if movimento == "Movimento harmônico simples":
    A = st.slider("Amplitude A (m)", 0.01, 10.0, 1.0)
    phi = st.slider("Constante de fase φ (rad)", 0.0, 2*np.pi, 0.0)

    x = A * np.sin(omega0*t + phi)
    v = A * omega0 * np.cos(omega0*t + phi)
    a = -A * omega0**2 * np.sin(omega0*t + phi)

    st.latex(r"x(t)=A\sin(\omega_0 t+\phi)")
    st.latex(fr"x(t)={fs(A)}\sin({fs(omega0)}t+{fs(phi)})")

    st.latex(r"v(t)=A\omega_0\cos(\omega_0 t+\phi)")
    st.latex(fr"v(t)={fs(A*omega0)}\cos({fs(omega0)}t+{fs(phi)})")

    st.latex(r"a(t)=-A\omega_0^2\sin(\omega_0 t+\phi)")
    st.latex(fr"a(t)={fs(-A*omega0**2)}\sin({fs(omega0)}t+{fs(phi)})")

# ================= SUBAMORTECIDO =================
elif movimento == "Movimento harmônico subamortecido":
    C = st.slider("Constante C (m)", 0.01, 10.0, 1.0)
    phi = st.slider("Constante de fase φ (rad)", 0.0, 2*np.pi, 0.0)

    omega = sig(np.sqrt(omega0**2 - gamma**2))

    x = C*np.exp(-gamma*t)*np.sin(omega*t+phi)
    v = C*np.exp(-gamma*t)*(
        omega*np.cos(omega*t+phi)
        -gamma*np.sin(omega*t+phi)
    )
    a = C*np.exp(-gamma*t)*(
        -(omega**2+gamma**2)*np.sin(omega*t+phi)
        -2*gamma*omega*np.cos(omega*t+phi)
    )

    st.latex(r"x(t)=Ce^{-\gamma t}\sin(\omega t+\phi)")
    st.latex(fr"x(t)={fs(C)}e^{{-{fs(gamma)}t}}\sin({fs(omega)}t+{fs(phi)})")

    st.latex(
        r"v(t)=Ce^{-\gamma t}"
        r"[\omega\cos(\omega t+\phi)-\gamma\sin(\omega t+\phi)]"
    )
    st.latex(
        fr"v(t)={fs(C)}e^{{-{fs(gamma)}t}}"
        fr"[{fs(omega)}\cos({fs(omega)}t+{fs(phi)})"
        fr"-{fs(gamma)}\sin({fs(omega)}t+{fs(phi)})]"
    )

    st.latex(
        r"a(t)=Ce^{-\gamma t}"
        r"[-(\omega^2+\gamma^2)\sin(\omega t+\phi)"
        r"-2\gamma\omega\cos(\omega t+\phi)]"
    )
    st.latex(
        fr"a(t)={fs(C)}e^{{-{fs(gamma)}t}}"
        fr"[{-fs(omega**2+gamma**2)}\sin({fs(omega)}t+{fs(phi)})"
        fr"-{fs(2*gamma*omega)}\cos({fs(omega)}t+{fs(phi)})]"
    )

# ============== CRITICAMENTE AMORTECIDO ==============
elif movimento == "Movimento criticamente amortecido":
    a0 = st.slider("Constante a (m)", 0.01, 10.0, 1.0)
    B = st.slider("Constante B (m/s)", -10.0, 10.0, 0.0)

    x = (a0 + B*t)*np.exp(-gamma*t)
    v = np.exp(-gamma*t)*(B - gamma*(a0 + B*t))
    a = np.exp(-gamma*t)*(gamma**2*(a0 + B*t) - 2*gamma*B)

    st.latex(r"x(t)=(a+Bt)e^{-\gamma t}")
    st.latex(fr"x(t)=({fs(a0)}+{fs(B)}t)e^{{-{fs(gamma)}t}}")

    st.latex(r"v(t)=e^{-\gamma t}[B-\gamma(a+Bt)]")
    st.latex(
        fr"v(t)=e^{{-{fs(gamma)}t}}"
        fr"[{fs(B)}-{fs(gamma)}({fs(a0)}+{fs(B)}t)]"
    )

    st.latex(r"a(t)=e^{-\gamma t}[\gamma^2(a+Bt)-2\gamma B]")
    st.latex(
        fr"a(t)=e^{{-{fs(gamma)}t}}"
        fr"[{fs(gamma**2)}({fs(a0)}+{fs(B)}t)-{fs(2*gamma*B)}]"
    )

# ================= SUPERAMORTECIDO =================
else:
    a0 = st.slider("Constante a (m)", 0.01, 10.0, 1.0)
    B = st.slider("Constante B (m)", 0.01, 10.0, 1.0)

    alpha = np.sqrt(gamma**2 - omega0**2)  # uso interno

    x = np.exp(-gamma*t)*(a0*np.exp(alpha*t) + B*np.exp(-alpha*t))
    v = np.exp(-gamma*t)*(
        (alpha-gamma)*a0*np.exp(alpha*t)
        -(alpha+gamma)*B*np.exp(-alpha*t)
    )
    a = np.exp(-gamma*t)*(
        (alpha-gamma)**2*a0*np.exp(alpha*t)
        +(alpha+gamma)**2*B*np.exp(-alpha*t)
    )

    st.latex(
        r"x(t)=e^{-\gamma t}"
        r"[ae^{\sqrt{\gamma^2-\omega_0^2}t}"
        r"+Be^{-\sqrt{\gamma^2-\omega_0^2}t}]"
    )

    st.latex(
        r"v(t)=e^{-\gamma t}"
        r"[(\sqrt{\gamma^2-\omega_0^2}-\gamma)ae^{\sqrt{\gamma^2-\omega_0^2}t}"
        r"-(\sqrt{\gamma^2-\omega_0^2}+\gamma)Be^{-\sqrt{\gamma^2-\omega_0^2}t}]"
    )

    st.latex(
        r"a(t)=e^{-\gamma t}"
        r"[(\sqrt{\gamma^2-\omega_0^2}-\gamma)^2ae^{\sqrt{\gamma^2-\omega_0^2}t}"
        r"+(\sqrt{\gamma^2-\omega_0^2}+\gamma)^2Be^{-\sqrt{\gamma^2-\omega_0^2}t}]"
    )

# --------------------------------------------------
# Gráficos
# --------------------------------------------------
st.divider()
st.header("Gráficos")

Ec = 0.5 * m * v**2
Ep = 0.5 * k * x**2
Em = Ec + Ep

fig, axs = plt.subplots(4, 1, figsize=(9, 13), sharex=True)

axs[0].plot(t, x)
axs[0].set_ylabel("x (m)")

axs[1].plot(t, v)
axs[1].set_ylabel("v (m/s)")

axs[2].plot(t, a)
axs[2].set_ylabel("a (m/s²)")

axs[3].plot(t, Ep, label="Energia potencial", color="blue")
axs[3].plot(t, Ec, label="Energia cinética", color="red")
axs[3].plot(t, Em, label="Energia mecânica total", color="green")
axs[3].set_ylabel("Energia (J)")
axs[3].legend()

for ax in axs:
    ax.axhline(0, color="black", linewidth=2)
    ax.axvline(0, color="black", linewidth=2)
    ax.grid(True)

axs[-1].set_xlabel("Tempo (s)")

st.pyplot(fig)

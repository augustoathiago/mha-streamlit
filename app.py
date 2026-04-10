import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Configurações iniciais
# --------------------------------------------------
st.set_page_config(page_title="Oscilador Mecânico – Física II", layout="wide")

def sig(x):
    if x == 0:
        return 0.0
    return float(f"{x:.3g}")

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

col1, col2, col3 = st.columns(3)

with col1:
    b = st.slider("Coeficiente de amortecimento b (kg/s)", 0.0, 10.0, 0.0, 0.01)
    b = st.number_input("Valor numérico de b", 0.0, 10.0, b, 0.001)

with col2:
    m = st.slider("Massa m (kg)", 0.01, 10.0, 0.01, 0.01)
    m = st.number_input("Valor numérico de m", 0.01, 10.0, m, 0.001)

with col3:
    k = st.slider("Constante elástica k (N/m)", 0.01, 10.0, 0.01, 0.01)
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

if gamma == 0:
    movimento = "Movimento harmônico simples"
    comparacao = "="
elif gamma < omega0:
    movimento = "Movimento harmônico subamortecido"
    comparacao = "<"
elif gamma == omega0:
    movimento = "Movimento criticamente amortecido"
    comparacao = "="
else:
    movimento = "Movimento superamortecido"
    comparacao = ">"

st.markdown(
    f"### γ {comparacao} ω₀  →  **{movimento}**"
)

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
    st.latex(r"T = \frac{2\pi}{\omega_0}")
    st.latex(r"f = \frac{1}{T}")
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
    st.latex(r"\omega = \sqrt{\omega_0^2 - \gamma^2}")
    st.latex(r"T = \frac{2\pi}{\omega}")
    st.latex(r"f = \frac{1}{T}")
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

# ---------------- MHS -----------------
if movimento == "Movimento harmônico simples":
    A = st.slider("Amplitude A (m)", 0.01, 10.0, 1.0)
    phi = st.slider("Constante de fase φ (rad)", 0.0, 2*np.pi, 0.0)

    x = A * np.sin(omega0 * t + phi)
    v = A * omega0 * np.cos(omega0 * t + phi)
    a = -A * omega0**2 * np.sin(omega0 * t + phi)

    st.latex(r"x(t)=A\sin(\omega_0 t+\phi)")
    st.latex(fr"x(t)={sig(A)}\sin({omega0}t+{sig(phi)})")

    st.latex(r"v(t)=A\omega_0\cos(\omega_0 t+\phi)")
    st.latex(fr"v(t)={sig(A*omega0)}\cos({omega0}t+{sig(phi)})")

    st.latex(r"a(t)=-A\omega_0^2\sin(\omega_0 t+\phi)")
    st.latex(fr"a(t)={sig(-A*omega0**2)}\sin({omega0}t+{sig(phi)})")

# ------------- Subamortecido -------------
elif movimento == "Movimento harmônico subamortecido":
    C = st.slider("Constante C (m)", 0.01, 10.0, 1.0)
    phi = st.slider("Constante de fase φ (rad)", 0.0, 2*np.pi, 0.0)
    omega = sig(np.sqrt(omega0**2 - gamma**2))

    x = C * np.exp(-gamma*t) * np.sin(omega*t + phi)
    v = np.gradient(x, t)
    a = np.gradient(v, t)

    st.latex(r"x(t)=Ce^{-\gamma t}\sin(\omega t+\phi)")
    st.latex(fr"x(t)={sig(C)}e^{{-{gamma}t}}\sin({omega}t+{sig(phi)})")

    st.latex(r"v(t)=\frac{dx}{dt}")
    st.latex(r"a(t)=\frac{d^2x}{dt^2}")

# ----------- Criticamente amortecido -----------
elif movimento == "Movimento criticamente amortecido":
    a0 = st.slider("Constante a (m)", 0.01, 10.0, 1.0)
    B = st.slider("Constante B (m/s)", -10.0, 10.0, 0.0)

    x = (a0 + B*t) * np.exp(-gamma*t)
    v = np.gradient(x, t)
    a = np.gradient(v, t)

    st.latex(r"x(t)=(a+Bt)e^{-\gamma t}")
    st.latex(fr"x(t)=({sig(a0)}+{sig(B)}t)e^{{-{gamma}t}}")

    st.latex(r"v(t)=\frac{dx}{dt}")
    st.latex(r"a(t)=\frac{d^2x}{dt^2}")

# ----------- Superamortecido -----------
else:
    a0 = st.slider("Constante a (m)", 0.01, 10.0, 1.0)
    B = st.slider("Constante B (m)", 0.01, 10.0, 1.0)
    alpha = sig(np.sqrt(gamma**2 - omega0**2))

    x = np.exp(-gamma*t)*(a0*np.exp(alpha*t)+B*np.exp(-alpha*t))
    v = np.gradient(x, t)
    a = np.gradient(v, t)

    st.latex(
        r"x(t)=e^{-\gamma t}[ae^{\sqrt{\gamma^2-\omega_0^2}t}"
        r"+be^{-\sqrt{\gamma^2-\omega_0^2}t}]"
    )
    st.latex(
        fr"x(t)=e^{{-{gamma}t}}[{sig(a0)}e^{{{alpha}t}}+{sig(B)}e^{{-{alpha}t}}]"
    )

    st.latex(r"v(t)=\frac{dx}{dt}")
    st.latex(r"a(t)=\frac{d^2x}{dt^2}")

# --------------------------------------------------
# Gráficos
# --------------------------------------------------
st.divider()
st.header("Gráficos")

E_c = 0.5 * m * v**2
E_p = 0.5 * k * x**2
E_m = E_c + E_p

fig, axs = plt.subplots(4, 1, figsize=(9, 13), sharex=True)

axs[0].plot(t, x)
axs[0].set_ylabel("x (m)")

axs[1].plot(t, v)
axs[1].set_ylabel("v (m/s)")

axs[2].plot(t, a)
axs[2].set_ylabel("a (m/s²)")

axs[3].plot(t, E_p, label="Energia potencial", color="blue")
axs[3].plot(t, E_c, label="Energia cinética", color="red")
axs[3].plot(t, E_m, label="Energia mecânica total", color="green")
axs[3].set_ylabel("Energia (J)")
axs[3].legend()

for ax in axs:
    ax.axhline(0, color="black", linewidth=2)
    ax.axvline(0, color="black", linewidth=2)
    ax.grid(True)

axs[-1].set_xlabel("Tempo (s)")
st.pyplot(fig)

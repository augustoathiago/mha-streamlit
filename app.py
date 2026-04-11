import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# Configurações gerais
# -----------------------------
st.set_page_config(
    page_title="Oscilador Mecânico Física II",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def fmt3(x):
    """Formata com 3 algarismos significativos."""
    try:
        if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
            return "—"
        return f"{x:.3g}"
    except Exception:
        return str(x)

def sgn_comp(a, b, tol=None):
    """Retorna '<', '>' ou '=' com tolerância numérica."""
    if tol is None:
        tol = 1e-9 * max(1.0, abs(a), abs(b))
    if abs(a - b) <= tol:
        return "="
    return "<" if a < b else ">"

def style_axes(ax):
    """Eixos pretos destacados para não confundir com grade."""
    for spine in ax.spines.values():
        spine.set_color("black")
        spine.set_linewidth(1.6)
    ax.tick_params(axis="both", colors="black", width=1.2)
    ax.xaxis.label.set_color("black")
    ax.yaxis.label.set_color("black")
    ax.title.set_color("black")
    ax.grid(True, alpha=0.25)

def synced_slider_number(label, key, min_value, max_value, value, step, unit="", help_text=None):
    """
    Cria slider + number_input sincronizados via session_state.
    Retorna o valor atual (float).
    """
    slider_key = f"{key}_slider"
    number_key = f"{key}_number"

    if key not in st.session_state:
        st.session_state[key] = float(value)
    if slider_key not in st.session_state:
        st.session_state[slider_key] = float(value)
    if number_key not in st.session_state:
        st.session_state[number_key] = float(value)

    def from_slider():
        st.session_state[key] = float(st.session_state[slider_key])
        st.session_state[number_key] = float(st.session_state[key])

    def from_number():
        v = float(st.session_state[number_key])
        # Clamp por segurança
        v = min(max(v, min_value), max_value)
        st.session_state[key] = v
        st.session_state[slider_key] = float(st.session_state[key])

    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        st.slider(
            f"{label} {f'({unit})' if unit else ''}",
            min_value=float(min_value),
            max_value=float(max_value),
            value=float(st.session_state[key]),
            step=float(step),
            format="%.3g",
            key=slider_key,
            on_change=from_slider,
            help=help_text,
        )
    with c2:
        st.number_input(
            "Digite",
            min_value=float(min_value),
            max_value=float(max_value),
            value=float(st.session_state[key]),
            step=float(step),
            format="%.3g",
            key=number_key,
            on_change=from_number,
            label_visibility="visible",
        )

    return float(st.session_state[key])

# -----------------------------
# Cabeçalho: logo + título + descrição
# -----------------------------
col_logo, col_title = st.columns([1, 5], vertical_alignment="center")
with col_logo:
    try:
        st.image("logo_maua.png", use_container_width=True)
    except Exception:
        st.warning("Arquivo 'logo_maua.png' não encontrado na raiz do repositório.")
with col_title:
    st.title("Oscilador Mecânico Física II")
    st.write(
        "Escolha os valores do coeficiente de amortecimento, da massa e da constante elástica "
        "para observar os diferentes comportamentos do oscilador mecânico"
    )

st.divider()

# -----------------------------
# Seção: Parâmetros iniciais do sistema
# -----------------------------
st.header("Parâmetros iniciais do sistema")

b = synced_slider_number(
    "Coeficiente de amortecimento b",
    key="b",
    min_value=0.0, max_value=10.0,
    value=0.0, step=0.001,
    unit="kg/s",
)

m = synced_slider_number(
    "Massa m",
    key="m",
    min_value=0.01, max_value=10.0,
    value=0.01, step=0.001,
    unit="kg",
)

k = synced_slider_number(
    "Constante elástica k",
    key="k",
    min_value=0.01, max_value=10.0,
    value=0.01, step=0.001,
    unit="N/m",
)

st.divider()

# -----------------------------
# Seção: Classificação do movimento
# -----------------------------
st.header("Classificação do movimento")

if m <= 0 or k < 0:
    st.error("A massa deve ser positiva e a constante elástica não pode ser negativa.")
    st.stop()

gamma = b / (2.0 * m)   # s^-1 (rad/s por convenção aqui)
omega0 = np.sqrt(k / m) # rad/s

comp = sgn_comp(gamma, omega0)

# Caso especial: gamma = 0 (b=0)
if abs(gamma) < 1e-15:
    classificacao = "movimento harmônico simples"
else:
    if comp == "<":
        classificacao = "movimento harmônico subamortecido"
    elif comp == "=":
        classificacao = "movimento criticamente amortecido"
    else:
        classificacao = "movimento superamortecido"

c1, c2, c3 = st.columns([1.4, 1.4, 2.2])
with c1:
    st.subheader("Fator de amortecimento")
    st.latex(r"\gamma = \frac{b}{2m}")
    st.write(f"**γ = {fmt3(gamma)} rad/s**")
with c2:
    st.subheader("Frequência natural")
    st.latex(r"\omega_0 = \sqrt{\frac{k}{m}}")
    st.write(f"**ω₀ = {fmt3(omega0)} rad/s**")
with c3:
    st.subheader("Comparação e tipo de movimento")
    st.write(f"**γ {comp} ω₀**")
    st.success(f"**{classificacao}**")

# Mostrar também a comparação com valores
st.markdown("### Valores calculados")
st.write(
    f"- b = **{fmt3(b)} kg/s**, m = **{fmt3(m)} kg**, k = **{fmt3(k)} N/m**\n"
    f"- γ = **{fmt3(gamma)} rad/s**\n"
    f"- ω₀ = **{fmt3(omega0)} rad/s**\n"
    f"- Comparação: **{fmt3(gamma)} {comp} {fmt3(omega0)}**"
)

st.divider()

# -----------------------------
# Seção: Cálculos (somente quando aplicável)
# -----------------------------
omega = None
T = None
f = None

if classificacao == "movimento harmônico simples":
    st.header("Cálculos")
    st.latex(r"T = \frac{2\pi}{\omega_0}")
    T = 2 * np.pi / omega0
    st.write(f"**Período:** T = **{fmt3(T)} s**")

    st.latex(r"f = \frac{1}{T}")
    f = 1.0 / T
    st.write(f"**Frequência:** f = **{fmt3(f)} Hz**")

elif classificacao == "movimento harmônico subamortecido":
    st.header("Cálculos")
    st.latex(r"\omega = \sqrt{\omega_0^2 - \gamma^2}")
    inside = omega0**2 - gamma**2
    if inside <= 0:
        st.warning("A expressão ω² = ω₀² − γ² ficou não-positiva por arredondamento numérico. Ajuste b, m, k.")
        omega = np.nan
    else:
        omega = np.sqrt(inside)

    st.write(f"**Frequência angular amortecida:** ω = **{fmt3(omega)} rad/s**")

    st.latex(r"T = \frac{2\pi}{\omega}")
    T = 2 * np.pi / omega if omega and np.isfinite(omega) and omega > 0 else np.nan
    st.write(f"**Pseudoperíodo:** T = **{fmt3(T)} s**")

    st.latex(r"f = \frac{1}{T}")
    f = 1.0 / T if T and np.isfinite(T) and T > 0 else np.nan
    st.write(f"**Frequência:** f = **{fmt3(f)} Hz**")

# Nos casos crítico e superamortecido: não exibe seção Cálculos
st.divider()

# -----------------------------
# Seção: Equações do movimento
# -----------------------------
st.header("Equações do movimento")

# Domínio para sliders dos parâmetros das soluções
LEN_MIN, LEN_MAX = -10.0, 10.0
AMP_MIN, AMP_MAX = 0.0, 10.0
PHI_MIN, PHI_MAX = -2*np.pi, 2*np.pi

# Valores iniciais
if "A" not in st.session_state: st.session_state["A"] = 1.0
if "C" not in st.session_state: st.session_state["C"] = 1.0
if "phi" not in st.session_state: st.session_state["phi"] = 0.0
if "a_const" not in st.session_state: st.session_state["a_const"] = 1.0
if "B_const" not in st.session_state: st.session_state["B_const"] = 0.0

def slider_param(label, key, minv, maxv, val, step, unit=""):
    v = st.slider(
        f"{label} {f'({unit})' if unit else ''}",
        min_value=float(minv),
        max_value=float(maxv),
        value=float(st.session_state.get(key, val)),
        step=float(step),
        format="%.3g",
        key=key
    )
    return float(v)

# Define funções x(t), v(t), a(t) conforme o caso
def build_functions():
    global omega
    if classificacao == "movimento harmônico simples":
        A = slider_param("Amplitude A", "A", AMP_MIN, AMP_MAX, 1.0, 0.001, "m")
        phi = slider_param("Constante de fase φ", "phi", PHI_MIN, PHI_MAX, 0.0, 0.001, "rad")

        def x(t): return A*np.sin(omega0*t + phi)
        def v(t): return A*omega0*np.cos(omega0*t + phi)
        def a(t): return -A*(omega0**2)*np.sin(omega0*t + phi)

        eq_letters = {
            "x": r"x(t) = A\sin(\omega_0 t + \varphi)",
            "v": r"v(t) = A\omega_0\cos(\omega_0 t + \varphi)",
            "a": r"a(t) = -A\omega_0^2\sin(\omega_0 t + \varphi)",
        }
        eq_numbers = {
            "x": rf"x(t) = {fmt3(A)}\sin\!\left({fmt3(omega0)}\,t + {fmt3(phi)}\right)",
            "v": rf"v(t) = {fmt3(A)}\cdot {fmt3(omega0)}\cos\!\left({fmt3(omega0)}\,t + {fmt3(phi)}\right)",
            "a": rf"a(t) = -{fmt3(A)}\cdot ({fmt3(omega0)})^2\sin\!\left({fmt3(omega0)}\,t + {fmt3(phi)}\right)",
        }
        params = {"A": A, "phi": phi}

    elif classificacao == "movimento harmônico subamortecido":
        # garante omega
        inside = omega0**2 - gamma**2
        omega_loc = np.sqrt(inside) if inside > 0 else np.nan
        omega = omega_loc

        C = slider_param("Constante C", "C", AMP_MIN, AMP_MAX, 1.0, 0.001, "m")
        phi = slider_param("Constante de fase φ", "phi", PHI_MIN, PHI_MAX, 0.0, 0.001, "rad")

        def x(t):
            return C*np.exp(-gamma*t)*np.sin(omega*t + phi)

        def v(t):
            s = np.sin(omega*t + phi)
            c = np.cos(omega*t + phi)
            return C*np.exp(-gamma*t)*(omega*c - gamma*s)

        def a(t):
            s = np.sin(omega*t + phi)
            c = np.cos(omega*t + phi)
            return C*np.exp(-gamma*t)*((gamma**2 - omega**2)*s - 2*gamma*omega*c)

        eq_letters = {
            "x": r"x(t) = C\,e^{-\gamma t}\,\sin(\omega t+\varphi)",
            "v": r"v(t) = C\,e^{-\gamma t}\left(\omega\cos(\omega t+\varphi)-\gamma\sin(\omega t+\varphi)\right)",
            "a": r"a(t) = C\,e^{-\gamma t}\left((\gamma^2-\omega^2)\sin(\omega t+\varphi)-2\gamma\omega\cos(\omega t+\varphi)\right)",
        }
        eq_numbers = {
            "x": rf"x(t) = {fmt3(C)}\,e^{{-{fmt3(gamma)}t}}\,\sin\!\left({fmt3(omega)}\,t + {fmt3(phi)}\right)",
            "v": rf"v(t) = {fmt3(C)}\,e^{{-{fmt3(gamma)}t}}\left({fmt3(omega)}\cos({fmt3(omega)}t+{fmt3(phi)})-{fmt3(gamma)}\sin({fmt3(omega)}t+{fmt3(phi)})\right)",
            "a": rf"a(t) = {fmt3(C)}\,e^{{-{fmt3(gamma)}t}}\left((({fmt3(gamma)})^2-({fmt3(omega)})^2)\sin({fmt3(omega)}t+{fmt3(phi)})-2\cdot{fmt3(gamma)}\cdot{fmt3(omega)}\cos({fmt3(omega)}t+{fmt3(phi)})\right)",
        }
        params = {"C": C, "phi": phi, "omega": omega}

    elif classificacao == "movimento criticamente amortecido":
        a0 = slider_param("Constante a", "a_const", LEN_MIN, LEN_MAX, 1.0, 0.001, "m")
        B = slider_param("Constante B", "B_const", LEN_MIN, LEN_MAX, 0.0, 0.001, "m/s")

        def x(t): return (a0 + B*t)*np.exp(-gamma*t)
        def v(t): return np.exp(-gamma*t)*(B - gamma*(a0 + B*t))
        def a(t): return np.exp(-gamma*t)*(gamma**2*(a0 + B*t) - 2*gamma*B)

        eq_letters = {
            "x": r"x(t) = (a + Bt)\,e^{-\gamma t}",
            "v": r"v(t) = e^{-\gamma t}\left(B-\gamma(a+Bt)\right)",
            "a": r"a(t) = e^{-\gamma t}\left(\gamma^2(a+Bt)-2\gamma B\right)",
        }
        eq_numbers = {
            "x": rf"x(t) = \left({fmt3(a0)} + {fmt3(B)}t\right)e^{{-{fmt3(gamma)}t}}",
            "v": rf"v(t) = e^{{-{fmt3(gamma)}t}}\left({fmt3(B)}-{fmt3(gamma)}({fmt3(a0)}+{fmt3(B)}t)\right)",
            "a": rf"a(t) = e^{{-{fmt3(gamma)}t}}\left(({fmt3(gamma)})^2({fmt3(a0)}+{fmt3(B)}t)-2\cdot{fmt3(gamma)}\cdot{fmt3(B)}\right)",
        }
        params = {"a": a0, "B": B}

    else:  # superamortecido
        alpha = np.sqrt(max(0.0, gamma**2 - omega0**2))
        a0 = slider_param("Constante a", "a_const", LEN_MIN, LEN_MAX, 1.0, 0.001, "m")
        B = slider_param("Constante B", "B_const", LEN_MIN, LEN_MAX, 0.0, 0.001, "m")

        lam1 = -gamma + alpha
        lam2 = -gamma - alpha

        def x(t): return a0*np.exp(lam1*t) + B*np.exp(lam2*t)
        def v(t): return a0*lam1*np.exp(lam1*t) + B*lam2*np.exp(lam2*t)
        def a(t): return a0*(lam1**2)*np.exp(lam1*t) + B*(lam2**2)*np.exp(lam2*t)

        # Fórmula na forma que você descreveu (equivalente)
        eq_letters = {
            "x": r"x(t)=e^{-\gamma t}\left(a\,e^{\alpha t}+B\,e^{-\alpha t}\right),\quad \alpha=\sqrt{\gamma^2-\omega_0^2}",
            "v": r"v(t)=\frac{dx}{dt}",
            "a": r"a(t)=\frac{d^2x}{dt^2}",
        }
        eq_numbers = {
            "x": rf"x(t)= {fmt3(a0)}\,e^{{({fmt3(lam1)})t}} + {fmt3(B)}\,e^{{({fmt3(lam2)})t}}",
            "v": rf"v(t)= {fmt3(a0)}({fmt3(lam1)})e^{{({fmt3(lam1)})t}} + {fmt3(B)}({fmt3(lam2)})e^{{({fmt3(lam2)})t}}",
            "a": rf"a(t)= {fmt3(a0)}({fmt3(lam1)})^2 e^{{({fmt3(lam1)})t}} + {fmt3(B)}({fmt3(lam2)})^2 e^{{({fmt3(lam2)})t}}",
        }
        params = {"a": a0, "B": B, "alpha": alpha}

    return x, v, a, eq_letters, eq_numbers, params

x_fun, v_fun, a_fun, eqL, eqN, params = build_functions()

st.markdown("### Equações (forma simbólica)")
st.latex(eqL["x"])
st.latex(eqL["v"])
st.latex(eqL["a"])

st.markdown("### Equações (com valores numéricos)")
st.latex(eqN["x"])
st.latex(eqN["v"])
st.latex(eqN["a"])

st.divider()

# -----------------------------
# Seção: Gráficos
# -----------------------------
st.header("Gráficos")

# Define um tempo máximo automático para visualizar bem
def choose_tmax():
    # Se existe período utilizável, mostre ~5 ciclos
    if T is not None and np.isfinite(T) and T > 0:
        return float(min(50.0, max(2.0, 5.0*T)))
    # Caso amortecido: escala ~ (decaimento)
    if gamma is not None and np.isfinite(gamma) and gamma > 0:
        return float(min(50.0, max(2.0, 10.0/gamma)))
    return 10.0

tmax = choose_tmax()
N = 1400
t = np.linspace(0.0, tmax, N)

# Calcula sinais
x = x_fun(t)
v = v_fun(t)
acc = a_fun(t)

# Energias
Ep = 0.5 * k * (x**2)
Ec = 0.5 * m * (v**2)
Em = Ep + Ec

# Layout de gráficos: 2 linhas (posição/velocidade), (aceleração/energia)
fig1, ax1 = plt.subplots(figsize=(8, 3.6))
ax1.plot(t, x, linewidth=2.2)
ax1.set_title("Posição x(t)")
ax1.set_xlabel("Tempo (s)")
ax1.set_ylabel("x (m)")
ax1.set_xlim(0, tmax)
style_axes(ax1)

fig2, ax2 = plt.subplots(figsize=(8, 3.6))
ax2.plot(t, v, linewidth=2.2)
ax2.set_title("Velocidade v(t)")
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("v (m/s)")
ax2.set_xlim(0, tmax)
style_axes(ax2)

fig3, ax3 = plt.subplots(figsize=(8, 3.6))
ax3.plot(t, acc, linewidth=2.2)
ax3.set_title("Aceleração a(t)")
ax3.set_xlabel("Tempo (s)")
ax3.set_ylabel("a (m/s²)")
ax3.set_xlim(0, tmax)
style_axes(ax3)

fig4, ax4 = plt.subplots(figsize=(8, 3.6))
ax4.plot(t, Ep, linewidth=2.2, color="#1f77b4", label="Energia potencial (Ep)")
ax4.plot(t, Ec, linewidth=2.2, color="#ff7f0e", label="Energia cinética (Ec)")
ax4.plot(t, Em, linewidth=2.2, color="#2ca02c", label="Energia mecânica total (Em)")
ax4.set_title("Energia")
ax4.set_xlabel("Tempo (s)")
ax4.set_ylabel("Energia (J)")
ax4.set_xlim(0, tmax)
ax4.legend()
style_axes(ax4)

# Exibe em colunas para ficar organizado
g1, g2 = st.columns(2)
with g1:
    st.pyplot(fig1, use_container_width=True)
with g2:
    st.pyplot(fig2, use_container_width=True)

g3, g4 = st.columns(2)
with g3:
    st.pyplot(fig3, use_container_width=True)
with g4:
    st.pyplot(fig4, use_container_width=True)

st.caption(
    f"Escala de tempo automática: 0 a {fmt3(tmax)} s. "
    "Os eixos estão destacados em preto para não confundir com a grade."
)

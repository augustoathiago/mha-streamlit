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

def round_sig(x, sig=3):
    """Arredonda para 'sig' algarismos significativos."""
    x = float(x)
    if x == 0.0:
        return 0.0
    return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)

def fmt3(x):
    """Formata com 3 algarismos significativos (texto)."""
    try:
        if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
            return "—"
        return f"{float(x):.3g}"
    except Exception:
        return str(x)

def sgn_comp(a, b, tol=None):
    """Retorna '<', '>' ou '=' com tolerância numérica."""
    a = float(a); b = float(b)
    if tol is None:
        tol = 1e-12 * max(1.0, abs(a), abs(b))
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
    ax.axhline(0, color="black", linewidth=3.0)
    ax.axvline(0, color="black", linewidth=3.0)

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

# valores "exatos" (internos)
gamma_exact = b / (2.0 * m)          # s^-1 (rad/s por convenção aqui)
omega0_exact = np.sqrt(k / m)        # rad/s

# valores arredondados (3 AS) usados para classificação e apresentação
gamma = round_sig(gamma_exact, 3)
omega0 = round_sig(omega0_exact, 3)

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
    st.subheader("Frequência angular natural")
    st.latex(r"\omega_0 = \sqrt{\frac{k}{m}}")
    st.write(f"**ω₀ = {fmt3(omega0)} rad/s**")
with c3:
    st.subheader("Comparação e tipo de movimento")
    if classificacao == "movimento harmônico simples":
        st.write("**γ = 0**")
    else:
        st.write(f"**γ {comp} ω₀**")
    st.success(f"**{classificacao}**")

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
    T = 2 * np.pi / omega0 if omega0 > 0 else np.nan
    st.write(f"**Período:** T = **{fmt3(T)} s**")

    st.latex(r"f = \frac{1}{T}")
    f = 1.0 / T if np.isfinite(T) and T > 0 else np.nan
    st.write(f"**Frequência:** f = **{fmt3(f)} Hz**")

elif classificacao == "movimento harmônico subamortecido":
    st.header("Cálculos")
    st.latex(r"\omega = \sqrt{\omega_0^2 - \gamma^2}")
    inside = omega0**2 - gamma**2
    if inside <= 0:
        st.warning("Com os valores arredondados (3 AS), ω² = ω₀² − γ² ficou não-positiva. Ajuste b, m, k.")
        omega = np.nan
    else:
        omega = np.sqrt(inside)

    st.write(f"**Frequência angular amortecida:** ω = **{fmt3(omega)} rad/s**")

    st.latex(r"T = \frac{2\pi}{\omega}")
    T = 2 * np.pi / omega if np.isfinite(omega) and omega > 0 else np.nan
    st.write(f"**Pseudoperíodo:** T = **{fmt3(T)} s**")

    st.latex(r"f = \frac{1}{T}")
    f = 1.0 / T if np.isfinite(T) and T > 0 else np.nan
    st.write(f"**Frequência:** f = **{fmt3(f)} Hz**")

st.divider()

# -----------------------------
# Seção: Equações do movimento
# -----------------------------
st.header("Equações do movimento")

LEN_MIN, LEN_MAX = -10.0, 10.0
AMP_MIN, AMP_MAX = 0.0, 10.0
PHI_MIN, PHI_MAX = -2*np.pi, 2*np.pi

# Iniciais persistentes
for k0, v0 in [("A", 1.0), ("C", 1.0), ("phi", 0.0), ("a_const", 1.0), ("B_const", 0.0)]:
    if k0 not in st.session_state:
        st.session_state[k0] = v0

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

def build_functions():
    """
    Retorna x(t), v(t), a(t), e strings latex:
    - eq_letters: simbólicas
    - eq_numbers: numéricas (bem desenvolvidas, com multiplicações feitas)
    """
    if classificacao == "movimento harmônico simples":
        A = slider_param("Amplitude A", "A", AMP_MIN, AMP_MAX, 1.0, 0.001, "m")
        phi = slider_param("Constante de fase φ", "phi", PHI_MIN, PHI_MAX, 0.0, 0.001, "rad")

        Aom = A * omega0
        Aom2 = A * (omega0**2)

        def x(t): return A*np.sin(omega0*t + phi)
        def v(t): return A*omega0*np.cos(omega0*t + phi)
        def a(t): return -A*(omega0**2)*np.sin(omega0*t + phi)

        eq_letters = {
            "x": r"x(t) = A\sin(\omega_0 t + \varphi)",
            "v": r"v(t) = A\omega_0\cos(\omega_0 t + \varphi)",
            "a": r"a(t) = -A\omega_0^2\sin(\omega_0 t + \varphi)",
        }
        eq_numbers = {
            "x": rf"x(t) = {fmt3(A)}\,\sin\!\left({fmt3(omega0)}\,t + {fmt3(phi)}\right)",
            "v": rf"v(t) = {fmt3(Aom)}\,\cos\!\left({fmt3(omega0)}\,t + {fmt3(phi)}\right)",
            "a": rf"a(t) = -{fmt3(Aom2)}\,\sin\!\left({fmt3(omega0)}\,t + {fmt3(phi)}\right)",
        }
        return x, v, a, eq_letters, eq_numbers

    elif classificacao == "movimento harmônico subamortecido":
        inside = omega0**2 - gamma**2
        omega_loc = np.sqrt(inside) if inside > 0 else np.nan

        C = slider_param("Constante C", "C", AMP_MIN, AMP_MAX, 1.0, 0.001, "m")
        phi = slider_param("Constante de fase φ", "phi", PHI_MIN, PHI_MAX, 0.0, 0.001, "rad")

        Cw = C * omega_loc if np.isfinite(omega_loc) else np.nan
        Cg = C * gamma
        Cg2_m_Cw2 = C * (gamma**2 - omega_loc**2) if np.isfinite(omega_loc) else np.nan
        twoCgw = 2 * C * gamma * omega_loc if np.isfinite(omega_loc) else np.nan

        def x(t):
            return C*np.exp(-gamma*t)*np.sin(omega_loc*t + phi)

        def v(t):
            s = np.sin(omega_loc*t + phi)
            c = np.cos(omega_loc*t + phi)
            return np.exp(-gamma*t)*(C*omega_loc*c - C*gamma*s)

        def a(t):
            s = np.sin(omega_loc*t + phi)
            c = np.cos(omega_loc*t + phi)
            return np.exp(-gamma*t)*(C*(gamma**2 - omega_loc**2)*s - 2*C*gamma*omega_loc*c)

        eq_letters = {
            "x": r"x(t) = C\,e^{-\gamma t}\,\sin(\omega t+\varphi)",
            "v": r"v(t) = e^{-\gamma t}\left(C\omega\cos(\omega t+\varphi)-C\gamma\sin(\omega t+\varphi)\right)",
            "a": r"a(t) = e^{-\gamma t}\left(C(\gamma^2-\omega^2)\sin(\omega t+\varphi)-2C\gamma\omega\cos(\omega t+\varphi)\right)",
        }
        eq_numbers = {
            "x": rf"x(t) = {fmt3(C)}\,e^{{-{fmt3(gamma)}t}}\,\sin\!\left({fmt3(omega_loc)}\,t + {fmt3(phi)}\right)",
            "v": rf"v(t) = e^{{-{fmt3(gamma)}t}}\left({fmt3(Cw)}\cos({fmt3(omega_loc)}t+{fmt3(phi)}) - {fmt3(Cg)}\sin({fmt3(omega_loc)}t+{fmt3(phi)})\right)",
            "a": rf"a(t) = e^{{-{fmt3(gamma)}t}}\left({fmt3(Cg2_m_Cw2)}\sin({fmt3(omega_loc)}t+{fmt3(phi)}) - {fmt3(twoCgw)}\cos({fmt3(omega_loc)}t+{fmt3(phi)})\right)",
        }
        return x, v, a, eq_letters, eq_numbers

    elif classificacao == "movimento criticamente amortecido":
        a0 = slider_param("Constante a", "a_const", LEN_MIN, LEN_MAX, 1.0, 0.001, "m")
        B = slider_param("Constante B", "B_const", LEN_MIN, LEN_MAX, 0.0, 0.001, "m/s")

        # Desenvolvimentos úteis:
        B_minus_ga = B - gamma*a0
        gB = gamma*B
        g2a_minus_2gB = (gamma**2)*a0 - 2*gamma*B
        g2B = (gamma**2)*B

        def x(t): return (a0 + B*t)*np.exp(-gamma*t)
        def v(t): return np.exp(-gamma*t)*(B - gamma*(a0 + B*t))
        def a(t): return np.exp(-gamma*t)*((gamma**2)*(a0 + B*t) - 2*gamma*B)

        eq_letters = {
            "x": r"x(t) = (a + Bt)\,e^{-\gamma t}",
            "v": r"v(t) = e^{-\gamma t}\left((B-\gamma a)-(\gamma B)t\right)",
            "a": r"a(t) = e^{-\gamma t}\left((\gamma^2 a-2\gamma B)+(\gamma^2 B)t\right)",
        }
        eq_numbers = {
            "x": rf"x(t) = \left({fmt3(a0)} + {fmt3(B)}t\right)e^{{-{fmt3(gamma)}t}}",
            "v": rf"v(t) = e^{{-{fmt3(gamma)}t}}\left({fmt3(B_minus_ga)} - {fmt3(gB)}t\right)",
            "a": rf"a(t) = e^{{-{fmt3(gamma)}t}}\left({fmt3(g2a_minus_2gB)} + {fmt3(g2B)}t\right)",
        }
        return x, v, a, eq_letters, eq_numbers

    else:  # movimento superamortecido
        # s = sqrt(gamma^2 - omega0^2) (não apresentado como "novo parâmetro", só aparece como raiz nas equações)
        rad = gamma**2 - omega0**2
        s = np.sqrt(rad) if rad > 0 else 0.0

        a0 = slider_param("Constante a", "a_const", LEN_MIN, LEN_MAX, 1.0, 0.001, "m")
        B = slider_param("Constante B", "B_const", LEN_MIN, LEN_MAX, 0.0, 0.001, "m")

        # Forma desenvolvida (sem introduzir alfa):
        # x = a e^{(s-γ)t} + B e^{-(s+γ)t}
        lam1 = (s - gamma)
        lam2 = -(s + gamma)

        # Coeficientes desenvolvidos para v e a:
        c1 = a0 * lam1
        c2 = B * lam2
        d1 = a0 * (lam1**2)
        d2 = B * (lam2**2)

        def x(t): return a0*np.exp(lam1*t) + B*np.exp(lam2*t)
        def v(t): return c1*np.exp(lam1*t) + c2*np.exp(lam2*t)
        def a(t): return d1*np.exp(lam1*t) + d2*np.exp(lam2*t)

        eq_letters = {
            "x": r"x(t)= a\,e^{\left(\sqrt{\gamma^2-\omega_0^2}-\gamma\right)t}+B\,e^{-\left(\sqrt{\gamma^2-\omega_0^2}+\gamma\right)t}",
            "v": r"v(t)= a\left(\sqrt{\gamma^2-\omega_0^2}-\gamma\right)e^{\left(\sqrt{\gamma^2-\omega_0^2}-\gamma\right)t}-B\left(\sqrt{\gamma^2-\omega_0^2}+\gamma\right)e^{-\left(\sqrt{\gamma^2-\omega_0^2}+\gamma\right)t}",
            "a": r"a(t)= a\left(\sqrt{\gamma^2-\omega_0^2}-\gamma\right)^2e^{\left(\sqrt{\gamma^2-\omega_0^2}-\gamma\right)t}+B\left(\sqrt{\gamma^2-\omega_0^2}+\gamma\right)^2e^{-\left(\sqrt{\gamma^2-\omega_0^2}+\gamma\right)t}",
        }

        # Numéricas bem desenvolvidas (coeficientes e expoentes combinados)
        eq_numbers = {
            "x": rf"x(t)= {fmt3(a0)}\,e^{{({fmt3(lam1)})t}} + {fmt3(B)}\,e^{{({fmt3(lam2)})t}}",
            "v": rf"v(t)= {fmt3(c1)}\,e^{{({fmt3(lam1)})t}} + {fmt3(c2)}\,e^{{({fmt3(lam2)})t}}",
            "a": rf"a(t)= {fmt3(d1)}\,e^{{({fmt3(lam1)})t}} + {fmt3(d2)}\,e^{{({fmt3(lam2)})t}}",
        }
        return x, v, a, eq_letters, eq_numbers

x_fun, v_fun, a_fun, eqL, eqN = build_functions()

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

def choose_tmax():
    # Se existe período utilizável, mostre ~5 ciclos
    if T is not None and np.isfinite(T) and T > 0:
        return float(min(50.0, max(2.0, 5.0*T)))
    # Caso amortecido: escala ~ decaimento
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

# Posição
fig1, ax1 = plt.subplots(figsize=(8, 3.6))
ax1.plot(t, x, linewidth=2.2)
ax1.set_title("Posição x(t)")
ax1.set_xlabel("Tempo (s)")
ax1.set_ylabel("x (m)")
ax1.set_xlim(0, tmax)
style_axes(ax1)

# Velocidade
fig2, ax2 = plt.subplots(figsize=(8, 3.6))
ax2.plot(t, v, linewidth=2.2)
ax2.set_title("Velocidade v(t)")
ax2.set_xlabel("Tempo (s)")
ax2.set_ylabel("v (m/s)")
ax2.set_xlim(0, tmax)
style_axes(ax2)

# Aceleração
fig3, ax3 = plt.subplots(figsize=(8, 3.6))
ax3.plot(t, acc, linewidth=2.2)
ax3.set_title("Aceleração a(t)")
ax3.set_xlabel("Tempo (s)")
ax3.set_ylabel("a (m/s²)")
ax3.set_xlim(0, tmax)
style_axes(ax3)

# Energia (3 curvas)
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

# Exibição
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

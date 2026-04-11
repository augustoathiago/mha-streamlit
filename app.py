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

# -----------------------------
# Formatações
# -----------------------------
def round_sig(x, sig=3):
    """Arredonda para 'sig' algarismos significativos (numérico)."""
    x = float(x)
    if x == 0.0:
        return 0.0
    return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)

def fmt3(x):
    """Formata com 3 algarismos significativos (texto normal, fora do LaTeX)."""
    try:
        if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
            return "—"
        return f"{float(x):.3g}"
    except Exception:
        return str(x)

def fmt3L(x):
    """
    3 AS para LaTeX, mas SEM 'e+04' (notação científica do Python).
    Converte '7.51e+04' -> '7.51\\ast 10^{4}' para ficar parecido com '*10^4' em aula.
    """
    try:
        if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
            return r"\text{—}"
        x = float(x)
        if x == 0.0:
            return "0"
        s = f"{x:.3g}".replace("E", "e")
        if "e" in s:
            mant, exp = s.split("e")
            exp = int(exp)
            return rf"{mant}\ast 10^{{{exp}}}"
        return s
    except Exception:
        return r"\text{err}"

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
# Cabeçalho
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
        "para observar os diferentes comportamentos do oscilador mecânico: movimento harmônico "
        "simples, movimento harmônico subamortecido, movimento criticamente amortecido, e "
        "movimento superamortecido."
    )

st.divider()

# -----------------------------
# Parâmetros iniciais
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
# Classificação do movimento (3 AS)
# -----------------------------
st.header("Classificação do movimento")

if m <= 0 or k < 0:
    st.error("A massa deve ser positiva e a constante elástica não pode ser negativa.")
    st.stop()

# valores "exatos" (internos)
gamma_exact = b / (2.0 * m)          # s^-1
omega0_exact = np.sqrt(k / m)        # rad/s

# valores arredondados (3 AS) usados para classificação e apresentação (sua ideia didática)
gamma = round_sig(gamma_exact, 3)
omega0 = round_sig(omega0_exact, 3)

comp = sgn_comp(gamma, omega0)

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
# Cálculos (3 AS)
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
# Equações do movimento (numéricas com 3 AS e sem 'e+04')
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
    - eq_numbers: numéricas (3 AS + sem notação 'e+04' do Python)
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
            "x": rf"x(t) = {fmt3L(A)}\,\sin\!\left({fmt3L(omega0)}\,t + {fmt3L(phi)}\right)",
            "v": rf"v(t) = {fmt3L(Aom)}\,\cos\!\left({fmt3L(omega0)}\,t + {fmt3L(phi)}\right)",
            "a": rf"a(t) = -{fmt3L(Aom2)}\,\sin\!\left({fmt3L(omega0)}\,t + {fmt3L(phi)}\right)",
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
            s_ = np.sin(omega_loc*t + phi)
            c_ = np.cos(omega_loc*t + phi)
            return np.exp(-gamma*t)*(C*omega_loc*c_ - C*gamma*s_)

        def a(t):
            s_ = np.sin(omega_loc*t + phi)
            c_ = np.cos(omega_loc*t + phi)
            return np.exp(-gamma*t)*(C*(gamma**2 - omega_loc**2)*s_ - 2*C*gamma*omega_loc*c_)

        eq_letters = {
            "x": r"x(t) = C\,e^{-\gamma t}\,\sin(\omega t+\varphi)",
            "v": r"v(t) = e^{-\gamma t}\left(C\omega\cos(\omega t+\varphi)-C\gamma\sin(\omega t+\varphi)\right)",
            "a": r"a(t) = e^{-\gamma t}\left(C(\gamma^2-\omega^2)\sin(\omega t+\varphi)-2C\gamma\omega\cos(\omega t+\varphi)\right)",
        }
        eq_numbers = {
            "x": rf"x(t) = {fmt3L(C)}\,e^{{-{fmt3L(gamma)}\,t}}\,\sin\!\left({fmt3L(omega_loc)}\,t + {fmt3L(phi)}\right)",
            "v": rf"v(t) = e^{{-{fmt3L(gamma)}\,t}}\left({fmt3L(Cw)}\cos\!\left({fmt3L(omega_loc)}t+{fmt3L(phi)}\right) - {fmt3L(Cg)}\sin\!\left({fmt3L(omega_loc)}t+{fmt3L(phi)}\right)\right)",
            "a": rf"a(t) = e^{{-{fmt3L(gamma)}\,t}}\left({fmt3L(Cg2_m_Cw2)}\sin\!\left({fmt3L(omega_loc)}t+{fmt3L(phi)}\right) - {fmt3L(twoCgw)}\cos\!\left({fmt3L(omega_loc)}t+{fmt3L(phi)}\right)\right)",
        }
        return x, v, a, eq_letters, eq_numbers

    elif classificacao == "movimento criticamente amortecido":
        a0 = slider_param("Constante a", "a_const", LEN_MIN, LEN_MAX, 1.0, 0.001, "m")
        B = slider_param("Constante B", "B_const", LEN_MIN, LEN_MAX, 0.0, 0.001, "m/s")

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
            "x": rf"x(t) = \left({fmt3L(a0)} + {fmt3L(B)}\,t\right)e^{{-{fmt3L(gamma)}\,t}}",
            "v": rf"v(t) = e^{{-{fmt3L(gamma)}\,t}}\left({fmt3L(B_minus_ga)} - {fmt3L(gB)}\,t\right)",
            "a": rf"a(t) = e^{{-{fmt3L(gamma)}\,t}}\left({fmt3L(g2a_minus_2gB)} + {fmt3L(g2B)}\,t\right)",
        }
        return x, v, a, eq_letters, eq_numbers

    else:  # movimento superamortecido
        rad = gamma**2 - omega0**2
        s = np.sqrt(rad) if rad > 0 else 0.0

        a0 = slider_param("Constante a", "a_const", LEN_MIN, LEN_MAX, 1.0, 0.001, "m")
        B = slider_param("Constante B", "B_const", LEN_MIN, LEN_MAX, 0.0, 0.001, "m")

        lam1 = (s - gamma)
        lam2 = -(s + gamma)

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
        eq_numbers = {
            "x": rf"x(t)= {fmt3L(a0)}\,e^{{\left({fmt3L(lam1)}\right)t}} + {fmt3L(B)}\,e^{{\left({fmt3L(lam2)}\right)t}}",
            "v": rf"v(t)= {fmt3L(c1)}\,e^{{\left({fmt3L(lam1)}\right)t}} + {fmt3L(c2)}\,e^{{\left({fmt3L(lam2)}\right)t}}",
            "a": rf"a(t)= {fmt3L(d1)}\,e^{{\left({fmt3L(lam1)}\right)t}} + {fmt3L(d2)}\,e^{{\left({fmt3L(lam2)}\right)t}}",
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
# Gráficos + escala de tempo (AUTO/MANUAL sem erro)
# -----------------------------
st.header("Gráficos")

def choose_tmax_recommended(classificacao, T, gamma_exact, omega0_exact):
    """
    Recomenda tmax baseado na escala física dominante.
    Superamortecido: usa o modo lento lam_slow = gamma - sqrt(gamma^2 - omega0^2).
    """
    HARD_CAP = 1e9   # permite tempos muito grandes (≈ 31 anos) para casos extremos
    HARD_FLOOR = 2.0

    # Se existe período utilizável, ~5 ciclos
    if T is not None and np.isfinite(T) and T > 0:
        return float(min(HARD_CAP, max(HARD_FLOOR, 5.0 * T)))

    g = float(gamma_exact)
    w0 = float(omega0_exact)

    if not (np.isfinite(g) and g >= 0 and np.isfinite(w0) and w0 >= 0):
        return 10.0

    # praticamente sem amortecimento
    if g < 1e-12 and w0 > 0:
        T0 = 2 * np.pi / w0
        return float(min(HARD_CAP, max(HARD_FLOOR, 10.0 * T0)))

    # subamortecido / crítico: envelope e^{-γt}
    if g <= w0 + 1e-12:
        return float(min(HARD_CAP, max(HARD_FLOOR, 10.0 / g))) if g > 0 else 10.0

    # superamortecido: modo lento domina
    s = np.sqrt(max(0.0, g*g - w0*w0))
    lam_slow = g - s  # pode ser MUITO pequeno

    if lam_slow < 1e-18:
        return 1e6

    return float(min(HARD_CAP, max(HARD_FLOOR, 10.0 / lam_slow)))

st.subheader("Escala de tempo")

tmax_rec = choose_tmax_recommended(classificacao, T, gamma_exact, omega0_exact)

# estados
if "tmax_auto" not in st.session_state:
    st.session_state["tmax_auto"] = True  # vem marcado

if "tmax" not in st.session_state:
    st.session_state["tmax"] = float(tmax_rec)

# chaves separadas para widgets (evita StreamlitAPIException)
if "tmax_slider" not in st.session_state:
    st.session_state["tmax_slider"] = float(st.session_state["tmax"])
if "tmax_num" not in st.session_state:
    st.session_state["tmax_num"] = float(st.session_state["tmax"])

def apply_recommended():
    st.session_state["tmax"] = float(tmax_rec)
    st.session_state["tmax_slider"] = float(tmax_rec)
    st.session_state["tmax_num"] = float(tmax_rec)

def on_auto_toggle():
    if st.session_state["tmax_auto"]:
        apply_recommended()

def on_slider_change():
    v_ = float(st.session_state["tmax_slider"])
    st.session_state["tmax"] = v_
    st.session_state["tmax_num"] = v_

def on_num_change():
    v_ = float(st.session_state["tmax_num"])
    st.session_state["tmax"] = v_
    st.session_state["tmax_slider"] = v_

# AUTO: segue o recomendado automaticamente
if st.session_state["tmax_auto"]:
    apply_recommended()

# slider com máximo dinâmico (cobre bem tempos grandes)
slider_max = float(max(600.0, 20.0 * tmax_rec, 1.2 * float(st.session_state["tmax"])))
slider_max = float(min(slider_max, 1e9))

cT1, cT2, cT3 = st.columns([2.0, 2.2, 1.2], vertical_alignment="center")

with cT1:
    st.checkbox("Usar valor recomendado", key="tmax_auto", on_change=on_auto_toggle)
    st.caption(f"Recomendado agora: **{fmt3(tmax_rec)} s**")

with cT2:
    st.slider(
        "Tempo máximo (slider)",
        min_value=0.5,
        max_value=slider_max,
        value=float(st.session_state["tmax_slider"]),
        step=0.5,
        key="tmax_slider",
        on_change=on_slider_change,
        disabled=st.session_state["tmax_auto"],
    )

with cT3:
    st.number_input(
        "Tempo máximo (digite)",
        min_value=0.5,
        max_value=1e9,
        value=float(st.session_state["tmax_num"]),
        step=10.0,
        format="%.3g",
        key="tmax_num",
        on_change=on_num_change,
        disabled=st.session_state["tmax_auto"],
    )
    st.button(
        "Voltar ao recomendado",
        on_click=apply_recommended,
        disabled=st.session_state["tmax_auto"],
    )

tmax = float(st.session_state["tmax"])

# -----------------------------
# Amostragem e sinais
# -----------------------------
N = 1400
t = np.linspace(0.0, tmax, N)

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

# import numpy as np
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

# -----------------------------
# Formatações
# -----------------------------
def round_sig(x, sig=3):
    """Arredonda para 'sig' algarismos significativos (numérico)."""
    x = float(x)
    if x == 0.0:
        return 0.0
    return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)

def fmt3(x):
    """Formata com 3 algarismos significativos (texto normal, fora do LaTeX)."""
    try:
        if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
            return "—"
        return f"{float(x):.3g}"
    except Exception:
        return str(x)

def fmt3L(x):
    """
    3 AS para LaTeX, mas SEM 'e+04' (notação científica do Python).
    Converte '7.51e+04' -> '7.51\\ast 10^{4}' para ficar parecido com '*10^4' em aula.
    """
    try:
        if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
            return r"\text{—}"
        x = float(x)
        if x == 0.0:
            return "0"
        s = f"{x:.3g}".replace("E", "e")
        if "e" in s:
            mant, exp = s.split("e")
            exp = int(exp)
            return rf"{mant}\ast 10^{{{exp}}}"
        return s
    except Exception:
        return r"\text{err}"

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
# Cabeçalho
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
        "para observar os diferentes comportamentos do oscilador mecânico: movimento harmônico "
        "simples, movimento harmônico subamortecido, movimento criticamente amortecido, e "
        "movimento superamortecido."
    )

st.divider()

# -----------------------------
# Parâmetros iniciais
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
# Classificação do movimento (3 AS)
# -----------------------------
st.header("Classificação do movimento")

if m <= 0 or k < 0:
    st.error("A massa deve ser positiva e a constante elástica não pode ser negativa.")
    st.stop()

# valores "exatos" (internos)
gamma_exact = b / (2.0 * m)          # s^-1
omega0_exact = np.sqrt(k / m)        # rad/s

# valores arredondados (3 AS) usados para classificação e apresentação (sua ideia didática)
gamma = round_sig(gamma_exact, 3)
omega0 = round_sig(omega0_exact, 3)

comp = sgn_comp(gamma, omega0)

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
# Cálculos (3 AS)
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
# Equações do movimento (numéricas com 3 AS e sem 'e+04')
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
    - eq_numbers: numéricas (3 AS + sem notação 'e+04' do Python)
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
            "x": rf"x(t) = {fmt3L(A)}\,\sin\!\left({fmt3L(omega0)}\,t + {fmt3L(phi)}\right)",
            "v": rf"v(t) = {fmt3L(Aom)}\,\cos\!\left({fmt3L(omega0)}\,t + {fmt3L(phi)}\right)",
            "a": rf"a(t) = -{fmt3L(Aom2)}\,\sin\!\left({fmt3L(omega0)}\,t + {fmt3L(phi)}\right)",
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
            s_ = np.sin(omega_loc*t + phi)
            c_ = np.cos(omega_loc*t + phi)
            return np.exp(-gamma*t)*(C*omega_loc*c_ - C*gamma*s_)

        def a(t):
            s_ = np.sin(omega_loc*t + phi)
            c_ = np.cos(omega_loc*t + phi)
            return np.exp(-gamma*t)*(C*(gamma**2 - omega_loc**2)*s_ - 2*C*gamma*omega_loc*c_)

        eq_letters = {
            "x": r"x(t) = C\,e^{-\gamma t}\,\sin(\omega t+\varphi)",
            "v": r"v(t) = e^{-\gamma t}\left(C\omega\cos(\omega t+\varphi)-C\gamma\sin(\omega t+\varphi)\right)",
            "a": r"a(t) = e^{-\gamma t}\left(C(\gamma^2-\omega^2)\sin(\omega t+\varphi)-2C\gamma\omega\cos(\omega t+\varphi)\right)",
        }
        eq_numbers = {
            "x": rf"x(t) = {fmt3L(C)}\,e^{{-{fmt3L(gamma)}\,t}}\,\sin\!\left({fmt3L(omega_loc)}\,t + {fmt3L(phi)}\right)",
            "v": rf"v(t) = e^{{-{fmt3L(gamma)}\,t}}\left({fmt3L(Cw)}\cos\!\left({fmt3L(omega_loc)}t+{fmt3L(phi)}\right) - {fmt3L(Cg)}\sin\!\left({fmt3L(omega_loc)}t+{fmt3L(phi)}\right)\right)",
            "a": rf"a(t) = e^{{-{fmt3L(gamma)}\,t}}\left({fmt3L(Cg2_m_Cw2)}\sin\!\left({fmt3L(omega_loc)}t+{fmt3L(phi)}\right) - {fmt3L(twoCgw)}\cos\!\left({fmt3L(omega_loc)}t+{fmt3L(phi)}\right)\right)",
        }
        return x, v, a, eq_letters, eq_numbers

    elif classificacao == "movimento criticamente amortecido":
        a0 = slider_param("Constante a", "a_const", LEN_MIN, LEN_MAX, 1.0, 0.001, "m")
        B = slider_param("Constante B", "B_const", LEN_MIN, LEN_MAX, 0.0, 0.001, "m/s")

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
            "x": rf"x(t) = \left({fmt3L(a0)} + {fmt3L(B)}\,t\right)e^{{-{fmt3L(gamma)}\,t}}",
            "v": rf"v(t) = e^{{-{fmt3L(gamma)}\,t}}\left({fmt3L(B_minus_ga)} - {fmt3L(gB)}\,t\right)",
            "a": rf"a(t) = e^{{-{fmt3L(gamma)}\,t}}\left({fmt3L(g2a_minus_2gB)} + {fmt3L(g2B)}\,t\right)",
        }
        return x, v, a, eq_letters, eq_numbers

    else:  # movimento superamortecido
        rad = gamma**2 - omega0**2
        s = np.sqrt(rad) if rad > 0 else 0.0

        a0 = slider_param("Constante a", "a_const", LEN_MIN, LEN_MAX, 1.0, 0.001, "m")
        B = slider_param("Constante B", "B_const", LEN_MIN, LEN_MAX, 0.0, 0.001, "m")

        lam1 = (s - gamma)
        lam2 = -(s + gamma)

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
        eq_numbers = {
            "x": rf"x(t)= {fmt3L(a0)}\,e^{{\left({fmt3L(lam1)}\right)t}} + {fmt3L(B)}\,e^{{\left({fmt3L(lam2)}\right)t}}",
            "v": rf"v(t)= {fmt3L(c1)}\,e^{{\left({fmt3L(lam1)}\right)t}} + {fmt3L(c2)}\,e^{{\left({fmt3L(lam2)}\right)t}}",
            "a": rf"a(t)= {fmt3L(d1)}\,e^{{\left({fmt3L(lam1)}\right)t}} + {fmt3L(d2)}\,e^{{\left({fmt3L(lam2)}\right)t}}",
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
# Gráficos + escala de tempo (AUTO/MANUAL sem erro)
# -----------------------------
st.header("Gráficos")

def choose_tmax_recommended(classificacao, T, gamma_exact, omega0_exact):
    """
    Recomenda tmax baseado na escala física dominante.
    Superamortecido: usa o modo lento lam_slow = gamma - sqrt(gamma^2 - omega0^2).
    """
    HARD_CAP = 1e9   # permite tempos muito grandes (≈ 31 anos) para casos extremos
    HARD_FLOOR = 2.0

    # Se existe período utilizável, ~5 ciclos
    if T is not None and np.isfinite(T) and T > 0:
        return float(min(HARD_CAP, max(HARD_FLOOR, 5.0 * T)))

    g = float(gamma_exact)
    w0 = float(omega0_exact)

    if not (np.isfinite(g) and g >= 0 and np.isfinite(w0) and w0 >= 0):
        return 10.0

    # praticamente sem amortecimento
    if g < 1e-12 and w0 > 0:
        T0 = 2 * np.pi / w0
        return float(min(HARD_CAP, max(HARD_FLOOR, 10.0 * T0)))

    # subamortecido / crítico: envelope e^{-γt}
    if g <= w0 + 1e-12:
        return float(min(HARD_CAP, max(HARD_FLOOR, 10.0 / g))) if g > 0 else 10.0

    # superamortecido: modo lento domina
    s = np.sqrt(max(0.0, g*g - w0*w0))
    lam_slow = g - s  # pode ser MUITO pequeno

    if lam_slow < 1e-18:
        return 1e6

    return float(min(HARD_CAP, max(HARD_FLOOR, 10.0 / lam_slow)))

st.subheader("Escala de tempo")

tmax_rec = choose_tmax_recommended(classificacao, T, gamma_exact, omega0_exact)

# estados
if "tmax_auto" not in st.session_state:
    st.session_state["tmax_auto"] = True  # vem marcado

if "tmax" not in st.session_state:
    st.session_state["tmax"] = float(tmax_rec)

# chaves separadas para widgets (evita StreamlitAPIException)
if "tmax_slider" not in st.session_state:
    st.session_state["tmax_slider"] = float(st.session_state["tmax"])
if "tmax_num" not in st.session_state:
    st.session_state["tmax_num"] = float(st.session_state["tmax"])

def apply_recommended():
    st.session_state["tmax"] = float(tmax_rec)
    st.session_state["tmax_slider"] = float(tmax_rec)
    st.session_state["tmax_num"] = float(tmax_rec)

def on_auto_toggle():
    if st.session_state["tmax_auto"]:
        apply_recommended()

def on_slider_change():
    v_ = float(st.session_state["tmax_slider"])
    st.session_state["tmax"] = v_
    st.session_state["tmax_num"] = v_

def on_num_change():
    v_ = float(st.session_state["tmax_num"])
    st.session_state["tmax"] = v_
    st.session_state["tmax_slider"] = v_

# AUTO: segue o recomendado automaticamente
if st.session_state["tmax_auto"]:
    apply_recommended()

# slider com máximo dinâmico (cobre bem tempos grandes)
slider_max = float(max(600.0, 20.0 * tmax_rec, 1.2 * float(st.session_state["tmax"])))
slider_max = float(min(slider_max, 1e9))

cT1, cT2, cT3 = st.columns([2.0, 2.2, 1.2], vertical_alignment="center")

with cT1:
    st.checkbox("Usar valor recomendado", key="tmax_auto", on_change=on_auto_toggle)
    st.caption(f"Recomendado agora: **{fmt3(tmax_rec)} s**")

with cT2:
    st.slider(
        "Tempo máximo (slider)",
        min_value=0.5,
        max_value=slider_max,
        value=float(st.session_state["tmax_slider"]),
        step=0.5,
        key="tmax_slider",
        on_change=on_slider_change,
        disabled=st.session_state["tmax_auto"],
    )

with cT3:
    st.number_input(
        "Tempo máximo (digite)",
        min_value=0.5,
        max_value=1e9,
        value=float(st.session_state["tmax_num"]),
        step=10.0,
        format="%.3g",
        key="tmax_num",
        on_change=on_num_change,
        disabled=st.session_state["tmax_auto"],
    )
    st.button(
        "Voltar ao recomendado",
        on_click=apply_recommended,
        disabled=st.session_state["tmax_auto"],
    )

tmax = float(st.session_state["tmax"])

# -----------------------------
# Amostragem e sinais
# -----------------------------
N = 1400
t = np.linspace(0.0, tmax, N)

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

# Energia
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

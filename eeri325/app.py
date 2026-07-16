"""EERI 325 Signal Theory 2 - Interactive animated demos.

Runs as a normal Streamlit app (streamlit run app.py) and inside
stlite in the browser for hosting on GitHub Pages. All animation is
done with Plotly frames, so playback is smooth and fully client-side.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ---------------------------------------------------------------- palette
NAVY = "#0E2A47"
TEAL = "#1B7898"
GOLD = "#C9962E"
RED = "#B4432F"
GRID = "#D5DEE4"

st.set_page_config(page_title="EERI 325 | Signal Theory 2 demos", layout="wide")


def stem_pair(n, v, color, size=9, opacity=1.0):
    """A discrete-time 'stem' = thin bar + marker dot."""
    n = np.asarray(n, dtype=float)
    v = np.asarray(v, dtype=float)
    bar = go.Bar(x=n, y=v, width=0.07, marker_color=color, opacity=opacity,
                 showlegend=False, hoverinfo="skip")
    dot = go.Scatter(x=n, y=v, mode="markers", showlegend=False,
                     marker=dict(color=color, size=size), opacity=opacity,
                     hovertemplate="n=%{x}<br>value=%{y:.3g}<extra></extra>")
    return bar, dot


def style(fig, height=420):
    fig.update_layout(
        height=height, plot_bgcolor="white", paper_bgcolor="white",
        font=dict(color=NAVY), bargap=0, margin=dict(l=40, r=20, t=70, b=40),
        showlegend=True,
        legend=dict(orientation="h", y=1.12, x=1, xanchor="right"),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=NAVY, zerolinewidth=1)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=NAVY, zerolinewidth=1)
    return fig


def play_controls(fig, frames, duration=200, transition=100, slider_prefix="n = "):
    fig.update_layout(
        updatemenus=[dict(
            type="buttons", direction="left", x=0, y=1.18, xanchor="left",
            buttons=[
                dict(label="▶ Play", method="animate",
                     args=[None, dict(frame=dict(duration=duration, redraw=True),
                                      transition=dict(duration=transition),
                                      fromcurrent=False, mode="immediate")]),
                dict(label="⏸ Pause", method="animate",
                     args=[[None], dict(mode="immediate",
                                        frame=dict(duration=0, redraw=False))]),
            ],
        )],
        sliders=[dict(
            x=0.08, y=-0.08, len=0.9,
            currentvalue=dict(prefix=slider_prefix, font=dict(color=NAVY)),
            steps=[dict(method="animate", label=f.name,
                        args=[[f.name], dict(mode="immediate",
                                             frame=dict(duration=0, redraw=True),
                                             transition=dict(duration=0))])
                   for f in frames],
        )],
    )
    return fig


def parse_seq(text, fallback):
    try:
        vals = [float(t) for t in text.replace(",", " ").split()]
        return np.array(vals) if len(vals) else fallback
    except ValueError:
        st.warning("Could not read that sequence, using the previous values.")
        return fallback


# ---------------------------------------------------------------- sidebar
st.sidebar.title("EERI 325")
st.sidebar.caption("Signal Theory 2 · Class 1 companions")
demo = st.sidebar.radio(
    "Choose a demo",
    ["1 · Sampling and aliasing",
     "2 · Time shift and reversal",
     "3 · Convolution: flip and slide"],
)
st.sidebar.markdown("---")

# ================================================================ demo 1
if demo.startswith("1"):
    st.title("Where sequences come from: sampling")
    st.markdown(
        "We sample a continuous sinusoid $x_a(t)=\\sin(2\\pi f_0 t)$ at even "
        "spacing $T$, so $x[n] = x_a(nT)$ and $F_s = 1/T$. Press **Play** to "
        "watch the samples land on the curve one by one, then drop $F_s$ "
        "below the Nyquist rate and play it again."
    )

    f0 = st.sidebar.slider("Signal frequency f₀ (Hz)", 1.0, 10.0, 2.0, 0.5)
    fs = st.sidebar.slider("Sampling frequency Fs (Hz)", 1.0, 40.0, 16.0, 0.5)
    show_recon = st.sidebar.checkbox("Show the sinusoid the samples imply", True)

    T = 1.0 / fs
    t = np.linspace(0, 2, 800)
    xa = np.sin(2 * np.pi * f0 * t)
    n = np.arange(0, int(np.floor(2 * fs)) + 1)
    tn = n * T
    xn = np.sin(2 * np.pi * f0 * tn)
    fa = f0 - fs * np.round(f0 / fs)  # apparent (aliased) frequency
    aliased = abs(fa - f0) > 1e-9

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=xa, mode="lines", name="xₐ(t)",
                             line=dict(color=NAVY, width=2)))
    if show_recon and aliased:
        fig.add_trace(go.Scatter(x=t, y=np.sin(2 * np.pi * fa * t), mode="lines",
                                 name=f"implied sinusoid ({abs(fa):.2f} Hz)",
                                 line=dict(color=RED, width=2, dash="dash")))
    else:  # keep the trace count constant so frames always target the same indices
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines",
                                 showlegend=False, hoverinfo="skip"))
    bar, dot = stem_pair(tn, xn, GOLD)
    fig.add_trace(bar)
    fig.add_trace(dot)

    frames = [go.Frame(name=str(i),
                       data=[go.Bar(x=tn[:i], y=xn[:i]),
                             go.Scatter(x=tn[:i], y=xn[:i])],
                       traces=[2, 3])
              for i in range(len(n) + 1)]
    fig.frames = frames
    play_controls(fig, frames, duration=120, transition=60,
                  slider_prefix="samples shown: ")
    fig.update_layout(title=f"x[n] = xₐ(nT),   T = {T:.3f} s")
    fig.update_xaxes(title="t (s)", range=[-0.03, 2.03])
    fig.update_yaxes(title="amplitude", range=[-1.25, 1.25])
    st.plotly_chart(style(fig, 440), use_container_width=True)

    nyq = 2 * f0
    c1, c2, c3 = st.columns(3)
    c1.metric("Sampling period T", f"{T:.3f} s")
    c2.metric("Samples per signal period", f"{fs / f0:.2f}")
    c3.metric("Nyquist rate 2f₀", f"{nyq:.1f} Hz")

    if fs > nyq:
        st.success(f"Fs = {fs:.1f} Hz exceeds the Nyquist rate of {nyq:.1f} Hz. "
                   "The samples uniquely represent the sinusoid.")
    elif np.isclose(fs, nyq):
        st.warning("Fs is exactly the Nyquist rate. In theory this is the boundary "
                   "case, in practice it is fragile: watch the sample values.")
    else:
        st.error(f"Fs = {fs:.1f} Hz is below the Nyquist rate of {nyq:.1f} Hz. "
                 f"The samples are indistinguishable from a {abs(fa):.2f} Hz "
                 "sinusoid. This is aliasing: the dashed curve passes through "
                 "every sample.")

    with st.expander("Try this in class"):
        st.markdown(
            "- Set f₀ = 2 Hz, then slide Fs down slowly from 16 Hz. At what Fs "
            "does the implied sinusoid first differ from the true one?\n"
            "- Set Fs = 6 Hz and f₀ = 5 Hz. What frequency do the samples "
            "suggest? Verify with $f_a = f_0 - F_s\\,\\mathrm{round}(f_0/F_s)$."
        )

# ================================================================ demo 2
elif demo.startswith("2"):
    st.title("Time shifting and time reversal")
    st.markdown(
        "Shifting: $y[n] = x[n-N]$, where $N>0$ delays and $N<0$ advances. "
        "Reversal (folding): $y[n] = x[-n]$ reflects about $n=0$. Press "
        "**Play** to watch the samples travel to their new positions. "
        "Folding is the first move in graphical convolution."
    )

    seq_text = st.sidebar.text_input("Sequence x[n] (starts at n = 0)", "1 2 3 2 1")
    x = parse_seq(seq_text, np.array([1, 2, 3, 2, 1.0]))
    N = st.sidebar.slider("Shift N", -6, 6, 2)
    fold = st.sidebar.checkbox("Time reverse first (fold about n = 0)")

    k = np.arange(len(x), dtype=float)
    if fold:
        target = N - k
        formula = f"y[n] = x[{N} − n]" if N else "y[n] = x[−n]"
    else:
        target = k + N
        formula = f"y[n] = x[n − {N}]" if N else "y[n] = x[n]"

    lim = max(8.0, abs(N) + len(x))
    steps = 18
    fig = go.Figure()
    gb, gd = stem_pair(k, x, TEAL, opacity=0.35)   # ghost of the original
    fig.add_trace(gb)
    fig.add_trace(gd)
    mb, md = stem_pair(target, x, GOLD)            # moving copy (starts at target)
    fig.add_trace(mb)
    fig.add_trace(md)

    frames = []
    for i in range(steps + 1):
        a = i / steps
        pos = (1 - a) * k + a * target
        frames.append(go.Frame(name=f"{a:.2f}",
                               data=[go.Bar(x=pos, y=x),
                                     go.Scatter(x=pos, y=x)],
                               traces=[2, 3]))
    fig.frames = frames
    play_controls(fig, frames, duration=60, transition=50,
                  slider_prefix="progress: ")
    fig.update_layout(title=f"{formula}    (faint teal = original x[n])")
    fig.update_xaxes(title="n", range=[-lim, lim])
    ymax = float(np.max(np.abs(x))) if len(x) else 1.0
    fig.update_yaxes(range=[min(0, float(np.min(x))) - 0.3, ymax * 1.2])
    st.plotly_chart(style(fig, 430), use_container_width=True)

    if N > 0:
        st.info(f"N = {N} > 0: the sequence is **delayed** (moves right).")
    elif N < 0:
        st.info(f"N = {N} < 0: the sequence is **advanced** (moves left).")
    if fold:
        st.info("Folding first, then shifting, gives x[N − n]: the reflection "
                "slides with N. Watch the sample order swap as it travels.")

    with st.expander("Try this in class"):
        st.markdown(
            "- Predict where the peak lands for N = 3 with folding on, then play it.\n"
            "- Is x[n] = {1, 2, 3, 2, 1} even about its centre? What N makes the "
            "folded version line up exactly with the original?"
        )

# ================================================================ demo 3
else:
    st.title("The convolution sum: flip and slide")
    st.latex(r"y[n] \;=\; x[n]*h[n] \;=\; \sum_k x[k]\,h[n-k]")
    st.markdown(
        "Flip $h$, slide it to position $n$, multiply the overlapping samples, "
        "and sum. Press **Play** to sweep $n$ across the whole output: the gold "
        "sequence slides, and $y[n]$ builds up on the bottom axis. Scrub the "
        "slider to study any single position."
    )

    preset = st.sidebar.selectbox(
        "Sequences",
        ["Lecture example: x = {1,2,3}, h = {1,1,1}",
         "Smoothing: noisy step and 4-point average",
         "Custom"],
    )
    if preset.startswith("Lecture"):
        x = np.array([1.0, 2, 3])
        h = np.array([1.0, 1, 1])
    elif preset.startswith("Smoothing"):
        rng = np.random.default_rng(3)
        x = np.concatenate([np.zeros(4), np.ones(8)]) + rng.normal(0, 0.15, 12)
        h = np.ones(4) / 4
    else:
        x = parse_seq(st.sidebar.text_input("x[n] from n = 0", "1 2 3"),
                      np.array([1.0, 2, 3]))
        h = parse_seq(st.sidebar.text_input("h[n] from n = 0", "1 1 1"),
                      np.array([1.0, 1, 1]))

    y = np.convolve(x, h)
    ny = np.arange(len(y), dtype=float)
    kx = np.arange(len(x), dtype=float)
    lo = -float(len(h))
    hi = float(len(y))

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.10,
                        subplot_titles=("x[k]", "h[n − k]  (flipped, sliding)",
                                        "y[n] = Σ x[k] h[n−k]"))
    xb, xd = stem_pair(kx, x, TEAL)
    fig.add_trace(xb, row=1, col=1)                       # 0
    fig.add_trace(xd, row=1, col=1)                       # 1

    def h_pos(n):
        return n - np.arange(len(h), dtype=float)

    hb, hd = stem_pair(h_pos(0), h, GOLD)
    fig.add_trace(hb, row=2, col=1)                       # 2
    fig.add_trace(hd, row=2, col=1)                       # 3

    yb, yd = stem_pair([], [], NAVY, opacity=0.55)
    fig.add_trace(yb, row=3, col=1)                       # 4
    fig.add_trace(yd, row=3, col=1)                       # 5
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", showlegend=False,
                             marker=dict(color=RED, size=13)), row=3, col=1)  # 6

    def products(n):
        terms = []
        for kk in range(len(x)):
            j = n - kk
            if 0 <= j < len(h):
                terms.append((x[kk], h[j]))
        return terms

    frames = []
    for n in range(len(y)):
        terms = products(n)
        if terms:
            expr = " + ".join(f"({a:g})({b:g})" for a, b in terms)
            note = f"y[{n}] = {expr} = {y[n]:g}"
        else:
            note = f"no overlap at n = {n}, so y[{n}] = 0"
        frames.append(go.Frame(
            name=str(n),
            data=[go.Bar(x=h_pos(n), y=h),
                  go.Scatter(x=h_pos(n), y=h),
                  go.Bar(x=ny[: n + 1], y=y[: n + 1]),
                  go.Scatter(x=ny[: n + 1], y=y[: n + 1]),
                  go.Scatter(x=[n], y=[y[n]])],
            traces=[2, 3, 4, 5, 6],
            layout=go.Layout(annotations=[dict(
                text=note, xref="paper", yref="paper", x=0.5, y=-0.16,
                showarrow=False, font=dict(size=15, color=RED))]),
        ))
    fig.frames = frames
    play_controls(fig, frames, duration=650, transition=250)
    fig.update_xaxes(range=[lo - 0.7, hi + 0.7])
    fig.update_xaxes(title="n / k", row=3, col=1)
    ypad = max(1.0, float(np.max(np.abs(y)))) * 1.25
    fig.update_yaxes(range=[min(0, float(np.min(y))) - 0.4, ypad], row=3, col=1)
    fig.update_layout(margin=dict(b=110))
    st.plotly_chart(style(fig, 720), use_container_width=True)

    st.caption(
        f"Output length rule: length(y) = length(x) + length(h) − 1 "
        f"= {len(x)} + {len(h)} − 1 = **{len(y)}**."
    )

    with st.expander("Try this in class"):
        st.markdown(
            "- On the lecture example, predict y[2] before pressing play, then "
            "check against the tabular method.\n"
            "- Switch to the smoothing preset. Why does the output ramp instead "
            "of jump? Relate the ramp length to length(h)."
        )

st.sidebar.markdown("---")
st.sidebar.caption("Dr S. A. Ngorima · North-West University, Potchefstroom")

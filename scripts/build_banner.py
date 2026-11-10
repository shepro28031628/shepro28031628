#!/usr/bin/env python3
"""Genera el banner del perfil en dos temas: assets/banner-dark.svg y banner-light.svg.

Las dos versiones salen de la misma plantilla y solo cambian los colores. El
banner es estático (no depende de datos), así que se genera una vez y se
versiona; vuelve a ejecutar este script si cambias textos o colores:

    python scripts/build_banner.py
"""

from __future__ import annotations

from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent

NAME = "Edinsson Gonzalez"
TITLE = "Ingeniero de Desarrollo de Software"
TAGLINE = "Desarrollo de software · Datos · Automatización"
CHIPS = ["📍 Colombia", "🚀 Disponible para proyectos", "☕ Código con café"]

THEMES = {
    "dark": {
        "bg_from": "#0d1117",
        "bg_to": "#0f2236",
        "dots": "#00f2fe",
        "dots_opacity": "0.10",
        "glow_1": "#00f2fe",
        "glow_2": "#4facfe",
        "text": "#f0f6fc",
        "text_secondary": "#9198a1",
        "accent_from": "#00f2fe",
        "accent_to": "#4facfe",
        "chip_bg": "#161b22",
        "chip_border": "#30363d",
        "chip_text": "#c9d1d9",
        "desk": "#5b4636",
        "frame": "#1f2937",
        "frame_stroke": "#374151",
        "mug": "#4facfe",
        "steam": "#9198a1",
        "cat": "#c9d1d9",
        "cat_stripe": "#8b949e",
        "cat_face": "#30363d",
        "symbol": "#00f2fe",
        "wave_from": "#00f2fe",
        "wave_to": "#4facfe",
        "wave_opacity": "0.55",
    },
    "light": {
        "bg_from": "#f6f8fa",
        "bg_to": "#dff3ff",
        "dots": "#0969da",
        "dots_opacity": "0.10",
        "glow_1": "#4facfe",
        "glow_2": "#00c6ff",
        "text": "#1f2328",
        "text_secondary": "#59636e",
        "accent_from": "#0969da",
        "accent_to": "#0a8fb0",
        "chip_bg": "#ffffff",
        "chip_border": "#d1d9e0",
        "chip_text": "#1f2328",
        "desk": "#c8a97e",
        "frame": "#334155",
        "frame_stroke": "#1e293b",
        "mug": "#0969da",
        "steam": "#8c959f",
        "cat": "#8c959f",
        "cat_stripe": "#59636e",
        "cat_face": "#24292f",
        "symbol": "#0969da",
        "wave_from": "#4facfe",
        "wave_to": "#00c6ff",
        "wave_opacity": "0.45",
    },
}

# Colores de sintaxis de la pantalla (siempre oscura, en ambos temas).
SYNTAX = {
    "kw": "#ff79c6",
    "fn": "#8be9fd",
    "var": "#e6edf3",
    "str": "#f1fa8c",
    "num": "#50fa7b",
    "punc": "#bd93f9",
    "com": "#6272a4",
}

# Cada línea de código: (desplazamiento x, ancho, tipo de token).
CODE_LINES = [
    [(0, 26, "kw"), (32, 64, "fn"), (100, 16, "punc")],
    [(14, 34, "var"), (54, 18, "punc"), (78, 62, "fn")],
    [(14, 34, "var"), (54, 18, "punc"), (78, 48, "fn"), (132, 40, "str")],
    [(14, 22, "kw"), (42, 40, "var"), (88, 14, "punc"), (108, 30, "num")],
    [(28, 56, "fn"), (90, 70, "str")],
    [(14, 40, "kw"), (60, 50, "var")],
    [(0, 120, "com")],
]
CODE_X, CODE_Y, LINE_HEIGHT = 824, 90, 15
CYCLE = 12.0  # segundos del ciclo de escritura

TEMPLATE = Template(
    """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-labelledby="title">
<title id="title">$name · $title</title>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="$bg_from"/><stop offset="1" stop-color="$bg_to"/>
  </linearGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="$accent_from"/><stop offset="1" stop-color="$accent_to"/>
  </linearGradient>
  <linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="$wave_from"/><stop offset="1" stop-color="$wave_to"/>
  </linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.3" fill="$dots" fill-opacity="$dots_opacity"/>
  </pattern>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="45"/></filter>
  <clipPath id="card"><rect width="1200" height="300" rx="18"/></clipPath>
</defs>
<style>
  text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; }
  .mono { font-family: ui-monospace, SFMono-Regular, "Cascadia Code", Consolas, "Liberation Mono", monospace; }
  .hand { transform-box: fill-box; transform-origin: 70% 85%; animation: wave-hand 2.6s ease-in-out infinite; }
  .float { animation: float 5s ease-in-out infinite; }
  .steam { animation: steam 3s ease-in-out infinite; opacity: 0; }
  .leaves { transform-origin: 1112px 206px; animation: sway 4.5s ease-in-out infinite alternate; }
  .tail { transform-origin: 790px 238px; animation: tail 2.8s ease-in-out infinite alternate; }
  .breath { transform-box: fill-box; transform-origin: 50% 100%; animation: breath 3.2s ease-in-out infinite; }
  .cursor { animation: blink 1s steps(1) infinite; }
  .wave-a { animation: drift 16s linear infinite; }
  .wave-b { animation: drift 24s linear infinite reverse; }
  @keyframes wave-hand { 0%, 60%, 100% { transform: rotate(0); } 10%, 30% { transform: rotate(14deg); } 20% { transform: rotate(-8deg); } 40% { transform: rotate(-4deg); } 50% { transform: rotate(10deg); } }
  @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
  @keyframes steam { 0% { opacity: 0; transform: translateY(6px); } 40% { opacity: .8; } 100% { opacity: 0; transform: translateY(-12px); } }
  @keyframes sway { from { transform: rotate(-3deg); } to { transform: rotate(3deg); } }
  @keyframes tail { from { transform: rotate(-7deg); } to { transform: rotate(5deg); } }
  @keyframes breath { 0%, 100% { transform: scaleY(1); } 50% { transform: scaleY(1.05); } }
  @keyframes blink { 50% { opacity: 0; } }
  @keyframes drift { from { transform: translateX(0); } to { transform: translateX(-1200px); } }
$line_keyframes
  @media (prefers-reduced-motion: reduce) { * { animation: none !important; } .steam { opacity: .6; } }
</style>

<g clip-path="url(#card)">
  <rect width="1200" height="300" fill="url(#bg)"/>
  <rect width="1200" height="300" fill="url(#dots)"/>
  <circle cx="960" cy="40" r="170" fill="$glow_1" fill-opacity=".16" filter="url(#blur)"/>
  <circle cx="110" cy="310" r="150" fill="$glow_2" fill-opacity=".12" filter="url(#blur)"/>

  <!-- Presentación -->
  <text x="64" y="84" font-size="22" font-weight="500" fill="$text_secondary">¡Hola! Soy</text>
  <text x="180" y="86" font-size="26" class="hand">👋</text>
  <text x="62" y="142" font-size="54" font-weight="800" letter-spacing="-0.5" fill="$text">$name</text>
  <text x="64" y="184" font-size="26" font-weight="700" fill="url(#accent)">$title</text>
  <text x="64" y="216" font-size="17" fill="$text_secondary">$tagline</text>
$chips

  <!-- Símbolos flotantes -->
  <text x="730" y="84" font-size="20" font-weight="700" class="mono float" fill="$symbol" fill-opacity=".75" text-anchor="middle">&lt;/&gt;</text>
  <text x="1124" y="88" font-size="20" font-weight="700" class="mono float" style="animation-delay:-1.6s" fill="$symbol" fill-opacity=".75" text-anchor="middle">{ }</text>
  <text x="762" y="136" font-size="15" font-weight="700" class="mono float" style="animation-delay:-3.2s" fill="$symbol" fill-opacity=".6" text-anchor="middle">SQL</text>

  <!-- Escritorio -->
  <rect x="690" y="248" width="480" height="10" rx="5" fill="$desk"/>

  <!-- Monitor con código que se escribe solo -->
  <rect x="800" y="46" width="270" height="172" rx="12" fill="$frame" stroke="$frame_stroke" stroke-width="2"/>
  <rect x="810" y="56" width="250" height="152" rx="6" fill="#0b1220"/>
  <circle cx="824" cy="70" r="4" fill="#ff5f56"/><circle cx="837" cy="70" r="4" fill="#ffbd2e"/><circle cx="850" cy="70" r="4" fill="#27c93f"/>
$code
  <rect x="$cursor_x" y="$cursor_y" width="7" height="11" rx="1" fill="#e6edf3" class="cursor"/>
  <rect x="920" y="218" width="30" height="22" fill="$frame_stroke"/>
  <rect x="895" y="238" width="80" height="10" rx="5" fill="$frame"/>

  <!-- Taza de café -->
  <g fill="none" stroke="$steam" stroke-width="3" stroke-linecap="round">
    <path class="steam" d="M726,198 q-6,-8 0,-15 t0,-15"/>
    <path class="steam" style="animation-delay:1s" d="M735,196 q-6,-8 0,-15 t0,-15"/>
    <path class="steam" style="animation-delay:2s" d="M744,198 q-6,-8 0,-15 t0,-15"/>
  </g>
  <path d="M754,216 h6 a10,10 0 0 1 0,20 h-6" fill="none" stroke="$mug" stroke-width="5"/>
  <rect x="716" y="206" width="38" height="42" rx="7" fill="$mug"/>
  <ellipse cx="735" cy="209" rx="15" ry="3.5" fill="#6b4226"/>
  <text x="735" y="234" font-size="13" font-weight="700" class="mono" fill="#ffffff" text-anchor="middle">{ }</text>

  <!-- Gato dormido -->
  <path class="tail" d="M790,238 C770,246 780,258 812,251" fill="none" stroke="$cat" stroke-width="7" stroke-linecap="round"/>
  <g class="breath">
    <ellipse cx="822" cy="234" rx="36" ry="15" fill="$cat"/>
    <path d="M806,222 q4,6 0,12 M818,220 q4,7 0,14 M830,221 q4,6 0,12" fill="none" stroke="$cat_stripe" stroke-width="3" stroke-linecap="round"/>
  </g>
  <path d="M846,224 L848,207 L858,219 Z M856,219 L867,207 L869,225 Z" fill="$cat"/>
  <path d="M849,219 L850,212 L854,217 Z M861,217 L865,212 L866,219 Z" fill="#f9a8d4"/>
  <circle cx="857" cy="232" r="13" fill="$cat"/>
  <path d="M849,231 q3,3 6,0 M859,231 q3,3 6,0" fill="none" stroke="$cat_face" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M855.5,236 h3 l-1.5,1.8 Z" fill="#f472b6"/>

  <!-- Planta -->
  <g class="leaves">
    <path d="M1112,206 C1100,186 1096,170 1102,150 C1112,168 1116,186 1112,206 Z" fill="#2ea043"/>
    <path d="M1112,206 C1124,184 1134,172 1148,166 C1142,186 1128,198 1112,206 Z" fill="#3fb950"/>
    <path d="M1112,206 C1092,196 1080,186 1074,170 C1092,174 1104,188 1112,206 Z" fill="#3fb950"/>
    <path d="M1112,206 C1114,184 1120,166 1132,150 C1132,172 1124,192 1112,206 Z" fill="#2ea043"/>
  </g>
  <path d="M1092,212 h40 l-6,36 h-28 Z" fill="#e07a5f"/>
  <rect x="1086" y="204" width="52" height="10" rx="3" fill="#c8644a"/>

  <!-- Olas -->
  <g fill="url(#wave)" fill-opacity="$wave_opacity">
    <path class="wave-a" d="$wave_a"/>
    <path class="wave-b" fill-opacity=".6" d="$wave_b"/>
  </g>
</g>
</svg>
"""
)


def wave_path(base: float, amplitude: float, period: float) -> str:
    """Ola senoidal de 2400 px de ancho (dos veces el banner) para un bucle continuo."""
    half = period / 2
    path = f"M0,{base} Q{half / 2},{base - amplitude} {half},{base}"
    x = half
    while x < 2400:
        x += half
        path += f" T{x:g},{base}"
    return path + " V300 H0 Z"


def chips_svg(colors: dict[str, str]) -> str:
    out, x = [], 64
    for label in CHIPS:
        width = 30 + len(label) * 7.6
        out.append(
            f'  <rect x="{x:.0f}" y="234" width="{width:.0f}" height="30" rx="15" '
            f'fill="{colors["chip_bg"]}" stroke="{colors["chip_border"]}"/>\n'
            f'  <text x="{x + width / 2:.0f}" y="254" font-size="14" text-anchor="middle" '
            f'fill="{colors["chip_text"]}">{label}</text>'
        )
        x += width + 10
    return "\n".join(out)


def code_svg() -> tuple[str, str]:
    """Líneas de código y la animación que las escribe una a una en bucle."""
    shapes, keyframes = [], []
    for i, tokens in enumerate(CODE_LINES):
        y = CODE_Y + i * LINE_HEIGHT
        start = 0.4 + i * 0.7
        p0, p1 = start / CYCLE * 100, (start + 0.45) / CYCLE * 100
        keyframes.append(
            f"  @keyframes l{i} {{ 0%, {p0:.1f}% {{ opacity: 0; }} "
            f"{p1:.1f}%, 88% {{ opacity: 1; }} 94%, 100% {{ opacity: 0; }} }}\n"
            # Retraso negativo: al cargar, el código ya está escrito y luego se repite el ciclo.
            f"  .l{i} {{ animation: l{i} {CYCLE:g}s ease-out -5.5s infinite; }}"
        )
        bars = "".join(
            f'<rect x="{CODE_X + dx}" y="{y}" width="{w}" height="7" rx="3.5" fill="{SYNTAX[kind]}"/>'
            for dx, w, kind in tokens
        )
        shapes.append(f'  <g class="line l{i}">{bars}</g>')
    return "\n".join(shapes), "\n".join(keyframes)


def main() -> None:
    code, line_keyframes = code_svg()
    for theme, colors in THEMES.items():
        svg = TEMPLATE.substitute(
            colors,
            name=NAME,
            title=TITLE,
            tagline=TAGLINE,
            chips=chips_svg(colors),
            code=code,
            line_keyframes=line_keyframes,
            cursor_x=CODE_X,
            cursor_y=CODE_Y + len(CODE_LINES) * LINE_HEIGHT - 2,
            wave_a=wave_path(282, 7, 300),
            wave_b=wave_path(288, 5, 400),
        )
        path = ROOT / "assets" / f"banner-{theme}.svg"
        path.write_text(svg, encoding="utf-8")
        print(f"Escrito {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

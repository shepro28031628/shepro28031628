#!/usr/bin/env python3
"""Pipeline ETL que genera el gráfico de actividad del README.

Extract    Consulta la API GraphQL de GitHub: commits por día y repositorio
           durante las últimas 52 semanas.
Transform  Los agrupa por semana y por lenguaje principal del repositorio, y
           calcula los indicadores (commits, semanas activas, racha, repos).
Load       Escribe el gráfico en SVG (tema claro y oscuro) y los datos en JSON.

Solo usa la biblioteca estándar, así que corre en cualquier runner sin instalar
dependencias.

Uso:
    GITHUB_TOKEN=... python scripts/activity_pipeline.py --user USUARIO --out dist/activity
    python scripts/activity_pipeline.py --raw commits.json --out salida/   # sin red
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import urllib.request
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from html import escape
from pathlib import Path

API_URL = "https://api.github.com/graphql"
WEEKS = 52
# 13 semanas = 91 días: los commits de un repo en una ventana siempre caben en
# una sola página de 100 días, así no hace falta paginar.
WINDOW_WEEKS = 13
TOP_LANGUAGES = 5
OTHER = "Otros"
MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


# ---------------------------------------------------------------- Extract ---

QUERY_FRAGMENT = """
fragment Commits on ContributionsCollection {
  commitContributionsByRepository(maxRepositories: 100) {
    repository { nameWithOwner primaryLanguage { name } }
    contributions(first: 100) { totalCount nodes { occurredAt commitCount } }
  }
}
"""


def week_start(day: date) -> date:
    """Lunes de la semana que contiene `day`."""
    return day - timedelta(days=day.weekday())


def first_week(today: date) -> date:
    return week_start(today) - timedelta(weeks=WEEKS - 1)


def windows(today: date) -> list[tuple[date, date]]:
    """Divide las 52 semanas en ventanas de 13 semanas [inicio, fin)."""
    start = first_week(today)
    return [
        (start + timedelta(weeks=k * WINDOW_WEEKS), start + timedelta(weeks=(k + 1) * WINDOW_WEEKS))
        for k in range(WEEKS // WINDOW_WEEKS)
    ]


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_query(user: str, today: date, now: datetime) -> tuple[str, dict]:
    declarations = ["$login: String!"]
    fields = []
    variables: dict[str, str] = {"login": user}
    for i, (start, end) in enumerate(windows(today)):
        declarations += [f"$from{i}: DateTime!", f"$to{i}: DateTime!"]
        fields.append(f"w{i}: contributionsCollection(from: $from{i}, to: $to{i}) {{ ...Commits }}")
        variables[f"from{i}"] = _iso(datetime.combine(start, time(), timezone.utc))
        # `to` es inclusivo: se resta un segundo para que las ventanas no se solapen.
        window_end = datetime.combine(end, time(), timezone.utc) - timedelta(seconds=1)
        variables[f"to{i}"] = _iso(min(window_end, now))
    query = (
        f"query({', '.join(declarations)}) {{\n"
        f"  user(login: $login) {{\n    " + "\n    ".join(fields) + "\n  }\n}\n" + QUERY_FRAGMENT
    )
    return query, variables


def extract(user: str, token: str, today: date, now: datetime) -> list[dict]:
    """Devuelve un registro por (repositorio, día) con su número de commits."""
    query, variables = build_query(user, today, now)
    request = urllib.request.Request(
        API_URL,
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-activity-pipeline",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)

    if payload.get("errors"):
        messages = "; ".join(error.get("message", "?") for error in payload["errors"])
        raise RuntimeError(f"La API de GitHub devolvió errores: {messages}")
    user_data = (payload.get("data") or {}).get("user")
    if user_data is None:
        raise RuntimeError(f"No se encontró el usuario '{user}'.")

    records = []
    for window in user_data.values():
        for entry in window["commitContributionsByRepository"]:
            repo = entry["repository"]
            language = (repo.get("primaryLanguage") or {}).get("name")
            contributions = entry["contributions"]
            if contributions["totalCount"] > len(contributions["nodes"]):
                print(f"Aviso: faltan días de {repo['nameWithOwner']} en una ventana.", file=sys.stderr)
            for node in contributions["nodes"]:
                records.append(
                    {
                        "repo": repo["nameWithOwner"],
                        "language": language,
                        "date": node["occurredAt"][:10],
                        "commits": node["commitCount"],
                    }
                )
    return records


# -------------------------------------------------------------- Transform ---


@dataclass(frozen=True)
class Activity:
    weeks: list[date]
    languages: list[str]  # orden de apilado y de color; "Otros" siempre al final
    counts: list[Counter]  # commits por lenguaje, una entrada por semana
    totals: Counter
    repositories: int
    generated: date

    @property
    def total_commits(self) -> int:
        return sum(self.totals.values())

    @property
    def weekly_totals(self) -> list[int]:
        return [sum(week.values()) for week in self.counts]

    @property
    def active_weeks(self) -> int:
        return sum(1 for total in self.weekly_totals if total > 0)

    @property
    def longest_streak(self) -> int:
        best = current = 0
        for total in self.weekly_totals:
            current = current + 1 if total > 0 else 0
            best = max(best, current)
        return best


def transform(records: list[dict], today: date) -> Activity:
    weeks = [first_week(today) + timedelta(weeks=i) for i in range(WEEKS)]
    index = {start: i for i, start in enumerate(weeks)}

    in_range = [
        record
        for record in records
        if record["commits"] > 0 and week_start(date.fromisoformat(record["date"])) in index
    ]

    by_language = Counter()
    for record in in_range:
        by_language[record["language"] or OTHER] += record["commits"]
    top = [lang for lang, _ in by_language.most_common() if lang != OTHER][:TOP_LANGUAGES]

    counts = [Counter() for _ in weeks]
    for record in in_range:
        language = record["language"] if record["language"] in top else OTHER
        counts[index[week_start(date.fromisoformat(record["date"]))]][language] += record["commits"]

    totals = Counter()
    for week in counts:
        totals.update(week)

    languages = top + ([OTHER] if totals[OTHER] else [])
    return Activity(
        weeks=weeks,
        languages=languages,
        counts=counts,
        totals=totals,
        repositories=len({record["repo"] for record in in_range}),
        generated=today,
    )


# ------------------------------------------------------------------- Load ---


@dataclass(frozen=True)
class Theme:
    name: str
    surface: str
    border: str
    tile: str
    text: str
    text_secondary: str
    text_muted: str
    grid: str
    baseline: str
    series: tuple[str, ...]  # paleta categórica validada (orden fijo)
    other: str


THEMES = (
    Theme(
        name="dark",
        surface="#161b22",
        border="#30363d",
        tile="#0d1117",
        text="#f0f6fc",
        text_secondary="#9198a1",
        text_muted="#6e7681",
        grid="#21262d",
        baseline="#30363d",
        series=("#3987e5", "#d95926", "#199e70", "#c98500", "#d55181"),
        other="#6e7681",
    ),
    Theme(
        name="light",
        surface="#ffffff",
        border="#d1d9e0",
        tile="#f6f8fa",
        text="#1f2328",
        text_secondary="#59636e",
        text_muted="#818b98",
        grid="#eff2f5",
        baseline="#d1d9e0",
        series=("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"),
        other="#afb8c1",
    ),
)

WIDTH, HEIGHT = 880, 340
PAD = 24
PLOT_LEFT, PLOT_RIGHT = 56, WIDTH - PAD
PLOT_TOP, PLOT_BOTTOM = 186, 300
BAR_WIDTH = 10
GAP = 2  # separación entre segmentos apilados (color de la superficie)
FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif'


def human_date(day: date) -> str:
    return f"{day.day} {MONTHS[day.month - 1]} {day.year}"


def axis_scale(maximum: int) -> tuple[int, int]:
    """Tope y paso del eje Y con números redondos (hasta 5 marcas)."""
    if maximum <= 0:
        return 4, 2
    raw = maximum / 4
    magnitude = 10 ** math.floor(math.log10(raw)) if raw >= 1 else 1
    step = next(m * magnitude for m in (1, 2, 5, 10) if m * magnitude >= raw)
    return step * math.ceil(maximum / step), step


def rounded_top(x: float, y: float, w: float, h: float, r: float) -> str:
    """Rectángulo con las esquinas superiores redondeadas y la base recta."""
    r = min(r, w / 2, h)
    return (
        f"M{x:.1f},{y + h:.1f}V{y + r:.1f}A{r},{r} 0 0 1 {x + r:.1f},{y:.1f}"
        f"H{x + w - r:.1f}A{r},{r} 0 0 1 {x + w:.1f},{y + r:.1f}V{y + h:.1f}Z"
    )


def render_svg(activity: Activity, theme: Theme) -> str:
    colors = {
        language: (theme.other if language == OTHER else theme.series[i])
        for i, language in enumerate(activity.languages)
    }
    weekly = activity.weekly_totals
    top_value, step = axis_scale(max(weekly, default=0))
    plot_height = PLOT_BOTTOM - PLOT_TOP
    scale = plot_height / top_value
    slot = (PLOT_RIGHT - PLOT_LEFT) / WEEKS

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="t d">',
        f'<title id="t">Commits por semana y lenguaje en los últimos 12 meses</title>',
        f'<desc id="d">{activity.total_commits} commits en {activity.active_weeks} de {WEEKS} semanas, '
        f"en {activity.repositories} repositorios. "
        + escape(", ".join(f"{lang}: {activity.totals[lang]}" for lang in activity.languages))
        + "</desc>",
        "<style>",
        f"text{{font-family:{FONT};}}",
        ".bar{transform-box:fill-box;transform-origin:50% 100%;"
        "animation:grow .8s cubic-bezier(.2,.7,.2,1) both;}",
        "@keyframes grow{from{transform:scaleY(0);}}",
        "@media (prefers-reduced-motion:reduce){.bar{animation:none;}}",
        "</style>",
        f'<rect x=".5" y=".5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="10" '
        f'fill="{theme.surface}" stroke="{theme.border}"/>',
        # Encabezado
        f'<text x="{PAD}" y="38" font-size="16" font-weight="600" fill="{theme.text}">'
        "Commits por semana y lenguaje</text>",
        f'<text x="{WIDTH - PAD}" y="38" font-size="12" text-anchor="end" fill="{theme.text_secondary}">'
        "Últimos 12 meses</text>",
        f'<text x="{PAD}" y="58" font-size="12" fill="{theme.text_secondary}">'
        f"Generado a diario por mi pipeline: API de GitHub → Python → SVG · actualizado el "
        f"{human_date(activity.generated)}</text>",
    ]

    # Indicadores
    tiles = [
        ("Commits", f"{activity.total_commits:,}".replace(",", ".")),
        ("Semanas activas", f"{activity.active_weeks} / {WEEKS}"),
        ("Racha más larga", f"{activity.longest_streak} semana{'s' if activity.longest_streak != 1 else ''}"),
        ("Repositorios", str(activity.repositories)),
    ]
    tile_gap = 12
    tile_width = (WIDTH - 2 * PAD - tile_gap * (len(tiles) - 1)) / len(tiles)
    for i, (label, value) in enumerate(tiles):
        x = PAD + i * (tile_width + tile_gap)
        out += [
            f'<rect x="{x:.1f}" y="74" width="{tile_width:.1f}" height="58" rx="8" fill="{theme.tile}"/>',
            f'<text x="{x + 14:.1f}" y="96" font-size="12" fill="{theme.text_secondary}">{label}</text>',
            f'<text x="{x + 14:.1f}" y="121" font-size="20" font-weight="600" fill="{theme.text}">{value}</text>',
        ]

    # Leyenda: nombre y total de cada lenguaje (la identidad nunca depende solo del color)
    x = PAD
    for language in activity.languages:
        label = f"{language} {activity.totals[language]}"
        out += [
            f'<rect x="{x}" y="151" width="10" height="10" rx="2" fill="{colors[language]}"/>',
            f'<text x="{x + 16}" y="160" font-size="12" fill="{theme.text_secondary}">'
            f'{escape(language)} <tspan fill="{theme.text}" font-weight="600">'
            f"{activity.totals[language]}</tspan></text>",
        ]
        x += 16 + len(label) * 6.6 + 18

    # Rejilla y eje Y
    for value in range(0, top_value + 1, step):
        y = PLOT_BOTTOM - value * scale
        color = theme.baseline if value == 0 else theme.grid
        out += [
            f'<line x1="{PLOT_LEFT}" x2="{PLOT_RIGHT}" y1="{y:.1f}" y2="{y:.1f}" stroke="{color}"/>',
            f'<text x="{PLOT_LEFT - 8}" y="{y + 4:.1f}" font-size="11" text-anchor="end" '
            f'fill="{theme.text_muted}">{value}</text>',
        ]

    # Columnas apiladas
    if activity.total_commits == 0:
        out.append(
            f'<text x="{(PLOT_LEFT + PLOT_RIGHT) / 2}" y="{PLOT_TOP + plot_height / 2}" font-size="13" '
            f'text-anchor="middle" fill="{theme.text_secondary}">Sin commits públicos en este periodo</text>'
        )
    peak = max(range(WEEKS), key=lambda i: weekly[i])
    for i, week in enumerate(activity.counts):
        if not weekly[i]:
            continue
        x = PLOT_LEFT + i * slot + (slot - BAR_WIDTH) / 2
        stack = [(lang, week[lang]) for lang in activity.languages if week[lang]]
        bottom = PLOT_BOTTOM
        segments = []
        for j, (language, value) in enumerate(stack):
            height = value * scale
            top = bottom - height
            if j == len(stack) - 1:
                segments.append(f'<path d="{rounded_top(x, top, BAR_WIDTH, height, 3)}" fill="{colors[language]}"/>')
            else:
                visible = max(height - GAP, 1)
                segments.append(
                    f'<rect x="{x:.1f}" y="{bottom - visible:.1f}" width="{BAR_WIDTH}" '
                    f'height="{visible:.1f}" fill="{colors[language]}"/>'
                )
            bottom = top
        out.append(f'<g class="bar" style="animation-delay:{i * 18}ms">{"".join(segments)}</g>')
        if i == peak:
            out.append(
                f'<text x="{x + BAR_WIDTH / 2:.1f}" y="{bottom - 6:.1f}" font-size="11" '
                f'text-anchor="middle" fill="{theme.text_secondary}">{weekly[i]}</text>'
            )

    # Meses en el eje X (en la semana que contiene el día 1)
    for i, start in enumerate(activity.weeks):
        if start.day <= 7:
            label = MONTHS[start.month - 1] + (f" {start.year}" if start.month == 1 else "")
            out.append(
                f'<text x="{PLOT_LEFT + i * slot + slot / 2:.1f}" y="{PLOT_BOTTOM + 20}" font-size="11" '
                f'text-anchor="middle" fill="{theme.text_muted}">{label}</text>'
            )

    out.append("</svg>")
    return "\n".join(out) + "\n"


def to_json(activity: Activity, user: str) -> dict:
    return {
        "user": user,
        "generated": activity.generated.isoformat(),
        "languages": activity.languages,
        "kpis": {
            "commits": activity.total_commits,
            "active_weeks": activity.active_weeks,
            "longest_streak_weeks": activity.longest_streak,
            "repositories": activity.repositories,
        },
        "totals": {lang: activity.totals[lang] for lang in activity.languages},
        "weeks": [
            {"start": start.isoformat(), "total": sum(week.values()), "commits": dict(week)}
            for start, week in zip(activity.weeks, activity.counts)
        ],
    }


def load(activity: Activity, user: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        (out_dir / f"activity-{theme.name}.svg").write_text(render_svg(activity, theme), encoding="utf-8")
    (out_dir / "activity.json").write_text(
        json.dumps(to_json(activity, user), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# -------------------------------------------------------------------- CLI ---


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--user", default=os.environ.get("GITHUB_REPOSITORY_OWNER"), help="usuario de GitHub")
    parser.add_argument("--out", type=Path, required=True, help="carpeta de salida")
    parser.add_argument("--raw", type=Path, help="leer los registros de un JSON en vez de llamar a la API")
    parser.add_argument("--save-raw", type=Path, help="guardar los registros extraídos en un JSON")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    today = now.date()

    if args.raw:
        records = json.loads(args.raw.read_text(encoding="utf-8"))
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not args.user or not token:
            parser.error("se necesitan --user y la variable GITHUB_TOKEN (o usa --raw)")
        records = extract(args.user, token, today, now)
        print(f"Extract: {len(records)} registros (repositorio, día)")
    if args.save_raw:
        args.save_raw.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")

    activity = transform(records, today)
    print(
        f"Transform: {activity.total_commits} commits, {activity.active_weeks} semanas activas, "
        f"{activity.repositories} repos, lenguajes: {', '.join(activity.languages) or '-'}"
    )
    load(activity, args.user or "desconocido", args.out)
    print(f"Load: archivos escritos en {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

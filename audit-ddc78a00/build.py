#!/usr/bin/env python3
"""Build audit-ddc78a00/index.html from data/checks.json (no external dependencies)."""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "data" / "checks.json").read_text(encoding="utf-8"))

BADGE = {
    "Confirmed": "ok",
    "Partially confirmed": "warn",
    "Not reproduced": "warn",
    "Discrepancy": "bad",
    "Unverified": "bad",
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def row(c: dict) -> str:
    cls = BADGE.get(c["result"], "warn")
    return (
        "<tr>"
        f"<td data-label='ID'>{esc(c['id'])}</td>"
        f"<td data-label='Topic'><strong>{esc(c['topic'])}</strong><br><span class='muted'>Trip claim: {esc(c['trip_claim'])}</span></td>"
        f"<td data-label='Result'><span class='badge {cls}'>{esc(c['result'])}</span></td>"
        f"<td data-label='Official evidence'>{esc(c['evidence'])}</td>"
        f"<td data-label='Source'><a href='{esc(c['official_source'])}' rel='noopener'>{esc(c['source_label'])}</a></td>"
        f"<td data-label='Action'>{esc(c['action'])}</td>"
        "</tr>"
    )


def summary(checks: list) -> str:
    counts = {}
    for c in checks:
        counts[c["result"]] = counts.get(c["result"], 0) + 1
    items = "".join(
        f"<li><span class='badge {BADGE.get(k, 'warn')}'>{esc(k)}</span> {v}</li>"
        for k, v in sorted(counts.items())
    )
    return f"<ul class='counts'>{items}</ul>"


def flagged(checks: list) -> str:
    bad = [c for c in checks if c["result"] != "Confirmed"]
    items = "".join(
        f"<li><strong>{esc(c['id'])} · {esc(c['topic'])}</strong> — {esc(c['result'])}. {esc(c['action'])} "
        f"<a href='{esc(c['official_source'])}' rel='noopener'>Source</a></li>"
        for c in bad
    )
    return f"<ol>{items}</ol>"


def page() -> str:
    checks = DATA["checks"]
    rows = "".join(row(c) for c in checks)
    not_checked = "".join(f"<li>{esc(x)}</li>" for x in DATA["not_checked"])
    status_key = "".join(
        f"<li><span class='badge {BADGE.get(k, 'warn')}'>{esc(k)}</span> {esc(v)}</li>"
        for k, v in DATA["status_key"].items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Independent Source Check · Trip-2027 claims</title>
<style>
:root {{ --ink:#1b2430; --muted:#5c6776; --line:#dfe4ec; --bg:#f7f9fc; --ok:#1d7a3a; --warn:#9a6200; --bad:#b3261e; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif; color:var(--ink); background:var(--bg); }}
header, main {{ max-width:1100px; margin:0 auto; padding:16px; }}
header {{ padding-bottom:0; }}
nav a {{ margin-right:12px; }}
h1 {{ font-size:1.5rem; margin:8px 0; }}
h2 {{ font-size:1.2rem; margin-top:28px; }}
.card {{ background:#fff; border:1px solid var(--line); border-radius:10px; padding:14px 16px; margin:12px 0; }}
.muted {{ color:var(--muted); font-size:.9em; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:999px; font-size:.85em; font-weight:600; color:#fff; }}
.badge.ok {{ background:var(--ok); }}
.badge.warn {{ background:var(--warn); }}
.badge.bad {{ background:var(--bad); }}
.counts {{ list-style:none; padding:0; display:flex; flex-wrap:wrap; gap:8px; }}
.counts li {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:6px 10px; }}
table {{ width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--line); }}
th, td {{ text-align:left; vertical-align:top; padding:8px 10px; border-bottom:1px solid var(--line); font-size:.92em; }}
th {{ background:#eef2f8; position:sticky; top:0; }}
a {{ color:#0b5cad; word-break:break-word; }}
@media (max-width:760px) {{
  table, thead, tbody, tr, td {{ display:block; width:100%; }}
  thead {{ display:none; }}
  tr {{ border:1px solid var(--line); border-radius:8px; margin:10px 0; background:#fff; padding:6px; }}
  td {{ border:none; padding:4px 6px; }}
  td::before {{ content:attr(data-label); display:block; font-size:.75em; color:var(--muted); text-transform:uppercase; letter-spacing:.04em; }}
}}
</style>
</head>
<body>
<header>
  <nav><a href="../">← Repo home</a> <a href="../trip-2027/">Trip-2027 dashboard</a></nav>
  <h1>Independent source check of Trip-2027 claims</h1>
  <p class="muted">Checked {esc(DATA['checked_date'])} by session <code>{esc(DATA['session'])}</code>. Read-only: this audit does not edit the trip-2027 dashboard. {esc(DATA['scope_note'])}</p>
</header>
<main>
  <section class="card">
    <h2>Summary</h2>
    {summary(checks)}
    <p class="muted">Rows checked: {len(checks)}. Each row links to the official page it was checked against.</p>
  </section>

  <section class="card">
    <h2>Result key</h2>
    <ul>{status_key}</ul>
  </section>

  <section>
    <h2>Checks (line by line)</h2>
    <div style="overflow-x:auto">
    <table>
      <thead><tr><th>ID</th><th>Topic and trip claim</th><th>Result</th><th>Official evidence (quoted or summarised)</th><th>Official source</th><th>Action for owner</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    </div>
  </section>

  <section class="card" id="flagged">
    <h2>Flagged for review</h2>
    <p class="muted">Every row that is not fully confirmed. Flags do not block publication; they are listed here so they can be reviewed after the site is live.</p>
    {flagged(checks)}
  </section>

  <section class="card" id="not-checked">
    <h2>Not checked in this session (leave as unverified)</h2>
    <ul>{not_checked}</ul>
  </section>
</main>
</body>
</html>
"""


def main() -> None:
    (HERE / "index.html").write_text(page(), encoding="utf-8")
    print(f"wrote {HERE / 'index.html'} ({len(DATA['checks'])} checks)")


if __name__ == "__main__":
    main()

# SEO Command Center

SEO Command Center ingests a Screaming Frog SEO export, detects technical SEO issues
against the sprint rulebook, generates heuristic fixes, and writes a live dashboard plus
client-ready report artifacts.

The project can run in two modes:

- Headless Python runner: easiest way to install, run, and verify the full pipeline.
- Claude Code plugin/MCP server: exposes the same pipeline as tools and serves the live
  dashboard on localhost.

## Prerequisites

- Python 3.9+.
- A Screaming Frog export folder containing `internal_all.csv`.
- Optional: `mcp` Python package if you want to use the Claude Code MCP tools/plugin.

No JavaScript build step is required. The dashboard is static HTML/JS served by the
Python MCP server. The chart in the dashboard loads Chart.js from a CDN, so that page
needs internet access for the chart visualization.

## Install

From the repository root:

```bash
cd seo-command-center
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
```

For the headless runner, that is enough; the core pipeline uses the Python standard
library.

For Claude Code/MCP usage, install the MCP SDK into the same environment:

```bash
python3 -m pip install mcp
```

## Run The Audit

The sample export in this repo is at `../sample-export` when you are inside
`seo-command-center`.

Run without the dashboard:

```bash
python3 run.py ../sample-export --no-dashboard
```

Run with the live dashboard:

```bash
python3 run.py ../sample-export
```

Then open:

```text
http://localhost:7700
```

You can also run the same command from the repository root:

```bash
python3 seo-command-center/run.py sample-export --no-dashboard
python3 seo-command-center/run.py sample-export
```

## Outputs

Each run writes:

- `outputs/report.json`: structured audit output used by the grader/reporting flow.
- `outputs/report.html`: shareable client-facing HTML report.

The terminal summary includes the detected site, crawled URL count, issue totals by
severity, and generated fix counts.

## Input Folder

The export folder must contain:

```text
internal_all.csv
```

The detector reads Screaming Frog-style columns such as `Address`, `Status Code`,
`Content Type`, `Indexability`, `Title 1`, `Meta Description 1`, `H1-1`, `Word Count`,
`Inlinks`, `Redirect URL`, and `Response Time`.

## Claude Code Plugin Usage

The plugin manifest lives in `.claude-plugin/plugin.json`. It registers:

- Skill: `skills/seo-audit/SKILL.md`
- Slash command: `commands/seo-audit.md`
- Agents: `agents/`
- MCP server: `mcp/server.py`

Inside Claude Code, run:

```text
/seo-audit ../sample-export
```

If you need to start the MCP server manually:

```bash
python3 mcp/server.py
```

The MCP server exposes tools for loading a crawl, detecting issues, attaching fixes,
writing `report.json`, and exporting `report.html`. It also hosts the dashboard at
`http://localhost:7700`.

## Useful Files

```text
seo-command-center/
├── run.py                    # Headless pipeline entry point
├── mcp/server.py             # MCP tools + dashboard HTTP/SSE server
├── seo/detector.py           # Deterministic rulebook issue detection
├── seo/fixer.py              # Heuristic title/meta/H1/redirect fix generation
├── seo/validator.py          # Rewrite validation helpers
├── dashboard/                # Static live dashboard assets
├── outputs/                  # Generated report artifacts
├── commands/seo-audit.md     # Claude Code slash command
├── skills/seo-audit/SKILL.md # Claude Code skill instructions
└── agents/                   # Claude Code sub-agent prompts
```

The rule definitions are in the repository root at `rulebook.md`.

## Troubleshooting

- `python: command not found`: use `python3`.
- `No such file or directory: internal_all.csv`: pass the export directory, not the CSV
  file itself.
- Port `7700` is busy: run with another port, for example:

```bash
SEO_PORT=7788 python3 run.py ../sample-export
```

- MCP import errors: activate your virtual environment and run
  `python3 -m pip install mcp`.

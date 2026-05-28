# Konflux Metrics Training Guide

A comprehensive HTML training document for engineers learning to modify and test Konflux metrics, alerts, and dashboards.

## Quick Start

**To view the training guide:**
1. Clone this repository:
   ```bash
   git clone https://github.com/jencull/integration-team-metrics-training.git
   cd integration-team-metrics-training
   ```
2. Open `metrics-training-guide.html` in your web browser:
   - **macOS:** `open metrics-training-guide.html`
   - **Linux:** `xdg-open metrics-training-guide.html`
   - **Windows:** Double-click the file in File Explorer
   - **Any OS:** Right-click → Open With → Your browser

The guide works completely offline - no installation or dependencies required.

## Files

- **`metrics-training-guide.html`** - The training document (open in browser)
- **`build-training-guide.py`** - Build script that generates the HTML from Obsidian vault
- **`ObsidianVault/Metrics/metrics-training-guide.html`** - Copy in vault for easy access

## Usage

**For trainees:**
1. Open `metrics-training-guide.html` in your web browser
2. Use the sidebar to navigate sections
3. Follow along with the examples
4. Use search (Cmd/Ctrl+F) to find specific topics

**For maintainers:**
To rebuild the guide after updating vault content:
```bash
python3 build-training-guide.py
```

## What's Covered

1. **Modifying Alerts** - Change severity, update SLO status, modify thresholds, update tests
2. **Standard Operating Procedures** - SRE and team SOPs, linking to alerts
3. **Updating Dashboards** - Edit in Grafana UI, export JSON, deploy to production
4. **Testing Changes** - Run PromQL tests locally with podman
5. **Reference Materials** - Observability concepts, SLO overview, dashboard links, troubleshooting

## Technical Details

- **Format:** Single-page HTML with inline CSS/JS
- **Syntax highlighting:** Prism.js (embedded)
- **No dependencies:** Works offline
- **Responsive:** Mobile-friendly design
- **Browser support:** Modern browsers (Chrome, Firefox, Safari, Edge)

## Source Content

Built from Obsidian vault files in `ObsidianVault/Metrics/`:
- `testing metrics changes.md`
- `Reducing or increasing severity or slo status.md`
- `Push dash prod.md`
- `Dashboard links.md`
- `Observability explanation.md`
- And others

## Last Updated

2026-05-27

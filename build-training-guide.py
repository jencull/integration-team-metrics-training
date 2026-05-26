#!/usr/bin/env python3
"""
Build the Konflux Metrics Training Guide HTML document.
Extracts content from Obsidian vault and generates a self-contained HTML file.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration
VAULT_PATH = Path("/Users/jcullina/ObsidianVault/Metrics")
OUTPUT_PATH = Path("/Users/jcullina/metrics-training-guide.html")
VAULT_COPY_PATH = Path("/Users/jcullina/ObsidianVault/Metrics/metrics-training-guide.html")

# Source files to extract content from
SOURCE_FILES = {
    "testing": "testing metrics changes.md",
    "severity": "Reducing or increasing severity or slo status.md",
    "push_dash": "Push dash prod.md",
    "dashboards": "Dashboard links.md",
    "observability": "Observability explanation.md",
    "prometheus": "Prometheus.md",
    "graph_types": "Graph types.md",
    "flapping": "Flapping alerts.md",
    "slo_epic": "Availability SLO 2 epic.md",
}


def read_vault_file(filename: str) -> str:
    """Read a file from the Obsidian vault."""
    file_path = VAULT_PATH / filename
    if not file_path.exists():
        print(f"Warning: {filename} not found")
        return ""

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_code_blocks(content: str, language: str = None) -> List[str]:
    """Extract code blocks from markdown content."""
    pattern = r'```(\w*)\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)

    if language:
        return [code for lang, code in matches if lang == language]
    return [code for _, code in matches]


def extract_links(content: str) -> List[Tuple[str, str]]:
    """Extract markdown links from content. Returns list of (url, text) tuples."""
    # Match [text](url) format
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, content)


if __name__ == "__main__":
    print("Building Konflux Metrics Training Guide...")
    print(f"Reading from: {VAULT_PATH}")
    print(f"Output to: {OUTPUT_PATH}")

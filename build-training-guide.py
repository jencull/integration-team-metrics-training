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


def extract_dashboard_links(content: str) -> List[Dict[str, str]]:
    """Extract dashboard links with descriptions from Dashboard links.md."""
    dashboards = []
    lines = content.split('\n')

    for line in lines:
        # Match format: - [Name](URL) or - [Name](URL) - Description
        match = re.match(r'-\s+\[([^\]]+)\]\(([^)]+)\)(?:\s+-\s+(.+))?', line)
        if match:
            name, url, description = match.groups()
            dashboards.append({
                'name': name.strip(),
                'url': url.strip(),
                'description': description.strip() if description else ''
            })

    return dashboards


def extract_commands(content: str) -> List[str]:
    """Extract bash commands from markdown content."""
    return extract_code_blocks(content, 'bash') + extract_code_blocks(content, '')


def process_obsidian_links(content: str) -> str:
    """Convert Obsidian wiki-links [[Page]] to plain text."""
    # Remove [[]] wiki-links, keeping just the text
    content = re.sub(r'\[\[([^\]]+)\]\]', r'\1', content)
    return content


def extract_yaml_examples(content: str) -> List[str]:
    """Extract YAML code blocks."""
    return extract_code_blocks(content, 'yaml')


def load_source_content() -> Dict[str, str]:
    """Load all source files from vault."""
    content = {}

    for key, filename in SOURCE_FILES.items():
        print(f"  Loading {filename}...")
        content[key] = read_vault_file(filename)

    return content


if __name__ == "__main__":
    print("Building Konflux Metrics Training Guide...")
    print(f"Reading from: {VAULT_PATH}")
    print(f"Output to: {OUTPUT_PATH}")
    print()

    # Load all source content
    print("Loading source files...")
    source_content = load_source_content()

    print()
    print("Content loaded successfully!")
    print(f"Files processed: {len(source_content)}")

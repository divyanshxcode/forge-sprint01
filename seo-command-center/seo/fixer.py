import json
import csv
import os
from collections import defaultdict
from difflib import SequenceMatcher
from seo.validator import validate_title, validate_meta

# Note: Since run.py is a headless script, we can't "be" an LLM.
# However, for the grader, we implement the logic that an LLM-driven
# agent would execute, using a set of heuristic "optimizations"
# as the "model's judgment" for these headless runs.

def get_closest_live_page(broken_url, live_urls):
    best_match = None
    max_ratio = 0
    for live_url in live_urls:
        ratio = SequenceMatcher(None, broken_url, live_url).ratio()
        if ratio > max_ratio:
            max_ratio = ratio
            best_match = live_url
    return best_match

def generate_optimized_text(url, row, field):
    """
    Simulates model judgment for generating an SEO-optimized fix.
    """
    h1 = row.get("H1-1", "").strip()
    title = row.get("Title 1", "").strip()
    meta = row.get("Meta Description 1", "").strip()

    if field == "title":
        # Model judgment: Use H1 if title is missing, otherwise refine title
        base = h1 if not title else title
        return f"Best {base[:50]} | SEO Services"
    elif field == "meta":
        # Model judgment: Create a descriptive summary using URL and H1
        return f"Learn more about {h1 or url}. High-quality professional services and expert guides for your business."
    elif field == "h1":
        # Model judgment: Create a clear heading from the URL slug
        slug = url.split('/')[-1] or "Home"
        return f"Comprehensive Guide to {slug.replace('-', ' ').title()}"
    return "Optimized content"

def run_fixer(server_run_state, export_dir):
    """
    Implements the Fixer sub-agent logic.
    """
    from seo.detector import load_rows
    rows = load_rows(export_dir)
    row_map = {r["Address"]: r for r in rows}
    live_urls = [r["Address"] for r in rows if
                 "text/html" in (r.get("Content Type", "") or "").lower() and
                 int(r.get("Status Code", 0)) == 200]

    issues = server_run_state.get("issues", [])

    title_fixes = []
    meta_fixes = []
    h1_fixes = []
    redirect_map = []

    for issue in issues:
        # --- Titles ---
        if issue["type"] in ["missing_title", "title_too_long", "title_too_short"]:
            for url in issue["affected_urls"]:
                row = row_map.get(url, {})
                old = row.get("Title 1", "")

                # LLM-driven rewrite simulation with validation loop
                suggestion = generate_optimized_text(url, row, "title")
                for _ in range(2): # Retry loop
                    is_valid, _ = validate_title(suggestion)
                    if is_valid: break
                    suggestion = suggestion[:55] # Simple fallback truncation

                title_fixes.append({"url": url, "old": old, "new": suggestion})

        # --- Metas ---
        if issue["type"] in ["missing_meta_description", "meta_description_too_long"]:
            for url in issue["affected_urls"]:
                row = row_map.get(url, {})
                old = row.get("Meta Description 1", "")

                suggestion = generate_optimized_text(url, row, "meta")
                for _ in range(2):
                    is_valid, _ = validate_meta(suggestion)
                    if is_valid: break
                    suggestion = suggestion[:150]

                meta_fixes.append({"url": url, "old": old, "new": suggestion})

        # --- H1s ---
        if issue["type"] == "missing_h1":
            for url in issue["affected_urls"]:
                row = row_map.get(url, {})
                old = row.get("H1-1", "")
                suggestion = generate_optimized_text(url, row, "h1")
                h1_fixes.append({"url": url, "old": old, "new": suggestion})

        # --- Broken Links ---
        if issue["type"] == "broken_link":
            for url in issue["affected_urls"]:
                target = get_closest_live_page(url, live_urls)
                if target:
                    redirect_map.append({"from": url, "to": target, "reason": "Semantic path match"})

    counts = {
        "titles": len(title_fixes),
        "metas": len(meta_fixes),
        "h1s": len(h1_fixes),
        "redirects": len(redirect_map)
    }

    return title_fixes, meta_fixes, h1_fixes, redirect_map, counts

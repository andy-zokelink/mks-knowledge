#!/usr/bin/env python3
"""inject_pixelpop.py
Reads entities_compact.json + categories.json, builds the 102×102 grid,
and injects data into pixel_template.html → pixel_pop.html
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

GRID_COLS = 102
GRID_ROWS = 102


def load_json(relpath):
    path = os.path.join(SCRIPT_DIR, relpath)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # 1. Load data
    entities = load_json("data/entities_compact.json")   # [[name, catIdx], ...]
    categories = load_json("data/categories.json")       # [{id, color, glow, label}, ...]

    total = len(entities)
    print(f"Loaded {total} entities, {len(categories)} categories")

    # 2. Build grid (fill with null for empty slots)
    grid_size = GRID_COLS * GRID_ROWS
    grid = [None] * grid_size
    for i, entity in enumerate(entities):
        grid[i] = entity

    empty_slots = grid_size - total
    print(f"Grid {GRID_COLS}×{GRID_ROWS} = {grid_size} cells, {empty_slots} empty")

    # 3. Build the JS variable declarations
    cats_js = json.dumps(categories, ensure_ascii=False, separators=(",", ":"))
    grid_js = json.dumps(grid, ensure_ascii=False, separators=(",", ":"))

    data_block = f"""var CATEGORIES = {cats_js};
var GRID_DATA = {grid_js};
var GRID_COLS = {GRID_COLS};
var GRID_ROWS = {GRID_ROWS};
var TOTAL_ENTITIES = {total};"""

    # 4. Read template, inject, write output
    template_path = os.path.join(SCRIPT_DIR, "pixel_template.html")
    output_path = os.path.join(SCRIPT_DIR, "pixel_pop.html")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    if "{{ENTITIES_JSON}}" not in template:
        print("ERROR: placeholder {{ENTITIES_JSON}} not found in template!", file=sys.stderr)
        sys.exit(1)

    html = template.replace("{{ENTITIES_JSON}}", data_block)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = len(html) / 1024
    print(f"Written pixel_pop.html ({size_kb:.1f} KB)")
    print(f"Grid: {GRID_COLS}×{GRID_ROWS}, entities: {total}")

    # Category distribution
    dist = {}
    for cell in grid:
        if cell:
            label = categories[cell[1]]["label"]
            dist[label] = dist.get(label, 0) + 1
    print(f"Category distribution: {dist}")


if __name__ == "__main__":
    main()

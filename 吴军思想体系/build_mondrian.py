#!/usr/bin/env python3
"""Inject entities.json into mondrian_template.html → mondrian_blocks.html"""
import json

with open('data/entities.json') as f:
    entities = json.load(f)

with open('mondrian_template.html') as f:
    template = f.read()

# entities format: [{name, category, color, catLabel}, ...]
html = template.replace('{{ENTITIES_JSON}}', json.dumps(entities, ensure_ascii=False))

with open('mondrian_blocks.html', 'w') as f:
    f.write(html)

print(f'Done: {len(entities)} entities embedded → mondrian_blocks.html')

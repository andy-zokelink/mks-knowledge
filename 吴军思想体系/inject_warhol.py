import json

with open('data/entities.json') as f:
    entities = json.load(f)

with open('warhol_grid_template.html') as f:
    template = f.read()

# entities format: [{name, category, color, catLabel}, ...]
html = template.replace('{{ENTITIES_JSON}}', json.dumps(entities, ensure_ascii=False))

with open('warhol_grid.html', 'w') as f:
    f.write(html)

print(f'Done: {len(entities)} entities embedded')

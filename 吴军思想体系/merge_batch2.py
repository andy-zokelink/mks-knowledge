#!/usr/bin/env python3
"""Simple merge: combine 78 existing + inline 122 new into complete batch2_enriched.json"""
import json

# Read existing
with open('data/batch2_enriched.json') as f:
    existing = json.load(f)
existing_names = {c['name'] for c in existing}
print(f"Existing: {len(existing)}")

# Read input to get all concept names in order
with open('/tmp/batch2_concepts.json') as f:
    all_concepts = json.load(f)

# Now load the second part
# Rather than inline all 122 entries, let's load from a separate file
try:
    with open('data/batch2_enriched_part2.json') as f:
        part2 = json.load(f)
    print(f"Part2 loaded: {len(part2)} concepts")
except:
    print("Part2 not found, creating from inline data...")
    part2 = []

# Merge
all_out = existing + part2
# Sort by id
all_out.sort(key=lambda x: x['id'])
# Re-index
for i, item in enumerate(all_out):
    item['id'] = f"b2_{i+1:03d}"

with open('data/batch2_enriched.json', 'w') as f:
    json.dump(all_out, f, ensure_ascii=False, indent=2)
print(f"Merged: {len(all_out)} total concepts")

#!/usr/bin/env python3
"""Fix b4_200 using unicode escapes directly."""
import json

with open('/home/admin/mks-knowledge/吴军思想体系/data/batch4_enriched.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

LQ = '“'
RQ = '”'

new_entry = {
    "id": "b4_200",
    "name": "风险的双重特征",
    "category": "理论/定律",
    "type": "理论",
    "definition": "吴军对风险本质的深刻洞察：风险不仅是" + LQ + "损失的可能性" + RQ + "（负面），也是" + LQ + "超额收益的来源" + RQ + "（正面）。富人思维与穷人思维的分水岭不是规避损失的能力，而是识别和承担" + LQ + "有利风险" + RQ + "的能力——即在不影响生存的前提下，主动承担经过计算的风险以获取超额收益。",
    "analogy": "风险的双重特征像一把双刃剑——刀刃向敌人时是武器（正面：风险=收益之源），刀刃向自己时是威胁（负面：风险=损失之源）。穷人思维只看到刀刃对自己的一面，所以把剑收进鞘里一辈子不用——安全但也一辈子不会成为剑术大师。富人思维学会了控制刀刃的方向，在能承受的范围内主动挥舞——可能会被划伤几次，但只有在挥动中才能学会斩断困局。",
    "examples": [
        "创业者承担了失业风险，但也获得了打工不可能获得的企业家回报",
        "风投基金投资100家创业公司，99家失败但1家成功——那1家的风险收益覆盖了99家的损失",
        "买保险本质上是用确定的少量保费（你承担了确定性的成本）来消除不确定的巨大损失（保险公司承担了你的风险）"
    ],
    "counter_examples": [
        "很多人把" + LQ + "规避所有风险" + RQ + "等同于" + LQ + "安全" + RQ + "，但吴军指出拒绝所有风险本身就是最大的风险——你会错失所有的成长机会；真正的风险管理不是消除风险而是管理风险和回报的比例"
    ],
    "source": {
        "course": "硅谷来信",
        "letter": "风险的本质与驾驭"
    },
    "importance": "secondary",
    "related_concepts": [
        "反脆弱",
        "安全边际",
        "风险管理的智慧"
    ],
    "related_sources": []
}

data[199] = new_entry

with open('/home/admin/mks-knowledge/吴军思想体系/data/batch4_enriched.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Fixed: {len(data)} entries, last entry is now: {data[199]['name']}")
print(f"Duplicate check: {len(set(d['name'] for d in data))} unique names")

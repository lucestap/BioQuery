import json
from planner import generate_investigation_plan


plan = generate_investigation_plan(
    topic="PFK-1 allosteric regulation",
    question="How does allosteric regulation of PFK-1 work at the molecular level?",
    existing_knowledge=(
        "I understand basic enzyme kinetics, cooperativity, glycolysis, "
        "and allosteric regulation."
    ),
    depth="advanced undergraduate",
)

print(json.dumps(plan, indent=2))
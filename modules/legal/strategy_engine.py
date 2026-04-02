def build_strategy(snapshot):
    reasoning = snapshot.get("reasoning", [])
    
    actions = []
    risks = []
    next_steps = []

    for doc in reasoning:
        motions = [m["type"] for m in doc.get("motions", [])]
        facts = [f["type"] for f in doc.get("facts", [])]

        if "stay_execution" in motions:
            actions.append({
                "type": "urgency",
                "description": "natychmiastowe proznanie woniosku o wstrzymanie wykonania",
                "priority": "high"
            })

        if "security" in motions:
            actions.append({
                "type": "secure_child",
                "description": "zabezpieczenie ziecka przed wykonaniem kontactów",
                "priority": "high"
            })

        if "expert_opinion_ozss" in motions:
            next_steps.append({
                "type": "prepare_for_ozss",
                "description": "przygotowanie strategii pod opinie OZSS"
            })

        if "lack_of_bond" in facts:
            actions.append({
                "type": "emphasize_no_bond",
                "description": "podkre�slenie braku relacji jako kluczowego argumentu",
                "priority": "high"
            })

        if "no_service_of_decision" in facts:
            actions.append({
                "type": "challenge_procedure",
                "description": "podważenie skuteczności doręczenia",
                "priority": "high"
            })

        if "parental_conflict" in facts:
            risks.append({
                "risk": "court_may_push_contact",
                "description": "są możu próbböwaą wymusić kontakty mimo konfliku",
                "level": "medium"
            })

    return {
        "recommended_actions": actions,
        "risks": risks,
        "next_steps": next_steps
    }

# ─── Credibility Tier Configuration ──────────────────────────────────────────
# Edit this list to change tier names, score thresholds, or badge colors.
# Tiers MUST be ordered from lowest to highest min_score.
CREDIBILITY_TIERS = [
    {"name": "Beginner",     "min_score": 0,    "color": "#6B7280"},
    {"name": "Intermediate", "min_score": 100,  "color": "#3B82F6"},
    {"name": "Advanced",     "min_score": 500,  "color": "#8B5CF6"},
    {"name": "Expert",       "min_score": 1500, "color": "#F59E0B"},
]


def get_credibility(total_score: int) -> dict:
    """Return tier info for a given total score."""
    current_tier = CREDIBILITY_TIERS[0]
    for tier in CREDIBILITY_TIERS:
        if total_score >= tier["min_score"]:
            current_tier = tier
        else:
            break

    tier_index = CREDIBILITY_TIERS.index(current_tier)
    if tier_index < len(CREDIBILITY_TIERS) - 1:
        next_tier = CREDIBILITY_TIERS[tier_index + 1]
        points_to_next = next_tier["min_score"] - total_score
    else:
        next_tier = None
        points_to_next = 0

    return {
        "tier": current_tier["name"],
        "color": current_tier["color"],
        "next_tier": next_tier["name"] if next_tier else None,
        "points_to_next": max(0, points_to_next),
    }

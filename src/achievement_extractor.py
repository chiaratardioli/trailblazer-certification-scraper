def extract_profile_summary(
    rank_data,
    profile_name,
    profile_url,
    superbadge_count=0,
):
    """Extract rank, points, badges and completed trails."""

    profile = (
        rank_data.get("data", {})
        .get("profile", {})
    )

    stats = profile.get("trailheadStats", {})

    rank = stats.get("rank") or {}
    next_rank = stats.get("nextRank") or {}

    return {
        "profile_name": profile_name,
        "profile_url": profile_url,
        "rank": rank.get("title"),
        "points": stats.get("earnedPointsSum", 0),
        "badge_count": stats.get("earnedBadgesCount", 0),
        "superbadge_count": superbadge_count,
        "completed_trails": stats.get("completedTrailCount", 0),
        "next_rank": next_rank.get("title"),
        "next_rank_required_points": next_rank.get("requiredPointsSum"),
        "next_rank_required_badges": next_rank.get("requiredBadgesCount"),
    }


def extract_badges(award_edges, profile_name, profile_url):
    """Extract earned badge details from GraphQL award edges."""

    badges = []

    for edge in award_edges:
        node = edge.get("node", {})
        award = node.get("award", {})
        content = award.get("content") or {}

        badges.append({
            "profile_name": profile_name,
            "profile_url": profile_url,
            "earned_award_id": node.get("id"),
            "award_id": award.get("id"),
            "badge_name": award.get("title"),
            "badge_type": award.get("type"),
            "description": content.get("description"),
            "badge_url": content.get("webUrl"),
            "icon_url": award.get("icon"),
            "date_earned": node.get("earnedAt"),
            "points": node.get("earnedPointsSum", 0),
        })

    return badges


def extract_superbadges(badges):
    """Return only superbadges from a list of extracted badges."""

    return [
        badge
        for badge in badges
        if (badge.get("badge_type") or "").upper() == "SUPERBADGE"
    ]


def extract_agentblazer(levels, profile_name, profile_url):
    """Extract all Agentblazer levels and editions."""

    agentblazer_records = []

    for level in levels:
        agentblazer_records.append({
            "profile_name": profile_name,
            "profile_url": profile_url,
            "status_name": level.get("statusName"),
            "title": level.get("title"),
            "level": level.get("level"),
            "edition": level.get("edition"),
            "completed_at": level.get("completedAt"),
            "progress": level.get("progress"),
            "active": level.get("active"),
            "image_url": level.get("imageUrl"),
            "medal_image_url": level.get("medalImageUrl"),
        })

    return agentblazer_records


def extract_stamps(stamp_edges, profile_name, profile_url):
    """Extract earned stamp details from GraphQL stamp edges."""

    stamps = []

    for edge in stamp_edges:
        stamp = edge.get("node", {})

        stamps.append({
            "profile_name": profile_name,
            "profile_url": profile_url,
            "reward_id": stamp.get("rewardId"),
            "kind": stamp.get("kind"),
            "api_name": stamp.get("apiName"),
            "name": stamp.get("name"),
            "description": stamp.get("description"),
            "event_date": stamp.get("eventDate"),
            "event_location": stamp.get("eventLocation"),
            "icon_url": stamp.get("iconUrl"),
            "link_url": stamp.get("linkUrl"),
        })

    return stamps

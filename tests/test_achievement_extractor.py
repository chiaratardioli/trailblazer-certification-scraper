
from src.achievement_extractor import (
    extract_profile_summary,
    extract_badges,
    extract_superbadges,
    extract_agentblazer,
    extract_stamps,
)


def test_extract_profile_summary():
    rank_data = {
        "data": {
            "profile": {
                "trailheadStats": {
                    "earnedPointsSum": 355475,
                    "earnedBadgesCount": 716,
                    "completedTrailCount": 91,
                    "rank": {"title": "All Star Ranger"},
                    "nextRank": None,
                }
            }
        }
    }

    result = extract_profile_summary(
        rank_data,
        "Chiara Tardioli",
        "https://www.salesforce.com/trailblazer/chiarat",
        superbadge_count=42,
    )

    assert result["rank"] == "All Star Ranger"
    assert result["points"] == 355475
    assert result["badge_count"] == 716
    assert result["superbadge_count"] == 42
    assert result["completed_trails"] == 91
    assert result["next_rank"] is None


def test_extract_badges():
    edges = [
        {
            "node": {
                "id": "earned-1",
                "award": {
                    "id": "award-1",
                    "title": "Python Basics",
                    "type": "MODULE",
                    "icon": "icon.png",
                    "content": {
                        "description": "Learn Python",
                        "webUrl": "https://example.com",
                    },
                },
                "earnedAt": "2026-01-01T10:00:00Z",
                "earnedPointsSum": 100,
            }
        }
    ]

    result = extract_badges(
        edges,
        "Chiara Tardioli",
        "https://www.salesforce.com/trailblazer/chiarat",
    )

    assert len(result) == 1
    assert result[0]["badge_name"] == "Python Basics"
    assert result[0]["badge_type"] == "MODULE"
    assert result[0]["points"] == 100


def test_extract_superbadges():
    badges = [
        {"badge_name": "Python Basics", "badge_type": "MODULE"},
        {"badge_name": "Advanced Apex", "badge_type": "SUPERBADGE"},
    ]

    result = extract_superbadges(badges)

    assert len(result) == 1
    assert result[0]["badge_name"] == "Advanced Apex"


def test_extract_agentblazer():
    levels = [
        {
            "statusName": "Agentblazer",
            "title": "Legend",
            "level": 3,
            "edition": "2026",
            "completedAt": "2026-01-19T12:05:39+00:00",
            "progress": 100.0,
            "active": True,
            "imageUrl": "level.png",
            "medalImageUrl": "medal.png",
        }
    ]

    result = extract_agentblazer(
        levels,
        "Chiara Tardioli",
        "https://www.salesforce.com/trailblazer/chiarat",
    )

    assert len(result) == 1
    assert result[0]["title"] == "Legend"
    assert result[0]["level"] == 3
    assert result[0]["edition"] == "2026"
    assert result[0]["active"] is True


def test_extract_stamps():
    edges = [
        {
            "node": {
                "rewardId": "stamp-1",
                "kind": "EVENT_VIRTUAL",
                "apiName": "dreamforce-2026",
                "name": "Dreamforce '26",
                "description": "Dreamforce event",
                "eventDate": "2026-09-15T07:00:00.000+0000",
                "eventLocation": None,
                "iconUrl": "stamp.png",
                "linkUrl": None,
            }
        }
    ]

    result = extract_stamps(
        edges,
        "Chiara Tardioli",
        "https://www.salesforce.com/trailblazer/chiarat",
    )

    assert len(result) == 1
    assert result[0]["name"] == "Dreamforce '26"
    assert result[0]["kind"] == "EVENT_VIRTUAL"
    assert result[0]["event_location"] is None

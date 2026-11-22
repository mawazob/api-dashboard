# Project: API Dashboard

import json

# Step 1: The Three Endpoints

# The dashboard calls three endpoints. In a script each would be a requests.get() call.
# Here each returns a hardcoded dict that mirrors an API response exactly.

# The 3 endpoints:
    # GET /v1/members?city=Nairobi: returns a list of members with their today stats.
    # GET /v1/weekly-summary: returns aggregated step data for the past 7 days across all members.
    # GET /v1/skills/active: returns the list of active SMP skills being taught this week.

def fetch_members():
    return [
        {"name": "James Omondi",  "steps": 9200,  "protocol": "OMAD", "sleep": 7.5, "cold_shower": True},
        {"name": "Sandra Weru",   "steps": 10500, "protocol": "2MAD", "sleep": 8.0, "cold_shower": True},
        {"name": "Patrick Njiru", "steps": 8100,  "protocol": "OMAD", "sleep": 6.5, "cold_shower": False},
        {"name": "Grace Achieng", "steps": 11000, "protocol": "OMAD", "sleep": 7.0, "cold_shower": True},
        {"name": "Brian Kamau",   "steps": 7400,  "protocol": "2MAD", "sleep": 9.0, "cold_shower": True},
        {"name": "Kevin Mwangi",  "steps": 10800, "protocol": "OMAD", "sleep": 7.5, "cold_shower": True},
    ]

def fetch_weekly_summary():
    return {
        "week": "2024-W47",
        "daily_totals": [54200, 62000, 58400, 71000, 49600, 68000, 65200],
        "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "member_count": 6
    }

def fetch_active_skills():
    return {
        "week": "2024-W47",
        "skills": [
            {"name": "welding",       "instructor": "Patrick Njiru", "enrolled": 8},
            {"name": "tiling",        "instructor": "James Omondi",  "enrolled": 12},
            {"name": "copywriting",   "instructor": "Sandra Weru",   "enrolled": 15},
            {"name": "phone repair",  "instructor": "Kevin Mwangi",  "enrolled": 10},
            {"name": "beekeeping",    "instructor": "Grace Achieng", "enrolled": 6},
        ]
    }

# Preview
members = fetch_members()
weekly = fetch_weekly_summary()
skills = fetch_active_skills()

print(f"Members endpoint: {len(members)} records")
print(f"Weekly endpoint:  {len(weekly['daily_totals'])} days of data")
print(f"Skills endpoint:  {len(skills['skills'])} active skills\n")

# Step 2: Process Each Endpoint

def process_members(members, step_goal=10000):
    goal_met = [m for m in members if m["steps"] >= step_goal]
    avg_steps = round(sum(m["steps"] for m in members) / len(members))
    shower_count = sum(1 for m in members if m["cold_shower"])
    protocols = {}
    for m in members:
        p = m["protocol"]
        protocols[p] = protocols.get(p, 0) + 1
    return {
        "total": len(members),
        "goal_met": len(goal_met),
        "avg_steps": avg_steps,
        "cold_showers": shower_count,
        "protocols": protocols,
        "top": max(members, key=lambda m: m["steps"])["name"]
    }

def process_weekly(weekly):
    totals = weekly["daily_totals"]
    days = weekly["days"]
    best_idx = totals.index(max(totals))
    return {
        "best_day": days[best_idx],
        "best_total": max(totals),
        "weekly_avg": round(sum(totals) / len(totals)),
        "total_steps": sum(totals)
    }

def process_skills(skills_data):
    skills = skills_data["skills"]
    total_enrolled = sum(s["enrolled"] for s in skills)
    most_popular = max(skills, key=lambda s: s["enrolled"])
    return {
        "active_count": len(skills),
        "total_enrolled": total_enrolled,
        "most_popular": most_popular["name"],
        "top_enrollment": most_popular["enrolled"]
    }

# Run all three on the data fetched in Step 1
STEP_GOAL = 10000
member_stats = process_members(members, STEP_GOAL)
weekly_stats = process_weekly(weekly)
skill_stats = process_skills(skills)

print("Member stats:", member_stats)
print("Weekly stats:", weekly_stats)
print("Skill stats: ", skill_stats)

# Step 3: Full Dashboard Output
print()

W = 52
print("=" * W)
print(f"  SMP COMMAND CENTRE DASHBOARD  |  Week {weekly['week']}")
print("=" * W)

print("\n  SECTION 1: MEMBER PERFORMANCE")
print(f"  {'Total members:':<28} {member_stats['total']}")
print(f"  {f'Hit {STEP_GOAL:,} step goal:':<28} {member_stats['goal_met']}/{member_stats['total']}")
print(f"  {'Average steps:':<28} {member_stats['avg_steps']:,}")
print(f"  {'Cold showers today:':<28} {member_stats['cold_showers']}/{member_stats['total']}")
print(f"  Goal hitters: {', '.join(m['name'] for m in members if m['steps'] >= STEP_GOAL)}")

print("\n  SECTION 2: WEEKLY STEPS")
for day, total in zip(weekly["days"], weekly["daily_totals"]):
    bar = "#" * (total // 5000)
    print(f"  {day:4} {total:>7,}  {bar}")
print(f"  Best day: {weekly_stats['best_day']} ({weekly_stats['best_total']:,} total steps)")
print(f"  Week avg: {weekly_stats['weekly_avg']:,} steps/day")

print("\n  SECTION 3: ACTIVE SMP SKILLS")
for s in sorted(skills["skills"], key=lambda x: -x["enrolled"]):
    print(f"  {s['name']:15} {s['enrolled']} enrolled")
print(f"  Most popular: {skill_stats['most_popular']} ({skill_stats['top_enrollment']} enrolled)")

print(f"\n{'=' * W}")

# JSON export
export = {
    "week": weekly["week"],
    "members": {
        "total": member_stats["total"],
        "goal_met": member_stats["goal_met"],
        "avg_steps": member_stats["avg_steps"]
    },
    "weekly": {
        "best_day": weekly_stats["best_day"],
        "total_steps": weekly_stats["total_steps"]
    },
    "skills": {
        "active": skill_stats["active_count"],
        "most_popular": skill_stats["most_popular"]
    }
}
print("\nJSON export:")
print(json.dumps(export, indent=2))
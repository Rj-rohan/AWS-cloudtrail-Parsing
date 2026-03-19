"""
Test log generator for CloudProof.
Generates realistic CloudTrail-format events and injects them directly
into the scoring engine for a given username — no S3 or AWS needed.

Usage:
    python generate_test_logs.py --username testuser --days 90
"""

import argparse
import json
import random
import uuid
from datetime import datetime, timedelta
from database import execute_query
from ingestion import store_activities
from scoring import calculate_score, DAILY_SCORE_CAP, SERVICE_DAILY_CAP, ACTION_DAILY_CAP

# Realistic CloudTrail actions to simulate
SIMULATED_EVENTS = [
    ("ec2", "RunInstances"),
    ("ec2", "TerminateInstances"),
    ("ec2", "StopInstances"),
    ("ec2", "StartInstances"),
    ("ec2", "CreateVpc"),
    ("ec2", "DeleteVpc"),
    ("ec2", "CreateSecurityGroup"),
    ("ec2", "AuthorizeSecurityGroupIngress"),
    ("s3", "CreateBucket"),
    ("s3", "DeleteBucket"),
    ("s3", "PutBucketPolicy"),
    ("iam", "CreateRole"),
    ("iam", "AttachRolePolicy"),
    ("iam", "CreatePolicy"),
    ("lambda", "CreateFunction"),
    ("lambda", "UpdateFunctionCode"),
    ("lambda", "InvokeFunction"),
    ("rds", "CreateDBInstance"),
    ("rds", "DeleteDBInstance"),
    ("cloudformation", "CreateStack"),
    ("cloudformation", "UpdateStack"),
    ("cloudformation", "DeleteStack"),
    ("eks", "CreateCluster"),
]

# Weights — more common actions appear more often
WEIGHTS = [
    8, 3, 5, 5, 2, 1, 6, 6,   # ec2
    4, 1, 2,                    # s3
    3, 3, 2,                    # iam
    4, 5, 8,                    # lambda
    2, 1,                       # rds
    3, 3, 1,                    # cloudformation
    1,                          # eks
]


def get_user_id(username: str) -> int:
    rows = execute_query(
        "SELECT id FROM users WHERE username = %s", (username,), fetch=True
    )
    if not rows:
        raise SystemExit(f"No profile found for username '{username}'. Create one first at http://localhost:3000/")
    return rows[0]["id"]


def generate_activities(user_id: int, days: int) -> list:
    today = datetime.now().date()
    activities = []

    for day_offset in range(days, 0, -1):
        date = today - timedelta(days=day_offset)

        # Skip ~30% of days to make the heatmap look realistic (gaps)
        if random.random() < 0.30:
            continue

        # Between 2 and 12 events on active days
        num_events = random.randint(2, 12)
        events_today = random.choices(SIMULATED_EVENTS, weights=WEIGHTS, k=num_events)

        daily_total = 0
        service_totals = {}
        action_totals = {}

        for event_source, event_name in events_today:
            service = event_source.upper()
            score = calculate_score(service, event_name)
            if score <= 0:
                continue

            service_key = f"{date}_{service}"
            action_key = f"{date}_{service}_{event_name}"

            service_totals.setdefault(service_key, 0)
            action_totals.setdefault(action_key, 0)

            if daily_total >= DAILY_SCORE_CAP:
                break
            if service_totals[service_key] >= SERVICE_DAILY_CAP:
                continue
            if action_totals[action_key] >= ACTION_DAILY_CAP:
                continue

            activities.append({
                "user_id": user_id,
                "date": date,
                "service": service,
                "action": event_name,
                "score": score,
                "event_id": str(uuid.uuid4()),  # unique per generated event
            })

            daily_total += score
            service_totals[service_key] += score
            action_totals[action_key] += score

    return activities


def main():
    parser = argparse.ArgumentParser(description="Generate test CloudTrail activity for a CloudProof profile")
    parser.add_argument("--username", required=True, help="Target username")
    parser.add_argument("--days", type=int, default=90, help="Number of past days to generate activity for (default: 90)")
    args = parser.parse_args()

    print(f"Looking up profile '{args.username}'...")
    user_id = get_user_id(args.username)

    print(f"Generating {args.days} days of simulated AWS activity...")
    activities = generate_activities(user_id, args.days)

    if not activities:
        print("No scoreable activities generated.")
        return

    print(f"Storing {len(activities)} scored events...")
    store_activities(activities)

    # Summary
    total_score = sum(a["score"] for a in activities)
    services_used = set(a["service"] for a in activities)
    active_days = len(set(a["date"] for a in activities))

    print(f"\nDone!")
    print(f"  Active days  : {active_days}")
    print(f"  Total events : {len(activities)}")
    print(f"  Total score  : {total_score}")
    print(f"  Services     : {', '.join(sorted(services_used))}")
    print(f"\nView your profile at: http://localhost:3000/{args.username}")


if __name__ == "__main__":
    main()

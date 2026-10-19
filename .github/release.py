# Runs every 5 minutes (see release.yml). Publishes or withdraws puzzle unlock tokens to match schedule.json.
import json, os
from datetime import datetime, timedelta, timezone

tokens = json.loads(os.environ["TOKENS"])           # secret: {"2": "...", "3": "...", ...}
sched = json.load(open("schedule.json"))
now = datetime.now(timezone.utc)
launch = sched.get("launch")
start = datetime.fromisoformat(launch.replace("Z", "+00:00")) if launch else None
os.makedirs("r", exist_ok=True)
for n, hours in sched["offsets"].items():
    due = True if start is None else now >= start + timedelta(hours=float(hours))
    path = "r/%s.json" % n
    if due and n in tokens and not os.path.exists(path):
        json.dump({"t": tokens[n]}, open(path, "w")); print("released puzzle", n)
    elif not due and os.path.exists(path):
        os.remove(path); print("locked puzzle", n)
print("done at", now.isoformat(), "| launch:", launch)

import datetime
from pathlib import Path

STATE_FILE = Path("/tmp/last_wakeup.txt")

def is_first_wakeup_today():
    today = datetime.date.today().isoformat()
    if not STATE_FILE.exists():
        STATE_FILE.write_text(today)
        return True
    last = STATE_FILE.read_text().strip()
    if last != today:
        STATE_FILE.write_text(today)
        return True
    return False

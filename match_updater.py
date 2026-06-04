import requests
import schedule
import threading
import time
from datetime import datetime, timedelta
from database import get_matches, set_matches, get_all_users
from config import FOOTBALL_API

LEAGUES = {
    "Premier League": 2021,
    "La Liga": 2014,
    "Champions League": 2001,
    "Serie A": 2019,
    "Bundesliga": 2002
}

def fetch_matches():
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    matches = []
    headers = {"X-Auth-Token": FOOTBALL_API}
    for league_name, league_id in LEAGUES.items():
        try:
            url = f"https://api.football-data.org/v4/competitions/{league_id}/matches"
            params = {"dateFrom": today, "dateTo": tomorrow, "status": "SCHEDULED,TIMED"}
            r = requests.get(url, headers=headers, params=params, timeout=10)
            if r.status_code == 200:
                data = r.json()
                for m in data.get("matches", []):
                    utc_time = m["utcDate"][:16].replace("T", " ")
                    matches.append({
                        "id": m["id"],
                        "league": league_name,
                        "home": m["homeTeam"]["name"],
                        "away": m["awayTeam"]["name"],
                        "time": utc_time,
                        "status": m["status"],
                        "finished": False
                    })
        except Exception as e:
            print(f"API error {league_name}: {e}")
    return matches

def check_finished_matches():
    matches = get_matches()
    if not matches:
        return
    headers = {"X-Auth-Token": FOOTBALL_API}
    updated = []
    for m in matches:
        try:
            r = requests.get(
                f"https://api.football-data.org/v4/matches/{m['id']}",
                headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                status = data.get("status", "")
                if status in ["FINISHED", "AWARDED"]:
                    m["finished"] = True
                    m["status"] = "FINISHED"
                else:
                    updated.append(m)
            else:
                updated.append(m)
        except:
            updated.append(m)
    set_matches(updated)
    print(f"Матчтар жаңыланды: {len(updated)} активдүү")

def update_matches_job(bot):
    print("Матчтар жүктөлүүдө...")
    matches = fetch_matches()
    set_matches(matches)
    print(f"{len(matches)} матч табылды")

def notify_upcoming(bot):
    from datetime import datetime, timedelta
    matches = get_matches()
    now = datetime.utcnow()
    for m in matches:
        try:
            match_time = datetime.strptime(m["time"], "%Y-%m-%d %H:%M")
            diff = match_time - now
            if timedelta(hours=23) < diff < timedelta(hours=25):
                users = get_all_users()
                text = (
                    f"🔔 *Эртең чоң матч!*\n\n"
                    f"⚽ {m['home']} vs {m['away']}\n"
                    f"🏆 {m['league']}\n"
                    f"🕐 {m['time']} UTC\n\n"
                    f"📊 Анализ алуу үчүн боттон: ⚽ Спорт анализ"
                )
                for uid in list(users.keys())[:200]:
                    try:
                        bot.send_message(int(uid), text, parse_mode="Markdown")
                        time.sleep(0.05)
                    except:
                        pass
        except:
            pass

def start_match_updater(bot):
    update_matches_job(bot)
    schedule.every(6).hours.do(update_matches_job, bot)
    schedule.every(30).minutes.do(check_finished_matches)
    schedule.every(1).hours.do(notify_upcoming, bot)
    print("Match updater иштеп баштады")

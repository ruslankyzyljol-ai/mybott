import json
import os

DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}, "links": {}, "matches": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user(user_id):
    db = load_db()
    uid = str(user_id)
    if uid not in db["users"]:
        db["users"][uid] = {
            "id": user_id,
            "vip": False,
            "vip_until": None,
            "referrals": [],
            "referred_by": None,
            "lang": "ky",
            "joined": str(__import__("datetime").datetime.now())
        }
        save_db(db)
    return db["users"][uid]

def save_user(user_id, data):
    db = load_db()
    db["users"][str(user_id)] = data
    save_db(db)

def get_all_users():
    db = load_db()
    return db["users"]

def get_link(bm_key):
    db = load_db()
    return db.get("links", {}).get(bm_key, None)

def set_link(bm_key, link, promo):
    db = load_db()
    if "links" not in db:
        db["links"] = {}
    db["links"][bm_key] = {"link": link, "promo": promo}
    save_db(db)

def get_matches():
    db = load_db()
    return db.get("matches", [])

def set_matches(matches):
    db = load_db()
    db["matches"] = matches
    save_db(db)

def is_vip(user_id):
    import datetime
    user = get_user(user_id)
    if not user.get("vip"):
        return False
    if user.get("vip_until"):
        until = datetime.datetime.fromisoformat(user["vip_until"])
        if datetime.datetime.now() > until:
            user["vip"] = False
            user["vip_until"] = None
            save_user(user_id, user)
            return False
    return True

def set_vip(user_id, days):
    import datetime
    user = get_user(user_id)
    user["vip"] = True
    user["vip_until"] = str(datetime.datetime.now() + datetime.timedelta(days=days))
    save_user(user_id, user)

def add_referral(referrer_id, new_user_id):
    from config import VIP_REFERRAL_DAYS
    db = load_db()
    uid = str(referrer_id)
    if uid in db["users"]:
        refs = db["users"][uid].get("referrals", [])
        if str(new_user_id) not in refs:
            refs.append(str(new_user_id))
            db["users"][uid]["referrals"] = refs
            save_db(db)
            count = len(refs)
            for needed, days in sorted(VIP_REFERRAL_DAYS.items()):
                if count == needed:
                    set_vip(referrer_id, days)
                    return days
    return 0

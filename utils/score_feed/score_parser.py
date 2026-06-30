import nextcord

import requests
from utils.score_feed import customizations

from utils import scoresaber, accsaber

def parse_score(score_id, bot_data):
    score_data = requests.get(f"https://scoresaber.com/api/v2/scores/{score_id}").json()
    user_customizations = customizations.get_user_customizations(score_data["score"]["player"]["id"], "scoresaber", bot_data)
    separator = user_customizations["separator"]["text"]

    converted_data = {
        "name": score_data["score"]["player"]["name"],
        "pfp": score_data["score"]["player"]["avatar"],
        "id": score_data["score"]["player"]["id"],
        "map_id": score_data["leaderboard"]["map"]["id"],
        "difficulty_id": score_data["leaderboard"]["difficulty"]["id"],
        "scoreId": score_data["score"]["id"],
        "modifiers": score_data["score"]["mods"],
        "characteristic": score_data["leaderboard"]["difficulty"]["gameMode"][4:],
        "difficulty": score_data["leaderboard"]["difficulty"]["gameMode"][4:] + " " + scoresaber.convert_difficulty(score_data["leaderboard"]["difficulty"]["difficulty"]),
        "songName": score_data["leaderboard"]["map"]["songName"],
        "songCode": score_data["leaderboard"]["map"]["bsid"],
        "coverImage": score_data["leaderboard"]["map"]["coverUrl"],
        "score": score_data["score"]["modifiedScore"],
        "acc": round(score_data["score"]["accuracy"] * 100, 2),
        "mistakes": score_data["score"]["missedNotes"] + score_data["score"]["badCuts"],
        "misses": score_data["score"]["missedNotes"],
        "badCuts": score_data["score"]["badCuts"],
        "rank": score_data["score"]["rank"],
        "max_combo": score_data["score"]["maxCombo"],
        "pp": round(score_data["score"]["pp"], 2),
        "stars": score_data["leaderboard"]["realm"]["stars"],
        "fc_acc": round(score_data["scoreStats"]["fcAcc"] * 100, 2),
        "left_avg": round(score_data["scoreStats"]["accLeft"], 2),
        "right_avg": round(score_data["scoreStats"]["accRight"], 2),
        "left_td": round(score_data["scoreStats"]["leftTimeDependence"], 2),
        "right_td": round(score_data["scoreStats"]["rightTimeDependence"], 2),
        "left_mistakes": score_data["scoreStats"]["leftMiss"] + score_data["scoreStats"]["leftBadCuts"],
        "left_misses": score_data["scoreStats"]["leftMiss"],
        "left_bad_cuts": score_data["scoreStats"]["leftBadCuts"],
        "right_mistakes": score_data["scoreStats"]["rightMiss"] + score_data["scoreStats"]["rightBadCuts"],
        "right_misses": score_data["scoreStats"]["rightMiss"],
        "right_bad_cuts": score_data["scoreStats"]["rightBadCuts"],
        "full_swing_acc": round(score_data["scoreStats"]["underswingStats"]["fullSwingAcc"], 2),
        "full_swing_fc_acc": round(score_data["scoreStats"]["underswingStats"]["fullSwingFcAcc"], 2),
        "115_streak": score_data["scoreStats"]["max115Streak"],
        "fc_pp": scoresaber.calculate_pp(score_data["scoreStats"]["fcAcc"] * 100,score_data["leaderboard"]["realm"]["stars"]),
        "full_swing_pp": scoresaber.calculate_pp(score_data["scoreStats"]["underswingStats"]["fullSwingAcc"],score_data["leaderboard"]["realm"]["stars"]),
        "full_swing_fc_pp": scoresaber.calculate_pp(score_data["scoreStats"]["underswingStats"]["fullSwingFcAcc"],score_data["leaderboard"]["realm"]["stars"]),
        "separated_mistakes": f"{score_data["scoreStats"]["leftMiss"] + score_data["scoreStats"]["leftBadCuts"]}{separator}{score_data["scoreStats"]["rightMiss"] + score_data["scoreStats"]["rightBadCuts"]}",
        "separated_misses": f"{score_data["scoreStats"]["leftMiss"]}{separator}{score_data["scoreStats"]["rightMiss"]}",
        "separated_bad_cuts": f"{score_data["scoreStats"]["leftBadCuts"]}{separator}{score_data["scoreStats"]["rightBadCuts"]}",
        "separated_avg": f"{round(score_data["scoreStats"]["accLeft"],2)}{separator}{round(score_data["scoreStats"]["accRight"],2)}",
        "separated_td": f"{round(score_data["scoreStats"]["leftTimeDependence"],2)}{separator}{round(score_data["scoreStats"]["rightTimeDependence"],2)}",
        "full_swing_points": score_data["scoreStats"]["underswingStats"]["fullSwingScore"],
        "under_swing_points": score_data["scoreStats"]["underswingStats"]["fullSwingScore"] - score_data["score"]["modifiedScore"],
        "empty": ""
    }
    if converted_data["mistakes"] == 0:
        converted_data["fc_pp"] = converted_data["pp"]
    accsaber_score_data = requests.get(f"https://api.accsaberreloaded.com/v1/maps/by-code/{converted_data["songCode"]}?difficulty={accsaber.convert_difficulty(score_data["leaderboard"]["difficulty"]["difficulty"])}&characteristic={converted_data["characteristic"]}").json()
    difficulties = accsaber_score_data.get("difficulties", [])
    if len(difficulties) > 0:
        converted_accsaber_data = {
            "complexity": accsaber_score_data["difficulties"][0]["complexity"],
            "ap": accsaber.calculate_ap(accsaber_score_data["difficulties"][0]["complexity"], score_data["score"]["accuracy"] * 100),
            "acc_saber_difficulty": accsaber.convert_difficulty(score_data["leaderboard"]["difficulty"]["difficulty"])
        }
    else:
        converted_accsaber_data = {
            "complexity": 0,
            "ap": 0,
            "acc_saber_difficulty": "UNKNOWN"
        }

    converted_data = {**converted_data, **converted_accsaber_data}

    if converted_data["rank"] == 1:
        converted_data["color"] = nextcord.Color.red()
    elif converted_data["rank"] <= 10:
        converted_data["color"] = nextcord.Color.dark_purple()
    elif converted_data["rank"] <= 25:
        converted_data["color"] = nextcord.Color.green()
    elif converted_data["rank"] <= 50:
        converted_data["color"] = nextcord.Color.yellow()
    else:
        converted_data["color"] = nextcord.Color.light_gray()
    return converted_data
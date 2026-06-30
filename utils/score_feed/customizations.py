import re

pattern = re.compile(r"{([a-zA-Z0-9_]+)}")

def parse_user_input(user_input: str):
    match = pattern.search(user_input)
    if not match:
        return user_input, "Empty", ""

    start, end = match.span()
    data = match.group(1)

    prefix = user_input[:start]
    suffix = user_input[end:]

    return prefix, data, suffix

def load_customizations(ss_id, leaderboard, bot_data):
    user_entry = bot_data.get("user_data", {}).get(ss_id, {})
    custom_fields = user_entry.get("score_feed_custom_elements", {})
    replay_colors = user_entry.get("score_feed_replay_settings", {})

    common = custom_fields.get("common", {})
    specific = custom_fields.get(leaderboard, {})

    return {**common, **specific, **replay_colors}

def get_user_customizations(ss_id, leaderboard, bot_data):
    elements = load_customizations(ss_id, leaderboard, bot_data)
    customizations = {}

    if "slot1" in elements:
        customizations["slot1"] = elements["slot1"]
    else:
        customizations["slot1"] = {
            "prefix": "#",
            "data": "rank",
            "suffix": ""
        }

    if "slot2" in elements:
        customizations["slot2"] = elements["slot2"]
    else:
        customizations["slot2"] = {
            "prefix": "",
            "data": "acc",
            "suffix": "%"
        }

    if "slot3" in elements:
        customizations["slot3"] = elements["slot3"]
    else:
        if leaderboard == "scoresaber":
            customizations["slot3"] = {
                "prefix": "",
                "data": "pp",
                "suffix": "pp"
            }
        elif leaderboard == "accsaber":
            customizations["slot3"] = {
                "prefix": "",
                "data": "ap",
                "suffix": "ap"
            }
        else:
            customizations["slot3"] = {
                "prefix": "Unranked",
                "data": "empty",
                "suffix": ""
            }

    if "slot4" in elements:
        customizations["slot4"] = elements["slot4"]
    else:
        if leaderboard == "scoresaber":
            customizations["slot4"] = {
                "prefix": "Difficulty ⭐ ",
                "data": "stars",
                "suffix": ""
            }
        elif leaderboard == "accsaber":
            customizations["slot4"] = {
                "prefix": "Difficulty ⭐ ",
                "data": "complexity",
                "suffix": ""
            }
        else:
            customizations["slot4"] = {
                "prefix": "Unranked",
                "data": "empty",
                "suffix": ""
            }

    if "slot5" in elements:
        customizations["slot5"] = elements["slot5"]
    else:
        customizations["slot5"] = {
            "prefix": "Max Combo 📈 ",
            "data": "max_combo",
            "suffix": ""
        }

    if "slot6" in elements:
        customizations["slot6"] = elements["slot6"]
    else:
        customizations["slot6"] = {
            "prefix": "Mistakes ❌ ",
            "data": "mistakes",
            "suffix": ""
        }

    if "slot7" in elements:
        customizations["slot7"] = elements["slot7"]
    else:
        customizations["slot7"] = {
            "prefix": "",
            "data": "empty",
            "suffix": ""
        }

    if "slot8" in elements:
        customizations["slot8"] = elements["slot8"]
    else:
        customizations["slot8"] = {
            "prefix": "",
            "data": "empty",
            "suffix": ""
        }

    if "slot9" in elements:
        customizations["slot9"] = elements["slot9"]
    else:
        customizations["slot9"] = {
            "prefix": "",
            "data": "empty",
            "suffix": ""
        }

    if "emoji" in elements:
        customizations["emoji"] = elements['emoji']
    else:
        if leaderboard == "scoresaber":
            customizations["emoji"] = {
                "text": "<:scoresaber:1503850957690110083> "
            }
        elif leaderboard == "accsaber":
            customizations["emoji"] = {
                "text": "<:accsaber_reloaded:1503871833647222815> "
            }
        else:
            customizations["emoji"] = {
                "text": ""
            }

    if "separator" in elements:
        customizations["separator"] = elements['separator']
    else:
        customizations["separator"] = {
            "text": f" / "
        }

    if "left_note_color" in elements:
        customizations["left_note_color"] = elements['left_note_color']
    else:
        customizations["left_note_color"] = None

    if "right_note_color" in elements:
        customizations["right_note_color"] = elements['right_note_color']
    else:
        customizations["right_note_color"] = None

    return customizations
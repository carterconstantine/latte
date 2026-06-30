import nextcord
import json
import urllib.parse

from utils.score_feed import customizations

def render_slot(slot: dict, data: dict):
    key = slot.get("data")

    if not key or key == "Empty":
        return f"{slot.get('prefix', '')}{slot.get('suffix', '')}"

    value = data.get(key)
    if value is None:
        value = f"[invalid key: {key}]"

    return f"{slot.get('prefix', '')}{value}{slot.get('suffix', '')}"


def build_embed(data, leaderboard, bot_data):
    user_customizations = customizations.get_user_customizations(data["id"], leaderboard, bot_data)

    emoji = user_customizations["emoji"]["text"]
    separator = user_customizations["separator"]["text"]
    slot1 = render_slot(user_customizations["slot1"], data)
    slot2 = render_slot(user_customizations["slot2"], data)
    slot3 = render_slot(user_customizations["slot3"], data)
    slot4 = render_slot(user_customizations["slot4"], data)
    slot5 = render_slot(user_customizations["slot5"], data)
    slot6 = render_slot(user_customizations["slot6"], data)
    slot7 = render_slot(user_customizations["slot7"], data)
    slot8 = render_slot(user_customizations["slot8"], data)
    slot9 = render_slot(user_customizations["slot9"], data)

    embed = nextcord.Embed(
        title=f"**{data['name']}** scored on **{data['songName']}** [{data['difficulty']}]!",
        description=f"# {emoji}**{slot1}**{separator}**{slot2}**{separator}**{slot3}**",
        color=data["color"],
        url=f"https://beatsaver.com/maps/{data['songCode']}"
    )

    embed.set_thumbnail(url=data['coverImage'])
    embed.set_author(
        name=data['name'],
        icon_url=data['pfp'],
        url=f"https://scoresaber.com/u/{data['id']}"
    )

    if slot4 != "":
        embed.add_field(name=slot4, value="\u200B", inline=True)
    if slot5 != "":
        embed.add_field(name=slot5, value="\u200B", inline=True)
    if slot6 != "":
        embed.add_field(name=slot6, value="\u200B", inline=True)
    if slot7 != "":
        embed.add_field(name=slot7, value="\u200B", inline=True)
    if slot8 != "":
        embed.add_field(name=slot8, value="\u200B", inline=True)
    if slot9 != "":
        embed.add_field(name=slot9, value="\u200B", inline=True)

    return embed

def build_view(data, leaderboard, bot_data):
    user_customizations = customizations.get_user_customizations(data["id"], leaderboard, bot_data)

    view = nextcord.ui.View()
    if leaderboard == "scoresaber":
        view.add_item(nextcord.ui.Button(
            label="View on ScoreSaber",
            url=f"https://scoresaber.com/map/{data['map_id']}/difficulty/{data['difficulty_id']}",
        ))
    if leaderboard == "accsaber":
        view.add_item(nextcord.ui.Button(
            label="View on AccSaber Reloaded",
            url=f"https://accsaberreloaded.com/maps/{data['songCode']}?difficulty={data['acc_saber_difficulty'].lower()}"
        ))

    settings_override = {
        "Bools": {
            "firstpersonreplay": True,
            "staticlightswarningacknowledged": True
        }
    }

    if user_customizations["left_note_color"]:
        settings_override["Bools"]["coloroverride"] = True
        settings_override["Bools"]["chromaobjectcolors"] = False
        settings_override["Bools"]["difficultycolors"] = False

        settings_override.setdefault("Floats", {})

        settings_override["Floats"]["rightnotecolor.r"] = user_customizations["left_note_color"]["r"]
        settings_override["Floats"]["rightnotecolor.g"] = user_customizations["left_note_color"]["g"]
        settings_override["Floats"]["rightnotecolor.b"] = user_customizations["left_note_color"]["b"]

    if user_customizations["right_note_color"]:
        settings_override["Bools"]["coloroverride"] = True
        settings_override["Bools"]["chromaobjectcolors"] = False
        settings_override["Bools"]["difficultycolors"] = False

        settings_override.setdefault("Floats", {})

        settings_override["Floats"]["rightnotecolor.r"] = user_customizations["right_note_color"]["r"]
        settings_override["Floats"]["rightnotecolor.g"] = user_customizations["right_note_color"]["g"]
        settings_override["Floats"]["rightnotecolor.b"] = user_customizations["right_note_color"]["b"]

    json_str = json.dumps(settings_override)
    encoded = urllib.parse.quote(json_str)

    view.add_item(nextcord.ui.Button(
        label="Watch Replay",
        url=f"https://watch.scoresaber.com/?ssScoreId={data['scoreId']}&autoPlay=true&settingsOverride={encoded}"
    ))

    return view
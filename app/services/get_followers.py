import requests
from app.services.node_call import call_validUrl_js
import subprocess
import json


def curl_request(url, headers):
    # Créez une commande curl avec les en-têtes requis
    curl_command = ["curl", "-s", url, "-H", f"User-Agent: {headers['User-Agent']}"]

    # Exécute la commande et récupère la sortie
    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Erreur lors de l'exécution de la commande curl : {result.stderr}")
        return None

    try:
        return json.loads(result.stdout)  # Parse la sortie JSON
    except json.JSONDecodeError as e:
        print(f"❌ Erreur lors du parsing JSON : {e}")
        return None


def build_list_base_url(secUid, minCursor=0):
    """
    Construit l'URL de base pour l'endpoint 'list' avec les secUid et cursors donnés.
    """
    return (
        "https://www.tiktok.com/api/user/list/"
        "?WebIdLastTime=1738575538"
        "&aid=1988"
        "&app_language=fr"
        "&app_name=tiktok_web"
        "&browser_language=fr"
        "&browser_name=Mozilla"
        "&browser_online=true"
        "&browser_platform=MacIntel"
        "&browser_version=5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F123.0.0.0+Safari%2F537.36+Edg%2F123.0.0.0"
        "&channel=tiktok_web"
        "&cookie_enabled=true"
        "&count=30"
        "&data_collection_enabled=true"
        "&device_id=7467116746588145174"
        "&device_platform=web_pc"
        "&focus_state=true"
        "&from_page=user"
        "&history_len=14"
        "&is_fullscreen=true"
        "&is_page_visible=true"
        "&maxCursor=0"
        f"&minCursor={minCursor}"
        "&odinId=6624247328809172997"
        "&os=mac"
        "&priority_region=FR"
        "&referer="
        "&region=FR"
        "&scene=67"
        "&screen_height=1080"
        "&screen_width=1920"
        f"&secUid={secUid}"
        "&tz_name=Europe%2FParis"
        "&user_is_login=true"
        "&webcast_language=fr"
        "&msToken=riqlJPr42AMSGAwHu9g9z5PhCqn3Hzp-CjRpNH8XqPTcwNCehHnQqvP5BAgx7HwkuQfAcVxbttMfK3fGHZvUXYB__GZK7iWaYaItDzaDJxeVock0JIurABWe1b5T30PY61UM"
    )


def validate_list_url(secUid, maxCursor=0):
    """
    Construit l'URL de base avec secUid et maxCursor,
    appelle validUrl.js via call_validUrl_js, et renvoie (signed_url, user_agent).
    """
    base_url = build_list_base_url(secUid, maxCursor)
    result_json = call_validUrl_js(base_url)
    if not result_json:
        return None, None

    if result_json.get("status") == "ok":
        data = result_json.get("data", {})
        signed_url = data.get("signed_url")  # URL signée complète
        navigator_info = data.get("navigator", {})
        user_agent = navigator_info.get("user_agent", "")
        return signed_url, user_agent
    else:
        print("Statut différent de 'ok':", result_json)
        return None, None


def fetch_followers(secUid, maxCursor=0, all_followers=None):
    """
    Récupère récursivement la liste des followers d'un utilisateur TikTok.
    """
    if all_followers is None:
        all_followers = []

    # Re-signer l'URL pour le cursor courant
    signed_url, user_agent = validate_list_url(secUid, maxCursor)
    # print(f"🔗 URL signée pour maxCursor = {signed_url} : {user_agent}")
    if not signed_url:
        print("Impossible de signer l'URL pour maxCursor =", maxCursor)
        return all_followers

    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(signed_url, headers=headers)
        response.raise_for_status()  # Vérifie si la requête a échoué

        data = response.json()
        print("data", data)
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la requête HTTP : {e}")
        return all_followers
    except ValueError as e:
        print("❌ Erreur lors du parsing du JSON :", e)
        return all_followers

    user_list = data.get("userList", [])
    if not user_list:
        print("❌ Aucun follower trouvé pour maxCursor =", maxCursor)
        return all_followers

    # Ajouter les informations des followers à la liste globale
    for user_info in user_list:
        user = user_info.get("user", {})
        stats = user_info.get("stats", {})
        follower_details = {
            "userId": user.get("id"),
            "secUid": user.get("secUid"),
            "uniqueId": user.get("uniqueId"),
            "nickname": user.get("nickname"),
            "signature": user.get("signature", ""),
            "avatar": user.get("avatarLarger"),
            "followerCount": stats.get("followerCount", 0),
            "followingCount": stats.get("followingCount", 0),
            "heartCount": stats.get("heartCount", 0),
            "videoCount": stats.get("videoCount", 0),
        }
        all_followers.append(follower_details)

    # Pagination
    new_minCursor = data.get("minCursor", -1)
    has_more = data.get("hasMore", False)

    print(
        f"🔄 Pagination : nouveau maxCursor = {new_minCursor}, followers récupérés = {len(all_followers)}"
    )

    if has_more and new_minCursor != -1:
        # Appel récursif avec le nouveau maxCursor
        return fetch_followers(
            secUid, maxCursor=new_minCursor, all_followers=all_followers
        )
    else:
        return all_followers

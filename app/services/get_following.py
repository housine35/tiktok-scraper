import requests
from app.services.node_call import call_validUrl_js
import pandas as pd
import subprocess
import json


def build_following_base_url(secUid, minCursor=0):
    """
    Construit l'URL de base pour l'endpoint 'following' avec les secUid et cursors donnés.
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
        "&history_len=4"
        "&is_fullscreen=true"
        "&is_page_visible=true"
        "&maxCursor=0"
        f"&minCursor={minCursor}"
        "&odinId=6624247328809172997"
        "&os=mac"
        "&priority_region=FR"
        "&referer="
        "&region=FR"
        "&scene=21"
        "&screen_height=1080"
        "&screen_width=1920"
        f"&secUid={secUid}"
        "&tz_name=Europe%2FParis"
        "&user_is_login=true"
        "&webcast_language=fr"
        "&msToken=riqlJPr42AMSGAwHu9g9z5PhCqn3Hzp-CjRpNH8XqPTcwNCehHnQqvP5BAgx7HwkuQfAcVxbttMfK3fGHZvUXYB__GZK7iWaYaItDzaDJxeVock0JIurABWe1b5T30PY61UM"
    )


def validate_following_url(secUid, minCursor=0):
    """
    Construit l'URL de base avec secUid et maxCursor,
    appelle validUrl.js via call_validUrl_js, et renvoie (signed_url, user_agent).
    """
    base_url = build_following_base_url(secUid, minCursor)
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


def fetch_following(secUid, minCursor=0, all_following=None):
    """
    Récupère récursivement la liste des utilisateurs suivis par l'utilisateur TikTok en utilisant requests.
    """

    proxy = "http://sp42jw6ggi:o~zA4ntN53ZMkyq0lk@isp.smartproxy.com:10000"  # Format proxy
    proxies = {"http": proxy, "https": proxy}  # Configuration des proxies pour requests

    if all_following is None:
        all_following = []

    # Re-signer l'URL pour le cursor courant
    signed_url, user_agent = validate_following_url(secUid, minCursor)
    if not signed_url:
        print("Impossible de signer l'URL pour minCursor =", minCursor)
        return all_following

    # Construire les en-têtes HTTP
    headers = {"User-Agent": user_agent}

    try:
        # Envoyer la requête GET
        response = requests.get(signed_url, headers=headers, proxies=proxies)

        if response.status_code != 200:
            print(f"❌ Erreur HTTP {response.status_code} : {response.text}")
            return all_following

        data = response.json()  # Convertir la réponse en JSON

    except requests.RequestException as e:
        print(f"❌ Erreur de requête : {e}")
        return all_following
    except ValueError as e:
        print(f"❌ Erreur lors du parsing du JSON : {e}")
        return all_following

    user_list = data.get("userList", [])
    if not user_list:
        print("❌ Aucun utilisateur suivi trouvé pour minCursor =", minCursor)
        return all_following

    # Ajouter les informations des utilisateurs suivis à la liste globale
    for user_info in user_list:
        user = user_info.get("user", {})
        stats = user_info.get("stats", {})
        following_details = {
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
        all_following.append(following_details)

    # Pagination
    new_minCursor = data.get("minCursor", -1)
    has_more = data.get("hasMore", False)

    print(f"🔄 Pagination : nouveau minCursor = {new_minCursor}, utilisateurs suivis récupérés = {len(all_following)}")

    if has_more and new_minCursor != -1:
        # Appel récursif avec le nouveau minCursor
        return fetch_following(secUid, minCursor=new_minCursor, all_following=all_following)
    else:
        return all_following


""" if __name__ == "__main__":
    secUid = "MS4wLjABAAAAI8OMuXkz6jllqzW1aGEVKwyJ-z1rKL326qbZ4DOKFZbRO1ASMHVaqgZ6tEZFk22d"
    print("Fetching following users...\n")

    # Récupérer tous les utilisateurs suivis via la pagination récursive
    following = fetch_following(secUid)

    if following:
        print(f"✅ {len(following)} utilisateurs suivis récupérés.")
        for user in following:
            print(f"👤 {user['nickname']} (@{user['uniqueId']}) - {user['followerCount']} followers") """

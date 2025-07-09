import requests
import urllib.parse
from app.services.node_call import call_validUrl_js
import pandas as pd
import subprocess
import json
from datetime import datetime


def build_base_url(secUid, cursor):
    """
    Construit l'URL de base avec le secUid et la valeur de cursor donnée.
    """
    return (
        "https://www.tiktok.com/api/post/item_list/"
        "?WebIdLastTime=1725912395"
        "&aid=1988"
        "&app_language=en"
        "&app_name=tiktok_web"
        "&browser_language=en-US"
        "&browser_name=Mozilla"
        "&browser_online=true"
        "&browser_platform=Win32"
        "&browser_version=5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F123.0.0.0+Safari%2F537.36+Edg%2F123.0.0.0"
        "&channel=tiktok_web"
        "&cookie_enabled=true"
        "&count=30"
        f"&cursor={cursor}"
        "&coverFormat=2"
        "&data_collection_enabled=true"
        "&device_id=7412737227186685446"
        "&device_platform=web_pc"
        "&focus_state=true"
        "&from_page=user"
        "&history_len=4"
        "&is_fullscreen=false"
        "&is_page_visible=true"
        "&language=en"
        "&odinId=7410901337687491602"
        "&os=windows"
        "&priority_region="
        "&referer="
        "&region=SA"
        "&screen_height=1080"
        "&screen_width=1920"
        f"&secUid={secUid}"
        "&tz_name=Asia%2FRiyadh"
        "&user_is_login=true"
        "&webcast_language=en"
        "&msToken=riqlJPr42AMSGAwHu9g9z5PhCqn3Hzp-CjRpNH8XqPTcwNCehHnQqvP5BAgx7HwkuQfAcVxbttMfK3fGHZvUXYB__GZK7iWaYaItDzaDJxeVock0JIurABWe1b5T30PY61UM"
        "&verifyFp=verify_5b161567bda98b6a50c0414d99909d4b"
    )


def validate_url(secUid, cursor=0):
    """
    Construit l'URL de base avec secUid et cursor,
    appelle validUrl.js via call_validUrl_js,
    et renvoie (signed_url, user_agent).
    """
    base_url = build_base_url(secUid, cursor)
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


def fetch_all_posts(secUid, cursor=0, all_posts=None, user_info=None):
    """
    Récupère récursivement tous les posts d'un utilisateur TikTok en
    recalculant l'URL signée à chaque nouvelle valeur de cursor.
    """
    if all_posts is None:
        all_posts = []

    # Re-signer l'URL pour le cursor courant
    signed_url, user_agent = validate_url(secUid, cursor)
    if not signed_url:
        print("Impossible de signer l'URL pour cursor =", cursor)
        return {"user": user_info, "posts": all_posts}

    # Construire la commande curl
    curl_command = [
        "curl",
        "-s",  # Mode silencieux pour ne pas afficher les logs de curl
        "-A",
        user_agent,  # Spécifier l'User-Agent
        signed_url,  # URL signée
    ]

    try:
        # Exécuter la commande et récupérer la sortie JSON
        result = subprocess.run(curl_command, capture_output=True, text=True)
        response_text = result.stdout

        if result.returncode != 0:
            print(f"❌ Erreur lors de la requête curl : {result.stderr.strip()}")
            return {"user": user_info, "posts": all_posts}

        # Parser la réponse en JSON
        data = json.loads(response_text)

    except json.JSONDecodeError as e:
        print("❌ Erreur lors du parsing du JSON :", e)
        return {"user": user_info, "posts": all_posts}

    item_list = data.get("itemList", [])
    if not item_list:
        print("❌ Aucun post trouvé pour cursor =", cursor)
        return {"user": user_info, "posts": all_posts}

    # Sur le premier appel, extraire les infos utilisateur
    if user_info is None:
        first_post = item_list[0]
        author_data = first_post.get("author", {})
        author_stats = first_post.get("authorStats", {})
        user_info = {
            "id": author_data.get("id"),
            "nickname": author_data.get("nickname"),
            "uniqueId": author_data.get("uniqueId"),
            "secUid": author_data.get("secUid"),
            "avatar": author_data.get("avatarLarger"),
            "bio": author_data.get("signature", ""),
            "followerCount": author_stats.get("followerCount", 0),
            "followingCount": author_stats.get("followingCount", 0),
            "videoCount": author_stats.get("videoCount", 0),
            "likeCount": author_stats.get("heartCount", 0),
        }

    # Parcourir les posts de la page actuelle
    for item in item_list:
        challenges = item.get("challenges", [])
        hashtags = [ch.get("title") for ch in challenges if ch.get("title")]
        music_info = item.get("music", {})
        music = {
            "id": music_info.get("id"),
            "title": music_info.get("title"),
            "authorName": music_info.get("authorName"),
            "playUrl": music_info.get("playUrl"),
            "coverLarge": music_info.get("coverLarge"),
            "duration": music_info.get("duration"),
        }
        poi = item.get("poi", {})
        location = {
            "id": poi.get("id"),
            "name": poi.get("name"),
            "address": poi.get("address"),
            "city": poi.get("city"),
            "country": poi.get("country"),
        }
        stats = item.get("stats", {})
        statsV2 = item.get("statsV2", {})

        post_info = {
            "id": item.get("id"),
            "desc": item.get("desc", ""),
            "createTime": datetime.utcfromtimestamp(item.get("createTime")).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "videoUrl": "https://www.tiktok.com/@movedz/video/" + item.get("id"),
            "coverUrl": item.get("video", {}).get("cover"),
            "likeCount": stats.get("diggCount", 0),
            "commentCount": stats.get("commentCount", 0),
            "shareCount": stats.get("shareCount", 0),
            "viewCount": stats.get("playCount", 0),
            "collectCount": stats.get("collectCount", 0),
            "repostCount": statsV2.get("repostCount", "0"),
            "privateItem": item.get("privateItem", False),
            "duetEnabled": item.get("duetEnabled", False),
            "stitchEnabled": item.get("stitchEnabled", False),
            "hashtags": hashtags,
            "music": music,
            "location": location,
        }
        all_posts.append(post_info)

    # Afficher le nouveau cursor pour le débogage
    new_cursor = data.get("cursor", -1)
    print("🔄 Pagination : nouveau cursor =", new_cursor)

    has_more = data.get("hasMore", False)
    if has_more and new_cursor != -1:
        # Appel récursif avec le nouveau cursor
        return fetch_all_posts(
            secUid, cursor=new_cursor, all_posts=all_posts, user_info=user_info
        )
    else:
        print(f"✅ {len(all_posts)} posts récupérés.")
        # print(f"ℹ️ Informations utilisateur : {user_info}")
        # print(f"ℹ️ Informations utilisateur : {all_posts}")
        return {"user": user_info, "posts": all_posts}

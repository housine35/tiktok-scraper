import requests
import json
from app.services.node_call import call_validUrl_js


def build_comment_base_url(post_id, cursor=0):
    """
    Construit l'URL de base pour récupérer les commentaires d'un post.
    """
    return (
        f"https://www.tiktok.com/api/comment/list/"
        "?WebIdLastTime=1738575538"
        "&aid=1988"
        "&app_language=ja-JP"
        "&app_name=tiktok_web"
        f"&aweme_id={post_id}"
        "&browser_language=fr"
        "&browser_name=Mozilla"
        "&browser_online=true"
        "&browser_platform=MacIntel"
        "&browser_version=5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F123.0.0.0+Safari%2F537.36+Edg%2F123.0.0.0"
        "&channel=tiktok_web"
        "&cookie_enabled=true"
        "&count=20"
        "&current_region=JP"
        f"&cursor={cursor}"
        "&data_collection_enabled=true"
        "&device_id=7467116746588145174"
        "&device_platform=web_pc"
        "&enter_from=tiktok_web"
        "&focus_state=true"
        "&fromWeb=1"
        "&from_page=video"
        "&history_len=3"
        "&is_fullscreen=true"
        "&is_non_personalized=false"
        "&is_page_visible=true"
        "&odinId=6624247328809172997"
        "&os=mac"
        "&priority_region=FR"
        "&referer="
        "&region=FR"
        "&screen_height=1080"
        "&screen_width=1920"
        "&tz_name=Europe%2FParis"
        "&user_is_login=true"
        "&webcast_language=fr"
        "&msToken=riqlJPr42AMSGAwHu9g9z5PhCqn3Hzp-CjRpNH8XqPTcwNCehHnQqvP5BAgx7HwkuQfAcVxbttMfK3fGHZvUXYB__GZK7iWaYaItDzaDJxeVock0JIurABWe1b5T30PY61UM"
    )


def build_reply_base_url(post_id, comment_id, cursor=0):
    """
    Construit l'URL de base pour récupérer les réponses d'un commentaire en utilisant post_id, comment_id et cursor.
    """
    return (
        "https://www.tiktok.com/api/comment/list/reply/"
        "?WebIdLastTime=1738575538"
        "&aid=1988"
        "&app_language=ja-JP"
        "&app_name=tiktok_web"
        "&browser_language=fr"
        "&browser_name=Mozilla"
        "&browser_online=true"
        "&browser_platform=MacIntel"
        "&channel=tiktok_web"
        "&cookie_enabled=true"
        "&current_region=JP"
        f"&cursor={cursor}"
        "&data_collection_enabled=true"
        "&device_id=7467116746588145174"
        "&device_platform=web_pc"
        "&enter_from=tiktok_web"
        "&focus_state=true"
        "&fromWeb=1"
        "&from_page=video"
        "&history_len=3"
        "&is_page_visible=true"
        "&odinId=6624247328809172997"
        "&os=mac"
        "&priority_region=FR"
        "&referer="
        "&region=FR"
        "&screen_height=1080"
        "&screen_width=1920"
        "&tz_name=Europe%2FParis"
        "&user_is_login=true"
        "&webcast_language=fr"
        "&browser_version=5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F123.0.0.0+Safari%2F537.36+Edg%2F123.0.0.0"
        f"&comment_id={comment_id}"
        "&count=20"
        "&is_fullscreen=false"
        f"&item_id={post_id}"
        "&msToken=riqlJPr42AMSGAwHu9g9z5PhCqn3Hzp-CjRpNH8XqPTcwNCehHnQqvP5BAgx7HwkuQfAcVxbttMfK3fGHZvUXYB__GZK7iWaYaItDzaDJxeVock0JIurABWe1b5T30PY61UM"
    )


def validate_comment_url(post_id, cursor=0):
    """
    Génère l'URL signée pour récupérer les commentaires.
    """
    base_url = build_comment_base_url(post_id, cursor)
    result_json = call_validUrl_js(base_url)
    if not result_json or result_json.get("status") != "ok":
        print("Erreur lors de la signature de l'URL des commentaires")
        return None, None

    return result_json["data"]["signed_url"], result_json["data"]["navigator"][
        "user_agent"
    ]


def validate_reply_url(post_id, comment_id, cursor=0):
    """
    Génère l'URL signée pour récupérer les réponses à un commentaire spécifique.
    """
    base_url = build_reply_base_url(post_id, comment_id, cursor)
    result_json = call_validUrl_js(base_url)

    if not result_json or result_json.get("status") != "ok":
        print(f"Erreur lors de la signature de l'URL des réponses pour {comment_id}")
        return None, None

    return result_json["data"]["signed_url"], result_json["data"]["navigator"][
        "user_agent"
    ]


def extract_comment_details(post_id, comment):
    """
    Extrait les détails d'un commentaire.
    """
    return {
        "postId": post_id,
        "commentId": comment.get("cid"),
        "text": comment.get("text", ""),
        "userId": comment.get("user", {}).get("uid"),
        "userSecUid": comment.get("user", {}).get("secUid"),
        "userNickname": comment.get("user", {}).get("nickname"),
        "userAvatar": comment.get("user", {})
        .get("avatarThumb", {})
        .get("url_list", [None])[0],
        "createTime": comment.get("create_time"),
        "likeCount": comment.get("digg_count", 0),
        "replyCount": comment.get("reply_comment_total", 0),
        "replies": [],
    }


def fetch_replies(post_id, comment_id, cursor=0, all_replies=None):
    """
    Récupère récursivement les réponses d'un commentaire.
    """
    if all_replies is None:
        all_replies = []

    signed_url, user_agent = validate_reply_url(post_id, comment_id, cursor)
    if not signed_url:
        return all_replies

    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(signed_url, headers=headers)
        if response.status_code != 200:
            return all_replies

        data = response.json()

    except requests.RequestException:
        return all_replies
    except ValueError:
        return all_replies

    reply_list = data.get("comments", [])
    for reply in reply_list:
        reply_details = extract_comment_details(post_id, reply)
        all_replies.append(reply_details)

    return all_replies


def fetch_comments(post_id, cursor=0, all_comments=None):
    """
    Récupère récursivement les commentaires et leurs réponses.
    """
    if all_comments is None:
        all_comments = []

    signed_url, user_agent = validate_comment_url(post_id, cursor)
    if not signed_url:
        return all_comments

    headers = {"User-Agent": user_agent}

    try:
        response = requests.get(signed_url, headers=headers)
        if response.status_code != 200:
            return all_comments

        data = response.json()

    except requests.RequestException:
        return all_comments
    except ValueError:
        return all_comments

    comment_list = data.get("comments", [])
    for comment_info in comment_list:
        comment_details = extract_comment_details(post_id, comment_info)
        if comment_details["replyCount"] > 0:
            print(f"Fetching replies for {comment_details['commentId']}...")
            comment_details["replies"] = fetch_replies(
                post_id, comment_details["commentId"]
            )

        all_comments.append(comment_details)

    return all_comments


""" # Exemple d'utilisation
if __name__ == "__main__":
    post_id = "7469424380787854614"
    print("Fetching comments and replies...\n")

    comments = fetch_comments(post_id)

    if comments:
        for comment in comments:
            print(f"💬 {comment['userNickname']} : {comment['text']} - {comment['likeCount']} likes")
            for reply in comment["replies"]:
                print(f"   ↳ {reply['userNickname']} : {reply['text']} - {reply['likeCount']} likes") """

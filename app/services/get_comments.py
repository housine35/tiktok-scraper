import requests
import json
from app.services.node_call import call_validUrl_js
from urllib.parse import urlencode, parse_qs, urlparse

# User-Agent (use a consistent one, preferably from call_validUrl_js)
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
)

# msToken (replace with a valid, fresh token from your browser)
MSTOKEN = "G1lr_8nRB3udnK_fFzgBD7sxvc0PK6Osokd1IJMaVPVcoB4mwSW-D6MQjTdoJ2o20PLt_MWNgtsAr095wVSShdmn_XVFS34bURvakVglDyWAHncoV_jVJCRdiJRdbJBi_E_KD_G8vpFF9-aOaJrk"

# Base parameters (aligned with original code)
BASE_PARAMS = {
    "aid": "1988",
    "app_language": "en",
    "app_name": "tiktok_web",
    "browser_language": "en-US",
    "browser_name": "Mozilla",
    "browser_online": "true",
    "browser_platform": "MacIntel",
    "browser_version": "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "channel": "tiktok_web",
    "cookie_enabled": "true",
    "current_region": "US",
    "device_id": "7525351986981094934",
    "device_platform": "web_pc",
    "from_page": "video",
    "os": "mac",
    "priority_region": "US",
    "referer": "",
    "region": "US",
    "screen_height": "1117",
    "screen_width": "1728",
    "webcast_language": "en",
    "msToken": MSTOKEN,
}


def build_comment_base_url(post_id, cursor=0):
    """
    Constructs the base URL for fetching comments of a post.
    """
    params = {
        **BASE_PARAMS,
        "aweme_id": post_id,
        "cursor": str(cursor),
        "count": "20",
    }
    return f"https://www.tiktok.com/api/comment/list/?{urlencode(params)}"


def build_reply_base_url(post_id, comment_id, cursor=0):
    """
    Constructs the base URL for fetching replies to a comment.
    """
    params = {
        **BASE_PARAMS,
        "aweme_id": post_id,
        "comment_id": comment_id,
        "cursor": str(cursor),
        "count": "20",
    }
    return f"https://www.tiktok.com/api/comment/list/reply/?{urlencode(params)}"


def validate_url(base_url):
    """
    Generates a signed URL and headers for the API request.
    """
    result_json = call_validUrl_js(base_url)
    if not result_json or result_json.get("status") != "ok":
        print(f"Error signing URL: {result_json}")
        return None, None, None

    data = result_json.get("data", {})
    signed_url = data.get("signed_url")
    x_tt_params = data.get("x-tt-params")
    user_agent = data.get("navigator", {}).get("user_agent")
    return signed_url, x_tt_params, user_agent


def extract_comment_details(post_id, comment):
    """
    Extracts details from a comment.
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


def fetch_replies(post_id, comment_id, tiktok_account, cursor=0, all_replies=None):
    """
    Recursively fetches replies to a comment.
    """
    if all_replies is None:
        all_replies = []

    base_url = build_reply_base_url(post_id, comment_id, cursor)
    signed_url, x_tt_params, user_agent = validate_url(base_url)
    if not signed_url:
        print(f"Failed to get signed URL for replies of comment {comment_id}")
        return all_replies

    referer = f"{tiktok_account.rstrip('/')}/video/{post_id}"
    headers = {
        "User-Agent": user_agent or USER_AGENT,
        "Referer": referer,
        "X-Tt-Params": x_tt_params,
    }

    try:
        response = requests.get(signed_url, headers=headers)
        print(f"Reply fetch status for comment {comment_id}: {response.status_code}")
        print(f"Reply fetch response: {response.text[:200]}...")
        if response.status_code != 200:
            print(f"Reply request failed with status {response.status_code}")
            return all_replies

        data = response.json()
        reply_list = data.get("comments", [])
        if reply_list is None:
            print(f"No replies found for comment {comment_id}. Response: {data}")
            return all_replies

        for reply in reply_list:
            reply_details = extract_comment_details(post_id, reply)
            all_replies.append(reply_details)

        has_more = data.get("has_more", 0)
        if has_more:
            next_cursor = data.get("cursor", cursor + 20)
            return fetch_replies(
                post_id, comment_id, tiktok_account, next_cursor, all_replies
            )

    except requests.RequestException as e:
        print(f"Reply request error: {e}")
        return all_replies
    except ValueError as e:
        print(f"Reply JSON decode error: {e}")
        return all_replies

    return all_replies


def fetch_comments(post_id, tiktok_account, cursor=0, all_comments=None):
    """
    Recursively fetches comments and their replies.
    """
    if all_comments is None:
        all_comments = []

    base_url = build_comment_base_url(post_id, cursor)
    signed_url, x_tt_params, user_agent = validate_url(base_url)
    if not signed_url:
        print("Failed to generate signed URL")
        return all_comments

    referer = f"{tiktok_account.rstrip('/')}/video/{post_id}"
    headers = {
        "User-Agent": user_agent or USER_AGENT,
        "Referer": referer,
        "X-Tt-Params": x_tt_params,
    }

    try:
        response = requests.get(signed_url, headers=headers)
        print(f"Comment fetch status: {response.status_code}")
        print(f"Comment fetch response: {response.text[:200]}...")
        if response.status_code != 200:
            print(f"Comment request failed with status {response.status_code}")
            return all_comments

        data = response.json()
        comment_list = data.get("comments", [])
        if comment_list is None:
            print(f"No comments found for post {post_id}. Response: {data}")
            status_msg = data.get("status_msg", "")
            if status_msg:
                print(f"API status message: {status_msg}")
            has_more = data.get("has_more", 0)
            if has_more:
                next_cursor = data.get("cursor", cursor + 20)
                return fetch_comments(
                    post_id, tiktok_account, next_cursor, all_comments
                )
            return all_comments

        for comment_info in comment_list:
            comment_details = extract_comment_details(post_id, comment_info)
            if comment_details["replyCount"] > 0:
                print(f"Fetching replies for comment {comment_details['commentId']}...")
                comment_details["replies"] = fetch_replies(
                    post_id, comment_details["commentId"], tiktok_account
                )

            all_comments.append(comment_details)

        has_more = data.get("has_more", 0)
        if has_more:
            next_cursor = data.get("cursor", cursor + 20)
            return fetch_comments(post_id, tiktok_account, next_cursor, all_comments)

    except requests.RequestException as e:
        print(f"Comment request error: {e}")
        return all_comments
    except ValueError as e:
        print(f"Comment JSON decode error: {e}")
        return all_comments

    return all_comments


""" # Example usage
if __name__ == "__main__":
    post_id = "7497745342759292182"
    tiktok_account = "https://www.tiktok.com/@wahraniiaaa"
    print("Fetching comments and replies...\n")

    comments = fetch_comments(post_id, tiktok_account)

    if comments:
        for comment in comments:
            print(
                f"💬 {comment['userNickname']} : {comment['text']} - {comment['likeCount']} likes"
            )
            for reply in comment["replies"]:
                print(
                    f"   ↳ {reply['userNickname']} : {reply['text']} - {reply['likeCount']} likes"
                )
    else:
        print("No comments fetched.") """

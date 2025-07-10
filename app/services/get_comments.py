import requests
import json
from app.services.node_call import call_validUrl_js

# User-Agent from GitHub recommendation
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
)

# msToken (replace with a valid token from your browser)
MSTOKEN = "G1lr_8nRB3udnK_fFzgBD7sxvc0PK6Osokd1IJMaVPVcoB4mwSW-D6MQjTdoJ2o20PLt_MWNgtsAr095wVSShdmn_XVFS34bURvakVglDyWAHncoV_jVJCRdiJRdbJBi_E_KD_G8vpFF9-aOaJrk"


def build_comment_base_url(post_id, cursor=0):
    """
    Constructs the base URL for fetching comments of a post.
    """
    return (
        f"https://www.tiktok.com/api/comment/list/"
        f"?aweme_id={post_id}"
        f"&cursor={cursor}"
        "&count=20"
        f"&msToken={MSTOKEN}"
        "&aid=1988"
        "&app_language=ja-JP"
        "&app_name=tiktok_web"
        "&browser_language=en-US"
        "&browser_name=Mozilla"
        "&browser_online=true"
        "&browser_platform=Win32"
        "&browser_version=5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F110.0.0.0+Safari%2F537.36+Edg%2F110.0.1587.63"
        "&channel=tiktok_web"
        "&cookie_enabled=true"
        "¤t_region=JP"
        "&device_id=7165118680723998214"
        "&device_platform=web_pc"
        "&from_page=video"
        "&os=windows"
        "&priority_region=US"
        "&referer="
        "®ion=US"
        "&screen_height=1440"
        "&screen_width=2560"
        "&webcast_language=en"
    )


def build_reply_base_url(post_id, comment_id, cursor=0):
    """
    Constructs the base URL for fetching replies to a comment.
    """
    return (
        "https://www.tiktok.com/api/comment/list/reply/"
        f"?aweme_id={post_id}"
        f"&comment_id={comment_id}"
        f"&cursor={cursor}"
        "&count=20"
        f"&msToken={MSTOKEN}"
        "&aid=1988"
        "&app_language=ja-JP"
        "&app_name=tiktok_web"
        "&browser_language=en-US"
        "&browser_name=Mozilla"
        "&browser_online=true"
        "&browser_platform=Win32"
        "&browser_version=5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F110.0.0.0+Safari%2F537.36+Edg%2F110.0.1587.63"
        "&channel=tiktok_web"
        "&cookie_enabled=true"
        "¤t_region=JP"
        "&device_id=7165118680723998214"
        "&device_platform=web_pc"
        "&from_page=video"
        "&os=windows"
        "&priority_region=US"
        "&referer="
        "®ion=ALL"
        "&screen_height=1440"
        "&screen_width=2560"
        "&webcast_language=en"
    )


def validate_comment_url(post_id, cursor=0):
    """
    Generates a signed URL for fetching comments.
    """
    base_url = build_comment_base_url(post_id, cursor)
    result_json = call_validUrl_js(base_url)
    if not result_json or result_json.get("status") != "ok":
        print(f"Error signing comment URL: {result_json}")
        return None, None

    return result_json["data"]["signed_url"], result_json["data"]["navigator"][
        "user_agent"
    ]


def validate_reply_url(post_id, comment_id, cursor=0):
    """
    Generates a signed URL for fetching replies to a comment.
    """
    base_url = build_reply_base_url(post_id, comment_id, cursor)
    result_json = call_validUrl_js(base_url)
    if not result_json or result_json.get("status") != "ok":
        print(f"Error signing reply URL for comment {comment_id}: {result_json}")
        return None, None

    return result_json["data"]["signed_url"], result_json["data"]["navigator"][
        "user_agent"
    ]


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

    signed_url, user_agent = validate_reply_url(post_id, comment_id, cursor)
    if not signed_url:
        print(f"Failed to get signed URL for replies of comment {comment_id}")
        return all_replies

    # Construct Referer using tiktok_account and post_id
    referer = f"{tiktok_account.rstrip('/')}/{post_id}"
    print(referer)
    headers = {"User-Agent": user_agent or USER_AGENT, "Referer": referer}

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
            print(f"No replies found for comment {comment_id}")
            return all_replies

        for reply in reply_list:
            reply_details = extract_comment_details(post_id, reply)
            all_replies.append(reply_details)

        # Handle pagination
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

    signed_url, user_agent = validate_comment_url(post_id, cursor)
    if not signed_url:
        print("Failed to generate signed URL")
        return all_comments

    # Construct Referer using tiktok_account and post_id
    referer = f"{tiktok_account.rstrip('/')}/video/{post_id}"
    print(referer)
    headers = {"User-Agent": user_agent or USER_AGENT, "Referer": referer}

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

        # Handle pagination
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
            print(f"💬 {comment['userNickname']} : {comment['text']} - {comment['likeCount']} likes")
            for reply in comment["replies"]:
                print(f"   ↳ {reply['userNickname']} : {reply['text']} - {reply['likeCount']} likes")
    else:
        print("No comments fetched.") """

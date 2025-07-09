import time
import requests
from app.services.node_call import call_validUrl_js
import random

def build_hashtag_base_url(challengeID, cursor=0):
    """Builds the base URL for the TikTok hashtag endpoint with given challengeID and cursor."""
    return (
        "https://tiktok.com/api/challenge/item_list/"
        "?WebIdLastTime=1747923269"
        "&aid=1988"
        "&app_language=fr"
        "&app_name=tiktok_web"
        "&browser_language=fr"
        "&browser_name=Mozilla"
        "&browser_online=true"
        "&browser_platform=MacIntel"
        "&browser_version=5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/123.0.0.0+Safari/537.36+Edg/123.0.0.0"
        "&challengeID={}"
        "&channel=tiktok_web"
        "&cookie_enabled=true"
        "&count=30"
        "&cursor={}"
        "&data_collection_enabled=true"
        "&device_id=7480134572539463190"
        "&device_platform=web_pc"
        "&focus_state=true"
        "&from_page=hashtag"
        "&history_len=2"
        "&is_fullscreen=true"
        "&is_page_visible=true"
        "&language=fr"
        "&odinId=6624247328809172997"
        "&os=mac"
        "&priority_region=FR"
        "&region=FR"
        "&screen_height=1080"
        "&screen_width=1920"
        "&tz_name=Europe/Paris"
        "&user_is_login=true"
        "&webcast_language=fr"
        "&msToken=riqlJPr42AMSGAwHu9g9z5PhCqn3Hzp-CjRpNH8XqPTcwNCehHnQqvP5BAgx7HwkuQfAcVxbttMfK3fGHZvUXYB__GZK7iWaYaItDzaDJxeVock0JIurABWe1b5T30PY61UM"
    ).format(challengeID, cursor)

def validate_hashtag_url(challengeID, cursor=0):
    """Builds and signs the hashtag URL, returning the signed URL and user-agent."""
    base_url = build_hashtag_base_url(challengeID, cursor)
    result_json = call_validUrl_js(base_url)
    if not result_json:
        return None, None

    if result_json.get("status") == "ok":
        data = result_json.get("data", {})
        signed_url = data.get("signed_url")
        user_agent = data.get("navigator", {}).get("user_agent", "")
        return signed_url, user_agent
    print(f"Error: Invalid response status - {result_json}")
    return None, None

def send_request(signed_url, user_agent):
    """Sends a GET request with the signed URL and user-agent, returning JSON response."""
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(signed_url, headers=headers)
        if response.status_code == 200:
            print("✅ Request successful!")
            return response.json()
        print(f"❌ HTTP Error {response.status_code}: {response.text}")
        return None
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def fetch_hashtag_posts_recursive(challengeID, cursor=0, all_posts=None):
    """Recursively fetches all posts for a hashtag, handling pagination via cursor."""
    if all_posts is None:
        all_posts = []

    signed_url, user_agent = validate_hashtag_url(challengeID, cursor)
    if not signed_url or not user_agent:
        print("❌ Failed to get signed URL or user-agent.")
        return all_posts

    data = send_request(signed_url, user_agent)
    if not data:
        return all_posts

    item_list = data.get("itemList", [])
    if not item_list:
        print(f"❌ No posts found for cursor = {cursor}")
        print(data)
        return all_posts

    for item in item_list:
        video_info = item.get("video", {})
        author_info = item.get("author", {})
        post_details = {
            "authorUniqueId": author_info.get("uniqueId"),
            "desc": item.get("desc", ""),
            "playCount": video_info.get("playCount", 0),
            "shareCount": item.get("shareCount", 0),
            "commentCount": item.get("commentCount", 0),
            "likeCount": video_info.get("likeCount", 0),
            "videoUrl": video_info.get("playAddr", "")
        }
        all_posts.append(post_details)

    new_cursor = data.get("cursor", -1)
    print(f"🔄 Pagination: new cursor = {new_cursor}, posts fetched = {len(all_posts)}")

    if new_cursor != -1:
        time.sleep(random.uniform(5, 10))  # Random delay to avoid detection
        return fetch_hashtag_posts_recursive(challengeID, new_cursor, all_posts)
    return all_posts

if __name__ == "__main__":
    challenge_id = "959445"  # Hashtag challenge ID
    print("Fetching hashtag posts...\n")
    posts = fetch_hashtag_posts_recursive(challenge_id)
    if posts:
        print(f"✅ {len(posts)} posts fetched.")
        for post in posts:
            print(f"📹 @{post['authorUniqueId']} - {post['desc'][:50]}... - {post['playCount']} views")
    else:
        print("❌ No posts fetched.")
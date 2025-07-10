import hashlib
import requests
import time
import gzip
from io import BytesIO
from lib.XGorgon import XGorgon
from lib.XArgus import Argus
from lib.XLadon import Ladon

# Target URL parameters (updated with cursor=60)
params = "music_id=7328869241331370798&cursor=60&count=20&type=0&video_cover_shrink=372_495&from_group_id=7522286854184488247&could_lazy_loading=1&experiment_params=%7B%22detail_page_need_standardize_text%22%3A%201%2C%20%22detail_page_need_friend_tag%22%3A%201%7D&device_platform=android&os=android&ssmix=a&_rticket=1752156062782&cdid=a08bb181-6e61-4678-a146-71230db6d140&channel=googleplay&aid=1233&app_name=musical_ly&version_code=400703&version_name=40.7.3&manifest_version_code=2024007030&update_version_code=2024007030&ab_version=40.7.3&resolution=1440*2891&dpi=560&device_type=sdk_gphone64_x86_64&device_brand=google&language=en&os_api=36&os_version=16&ac=wifi&is_pad=0&app_type=normal&sys_region=US&last_install_time=1752144253&mcc_mnc=310260&timezone_name=Europe%2FParis&carrier_region_v2=310&app_language=en&carrier_region=US&ac2=wifi&uoo=0&op_region=US&timezone_offset=3600&build_number=40.7.3&host_abi=arm64-v8a&locale=en®ion=US&ts=1752156067&iid=7525402045219161870&device_id=7525401655916135949&openudid=f12cd9259c6d7bde"

# Cookie and X-Tt-Token (must be updated with a new capture from Proxyman if expired)
headers = {
    "Cookie": "store-idc=useast5; tt-target-idc=useast8; multi_sids=7525402143944295438%3A20a84ec6360df93b0fa603ce836987c5; cmpl_token=AgQQAPNSF-RPsLhRd8dl8Z038g4B3OKbv4_ZYN4PEw; sid_guard=20a84ec6360df93b0fa603ce836987c5%7C1752144433%7C15551999%7CTue%2C+06-Jan-2026+10%3A47%3A12+GMT; uid_tt=1b3a5c59c27758080e3a4852ecc1dc1c4fcf73832a34ca7be0c34979827f73fb; uid_tt_ss=1b3a5c59c27758080e3a4852ecc1dc1c4fcf73832a34ca7be0c34979827f73fb; sid_tt=20a84ec6360df93b0fa603ce836987c5; sessionid=20a84ec6360df93b0fa603ce836987c5; sessionid_ss=20a84ec6360df93b0fa603ce836987c5; store-country-code=us; store-country-code-src=uid; passport_csrf_token=206b667cdf6528e9ee25a2ccde0ebd2b; passport_csrf_token_default=206b667cdf6528e9ee25a2ccde0ebd2b; odin_tt=37f52210cd8f819e42c0dae2399500a039621ba51d9157d4f0cc483742fc830847816ca39e5c3e24bc251f625f53ae972a59b76036167b92ad58abe4b106adb9a1e6130a72aee00873e343e3defa2f01; msToken=MthB5Q29v-RYE-v9ahmyftU4SQWiEqRqcQN21zWNj4WH1fbhPGCBvOWK7L6HZ1CPTRJt4CR-_cEcyqhtRtsMPoYquLJkIMcLDIa-1OM5h065MxcURfN0IcV1Ew==; tt_ticket_guard_has_set_public_key=1; store-country-sign=MEIEDBE7adSo3b8XnzVEPgQguai37HbHdl2Iswase0U8zl81-w_WRL0wCp1qVdFzHOQEEEJxGJzlDkQkMaIS4rTEPgo"
}

# Update the timestamp
current_ts = int(time.time())
current_rticket = int(current_ts * 1000)
params = params.replace("ts=1752156067", f"ts={current_ts}")
params = params.replace("_rticket=1752156062782", f"_rticket={current_rticket}")

# Step 1: Generate X-Gorgon and X-Khronos
xg = XGorgon()
try:
    gorgon_result = xg.calculate(params, headers)
    print("Gorgon result:", gorgon_result)
    if gorgon_result is None or "X-Gorgon" not in gorgon_result or "X-Khronos" not in gorgon_result:
        raise ValueError("XGorgon.calculate() failed to return X-Gorgon or X-Khronos")
    x_gorgon = gorgon_result["X-Gorgon"]
    x_khronos = int(gorgon_result["X-Khronos"])
    print("x_khronos type:", type(x_khronos))
except Exception as e:
    print(f"Error in XGorgon.calculate(): {e}")
    exit(1)

# Step 2: Generate X-Argus
stub = None  # Replace with hashlib.md5(body.encode()).hexdigest() if POST
try:
    print("Calling Argus.get_sign with params:", params[:50] + "...", "timestamp:", x_khronos, "stub:", stub)
    x_argus = Argus.get_sign(params, timestamp=x_khronos, stub=stub)
    if x_argus is None:
        raise ValueError("Argus.get_sign() returned None")
    print("x_argus:", x_argus)
except Exception as e:
    print(f"Error in Argus.get_sign(): {e}")
    exit(1)

# Step 3: Generate X-Ladon
try:
    x_ladon = Ladon.encrypt(timestamp=x_khronos, license_id=1611921764, aid=1233)
    if x_ladon is None:
        raise ValueError("Ladon.encrypt() returned None")
    print("X-Ladon:", x_ladon)
except Exception as e:
    print(f"Error in Ladon.encrypt(): {e}")
    exit(1)

# Step 4: Build the headers for the API request
final_headers = {
    "X-Gorgon": x_gorgon,
    "X-Khronos": str(x_khronos),
    "X-Argus": x_argus,
    "X-Ladon": x_ladon,
    "Cookie": headers["Cookie"],
    "User-Agent": "com.zhiliaoapp.musically/2024007030 (Linux; U; Android 16; en_US; sdk_gphone64_x86_64; Build/BP22.250325.006;tt-ok/3.12.13.20)",
    "rpc-persist-pyxis-policy-v-tnc": "1",
    "sdk-version": "2",
    "x-tt-dm-status": "login=1;ct=1;rt=1",
    "X-SS-REQ-TICKET": str(current_rticket),
    "passport-sdk-version": "-1",
    "x-vc-bdturing-sdk-version": "2.3.13.i18n",
    "x-tt-store-region": "us",
    "x-tt-store-region-src": "uid",
    "Host": "api16-normal-useast8.tiktokv.us",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip, deflate",
    "X-Tt-Token": "0420a84ec6360df93b0fa603ce836987c505afaa0721468d05170463075acf4760e9c46d9acf6d2beb8bd5abbcb7df248f6ed436ce056ab2ba0f0625283e22017c431ff91663a0bd44c6e3fd5a1452fc7e96c85cdf8ea5ac0212ea9cfe83589a56ae2--0a4e0a207e2fda0d7868b4a9f85e760fc158962eba545647eb81aea46ebf9c9eb566c230122019a4bf0949326f68c70710dfd0269f919374564a1b8c33865e0b9d72c7dbb6281801220674696b746f6b-3.0.0"
}

# Step 5: Make the TikTok API request
url = "https://api16-normal-useast8.tiktokv.us/aweme/v1/music/aweme/"
try:
    print("Request Headers:", final_headers)
    response = requests.get(url, params=params, headers=final_headers,verify=False)
    print("HTTP Status Code (TikTok API):", response.status_code)
    print("Response Headers (TikTok API):", response.headers)
    
    # Handle gzip compression
    response_text = response.text
    if response.headers.get("Content-Encoding") == "gzip":
        try:
            buf = BytesIO(response.content)
            with gzip.GzipFile(fileobj=buf) as gz:
                response_text = gz.read().decode("utf-8")
        except Exception as e:
            print(f"Error decompressing gzip response: {e}")
    
    print("Response Text (TikTok API):", response_text[:500] + "..." if len(response_text) > 500 else response_text)
    response_json = response.json()
    print("API response (TikTok API):", response_json)
except ValueError as e:
    print(f"Error parsing JSON response (TikTok API): {e}")
    print("Response content (raw):", response_text)
except Exception as e:
    print(f"Error in API request (TikTok API): {e}")

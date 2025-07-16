import requests

url = "https://api16-normal-useast8.tiktokv.us/aweme/v1/music/aweme/?music_id=7328869241331370798&cursor=72&count=20&type=0&video_cover_shrink=372_495&from_group_id=7522286854184488247&could_lazy_loading=1&experiment_params=%7B%22detail_page_need_standardize_text%22%3A%201%2C%20%22detail_page_need_friend_tag%22%3A%201%7D&device_platform=android&os=android&ssmix=a&_rticket=1752146183516&cdid=a08bb181-6e61-4678-a146-71230db6d140&channel=googleplay&aid=1233&app_name=musical_ly&version_code=400703&version_name=40.7.3&manifest_version_code=2024007030&update_version_code=2024007030&ab_version=40.7.3&resolution=1440*2891&dpi=560&device_type=sdk_gphone64_x86_64&device_brand=google&language=en&os_api=36&os_version=16&ac=wifi&is_pad=0&app_type=normal&sys_region=US&last_install_time=1752144253&mcc_mnc=310260&timezone_name=Europe%2FParis&carrier_region_v2=310&app_language=en&carrier_region=US&ac2=wifi&uoo=0&op_region=US&timezone_offset=3600&build_number=40.7.3&host_abi=arm64-v8a&locale=en&region=US&ts=1752146187&iid=7525402045219161870&device_id=7525401655916135949&openudid=f12cd9259c6d7bde"

payload = {}
headers = {
    "rpc-persist-pyxis-policy-v-tnc": "1",
    "sdk-version": "2",
    "x-tt-dm-status": "login=1;ct=1;rt=1",
    "X-Tt-Token": "0420a84ec6360df93b0fa603ce836987c505afaa0721468d05170463075acf4760e9c46d9acf6d2beb8bd5abbcb7df248f6ed436ce056ab2ba0f0625283e22017c431ff91663a0bd44c6e3fd5a1452fc7e96c85cdf8ea5ac0212ea9cfe83589a56ae2--0a4e0a207e2fda0d7868b4a9f85e760fc158962eba545647eb81aea46ebf9c9eb566c230122019a4bf0949326f68c70710dfd0269f919374564a1b8c33865e0b9d72c7dbb6281801220674696b746f6b-3.0.0",
    "X-SS-REQ-TICKET": "1752159800807",
    "passport-sdk-version": "-1",
    "x-vc-bdturing-sdk-version": "2.3.13.i18n",
    "x-tt-store-region": "us",
    "x-tt-store-region-src": "uid",
    "User-Agent": "com.zhiliaoapp.musically/2024007030 (Linux; U; Android 16; en_US; sdk_gphone64_x86_64; Build/BP22.250325.006;tt-ok/3.12.13.20)",
    "X-Ladon": "Pio0KLlz2rLQ/4J4szNrmYwACLeKFYVxLrdZFE3EP6auNzfs",
    "X-Khronos": "1752159800",
    "X-Argus": "8oEW98egusY+LFvG7FFEoEjWcAaUPwMYvSaUAPMjZlDHFHUcSVXHdHxUCSKFwOx6p7Cfitq3/KixHyW6A/SA87G32a3JlUDuLhfuhtbHMwX3RkM0wblOpH86P/4mcPpHBKqLIQUKJ0P19gUq/JJTqwxNcfrg6aHVWEkHQRQoL5z7EEkSQFj+/Aui9txShY3x+v/Ux/7QJvIYLsbAyqEnTR/+b8iqBnsk7Vjen6zDwMxnexhUi2BBIo6agbUPPeIAFC8sSzX6MluXHrCkBpkIgfsx",
    "X-Gorgon": "0404d0e40001aad8facb1704a5760372721ccf34c4e2fbbf1881",
    "Host": "api16-normal-useast8.tiktokv.us",
    "Connection": "Keep-Alive",
    "Cookie": "store-idc=useast5; tt-target-idc=useast8; multi_sids=7525402143944295438%3A20a84ec6360df93b0fa603ce836987c5; cmpl_token=AgQQAPNSF-RPsLhRd8dl8Z038g4B3OKbv4_ZYN4PEw; sid_guard=20a84ec6360df93b0fa603ce836987c5%7C1752144433%7C15551999%7CTue%2C+06-Jan-2026+10%3A47%3A12+GMT; uid_tt=1b3a5c59c27758080e3a4852ecc1dc1c4fcf73832a34ca7be0c34979827f73fb; uid_tt_ss=1b3a5c59c27758080e3a4852ecc1dc1c4fcf73832a34ca7be0c34979827f73fb; sid_tt=20a84ec6360df93b0fa603ce836987c5; sessionid=20a84ec6360df93b0fa603ce836987c5; sessionid_ss=20a84ec6360df93b0fa603ce836987c5; store-country-code=us; store-country-code-src=uid; passport_csrf_token=206b667cdf6528e9ee25a2ccde0ebd2b; passport_csrf_token_default=206b667cdf6528e9ee25a2ccde0ebd2b; odin_tt=37f52210cd8f819e42c0dae2399500a039621ba51d9157d4f0cc483742fc830847816ca39e5c3e24bc251f625f53ae972a59b76036167b92ad58abe4b106adb9a1e6130a72aee00873e343e3defa2f01; msToken=MthB5Q29v-RYE-v9ahmyftU4SQWiEqRqcQN21zWNj4WH1fbhPGCBvOWK7L6HZ1CPTRJt4CR-_cEcyqhtRtsMPoYquLJkIMcLDIa-1OM5h065MxcURfN0IcV1Ew==; tt_ticket_guard_has_set_public_key=1; store-country-sign=MEIEDB7B3Trax9AhlD3DzQQgqgWmVacaG5RfOTCbPA9vTcrpy8zLY0vKAJaoYHiEfAwEEJcJOnxGKUQNZZpSj2ajnfs; odin_tt=f01e2f6c9a28722c14d77ff4ec6242ae9e0becef48fae252a6789ba6a5f909212c7265a63b5eae0c3733a5b3f24958f049ed5e62217c1068f75532d87a231267ec7cdba57f3a5057f7e179ba897468a0",
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

print(response.text)

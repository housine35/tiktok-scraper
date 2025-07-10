const axios = require('axios');

let config = {
  method: 'get',
  maxBodyLength: Infinity,
  url: 'https://api16-normal-useast8.tiktokv.us/aweme/v1/music/aweme/?music_id=7328869241331370798&cursor=36&count=20&type=0&video_cover_shrink=372_495&from_group_id=7522286854184488247&could_lazy_loading=1&experiment_params=%7B%22detail_page_need_standardize_text%22%3A%201%2C%20%22detail_page_need_friend_tag%22%3A%201%7D&device_platform=android&os=android&ssmix=a&_rticket=1752144658336&cdid=a08bb181-6e61-4678-a146-71230db6d140&channel=googleplay&aid=1233&app_name=musical_ly&version_code=400703&version_name=40.7.3&manifest_version_code=2024007030&update_version_code=2024007030&ab_version=40.7.3&resolution=1440*2891&dpi=560&device_type=sdk_gphone64_x86_64&device_brand=google&language=en&os_api=36&os_version=16&ac=wifi&is_pad=0&app_type=normal&sys_region=US&last_install_time=1752144253&mcc_mnc=310260&timezone_name=Europe%2FParis&carrier_region_v2=310&app_language=en&carrier_region=US&ac2=wifi&uoo=0&op_region=US&timezone_offset=3600&build_number=40.7.3&host_abi=arm64-v8a&locale=en&region=US&ts=1752144662&iid=7525402045219161870&device_id=7525401655916135949&openudid=f12cd9259c6d7bde',
  headers: {
    'rpc-persist-pyxis-policy-v-tnc': '1',
    'sdk-version': '2',
    'x-tt-dm-status': 'login=1;ct=1;rt=1',
    'X-Tt-Token': '0420a84ec6360df93b0fa603ce836987c505afaa0721468d05170463075acf4760e9c46d9acf6d2beb8bd5abbcb7df248f6ed436ce056ab2ba0f0625283e22017c431ff91663a0bd44c6e3fd5a1452fc7e96c85cdf8ea5ac0212ea9cfe83589a56ae2--0a4e0a207e2fda0d7868b4a9f85e760fc158962eba545647eb81aea46ebf9c9eb566c230122019a4bf0949326f68c70710dfd0269f919374564a1b8c33865e0b9d72c7dbb6281801220674696b746f6b-3.0.0',
    'X-SS-REQ-TICKET': '1752144658344',
    'passport-sdk-version': '-1',
    'x-vc-bdturing-sdk-version': '2.3.13.i18n',
    'x-tt-store-region': 'us',
    'x-tt-store-region-src': 'uid',
    'User-Agent': 'com.zhiliaoapp.musically/2024007030 (Linux; U; Android 16; en_US; sdk_gphone64_x86_64; Build/BP22.250325.006;tt-ok/3.12.13.20)',
    'X-Ladon': 'ULkgJ3nDiCslPCLkx9dPQTvt8BPgKTn88G1Gqed+GMskUTSk',
    'X-Khronos': '1752144653',
    'X-Argus': 'VmOLz4WGTj7UJlkJT6S8VDIXRD6XOzezhyFm+whzzDwYXYPh8kJjE9HWSO/aqHtxBmZB/gZxMj/vEaEnnh1AT8Vul7QSI35kHCEB2QoE0rHeo7HbCnKTDMfnk9us6O7PKlXEhS1Pt2m7mOwXDL1PECoG4SEaxZ5QSx2iDy6ue7A2q/mAJ9WhytT1jaKX2HvarvY52MXI4w+UA2rV6agchj3MXe9mkf020jcXVj+fFDhG+1ZpnSTmtifhN7gZCcE4ogPIjcpIKB76udCP25PVmjOGsXGiLqdm/C0I8xBnA/gzJcdZTJNKzYET/N2rFFjEzmqM/SN/tvTMQjhxmgfnDQsXTTBQmYDaPDIxVwWOf7NJM2UkPNDiCW6CA0lKV8x8L0D8HKvn5CtUr2xf9bvTo5DAnX81TjEQtNKL8HIwAD8QT7pNhrn+DS65fljLEGWopxmjBujIImzZtB83S4/3OazRtDhQyZH4qTg7LqwOKlAwT2qbK4Aw2gvETlqWQ5Nn5S8mYvWbBrjIsAjec4wXbcZMvREsSAxe8Ux24RmUJjSDenphTNEfsJUxRxw4b/dgxULmGGBDO5PVOL44Aa3dWa5AwLDor6X8KhqIGIaJsccW9d7psi/vIacM/GwZ4YSS6PfQbqDnkEc/h5KO9/6LGgQ+zE5FeYPE1eaIc5jqu8Nvfg==',
    'X-Gorgon': '8404f04740003fd8a08d1aafa137be3aaf4b1434b6feeaaa6b6f',
    'Host': 'api16-normal-useast8.tiktokv.us',
    'Connection': 'Keep-Alive',
    'Cookie': 'store-idc=useast5; tt-target-idc=useast8; multi_sids=7525402143944295438%3A20a84ec6360df93b0fa603ce836987c5; cmpl_token=AgQQAPNSF-RPsLhRd8dl8Z038g4B3OKbv4_ZYN4PEw; sid_guard=20a84ec6360df93b0fa603ce836987c5%7C1752144433%7C15551999%7CTue%2C+06-Jan-2026+10%3A47%3A12+GMT; uid_tt=1b3a5c59c27758080e3a4852ecc1dc1c4fcf73832a34ca7be0c34979827f73fb; uid_tt_ss=1b3a5c59c27758080e3a4852ecc1dc1c4fcf73832a34ca7be0c34979827f73fb; sid_tt=20a84ec6360df93b0fa603ce836987c5; sessionid=20a84ec6360df93b0fa603ce836987c5; sessionid_ss=20a84ec6360df93b0fa603ce836987c5; store-country-code=us; store-country-code-src=uid; passport_csrf_token=206b667cdf6528e9ee25a2ccde0ebd2b; passport_csrf_token_default=206b667cdf6528e9ee25a2ccde0ebd2b; store-country-sign=MEIEDHA5l7erHW33dKOFrwQgDI0wPMlgWv8GiW7OFfpz9C4d98FXVmCg4U9486UEXQYEEAiePnR86iz7oxokJveGAnA; odin_tt=37f52210cd8f819e42c0dae2399500a039621ba51d9157d4f0cc483742fc830847816ca39e5c3e24bc251f625f53ae972a59b76036167b92ad58abe4b106adb9a1e6130a72aee00873e343e3defa2f01; msToken=MthB5Q29v-RYE-v9ahmyftU4SQWiEqRqcQN21zWNj4WH1fbhPGCBvOWK7L6HZ1CPTRJt4CR-_cEcyqhtRtsMPoYquLJkIMcLDIa-1OM5h065MxcURfN0IcV1Ew=='
  }
};

axios.request(config)
  .then((response) => {
    console.log(JSON.stringify(response.data));
  })
  .catch((error) => {
    console.log(error);
  });

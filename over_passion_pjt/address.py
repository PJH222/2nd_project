# 카카오API를 사용하여 좌표->주소 변환
import requests, json, pprint

def get_address(lat, lng):
    url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x="+lng+"&y="+lat
    # 'KaKaoAK '는 그대로 두시고 개인키만 지우고 입력해 주세요.
    # ex) KakaoAK 6af8d4826f0e56c54bc794fa8a294
    headers = {"Authorization": "KakaoAK 75270528aeadaa9ffdf4769b7c0d88ff"}
    api_json = requests.get(url, headers=headers)
    full_address = json.loads(api_json.text)

    return full_address
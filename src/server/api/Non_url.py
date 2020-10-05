import json
import requests
from ast import literal_eval
from bs4 import BeautifulSoup

def non_url_twitch(videoID):
    url = 'https://api.twitch.tv/v5/videos/' + videoID
    client_id = "x7cy2lvfh9aob9oyset31dhbfng1tc"
    param = {"content_offset_seconds": 0}
    response = requests.get(url, params=param, headers={"Client-ID": client_id})
    # 없는 영상이면 http 에러코드, 아니면 recorded
    j = json.loads(response.text)

    if j['status'] != 'recorded':
        return False
    else:
        platform = 'Twitch'
        return [platform, videoID]

def non_url_afreeca(videoID):
    url = 'http://vod.afreecatv.com/PLAYER/STATION/' + videoID
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    html = requests.get(url, headers = headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    # 아프리카는 동영상이 없으면 따로 페이지 없이 <script>한줄만 나타남(확인창?)
    # 오류시 길이 2, 오류 안나면 2초과
    len_soup = len(soup)

    # 오류, 다시보기 채팅이 없다면 False, 아니면 비디오 아이디와 플랫폼 반환
    if len_soup > 2:
        find_body = soup.find_all("body", class_='replay')
        if len(find_body) == 0:
            return False
        else:
            return ['AfreecaTV', videoID]
    else:
        return False

def non_url_youtube(videoID):
    url = "https://www.youtube.com/watch?v=" + videoID
    dict_str = ""

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

    html = requests.get(url, headers = headers)
    soup = BeautifulSoup(html.text, "html.parser")

    # 상태가 담겨있는 script
    for scrp in soup.find_all("script"):
        txt = scrp.text
        if 'ytInitialPlayerResponse' in txt:
            dict_str = scrp.text.split('["ytInitialPlayerResponse"] = ')[1]
            dict_str = dict_str.split('if (window.ytcsi)')[0]
            break

    # javascript 표기이므로 변형
    dict_str = dict_str.replace('false', 'False')
    dict_str = dict_str.replace('true', 'True')

    # 불필요한 공백 등 제거
    dict_str = dict_str.rstrip(' \n;()')

    # 사전 형식으로 변환
    dics = literal_eval(dict_str)
    new_dics = dics["playabilityStatus"]["status"]

    # 오류, 다시보기 채팅이 없다면 False, 아니면 비디오 아이디와 플랫폼 반환
    if new_dics == 'Error':
        return False
    else:
        is_live = dics['videoDetails']['isLiveContent']
        if is_live != True:
            return False
        else:
            return ['Youtube', videoID]
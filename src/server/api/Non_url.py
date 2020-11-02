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

    if j['status'] == 'recorded':
        return ['Twitch', videoID]
    return False


def non_url_afreeca(videoID):
    url = 'http://vod.afreecatv.com/PLAYER/STATION/' + videoID
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    # 아프리카는 동영상이 없으면 따로 페이지 없이 <script>한줄만 나타남(확인창?)
    # 오류시 길이 2, 오류 안나면 2초과

    if len(soup) > 2 and soup.find_all("body", class_='replay') != 0:
        return ['AfreecaTV', videoID]
    return False


def non_url_youtube(videoID):
    url = "https://www.youtube.com/watch?v=" + videoID
    dict_str = ""

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, "html.parser")

    # 상태가 담겨있는 script
    for scrp in soup.find_all("script"):
        if 'ytInitialPlayerResponse' in scrp.text:
            dict_str = scrp.text.split('["ytInitialPlayerResponse"] = ')[1].split('if (window.ytcsi)')[0]
            break

    # javascript 표기이므로 변형
    dict_str = dict_str.replace('false', 'False').replace('true', 'True').rstrip(' \n;()')

    # 사전 형식으로 변환
    dics = literal_eval(dict_str)
    if dics["playabilityStatus"]["status"] != 'Error' and dics['videoDetails']['isLiveContent'] == True:
        return ['Youtube', videoID]
    return False
import sys

sys.path.append('../')

from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, NotAcceptable, Conflict

from models.file import File
from settings.settings import MODE
from settings.utils import api
from download.audio import *
from analyze.volume_extract import *
from api.ana_url import split_url
import boto3

s3 = boto3.resource('s3')

app = Blueprint('SNDnormalize', __name__, url_prefix='/api')


def upload_image(data, db, platform, videoid):
    query = db.query(File).filter(
        File.url == data['url'],
        File.name == data['name'],
    ).first()
    if query:  # 이미 존재하는 데이터
        raise Conflict

    file = open(data['name'], 'rb')
    img = file.read()
    file.close()
    image_path = f'./audio/normalizeAudio/{platform}_{videoid}.png'
    file_name = image_path.split('/')[-1]
    if MODE == 'RUN':  # use EC2 only
        s3.meta.client.upload_file(
            image_path, 'yobaimageserver', file_name, ExtraArgs={'ContentType': 'image/png'})  # upload to s3
        image_path = 'https://yobaimageserver.s3.ap-northeast-2.amazonaws.com/' + file_name

    new_file = File(
        name=data['name'],
        file=img,
        url=data['url'],
        image_url=image_path
    )
    db.add(new_file)
    db.commit()
    return image_path


def download_image(data, db):
    file = db.query(File).filter(
        File.url == data['url']
    ).first()
    return file


@app.route('/SNDnormalize', methods=['GET'])
@api
def get_sound_normalize(data, db):
    req_list = ['url']
    for i in req_list:  # 필수 요소 들어있는지 검사
        if i not in data:
            raise BadRequest

    url = data['url']

    file = download_image(data, db)
    if file:  # 해당 url로 저장된 파일 없음
        return jsonify({'image_url': file.image_url})

    url_result = split_url(url)

    if url_result != False:
        download(url_result[0], url_result[1], url)

        volumesPerMinute = sound_extract(url_result[0], url_result[1])
        save_graph(url_result[0], url_result[1], volumesPerMinute)
        image = {'url': url, 'name': f"./audio/normalizeAudio/{url_result[0]}_{url_result[1]}.png"}

        image_path = upload_image(image, db, url_result[0], url_result[1])
        return jsonify({'image_url': image_path})
    else:
        raise NotAcceptable  # 유효하지 않은 URL

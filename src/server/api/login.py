import datetime

import bcrypt
from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized

from models.login_expiry import LoginExpiry
from models.user_info import UserInfo
from settings.serialize import serialize
from settings.settings import SALT
from settings.utils import api

app = Blueprint('login', __name__, url_prefix='/api')


@app.route('/login', methods=['GET'])
@api
def get_login(data, db):  # 회원정보 불러옴
    req_list = ['email', 'uuid']
    for i in req_list:  # 필수 요소 들어있는지 검사
        if i not in data:
            raise BadRequest
    user = db.query(UserInfo).filter(
        UserInfo.email == data['email'],
    ).first()
    if not user:
        raise NotFound

    login_expiry = db.query(LoginExpiry).filter(
        LoginExpiry.email == data['email'],
        LoginExpiry.uuid == data['uuid'],
    ).first()  # email과 uuid로 검색함
    if not login_expiry:  # 존재하지 않음
        raise NotFound
    calculate_date = datetime.datetime.now() - login_expiry.expiry  # expiry를 현재 date와 계산
    if calculate_date.seconds > 3600:  # 유효기간 만료
        raise Unauthorized

    new_login_expiry = LoginExpiry(  # 새로운 expiry를 생성
        email=data['email'],
        name=user.name,
    )
    db.add(new_login_expiry)
    db.commit()
    return jsonify(serialize(new_login_expiry))


@app.route('/login', methods=['POST'])
@api
def post_login(data, db):  # 로그인
    req_list = ['email', 'pw']
    for i in req_list:  # 필수 요소 들어있는지 검사
        if i not in data:
            raise BadRequest

    password_hash = bcrypt.hashpw(data['pw'].encode(), SALT)
    user_info = db.query(UserInfo).filter(
        UserInfo.email == data['email'],
        UserInfo.pw == password_hash.decode(),
    ).first()
    if not user_info:  # 검색 결과 없음
        raise NotFound

    login_expiry = LoginExpiry(
        email=data['email'],
        name=user_info.name,
    )
    db.add(login_expiry)
    db.commit()
    return jsonify(serialize(login_expiry))

import bcrypt
from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, Conflict

from models.user_info import UserInfo
from settings.serialize import serialize
from settings.settings import SALT
from settings.utils import api

app = Blueprint('account', __name__, url_prefix='/api')


@app.route('/signup', methods=['POST'])
@api
def post_signup(data, db):
    for i in ['email', 'pw', 'name', 'age']:  # 필수 요소 들어있는지 검사
        if i not in data:
            raise BadRequest

    password_hash = bcrypt.hashpw(data['pw'].encode(), SALT)
    user_info = db.query(UserInfo).filter(UserInfo.email == data['email'],).first()
    if user_info:  # 이미 존재하는 계정
        raise Conflict

    user_info = UserInfo(
        email=data['email'],
        pw=password_hash.decode(),
        name=data['name'],
        age=data['age'],
    )
    db.add(user_info)
    db.commit()

    return jsonify(serialize(user_info))

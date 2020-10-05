import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# define
HOST_ADDR = '127.0.0.1'  # localhost address
SERVER_PORT = 8000  # 서버 포트
DEBUG = False  # 디버그모드
MODE = os.environ.get('MODE')
SALT = b'$2b$12$tPrUCEr3KqxIcBEv0fx67e'
# connect db
USER = 'postgres'  # username
PASSWOLRD = 'root'  # postgresql pw
DB_PORT = '5432'  # postgresql port
NAME = 'yoba'  # db name
POSTGRESQL = f'postgresql://{USER}:{PASSWOLRD}@{HOST_ADDR}:{DB_PORT}/{NAME}'  # postgresql uri

# select operation mode
if MODE == 'TEST' or sys.argv[0].endswith('test'):  # use only pytest
    HOST_ADDR = '127.0.0.1'
    DEBUG = False
    POSTGRESQL = f'postgresql://{USER}:{PASSWOLRD}@{HOST_ADDR}:{DB_PORT}/yoba_test'  # postgresql uri

elif MODE == 'DEV':  # mode - development
    HOST_ADDR = '127.0.0.1'
    DEBUG = True
elif MODE == 'RUN':  # mode - release
    HOST_ADDR = '0.0.0.0'
    DEBUG = False
    PASSWOLRD = 'root2628!'
    POSTGRESQL = f'postgresql://{USER}:{PASSWOLRD}@capstone.cebsh5dyebyf.ap-northeast-2.rds.amazonaws.com:{DB_PORT}/{NAME}'  # postgresql uri
else:  # select not permission mode
    raise KeyError

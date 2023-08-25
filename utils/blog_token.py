import base64
import time
import ujson as ujson
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from utils.db_redis import redis_get_value
from utils.rsa_key import CHARS_PRIVATE_KEY

MAX_DECRYPT_SIZE = 128


def check_access_token(token):
    timestamp = str(int(round(time.time() * 1000)))
    rs = redis_get_value(token)
    if rs:
        user_info = analysis_access_token(token)
    else:
        raise AssertionError(
            {'code': 40004, 'msg': '请求失败', 'result': 'token已失效', 'date': timestamp})
    return user_info


def analysis_access_token(token):
    """
    解析token
    @param token:
    """
    token_md5 = base64.b64decode(token.encode('utf-8')).decode('utf-8')
    token_str = rsa_private_decrypt(token_md5)
    user_info = ujson.loads(token_str)
    return user_info


def rsa_private_decrypt(en_data):
    private_key_obj = RSA.importKey(CHARS_PRIVATE_KEY)
    cipher = PKCS1_v1_5.new(private_key_obj)
    decrypt_str = rsa_decrypt(cipher, en_data)

    return decrypt_str


def rsa_decrypt(cipher, en_data):
    de_data = []
    en_data = base64.b64decode(en_data.encode())
    for i in range(0, len(en_data), MAX_DECRYPT_SIZE):
        de_data.append(cipher.decrypt(en_data[i:i + MAX_DECRYPT_SIZE], 'RSA'))
    de_data = b''.join(de_data).decode('utf-8')
    return de_data

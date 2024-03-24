import jwt
import datetime


# 生成 token
def generate(payload, secret_key='eduSystem', algorithm='HS256', expiration=60):
    # 设置token的过期时间
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
    # 生成token
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


# 检查token是否过期
def verify(token, secret_key='eduSystem', algorithms='HS256'):
    try:
        jwt.decode(token, secret_key, algorithms=algorithms)
        return True
    except jwt.ExpiredSignatureError:
        return False

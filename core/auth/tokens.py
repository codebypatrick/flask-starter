from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def encode_confirm_token(email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt=current_app.config['SECURITY_SALT'])

def decode_confirm_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(
                token,
                salt=current_app.config['SECURITY_SALT'],
                max_age=expiration
                )
    except:
        return False

    return email


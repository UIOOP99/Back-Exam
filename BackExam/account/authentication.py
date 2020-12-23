from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import jwt

User = get_user_model()


class JWTAuthentication(BaseAuthentication):

    PUBLIC_KEY = b"""-----BEGIN PUBLIC KEY-----
MIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQAvdka1sq0QwhtA+bx1ATuSIA3Oj19
X2M+TLsd1wJPFm24SNNQqTXPbtQKjhEzhl+fC5a1gkmG3ii2Aqkz2tZMe3UACorR
mPexynTtpQRAaJjXC8jdEsCSu/2S+nZA2gAsnn40QAlshJAds2ndXwQAJ99OkWy5
pGnFD63N6W/889YAoZs=
-----END PUBLIC KEY-----"""
    ALGORITHMS = ['ES512', ]
    PREFIX = 'Bearer'

    def authenticate(self, request):
        authorization_value = self.verify_header(self.get_auth_header(request))
        #print(authorization_value)
        if not authorization_value:
            return None
        try:
            payload = self.get_payload(authorization_value[1])
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed("Invalid JWT")
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed("The JWT is expired")
        except Exception as e:
            #raise AuthenticationFailed()
            raise AuthenticationFailed(str(e))

        return self.get_user(payload), authorization_value[1]

    def verify_header(self, authorization_value: list):
        if not authorization_value or len(authorization_value) == 0:
            return None
            #raise AuthenticationFailed("THIS IS TEST")
        if len(authorization_value) >= 3 or len(authorization_value) == 1:
            raise AuthenticationFailed("Invalid Authorization header")

        if authorization_value[0] != self.PREFIX.encode():
            raise AuthenticationFailed("Invalid Authorization header")

        #raise AuthenticationFailed(str(authorization_value))
        return authorization_value

    def get_auth_header(self, request):
        return get_authorization_header(request).split()

    def get_user(self, payload):
        try:
            user_id = payload.get('user_id')
        except KeyError:
            raise AuthenticationFailed("Invalid signature")
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid signature")

        return user

    def get_payload(self, token: str):
        return jwt.decode(token, self.PUBLIC_KEY, algorithms=self.ALGORITHMS)

import requests
from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """This will fetch user information from auth token"""

    @staticmethod
    def validate(auth_token):
        try:
            id_info = id_token.verify_oauth2_token(auth_token, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info
        except:
            return "The token either invalid or has expired"

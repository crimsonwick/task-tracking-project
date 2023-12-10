from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, renderers
from rest_framework.status import is_server_error
from TaskTrackingApp import settings
import requests
from requests.auth import HTTPBasicAuth
# Create your views here.


class BaseAPIView(APIView):
    """
    Base Class for API Views
    """
    authentication_classes = []
    permission_classes = []
    renderer_classes = [renderers.JSONRenderer]

    def customResponse(
            self, success=False, code=None, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            payload={}, description=None, exception= None, count=0):
        """
        Generates response.
        :param success: bool tells if call is successful or not.
        :param code: str status code.
        :param status_code: int HTTP status code.
        :param payload: list data generated for respective API call.
        :param description: str description.
        :param exception: str description.
        :rtype: dict.
        """
        if not success and is_server_error(status_code):
            if settings.DEBUG:
                description = f'error message: {description}'
            else:
                description = 'internal server error'

        return Response(
            data= {
                "success": success,
                "code": code,
                "payload": payload,
                "description": description,
                "count": count
            },
            status=code
        )

    def customDataResponse(
            self, success=False, code='', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            payload={}, description=''):
        """
        Generates response for data tables.
        :param success: bool tells if call is successful or not.
        :param code: str status code.
        :param status_code: int HTTP status code.
        :param payload: list data generated for respective API call.
        :param description: str description.
        :rtype: dict.
        """
        if not success and is_server_error(status_code):
            if settings.DEBUG:
                description = f'error message: {description}'
            else:
                description = 'internal server error'

        return Response(
            data= {
                "success" : success,
                "code": code,
                "payload": payload,
                "description": description,
            },
            status=code
        )

    def get_oauth_token(self,email= '', password= '',grant_type='password'):
        try:
            url = settings.AUTHORIZATION_SERVER_URL
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'username': email.lower(),
                'password': password,
                'grant_type': grant_type
            }
            auth = HTTPBasicAuth(
                settings.OAUTH_CLIENT_ID,
                settings.OAUTH_CLIENT_SECRET
            )
            response = requests.post(
                url=url,
                headers=headers,
                data=data,
                auth=auth
            )
            if response.ok:
                json_response = response.json()
                return {
                    'access_token': json_response.get('access_token', ''),
                    'refresh_token': json_response.get('refresh_token', '')
                }
            else:
                return {'error': response.json().get('error')}
        except Exception as e:
            # fixme: Add logger to log this exception
            return {'exception': str(e)}

    @staticmethod
    def revoke_oauth_token(token):
        try:
            url = settings.REVOKE_TOKEN_URL
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'token': token,
                'client_secret': settings.OAUTH_CLIENT_SECRET,
                'client_id': settings.OAUTH_CLIENT_ID
            }
            response = requests.post(
                url=url,
                headers=headers,
                data=data
            )
            if response.ok:
                return True
            else:
                return False
        except Exception:
            # fixme: Add logger to log this exception
            return False
from api.views import BaseAPIView
from api.users.serializers import AuthenticateSerializer, UserSerializer
from api.users.models import Role, User, AccessLevel
from django.contrib.auth import authenticate, logout
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsOauthAuthenticatedSuperAdmin
from django.db.models import Q


# Create your views here.
class SignupView(BaseAPIView):
    """
    Signup View for Software Engineer
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data, context={"role" : Role.objects.get(code='software-engineer')})
            if serializer.is_valid():
                serializer.save()
                if serializer.is_valid():
                    email = request.data.get("email")
                    password = request.data.get("password")
                    user = authenticate(request, email=email, password=password)
                    if user:
                        if user.is_active:
                            oauth_token = self.get_oauth_token(email, password)
                            if 'access_token' in oauth_token:
                                serialized = UserSerializer(instance=User.objects.get(id=user.id))
                                user_data = serialized.data
                                user_data['access_token'] = oauth_token.get('access_token')
                                user_data['refresh_token'] = oauth_token.get('refresh_token')
                                return self.customResponse(
                                    success=True,
                                    code=f'201',
                                    status_code=status.HTTP_201_CREATED,
                                    payload=user_data,
                                    description='User has been registered'
                                )
                            return self.customResponse( # else statement
                                success=False,
                                code=f'422',
                                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                description='Something went wrong with token generation'
                            )
                        return self.customResponse(
                            success=False,
                            code=f'422',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            description='User is not in active state.'
                        )
                    return self.customResponse(
                        success=False,
                        code=f'422',
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        description='Email or password is incorrect'
                    )
            return self.customResponse(
                success=False,
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=serializer.errors
            )
        except Exception as e:
            return self.customResponse(
                success=False,
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

class LoginView(BaseAPIView):
    """
    Login View for all users
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, pk=None):
        try:
            serializer = AuthenticateSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data.get('email')
                password = serializer.data.get('password')
                user = authenticate(request, email=email, password=password)
                if user:
                    if user.is_active:
                        if user.is_approved:
                            oauth_token = self.get_oauth_token(email, password)
                            if 'access_token' in oauth_token:
                                serialized = UserSerializer(instance=User.objects.get(id=user.id))
                                user_data = serialized.data
                                user_data['access_token'] = oauth_token.get('access_token')
                                user_data['refresh_token'] = oauth_token.get('refresh_token')
                                return self.customResponse(
                                    success=True,
                                    code=f'200',
                                    status_code=status.HTTP_200_OK,
                                    payload=user_data,
                                    description='You are logged in!',
                                )
                            return self.customResponse(
                                success=False,
                                code=f'500',
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                description='Something went wrong with oauth token generation',
                            )
                        return self.customResponse(
                            code=f'422',
                            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
                            description = "Get your account approved from the CEO"
                        )
                    return self.customResponse(
                            success=False,
                            code=f'422',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            description='User is not in active state.'
                        )

                return self.customResponse(
                    success=False,
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description='Email or password is incorrect'
                )
            return self.customResponse(
                success=False,
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=serializer.errors
            )
        except Exception as e:
            return self.customResponse(
                success=False,
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

class LogoutView(BaseAPIView):
    """
    Logout user
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION','').replace('Bearer ', '')
            if not self.revoke_oauth_token(token):
                return self.customResponse(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description='User couldn\'t logout. Token couldn\'t revoke'
                )
            logout(request)
            # requestEmail = request.data['email']
            return self.customResponse(
                success=True,
                code= f'200',
                status_code=status.HTTP_200_OK,
                description=f'User logged out successfully'
            )
        except User.DoesNotExist:
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='User does not exist'
            )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

class ApproveUserView(BaseAPIView):
    """
    Toggles is_approved attribute for user
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def get(self, request, pk=None):
        try:
            user_id = pk
            user = User.objects.get(id=user_id)
            if user:
                email = user.email
                user.is_approved = not user.is_approved
                user.save()
                userStatus = 'unapproved'
                if user.is_approved:
                    userStatus = 'approved'
                return self.customResponse(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    description=f"User with email: {email} has been {userStatus}"
                )
        except User.DoesNotExist:
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='User with this id Does Not Exist'
        )

class EnableUserView(BaseAPIView):
    """
    Toggles is_active attribute for user
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def get(self, request, pk=None):
        try:
            userId = pk
            user = User.objects.get(id=userId)
            if user:
                email = user.email
                user.is_active = not user.is_active
                userStatus = 'disabled'
                user.save()
                if user.is_active:
                    userStatus = 'enabled'
                return self.customResponse(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    description=f"User with email: {email} has been {userStatus}"
                )
        except User.DoesNotExist:
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='User with this id Does Not Exist'
        )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

class UserListingView(BaseAPIView):
    """
    Listing and Detail View for Users, Allows only CEO
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def get(self, request, pk=None):
        try:
            if pk:
                userId = pk
                userObj = User.objects.get(id=userId)
                serialized = UserSerializer(userObj)
                userData = serialized.data
                return self.customResponse(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    payload=userData,
                    description='Listing of User',
                )


            queryset = User.objects.filter(Q(role__code=AccessLevel.SOFTWARE_ENGINEER_CODE) |
                                           Q(role__code=AccessLevel.TEAM_MANAGER_CODE)).order_by('-id')
            serialized = UserSerializer(queryset, many=True)

            userData = serialized.data
            userCount = queryset.count()
            return self.customResponse(
                success=True,
                code=f'200',
                status_code=status.HTTP_200_OK,
                description= 'Listing of All Users',
                payload=userData,
                count=userCount
            )


        except User.DoesNotExist:
            return self.customResponse(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='User with this id Does Not Exist'
            )
        except Exception as e:
            return self.customResponse(
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

class CreateEmployeeView(BaseAPIView):
    """
    View for CEO which can create either Team Manager or SWE employee/ Signup + Role
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def post(self, request):
        try:
            roleCode = request.data.get("code", None)
            if roleCode == 700:
                obj = Role.objects.get(code='team-manager')
            else:
                obj = Role.objects.get(code='software-engineer')
            serializer = UserSerializer(data=request.data, context={"role": obj})
            if serializer.is_valid():
                serializer.save()
                if serializer.is_valid():
                    email = request.data.get("email")
                    password = request.data.get("password")
                    user = authenticate(request, email=email, password=password)
                    if user:
                        if user.is_active:
                            oauth_token = self.get_oauth_token(email, password)
                            if 'access_token' in oauth_token:
                                serialized = UserSerializer(instance=User.objects.get(id=user.id))
                                user_data = serialized.data
                                user_data['access_token'] = oauth_token.get('access_token')
                                user_data['refresh_token'] = oauth_token.get('refresh_token')
                                return self.customResponse(
                                    success=True,
                                    code=f'201',
                                    status_code=status.HTTP_201_CREATED,
                                    payload=user_data,
                                    description='User has been registered'
                                )
                            return self.customResponse(  # else statement
                                success=False,
                                code=f'422',
                                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                description='Something went wrong with token generation'
                            )
                        return self.customResponse(
                            success=False,
                            code=f'422',
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            description='User is not in active state.'
                        )
                    return self.customResponse(
                        success=False,
                        code=f'422',
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        description='Email or password is incorrect'
                    )
            return self.customResponse(
                success=False,
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=serializer.errors
            )
        except Exception as e:
            return self.customResponse(
                success=False,
                code=f'500',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )


from rest_framework_simplejwt.authentication import JWTAuthentication

jwt_auth = JWTAuthentication()


def get_username_from_jwt(request):
    header = jwt_auth.get_header(request)
    token = jwt_auth.get_raw_token(header).decode()
    validated_token = jwt_auth.get_validated_token(token)
    user = jwt_auth.get_user(validated_token)
    return user

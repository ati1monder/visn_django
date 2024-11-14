import json
from django.contrib.auth import login, get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from admin_panel.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenUserView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if token is None:
            return Response({"error": "No token provided."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            decoded_data = RefreshToken(token).payload
            user_id = decoded_data.get('user_id')
            if user_id is None:
                return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
            User = get_user_model()
            user = User.objects.get(id=user_id)
            return Response({
                'username': user.username,
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone_number')

        if not last_name:
            return JsonResponse({"error": "Last name is required."}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "A user with this email already exists."}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "A user with this username already exists."}, status=400)

        user = User(username=username, email=email)
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True  # Prevent the user from logging in until they have confirmed their email
        user.save()

        # Generate email confirmation link
        # token = default_token_generator.make_token(user)
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # link = request.build_absolute_uri(reverse('email_confirm', args=[uid, token]))

        # Send email
        # send_mail(
        #     'Підвердження реєстрації на OKSYOGA',
        #     f'Намасте, цей email було використано для реєстрації на сайті oksyoga.com. Для активації акаунта натисніть на посилання нижче\n {link}\nЯкщо ви не реєструвалися на сайті, проігноруйте цей лист. \nДякуємо за реєстрацію на нашому сайті! \nЗ повагою, Анна Оксимець',
        #     'from@example.com',
        #     [user.email],
        #     fail_silently=False,
        # )

        return JsonResponse({"message": "Registration successful! Please check your email to confirm your account."}, status=200)
    return JsonResponse({"error": "This route only supports POST requests."}, status=405)
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')

        password = data.get('password')

        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if user is None:
            return JsonResponse({"error": "Username or email does not exist."}, status=400)

        if not user.is_active:
            return JsonResponse({"error": "Account is not active. Please activate your account."}, status=400)

        if check_password(password, user.password):
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'message': "Login successful!",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=200)
        else:
            return JsonResponse({"error": "Login failed. Check your username/email and/or password."}, status=400)
    return JsonResponse({"error": "This route only supports POST requests."}, status=405)
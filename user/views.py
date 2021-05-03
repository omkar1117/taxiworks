import random
from django.conf import settings
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user.serializers import UserSerializer, OtpSerializer
from user.models import User, Otp


# Create your views here.
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        is_rider = request.data.get("is_rider", False)
        is_provider = request.data.get("is_provider", False)

        if not username.isdigit() and (not username.__contains__('@') or username == settings.DEFAULT_EMAIL):
            return Response({"data": "Invalid Username"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username)
        if user and user.count() == 1:
            serializer = self.serializer_class(user.first())
            return Response({"data": serializer.data}, status=status.HTTP_208_ALREADY_REPORTED)

        if not is_provider and not is_rider:
            return Response({"data": "Invalid User, User must be Provider or Rider"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "username": username,
            "mobile": username if username.isdigit() else None,
            "first_name": request.data.get("first_name", settings.DEFAULT_FIRST_NAME),
            "last_name": request.data.get("last_name", settings.DEFAULT_LAST_NAME),
            "email": username if username.__contains__("@") else settings.DEFAULT_EMAIL,
            "password": settings.DEFAULT_PASSWORD,
            "is_provider": is_provider,
            "is_rider": is_rider
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": "User created successfully"}, status=status.HTTP_201_CREATED)


class OtpView(viewsets.ModelViewSet):
    """
        Viewset to Return / Send OTP to customer while Login
    """
    queryset = Otp.objects.all()
    serializer_class = OtpSerializer
    permission_classes = []

    def check_old_otps(self, user_id):
        otps = Otp.objects.filter(user=user_id)
        otps.update(is_active=False, is_expired=True)

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        user = User.objects.filter(username=username)
        if user and user.count() == 1:
            username = user.first().pk
            self.check_old_otps(username)
            otp = random.randint(1000, 9999)
            print("OTP Sent Here:::", otp)
            data = {"user": username, "otp": otp}
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            data = serializer.save()
            # Need to write logic to share OTP to customer.

            return Response(
                {"data": data.id},
                status=status.HTTP_201_CREATED
            )

    def update(self, request, *args, **kwargs):
        username = request.data.get("username")
        otp = request.data.get("otp")

        user = User.objects.get(username=username)
        otp_obj = Otp.objects.filter(user=user.pk, otp=otp, is_active=True, is_expired=False)

        if otp_obj and otp_obj.count() == 1:
            self.check_old_otps(user)
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response({"data": data}, status=status.HTTP_200_OK)

        return Response({"data": "OTP invalid, Please check otp"}, status=status.HTTP_226_IM_USED)


def landing(request):
    return render(request,"login.html", context={})

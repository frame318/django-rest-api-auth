from rest_framework import routers, serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.socialaccount.models import SocialAccount
from baseuser.models import UserProfile

class UserRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30 , required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=10, required=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
    
    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name')
        user.last_data = self.validated_data.get('last_name')
        user.email = self.validated_data.get('email')
        user.phone = self.validated_data.get('phone')
        user.save()
        return user

    def validate_phone(self, phone):
        if len(phone) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits")
        return phone

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    socialaccount_set = SocialAccountSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class BaseTokenSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Token
        fields = '__all__'

from rest_framework import serializers
from django.contrib.auth.base_user import BaseUserManager
from reviews.models import Comment, Review, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from django.contrib.auth import authenticate


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', ]

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать имя "me"')
        return username

    def create(self, validated_data):
        password = BaseUserManager().make_random_password()
        user = User(email=validated_data['email'],
                    username=validated_data['username'],
                    password=password,
                    confirmation_code=password)
        user.save()
        send_mail('Код подтверждения YaMDb',
                  f'{password}',
                  'yamdb@yamdb.com',
                  [f'{validated_data["email"]}', ],
                  fail_silently=False,
                  )
        return user


class TokenSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    # class Meta:
    #     model = User
    #     fields = ['username', 'confirmation_code', ]

    def validate(self, attrs):
        confirmation_code = attrs.get('confirmation_code')
        attrs.update({'password': f'{confirmation_code}'})
        return {'token': attrs.get('token')}

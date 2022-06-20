from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Comment, Review, User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_title(self, title):
        author = self.context['request'].author
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение!'
            )
        return title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Данное имя пользователя уже занято'
            )
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Данный email уже занят'
            )
        ]
    )

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
                    confirmation_code=password)
        user.set_password(password)
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

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        confirmation_code = attrs.get('confirmation_code')
        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения')
        attrs.update({'password': f'{confirmation_code}'})
        del attrs['confirmation_code']
        valid_result = super().validate(attrs)
        return valid_result

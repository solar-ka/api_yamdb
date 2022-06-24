from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Genre, Review, Title, User

from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsAuthorAdminModeratorOrReadOnly, ReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             CreateTitleSerializer, GenreSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleSerializer, TokenSerializer, UserSerializer)

from api.filters import TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('genre',)
    filterset_class = TitleFilter

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ("retrieve", "list", 'destroy'):
            return TitleSerializer
        return CreateTitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('name',)

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

    def destroy(self, request, pk):
        category = get_object_or_404(Category, slug=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        if pk != '':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk):
        if pk != '':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('name',)

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        if self.action == 'destroy':
            return(IsAdmin(),)
        return super().get_permissions()

    def destroy(self, request, pk):
        genre = get_object_or_404(Genre, slug=pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk):
        if pk != '':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk):
        if pk != '':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(email=serializer.data['email'],
                                                   username=serializer.data['username']
                                                   )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        send_mail('Код подтверждения YaMDb',
                  f'Код подтверждения YaMDb: {user.confirmation_code}',
                  'yamdb@yamdb.com',
                  [f'{serializer.data["email"]}', ],
                  fail_silently=False,
                  )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetToken(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'first_name', 'last_name', 'role')
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_permissions(self):
        if self.request.user.is_superuser:
            return (AllowAny(),)
        return super().get_permissions()

    @action(detail=False,
            url_path='me',
            permission_classes=(IsAuthenticated,),
            methods=['GET', 'PATCH'])
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        print(user)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.user.is_superuser or request.user.is_staff:
            serializer.save()
        else:
            serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
#from django.db.models import Avg

from .serializers import (CommentSerializer, ReviewSerializer, TitleSerializer,
                          CategorySerializer, GenreSerializer)

from reviews.models import Review, Title, Category, Genre


from .permissions import (IsAuthorAdminModeratorOrReadOnly, ReadOnly,
IsAdminOrReadOnly)



class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = IsAuthorAdminModeratorOrReadOnly

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
    permission_classes = IsAuthorAdminModeratorOrReadOnly

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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes =(IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()

    #def perform_create(self, serializer):
        #rating = Review.objects.aggregate(Avg('score'))


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes =(IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.action  == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes =(IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()

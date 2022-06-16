from rest_framework import serializers

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
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
        fields = '__all__'
        model = Comment

from django.contrib import admin

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_id',
        'text',
        'score',
        'author',
        'pub_date',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review_id',
        'text',
        'author',
        'pub_date',
    )


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GenreTitle)

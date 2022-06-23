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


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'id',
        'password',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio'
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'category',
        'description'
    )


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(GenreTitle)

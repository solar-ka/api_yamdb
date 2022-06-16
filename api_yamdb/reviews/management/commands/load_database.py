import csv
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def load_users(self):
        from reviews.models import User
        with open(r'static\data\users.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                user = User(
                    id=row[0], username=row[1],
                    email=row[2], role=row[3], bio=row[4],
                    first_name=row[5], last_name=row[6])
                user.save()

    def load_categories(self):
        from reviews.models import Category
        with open(r'static\data\category.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                category = Category(id=row[0], name=row[1], slug=row[2],)
                category.save()

    def load_genres(self, *args, **options):
        from reviews.models import Genre
        with open(r'static\data\genre.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                genre = Genre(id=row[0], name=row[1], slug=row[2],)
                genre.save()

    def load_titles(self):
        from reviews.models import Title
        with open(r'static\data\titles.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                title = Title(
                    id=row[0], name=row[1],
                    year=row[2], category_id=row[3]
                )
                title.save()

    def load_genre_title(self):
        from reviews.models import GenreTitle
        with open(r'static\data\genre_title.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                genre_title = GenreTitle(
                    id=row[0], title_id=row[1], genre_id=row[2]
                )
                genre_title.save()

    def load_reviews(self):
        from reviews.models import Review
        with open(r'static\data\review.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                review = Review(
                    id=row[0], title_id=row[1],
                    text=row[2], author_id=row[3],
                    score=row[4], pub_date=row[5]
                )
                review.save()

    def load_comments(self):
        from reviews.models import Comment
        with open(r'static\data\comments.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                comment = Comment(
                    id=row[0], review_id=row[1],
                    text=row[2], author_id=row[3], pub_date=row[4]
                )
                comment.save()

    def handle(self, *args, **options):
        self.load_categories()
        self.load_genres()
        self.load_users()
        self.load_titles()
        self.load_genre_title()
        self.load_reviews()
        self.load_comments()

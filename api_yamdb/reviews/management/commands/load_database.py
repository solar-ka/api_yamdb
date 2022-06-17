from reviews.management.commands.load_categories import \
    Command as CattegoriesCommand
from reviews.management.commands.load_comments import \
    Command as CommentsCommand
from reviews.management.commands.load_genre_title import \
    Command as GenreTitlesCommand
from reviews.management.commands.load_genres import Command as GenresCommand
from reviews.management.commands.load_reviews import Command as ReviewsCommand
from reviews.management.commands.load_titles import Command as TitlesCommand
from reviews.management.commands.load_users import Command as UsersCommand


class Command(
    CattegoriesCommand, UsersCommand,
    GenresCommand, TitlesCommand,
    GenreTitlesCommand, ReviewsCommand,
    CommentsCommand
):

    def handle(self, *args, **options):
        self.load_categories()
        self.load_genres()
        self.load_users()
        self.load_titles()
        self.load_genre_title()
        self.load_reviews()
        self.load_comments()

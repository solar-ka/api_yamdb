import csv
from reviews.models import Review

with open(r'\static\data\review.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        _, created = Review.objects.get_or_create(
            id=row[0],
            title=row[1],
            text=row[2],
            author=row[3],
            score=row[4],
            created=row[5]
        )

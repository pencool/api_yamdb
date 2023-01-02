from django.db import models


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(required=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(required=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__range=(1, 10)),
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(required=True)
    pub_date = models.DateTimeField(auto_now_add=True)

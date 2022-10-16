from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.exceptions import ValidationError


class Movie(models.Model):
    user_added = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_added')
    user_last_updated = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_updated')
    title_pl = models.CharField(max_length=100)
    title_eng = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    runtime = models.PositiveIntegerField()
    director = models.CharField(max_length=50)
    writer = models.CharField(max_length=50)
    star1 = models.CharField(max_length=50, null=True, blank=True)
    star2 = models.CharField(max_length=50, null=True, blank=True)
    star3 = models.CharField(max_length=50, null=True, blank=True)
    
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-added']

    def __str__(self):
        return self.title_pl
    
    def movie_avg_rating(self):
        return Review.objects.filter(movie=self).aggregate(Avg('rating_value'))['rating_value__avg']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_reviews')
    body = models.TextField(blank=True)
    rating_value = models.IntegerField()
    votes = models.ManyToManyField(User, through='Vote', related_name='user_voted')

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:100]

    def clean(self):
        super().clean()
        if self.rating_value < 1 or self.rating_value > 10:
            raise ValidationError('Out of range rating value. Must be 1-10.')

    def total_vote(self):
        votes_all = Vote.objects.filter(review=self).select_related()
        upvotes = votes_all.filter(upvote=True)
        downvotes = votes_all.filter(downvote=True)
        return upvotes.count() - downvotes.count()

    def comment_count(self):
        return self.comments.count()

    class Meta:
        unique_together = ['user', 'movie']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        if self.upvote and self.downvote:
            raise ValidationError('An entry may not have both votes.')
    
    class Meta:
        unique_together = ['user', 'review']

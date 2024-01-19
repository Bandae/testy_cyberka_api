from ..models import Movie, Review, Vote, Comment
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()

# TODO: change this to 2 fixtures, one client, one user
@pytest.fixture
def user_factory(db):
    def create_client(username: str ='test_user', is_staff: bool = False, is_anon: bool =False):
        client = APIClient()
        if is_anon:
            return client
        
        User = get_user_model()

        email = 'user@tests.com'
        password = 'Fu76YjK45TD90'
        user = User.objects.create_user(username, email, password, is_staff=is_staff)

        client.login(username=username, password=password)
        return client, user
    return create_client

@pytest.fixture
def movie_factory(db):
    def create_movie(
        user=None,
        title_pl='Incepcja',
        ):
        movie = Movie.objects.create(
            user_added=user,
            user_last_updated=user,
            title_pl=title_pl,
            title_eng='Inception',
            year=1998,
            runtime=75,
            director='testA'
        )
        return movie
    return create_movie


@pytest.fixture
def review_factory(db):
    def create_review(user, movie, rating_value=5):
        review = Review.objects.create(
            movie=movie,
            user=user,
            body='testing the review',
            rating_value=rating_value
        )
        return review
    return create_review


@pytest.fixture
def vote_factory(db):
    def create_vote(user, review, upvote=False, downvote=False):
        vote = Vote.objects.create(
            review=review,
            user=user,
            upvote=upvote,
            downvote=downvote
        )
        return vote
    return create_vote


@pytest.fixture
def comment_factory(db):
    def create_comment(user, review):
        comment = Comment.objects.create(
            review=review,
            user=user,
            body='testing the comment',
        )
        return comment
    return create_comment

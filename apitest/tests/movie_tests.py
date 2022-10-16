from ..models import Movie, Review
# test ordering
# test non int runtime/year
# test too long fields


def test_auth_movie_post(user_factory):
    """Only a staff user can post movies."""
    client_anon = user_factory(username='anon', is_anon=True)
    client_logged, _ = user_factory(username='user')
    client_staff, _ = user_factory(username='staff', is_staff=True)

    data = {
        "title_pl": "test",
        "title_eng": "tests",
        "year": 1998,
        "runtime": 75,
        "director": "test",
    }
    response = client_anon.post('/movies/', data)
    assert response.status_code == 403

    response = client_logged.post('/movies/', data)
    assert response.status_code == 403

    response = client_staff.post('/movies/', data)
    assert response.status_code == 201


def test_missing_field_movie_post(user_factory):
    """Movies require 'title_pl', 'title_eng', 'year', 'runtime', 'director', 'writer' fields."""
    client, _ = user_factory(is_staff=True)
    data = { "title_pl": "testA" }
    response = client.post('/movies/', data)
    assert response.status_code == 400


def test_non_int_year_movie_post(user_factory):
    """The year and runtime fields need to be integers."""
    client, _ = user_factory(is_staff=True)
    data = {
        "title_pl": "testA",
        "title_eng": "testsA",
        "year": "invalid",
        "runtime": 75,
        "director": "testA",
    }
    response = client.post('/movies/', data)
    assert response.status_code == 400


def test_movie_search_success(user_factory, movie_factory):
    """Test icontains search for movies - success"""
    client, _ = user_factory()
    movie_factory(title_pl='test_title')
    data = { "q":"Tes" }
    response = client.get('/movies/', data)
    assert response.status_code == 200
    assert len(response.data) ==  1


def test_movie_search_fail(user_factory, movie_factory):
    """Test icontains search for movies - failure"""
    client, _ = user_factory()
    movie_factory(title_pl='test_title')
    data = { "q":"mov" }
    response = client.get('/movies/', data)
    assert response.status_code == 200
    assert len(response.data) ==  0


def test_avg_rating(user_factory, movie_factory, review_factory):
    """Test if the avg_rating method properly computes it's value."""
    client1, user1 = user_factory(is_staff=True)
    client2, user2 = user_factory(username='user2')
    movie = movie_factory()
    assert movie.movie_avg_rating() == None

    review1 = review_factory(user1, movie, rating_value=4)
    assert movie.movie_avg_rating() == 4.0

    review2 = review_factory(user2, movie, rating_value=6)
    assert movie.movie_avg_rating() == 5.0


def test_add_update_times_info(user_factory, movie_factory):
    """TODO: """
    client1, user1 = user_factory(is_staff=True, username='first_user')
    client2, user2 = user_factory(is_staff=True)
    movie = movie_factory(user1)
    user_add, user_update = movie.user_added, movie.user_last_updated
    time_add, time_updated = movie.added, movie.updated

    assert movie.user_added == user1
    assert movie.user_last_updated == user1
    assert movie.updated == movie.added
    
    data = {
        "title_pl": "test",
        "title_eng": "tests",
        "year": 1998,
        "runtime": 75,
        "writer": "adams",
        "director": "test",
    }
    client2.put(f'/movie/{movie.id}/', data)
    movie_updated = Movie.objects.get(id=movie.id)
    assert movie_updated.user_added == user_add
    assert movie_updated.user_last_updated == user2
    assert movie_updated.added == time_add
    assert movie_updated.updated > time_updated


def test_delete_user_added(user_factory, movie_factory):
    """The 'user_added' and 'user_last_updated' fields should be set to null when the user is deleted."""
    client, user = user_factory(is_staff=True)
    movie = movie_factory(user)
    assert movie.user_added == user
    assert movie.user_last_updated == user
    
    user.delete()
    movie_updated = Movie.objects.get(id=movie.id)
    assert movie_updated.user_added == None
    assert movie_updated.user_last_updated == None

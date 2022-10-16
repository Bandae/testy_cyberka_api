# detail get ?
# no both votes post
def test_no_both_votes_post(user_factory, movie_factory, review_factory):
    """A vote cannot be created with both upvote=True and downvote=True."""
    client, user = user_factory(username='user')
    movie = movie_factory()
    review = review_factory(user, movie)
    data = {
        "review": review.id,
        "upvote": True,
        "downvote": True
    }
    response = client.post('/votes/', data)
    assert response.status_code == 400


# no both votes put
def test_no_both_votes_put(user_factory, movie_factory, review_factory, vote_factory):
    """A vote cannot be updated to both upvote=True and downvote=True."""
    client, user = user_factory(username='user')
    movie = movie_factory()
    review = review_factory(user, movie)
    vote = vote_factory(user, review, upvote=True)
    data = {
        "upvote": True,
        "downvote": True
    }
    response = client.put(f'/vote/{vote.id}/', data)
    assert response.status_code == 400


# unique together
def test_unique_together_post(user_factory, movie_factory, review_factory):
    """A user can only post one vote per review."""
    client, user = user_factory()
    movie = movie_factory()
    review = review_factory(user, movie)
    data = {
        "review": review.id,
        "upvote": True,
        "downvote": False
    }
    response = client.post('/votes/', data)
    assert response.status_code == 201

    response2 = client.post('/votes/', data)
    assert response2.status_code == 400


# no empty vote create
def test_no_empty_vote_create(user_factory, movie_factory, review_factory):
    """A vote cannot be created with both upvote=False and downvote=False."""
    client, user = user_factory()
    movie = movie_factory()
    review = review_factory(user, movie)
    data = {
        "review": review.id,
        "upvote": False,
        "downvote": False
    }
    response = client.post('/votes/', data)
    assert response.status_code == 400


# allow empty update
def test_allow_empty_update(user_factory, movie_factory, review_factory, vote_factory):
    """A vote CAN be updated to both upvote=False and downvote=False."""
    client, user = user_factory()
    movie = movie_factory()
    review = review_factory(user, movie)
    vote = vote_factory(user, review, upvote=True)
    data = {
        "upvote": False,
        "downvote": False
    }
    response = client.put(f'/vote/{vote.id}/', data)
    assert response.status_code == 200


# owner only update
def test_onwer_only(user_factory, movie_factory, review_factory, vote_factory):
    """Only the owner is allowed to update a vote."""
    owner_client, owner = user_factory(username='owner')
    user_client, _ = user_factory()
    movie = movie_factory()
    review = review_factory(owner, movie)
    vote = vote_factory(owner, review, upvote=True)

    data = {
        "upvote": False,
        "downvote": True
    }
    response = user_client.put(f'/vote/{vote.id}/', data)
    assert response.status_code == 403

    response = owner_client.put(f'/vote/{vote.id}/', data)
    assert response.status_code == 200


# no get list
def test_no_get_list(user_factory):
    """GET method not allowed for the /votes/ view."""
    client, _ = user_factory()
    response = client.get('/votes/')
    assert response.status_code == 405


# is auth create
def test_auth_post(user_factory, movie_factory, review_factory):
    """Only authorized users can post votes."""
    client_anon = user_factory(username='anon', is_anon=True)
    client_logged, user_logged = user_factory(username='user')
    movie = movie_factory()
    review = review_factory(user_logged, movie)
    data = {
        "review": review.id,
        "upvote": True,
        "downvote": False
    }
    response = client_anon.post('/votes/', data)
    assert response.status_code == 403

    response = client_logged.post('/votes/', data)
    assert response.status_code == 201


# no delete
def test_no_delete(user_factory, movie_factory, review_factory, vote_factory):
    """A vote delete request is not allowed."""
    owner_client, owner = user_factory(username='owner')
    movie = movie_factory()
    review = review_factory(owner, movie)
    vote = vote_factory(owner, review, upvote=True)

    response = owner_client.delete(f'/vote/{vote.id}/')
    assert response.status_code == 405

# TODO: check if client default is anon or auth, can i post reviews ex


# def test_no_get_review_list(user_factory):
#     client, _ = user_factory()
#     response = client.get('/reviews/')
#     assert response.status_code == 405


# def test_auth_review_post(user_factory, movie_factory):
#     client_anon = user_factory(username='anon', is_anon=True)
#     client_logged, _ = user_factory(username='user')
#     movie = movie_factory()
#     data = {
#         "movie": movie.id,
#         "rating_value": 4,
#     }
#     response = client_anon.post('/reviews/', data)
#     assert response.status_code == 403

#     response = client_logged.post('/reviews/', data)
#     assert response.status_code == 201


# def test_unique_together_review_post(user_factory, movie_factory):
#     client, _ = user_factory()
#     movie = movie_factory()
#     data = {
#         "movie": movie.id,
#         "rating_value": 4,
#     }
#     response = client.post('/reviews/', data)
#     assert response.status_code == 201

#     response2 = client.post('/reviews/', data)
#     assert response2.status_code == 400


# @pytest.mark.parametrize(
#     ('rating_value', 'expected_status'),
# 	(
# 		pytest.param(-4, 400, id='neg case'),
# 		pytest.param(0, 400, id='zero case'),
# 		pytest.param(11, 400, id='over10 case'),
#         pytest.param(5.5, 400, id='float case'),
#         pytest.param(5, 201, id='correct case')
# 	)
# )
# def test_rating_review_post(user_factory, movie_factory, rating_value, expected_status):
#     client, _ = user_factory()
#     movie = movie_factory()

#     data = {
#         "movie": movie.id,
#         "rating_value": rating_value,
#     }
#     response = client.post('/reviews/', data)
#     assert response.status_code == expected_status


# def test_review_detail_get(user_factory, movie_factory, review_factory):
#     owner_client, owner = user_factory(username='owner')
#     client, _ = user_factory()
#     movie = movie_factory()
#     review = review_factory(owner, movie)

#     response = owner_client.get(f'/review/{review.id}/')
#     assert response.status_code == 200

#     response = client.get(f'/review/{review.id}/')
#     assert response.status_code == 200


# def test_onwer_only(user_factory, movie_factory, review_factory):
#     owner_client, owner = user_factory(username='owner')
#     user_client, _ = user_factory()
#     movie = movie_factory()
#     review = review_factory(owner, movie)

#     data = {
#         "rating_value": 2,
#     }
#     response = user_client.put(f'/review/{review.id}/', data)
#     assert response.status_code == 403
#     response = user_client.delete(f'/review/{review.id}/')
#     assert response.status_code == 403

#     response = owner_client.put(f'/review/{review.id}/', data)
#     assert response.status_code == 200
#     response = owner_client.delete(f'/review/{review.id}/')
#     assert response.status_code == 204


# def test_total_vote_change(user_factory, movie_factory, review_factory):
#     client1, user1 = user_factory(username='user1')
#     client2, user2 = user_factory()
#     movie = movie_factory()
#     review = review_factory(user1, movie)
#     assert review.total_vote() == 0
#     data = {"review": review.id, "upvote": True, "downvote": False}
#     response = client1.post('/votes/', data)
#     assert review.total_vote() == 1
#     response = client2.post('/votes/', data)
#     assert review.total_vote() == 2


# def test_comment_count(user_factory, movie_factory, review_factory, comment_factory):
#     client1, user1 = user_factory(username='user1')
#     client2, user2 = user_factory()
#     movie = movie_factory()
#     review = review_factory(user1, movie)
#     assert review.comment_count() == 0
#     comment_factory(user1, review)
#     assert review.comment_count() == 1
#     comment_factory(user2, review)
#     assert review.comment_count() == 2

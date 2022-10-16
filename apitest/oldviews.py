@api_view(['GET', 'POST'])
def getMovies(request):
    if request.method == 'GET':
        return getMoviesList(request)

    if request.method == 'POST':
        return createMovie(request)


@api_view(['GET', 'PUT', 'DELETE'])
def getMovie(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return getMovieDetail(request, movie)

    if request.method == 'PUT':
        return updateMovie(request, movie)

    if request.method == 'DELETE':
        return deleteMovie(request, movie)



@permission_classes(IsOwnerOrReadOnly)
@api_view(['GET', 'PUT', 'DELETE'])
def getComment(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CommentSerializer(instance=comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def getUser(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


@permission_classes(IsAuthenticatedOrReadOnly)
@api_view(['GET', 'POST'])
def getComments(request):
    if request.method == 'POST':
        Review.objects.create(
            user=request.user,
            review=request.data.get('review'),
            body=request.data.get('body'),
        )
        return Response({"comment created succesfully"})


@permission_classes(IsAuthenticatedOrReadOnly)
@api_view(['GET', 'POST'])
def getReviews(request):
    if request.method == 'POST':
        return createReview(request)

# tylko swoje, albo getonly
@api_view(['GET', 'PUT', 'DELETE'])
def getReview(request, pk):
    try:
        review = Review.objects.get(id=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        return getReviewDetail(request, review)

    if request.method == 'PUT':
        return updateReview(request, review)

    if request.method == 'DELETE':
        return deleteReview(request, review)


@permission_classes(IsAuthenticatedOrReadOnly)
@api_view(['PUT', 'GET'])
def placeVote(request, pk):
    if request.method == 'GET':
        vote = Vote.objects.get(id=pk)
        serializer = VoteSerializer(vote)
        return Response(serializer.data)
    
    try:
        review = Review.objects.get(id=pk)
        vote = review.vote_set.get(user=request.user)
    except Vote.DoesNotExist:
        Vote.objects.create(
            user=request.user,
            review=review,
            upvote=request.data.get('upvote'),
            downvote=request.data.get('downvote'),
        )
        return Response({"object created": True})
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = VoteSerializer(instance=vote, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
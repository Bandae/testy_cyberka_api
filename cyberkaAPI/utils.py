from rest_framework.response import Response
from .models import Movie
from .serializers import MovieDetailSerializer, MovieVagueSerializer, ReviewSerializer
from django.db.models import Q, Count, Avg, Subquery, OuterRef, Prefetch
from .models import Movie, Review, Vote
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


def getMoviesList(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    queryset = Movie.objects.filter(
        Q(title_pl__icontains=q)|
        Q(title_eng__icontains=q)|
        Q(director__icontains=q)|
        Q(writer__icontains=q)|
        Q(star1__icontains=q)|
        Q(star2__icontains=q)|
        Q(star3__icontains=q)
    ).annotate(avg_rating=Avg('reviews__rating_value'))

    serializer = MovieVagueSerializer(queryset, many=True)
    return Response(serializer.data)


def getMovieDetail(request, movie):
    # reviews = movie.reviews.all().prefetch_related(Prefetch('comment_set', to_attr='comments'))
    # avg_rating = movie.movie_avg_rating()

    # zrobic serializer ktory te rzeczy robi

    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)


def createMovie(request):
    Movie.objects.create(
        user_added=request.user,
        user_last_updated=request.user,
        title_pl=request.POST.get('title_pl'),
        title_eng=request.POST.get('title_eng'),
        year=request.POST.get('year'),
        runtime=request.POST.get('runtime'),
        director=request.POST.get('director'),
        writer=request.POST.get('writer'),
        star1=request.POST.get('star1'),
        star2=request.POST.get('star2'),
        star3=request.POST.get('star3'),
        description=request.POST.get('description'),
    )

    # serializer = MovieDetailSerializer(Movie)
    return Response({"object created": True})


def updateMovie(request, movie):
    serializer = MovieDetailSerializer(instance=movie, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def deleteMovie(request, movie):
    movie.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def getReviewDetail(request, review):
    # reviews = movie.reviews.all().prefetch_related(Prefetch('comment_set', to_attr='comments'))
    # avg_rating = movie.movie_avg_rating()

    # zrobic serializer ktory te rzeczy robi

    serializer = ReviewSerializer(review)
    return Response(serializer.data)


def createReview(request):
    Review.objects.create(
        user=request.user,
        movie=request.data.get('movie'),
        body=request.data.get('body'),
        rating_value=request.data.get('rating_value'),
    )

    # serializer = ReviewDetailSerializer(Review)
    return Response({"object created": True})


def updateReview(request, review):
    serializer = ReviewSerializer(instance=review, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def deleteReview(request, review):
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

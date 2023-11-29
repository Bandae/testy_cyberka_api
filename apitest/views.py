from django.contrib.auth.models import User
from django.db.models import Q, Avg, Prefetch, Count

from .models import Movie, Vote, Review, Comment
from .serializers import UserProfileSerializer, VoteUpdateSerializer, VoteCreateSerializer, CommentSerializer, ReviewDetailSerializer, ReviewVagueSerializer, MovieDetailSerializer, MovieVagueSerializer, RegistrationSerializer
from .permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, generics
from rest_framework.permissions import IsAuthenticated

from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout

# TODO: bez .order_by, nawet z sortowaniem w modelu, nie uzywane to jest
import json

@api_view(["GET"])
def main(request):
    return Response({"detail": "main"}, status=200)

@api_view(["GET"])
def get_csrf_token(request):
    return Response({"detail": "CSRF cookie retrieved."}, headers={"X-CSRFToken": get_token(request)})

@api_view(["POST"])
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"detail": "user does not exist or wrong password"}, status=400)
    login(request, user)
    return Response({"detail": "User has been logged in.", "username": username}, status=200)

@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"detail": "user has been logged out."})

class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all().annotate(avg_rating=Avg('movie_reviews__rating_value')).annotate(review_amount=Count('movie_reviews')).order_by('-updated', '-added')
    serializer_class = MovieVagueSerializer
    permission_classes = [IsStaffOrReadOnly]
    ordering = ['-updated', '-added']

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        title_pl = self.kwargs.get('title_pl') if self.kwargs.get('title_pl') != None else ''
        title_eng = self.kwargs.get('title_eng') if self.kwargs.get('title_eng') != None else ''
        year = self.kwargs.get('year') if self.kwargs.get('year') != None else ''
        director = self.kwargs.get('director') if self.kwargs.get('director') != None else ''
        
        results = queryset.filter(
            Q(title_pl__icontains=title_pl)&
            Q(title_eng__icontains=title_eng)&
            Q(year__icontains=year)&
            Q(director__icontains=director)
        )
        return results

    def perform_create(self, serializer):
        serializer.save(user_added=self.request.user, user_last_updated=self.request.user)


class MovieInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all().prefetch_related(Prefetch('movie_reviews')).annotate(avg_rating=Avg('movie_reviews__rating_value'))
    serializer_class = MovieDetailSerializer
    permission_classes = [IsStaffOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user_last_updated=self.request.user)


class ReviewListView(generics.CreateAPIView):
    serializer_class = ReviewVagueSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all().prefetch_related(Prefetch('comments'))
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # def get_queryset(self, *args, **kwargs):
    #     queryset = super().get_queryset(*args, **kwargs)
    #     if self.request.user.is_anonymous:
    #         return queryset
    #     return queryset.prefetch_related(Prefetch('user_voted', queryset=Vote.objects.filter(user=self.request.user)))


class CommentListView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class CreateVoteView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateVoteView(generics.RetrieveUpdateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]


class MyVoteView(generics.ListAPIView):
    serializer_class = VoteUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        review_id = self.kwargs['review_id']
        return Vote.objects.filter(user=user, review=review_id)

# --------------------------------

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class MyUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# def logoutUser(request):
#     logout(request)

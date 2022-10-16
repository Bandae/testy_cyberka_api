from django.contrib.auth.models import User
from django.db.models import Q, Avg, Prefetch

from .models import Movie, Vote, Review, Comment
from .serializers import UserProfileSerializer, VoteUpdateSerializer, VoteCreateSerializer, CommentSerializer, ReviewDetailSerializer, ReviewVagueSerializer, MovieDetailSerializer, MovieVagueSerializer
from .permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, generics
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout

# TODO: bez .order_by, nawet z sortowaniem w modelu, nie uzywane to jest

@api_view(["GET"])
def main(request):
    return Response({"detail": "main"}, status=200)


class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all().annotate(avg_rating=Avg('movie_reviews__rating_value')).order_by('-updated', '-added')
    serializer_class = MovieVagueSerializer
    permission_classes = [IsStaffOrReadOnly]
    ordering = ['-updated', '-added']

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        if q is None:
            return queryset
        
        results = queryset.filter(
            Q(title_pl__icontains=q)|
            Q(title_eng__icontains=q)|
            Q(director__icontains=q)|
            Q(writer__icontains=q)|
            Q(star1__icontains=q)|
            Q(star2__icontains=q)|
            Q(star3__icontains=q)
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

# --------------------------------



# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(username = username)
#         except:
#             messages.error(request, 'User does not exist')

#         user = authenticate(request, username=username, password=password)

#         if user:
#             login(request, user)
#         else:
#             messages.error(request, 'Username or password does not exist') 

# def logoutUser(request):
#     logout(request)

# def registerUser(request):
#     form = CustomUserCreationForm()
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home-page')
#         else:
#             messages.error(request, 'an error occured')

#     context = {'form': form}
#     return render(request, 'apitest/login_register.html', context)

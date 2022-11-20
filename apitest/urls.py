from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),

    path('user/<str:pk>/', views.UserView.as_view()),
    path('users/', views.RegisterView.as_view()),

    path('movie/<str:pk>/', views.MovieInstanceView.as_view()),
    path('movies/', views.MovieListView.as_view()),

    path('votes/', views.CreateVoteView.as_view()),
    path('vote/<str:pk>/', views.UpdateVoteView.as_view()),

    path('reviews/', views.ReviewListView.as_view()),
    path('review/<str:pk>/', views.ReviewInstanceView.as_view()),

    path('comments/', views.CommentListView.as_view()),
    path('comment/<str:pk>/', views.CommentInstanceView.as_view()),
]

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('csrf/', views.get_csrf_token),
    path('login/', views.login_view),
    path('logout/', views.logout_view),

    path('user/<str:pk>/', views.UserView.as_view()),
    path('user-me/', views.MyUserView.as_view()),
    path('users/', views.RegisterView.as_view()),

    path('movie/<str:pk>/', views.MovieInstanceView.as_view()),
    path('movies/', views.MovieListView.as_view()),
    re_path('movies/title_pl=(?P<title_pl>.*)&title_eng=(?P<title_eng>.*)&year=(?P<year>.*)&director=(?P<director>.*)/', views.MovieListView.as_view()),

    path('votes/', views.CreateVoteView.as_view()),
    path('vote/<str:pk>/', views.UpdateVoteView.as_view()),
    re_path('myvote/review=(?P<review_id>.+)/$', views.MyVoteView.as_view()),

    path('reviews/', views.ReviewListView.as_view()),
    path('review/<str:pk>/', views.ReviewInstanceView.as_view()),

    path('comments/', views.CommentListView.as_view()),
    path('comment/<str:pk>/', views.CommentInstanceView.as_view()),
]

from django.contrib import admin

# Register your models here.

from .models import Movie, Review, Vote, Comment


admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Vote)

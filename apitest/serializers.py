from django.contrib.auth.models import User
from rest_framework import serializers, validators
from .models import Movie, Review, Comment, Vote
from .validators import exclusive_vote, no_empty_vote
import django.contrib.auth.password_validation as password_validators
from django.core.exceptions import ValidationError
#TODO: find how to check how many hits to the database
#TODO: serializer trzeba optymalizowac tym prefetch. spojrzec tu: https://www.django-rest-framework.org/api-guide/relations/#serializer-relations
#TODO: check default staff permissions
#TODO: str w stylu '5' sie licza jako int nie wiem czy to dobrze

class VoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        validators = [
            exclusive_vote,
            validators.UniqueTogetherValidator(queryset=Vote.objects.all(), fields=['user', 'review'])
        ]
        fields = '__all__'
        read_only_fields = ['user', 'review']
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}


class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        validators = [
            exclusive_vote,
            no_empty_vote,
            validators.UniqueTogetherValidator(queryset=Vote.objects.all(), fields=['user', 'review'])
        ]
        fields = '__all__'
        read_only_fields = ['user']
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'review', 'body', 'created']
        read_only_fields = ['user']


class ReviewVagueSerializer(serializers.ModelSerializer):
    total_vote = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    body_short = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = ['user', 'movie', 'body', 'body_short', 'rating_value', 'updated', 'created', 'total_vote', 'comment_count']
        read_only_fields = ['user']
        write_only_fields = ['body']
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}
        validators = [
            validators.UniqueTogetherValidator(queryset=Review.objects.all(), fields=['user', 'movie'])
        ]
    
    def get_total_vote(self, obj):
        return obj.total_vote()
    
    def get_comment_count(self, obj):
        return obj.comment_count()
    
    def get_body_short(self, obj):
        return obj.__str__()
    
    def validate_rating_value(self, rating_value):
        if rating_value < 1 or rating_value > 10:
            raise serializers.ValidationError('Rating must be between 1 and 10')
        return rating_value


class ReviewDetailSerializer(serializers.ModelSerializer):
    total_vote = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Review
        fields = ['user', 'movie', 'body', 'rating_value', 'updated', 'created', 'total_vote', 'comments']
        read_only_fields = ['user', 'movie']
        extra_kwargs = {'user': {'default': serializers.CurrentUserDefault()}}
        validators = [
            validators.UniqueTogetherValidator(queryset=Review.objects.all(), fields=['user', 'movie'])
        ]
    
    def get_total_vote(self, obj):
        return obj.total_vote()
    
    def validate_rating_value(self, rating_value):
        if rating_value < 1 or rating_value > 10:
            raise serializers.ValidationError('Rating must be between 1 and 10')
        return rating_value


class MovieVagueSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True) # this uses an annotated field
    user_added = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_last_updated = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Movie
        exclude = ['id', 'updated', 'added']


class MovieDetailSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True) # this uses an annotated field
    movie_reviews = ReviewVagueSerializer(read_only=True, many=True)
    user_last_updated = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Movie
        exclude = ['id', 'user_added', 'updated', 'added']


class UserProfileSerializer(serializers.ModelSerializer):
    user_reviews = ReviewDetailSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['username', 'user_reviews']


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[validators.UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def validate_password(self, value):
        try:
            password_validators.validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

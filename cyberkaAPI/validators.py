from rest_framework import serializers

def exclusive_vote(data):
    if data['upvote'] and data['downvote']:
        raise serializers.ValidationError('Cannot have both upvote and downvote')

def no_empty_vote(data):
    if not data['upvote'] and not data['downvote']:
        raise serializers.ValidationError('Cannot create an empty vote')
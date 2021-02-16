from rest_framework import serializers
from django.conf import settings
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']

    def validate(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("이 트윗은 너무 깁니다.")
        return value
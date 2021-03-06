from rest_framework import serializers
from django.conf import settings
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()

        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("Invalid Tweet action")

        return value


class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']

    def get_likes(self, obj):
        return obj.likes.count()

    def validate(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("이 트윗은 너무 깁니다.")
        return value


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    original_tweet = TweetCreateSerializer(source="parent", read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'is_retweet', 'original_tweet']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_content(self, obj):
        content = obj.content

        if obj.is_retweet:
            content = obj.parent.content
        
        return content

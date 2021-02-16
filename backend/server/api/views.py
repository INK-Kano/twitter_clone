from django.shortcuts import render, redirect

from django.conf import settings

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

import random

from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    query = Tweet.objects.all()
    serializer = TweetSerializer(query, many=True)

    return Response(serializer.data)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    return JsonResponse({}, status=400)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    query = Tweet.objects.filter(id=tweet_id)

    if not query.exists():
        return Response({"message": "찾는 트윗이 존재하지 않습니다."}, status=404)
    
    obj = query.first()
    serializer = TweetSerializer(obj)

    return Response(serializer.data)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    query = Tweet.objects.filter(id=tweet_id)

    if not query.exists():
        return Response({"message": "찾는 트윗이 존재하지 않습니다."}, status=404)
    
    query = query.filter(user=request.user)

    if not query.exists():
        return Response({"message": "트윗을 만든 사람만 삭제할 수 있습니다."}, status=401)

    obj = query.first()
    obj.delete()

    return Response({"message": "트윗이 삭제되었습니다."}, status=200)


# with Pure django
def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
    }

    status = 200

    try: 
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404

    return JsonResponse(data, status=status)
    

def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)

        return redirect(settings.LOGIN_URL)

    form = TweetForm(request.POST or None)

    next_url = request.POST.get("next") or None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()

        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)

        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()

    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    return render(request, "components/form.html", context={"form": form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]

    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)



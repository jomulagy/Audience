from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from account.models import Userable
from .models import Like, Dislike, Interest, UserInterest, Hashtag, Rating, EmployerRating
from employ.models import Postable
from job.models import Job_post

# 좋아요 tested
# ajax로 받기, load 받기
# filter(), exists()로 확인하는 방법이 더 바람직
def add_like(request):
    data = json.loads(request.body)
    user = request.user
    post_id = int(data['post_id'])
    post = Postable.objects.get(id=post_id)

    is_liked = Like.objects.filter(userable=user, postable=post).exists()
    is_disliked = Dislike.objects.filter(userable=user, postable=post).exists()

    if is_liked:
        like = Like.objects.get(userable=user, postable=post)
        like.delete()
    else:
        like = Like.objects.create(userable=user, postable=post)
        like.save()

    if is_disliked:
        dislike = Dislike.objects.get(userable=user, postable=post)
        dislike.delete()

    likes_count = Like.objects.filter(postable=post).count()
    dislikes_count = Dislike.objects.filter(postable=post).count()

    return JsonResponse({'likes_count': likes_count, 'dislikes_count': dislikes_count,
                         'is_liked': not is_liked, 'is_disliked': False})

# 싫어요 tested
def add_dislike(request):
    data = json.loads(request.body)
    # user = request.user
    user = Userable.objects.get(id = 3)

    post_id = int(data['post_id'])
    post = Postable.objects.get(id=post_id)

    is_liked = Like.objects.filter(userable=user, postable=post).exists()
    is_disliked = Dislike.objects.filter(userable=user, postable=post).exists()

    if is_disliked:
        dislike = Dislike.objects.get(userable=user, postable=post)
        dislike.delete()
    else:
        dislike = Dislike.objects.create(userable=user, postable=post)
        dislike.save()

    if is_liked:
        like = Like.objects.get(userable=user, postable=post)
        like.delete()

    likes_count = Like.objects.filter(postable=post).count()
    dislikes_count = Dislike.objects.filter(postable=post).count()

    return JsonResponse({'likes_count': likes_count, 'dislikes_count': dislikes_count,
                         'is_liked': False, 'is_disliked': not is_disliked})

# 평점 추가/변경
# 그냥 함수라고 생각, request 없이 그냥 함수
# rating 모델 만들기, like랑 비슷하게 만들되, 중간 테이블까지 생성
# 구인자에 mapping된 postable 수를 저장하는 필드(post_num)를 만들고 rating_sum/post_num으로 평균 rating을 나타낼 수 있을 듯
# Post Create에서 호출
def add_rating(applicant, employer, rating):
    if EmployerRating.objects.filter(applicant=applicant, employer=employer).exists():
        original_rating = EmployerRating.objects.get(applicant=applicant, employer=employer)
        original_rating.rating = rating
        original_rating.save()
    else:
        new_rating = EmployerRating.objects.create(applicant=applicant, employer=employer, rating=rating)
        new_rating.save()

# 관심분야 set
# 파이썬 함수처럼 만들어서 회원정보 수정에서 호출할 수 있도록 수정
def update_interest(user, interest_list):
    # 관심분야 clear
    UserInterest.objects.filter(userable=user).delete()
    # 다시 전부다 연결
    if len(interest_list) > 0:
        for interest in interest_list:

            UserInterest.objects.create(userable=user, interest=Interest.objects.get(name=interest))
    else:
        pass

# 해시태그 생성(게시물 id)
# 파이썬 함수처럼 만들기 게시글 생성 및 수정에서 호출할 수 있게
def add_hashtag(hashtag_list, post_id):
    post = Postable.objects.get(id=post_id)
    # 기존 해시태그 삭제
    Hashtag.objects.filter(postable=post_id).delete()

    for post_hashtag in hashtag_list:
        # 없으면 추가
        hashtag, created = Hashtag.objects.get_or_create(name=post_hashtag)
        # 게시물이랑 연결
        hashtag.postable.add(post)
        hashtag.save()

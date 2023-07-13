from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment, Reply
from account.models import Userable
from employ.models import Postable
import json
from django.http import JsonResponse

@login_required
def create_comment(request): # 댓글 생성(ajax)
    if request.method == 'POST':
        user = request.user

        data = json.loads(request.body)
        print(data)
        post = Postable.objects.get(id = data['post_id'])

        content = data['content']

        comment = Comment.objects.create(content = content, postable = post, userable = user)

        return JsonResponse({"id": comment.id})

@login_required
def update_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment = Comment.objects.get(id = data['comment_id'])
        content = data['content']

        comment.content = content
        comment.save()

        return JsonResponse({"success":True})

@login_required
def delete_comment(request): # 댓글 삭제(ajax)
    if request.method == 'POST':
        data = json.loads(request.body)
        comment = Comment.objects.get(id = data['comment_id'])
        comment.delete()

        return JsonResponse({})

@login_required
def create_reply(request):# 대댓글 쓰기(ajax)
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data['content']
        comment = Comment.objects.get(id = data["comment_id"])
        user = request.user

        reply = Reply.objects.create(content = content, comment = comment, userable = user)

        return JsonResponse({"id":reply.id,"author" : reply.userable.name})

@login_required
def update_reply(request):# 대댓글 쓰기(ajax)
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data['content']
        reply = Reply.objects.get(id = data['reply_id'])

        reply.content = content
        reply.save()

        return JsonResponse({})

@login_required
def delete_reply(request): # 대댓글 삭제(ajax)
    if request.method == 'POST':
        data = json.loads(request.body)
        reply = Reply.objects.get(id = data['reply_id'])
        reply.delete()

        return JsonResponse({})


from django.shortcuts import render,redirect, get_object_or_404
from .forms import QuestionForm, AnswerForm, FreePostForm_e, EPostForm
from .models import Employ_post, Freepost_e, Question, Postable
from job.models import report
from account.models import Employer
from django.http import JsonResponse
from util.views import add_hashtag
import json

def employ_post_detail(request,post_id,category) :#게시물 상세(id, 모집공고/Q&A)
    #회사
    if category == "recruitment" : #모집공고 일때
        post = Employ_post.objects.get(id = post_id)
        post.views +=1
        post.save()
        likes = post.like_set.all().count()
        dislikes = post.dislike_set.all().count()
        context = {
            "post" : post,
            "likes" : likes,
            "dislikes" : dislikes
        }

        return render(request,"employ_list.html",context)
    else:
        context = {
            "post" : post
        }
        return render(request,"employ_list.html",context)


def create_employ_post(request):  # 구인글 작성
    # 해시태그 저장 함수 utls에서 찾아서 사용
    if request.method == 'POST':
        form = EPostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save()
            # 해시태그들을 list로 바꾸기
            add_hashtag(tag_names)
            return redirect('employ_post_detail',post.id,"recruitment")

        else:
            return render(request, 'create_employ_post.html')

    else:
        return render(request, 'create_employ_post.html')


def update_employ_post(request,id): #구인글 수정 #해시태그 저장 함수 utls에서 찾아서 사용
    post = get_object_or_404(Employ_post, id=id)
    if request.method == 'POST':
        form = EPostForm(request.POST, request.FILES,instance = post)
        if form.is_valid():
            form.save()
            return redirect('employ_post_detail',id,"recruitment")
        else:
            print(form.errors)
            return render(request, 'create_employ_post.html')

    else:
        return render(request, 'create_employ_post.html')

def delete_employ_post(request,id): #구인글 삭제
    post = get_object_or_404(Postable, id=id)
    post.delete()
    #post list로 redirect
    return redirect('employ_post_detail')


def employ_free_post_detail(request,post_id):
    post = Freepost_e.objects.get(id=post_id)
    post.views += 1
    post.save()
    likes = post.like_set.all().count()
    dislikes = post.dislike_set.all().count()
    context = {
        "post": post,
        "likes": likes,
        "dislikes": dislikes
    }
    return render(request, "employ_list.html", context)

def create_employ_free_post(request): #구직/자유소통 작성 #해시태그 저장 함수 utls에서 찾아서 사용
    if request.method == 'POST':
        form = FreePostForm_e(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.userable = request.user
            # 해시태그들을 list로 바꾸기
            add_hashtag(tag_names)

            return redirect('employ_free_post_detail', post.id)
        else:
            return render(request, 'create_employ_free_post.html')
    else:
        return render(request, 'create_employ_free_post.html')

def update_employ_free_post(request,id): #구직/자유소통 수정
    #해시태그 저장 함수 utls에서 찾아서 사용
    post = get_object_or_404(Postable, id=id)
    if request.method == 'POST':
        form = FreePostForm_e(request.POST, request.FILES,instance = post)
        if form.is_valid():
            form.save()
            return redirect('employ_free_post_detail',id)
        else:
            return render(request, 'create_employ_free_post.html')

    else:
        return render(request, 'create_employ_free_post.html')

def delete_employ_free_post(request,id): #구직/자유소통 삭제
    post = get_object_or_404(Postable, id=id)
    post.delete()
    # post list로 redirect
    return redirect('employ_free_post_detail')


def QA_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Employ_post.objects.get(id = data['post_id'])
        QA_list = post.question_set.all()
        page_num = int(data["page_num"])
        QA_list = list(QA_list[5*(page_num-1):5*page_num-1].values())

        context = {
            "QA_List" : QA_list
        }
        return JsonResponse(context)


def create_question(request,post_id):  # Q&A 질문 작성(게시물 id)
    if request.method == 'POST':
        print(request.POST)
        form = QuestionForm(request.POST,request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.employ_post_ref = Employ_post.objects.get(id = post_id)
            question.userable = request.user
            question.progress = "답변대기중"
            question.save()
            return redirect('question_detail',post_id,question.id)
        else:
            print(form.errors)
            return render(request, 'create_question.html')
    else:
        return render(request, 'create_question.html')

def delete_question(request,question_id):  # Q&A 질문 삭제(질문 id)
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect('QA_list')

def question_detail(request,post_id,question_id):
    post = Postable.objects.get(id = post_id)
    question = Question.objects.get(id = question_id)
    answers = question.answer_set.all()

    context = {
        "post" : post,
        "question" : question,
        "answers" : answers
    }
    return render(request,"employ_list.html",context)

def create_answer(request, post_id,question_id):  # Q&A 답변 작성(질문 id)
    if request.method == 'POST':
        question = Question.objects.get(id = question_id)
        form = AnswerForm(request.POST,request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_ref = question
            answer.userable = request.user
            answer.save()
            question.progress = "답변완료"
            question.save()
            return redirect('question_detail',post_id,question.id)
        else:
             return render(request, 'create_answer.html')
    else:
        return render(request, 'create_answer.html')

def delete_answer(request,answer_id): #Q&A 답변 삭제?(답변 id)
    answer = get_object_or_404(Answer, id = answer_id)
    answer.delete()
    return redirect('question_detail')

def report_create_e(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Postable.objects.get(id = data['post_id'])
        content = data['content']
        new = report.objects.create(content = content, postable = post)

        return JsonResponse({})

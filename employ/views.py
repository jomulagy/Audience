from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionForm, AnswerForm, FreePostForm_e, EPostForm
from .models import Employ_post, Freepost_e, Question, Postable, Answer
from job.models import report, Freepost_j, Job_post
from account.models import Employer
from django.http import JsonResponse
from util.views import add_hashtag
from util.models import Hashtag
from Audience.views import post_list
import json


def employ_post_detail(request, post_id):  # 게시물 상세(id, 모집공고/Q&A)
    # 회사
    post = Employ_post.objects.get(id=post_id)
    post.views += 1
    post.save()
    likes = post.like_set.all().count()
    dislikes = post.dislike_set.all().count()
    hashtags = list(Hashtag.objects.filter(name__contains=add_hashtag).values("name"))
    context = {
        "post": post,
        "likes": likes,
        "dislikes": dislikes
    }

    return render(request, "Post/postView.html", context)


def create_employ_post(request):  # 구인글 작성
    # 해시태그 저장 함수 utls에서 찾아서 사용
    if request.method == 'POST':
        form = EPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            # 해시태그들을 list로 바꾸기
            add_hashtag()
            return redirect('post_detail', post.id, "recruitment")

        else:
            return render(request, 'findwork_company_QnA/write_company.html')

    else:
        return render(request, 'findwork_company_QnA/write_company.html')


def update_employ_post(request, id):  # 구인글 수정 #해시태그 저장 함수 utls에서 찾아서 사용
    post = get_object_or_404(Employ_post, id=id)
    if request.method == 'POST':
        form = EPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id, "recruitment")
        else:
            return render(request, 'findwork_company_QnA/write_company.html')

    else:
        return render(request, 'findwork_company_QnA/write_company.html', {"post": post})


def delete_employ_post(request, id):  # 구인글 삭제
    post = get_object_or_404(Postable, id=id)
    post.delete()
    return redirect('post_list')


def employ_free_post_detail(request, post_id):
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
    return render(request, "Post/postFree.html", context)


def create_employ_free_post(request):  # 구직/자유소통 작성 #해시태그 저장 함수 utls에서 찾아서 사용
    if request.method == 'POST':
        form = FreePostForm_e(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            post.userable = request.user
            # 해시태그들을 list로 바꾸기
            add_hashtag()

            return redirect('post_detail', post.id)
        else:
            return render(request, 'findwork_company_QnA/free_write.html', {"type": "post_e"})
    else:
        return render(request, 'findwork_company_QnA/free_write.html', {"type": "post_e"})


def update_employ_free_post(request, id):  # 구직/자유소통 수정
    # 해시태그 저장 함수 utls에서 찾아서 사용
    post = get_object_or_404(Postable, id=id)
    if request.method == 'POST':
        form = FreePostForm_e(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id)
        else:
            return render(request, 'findwork_company_QnA/free_write.html', {"type": "post_e", "post": post})

    else:
        return render(request, 'findwork_company_QnA/free_write.html', {"type": "post_e", "post": post})


def delete_employ_free_post(request, id):  # 구직/자유소통 삭제
    post = get_object_or_404(Postable, id=id)
    post.delete()
    return redirect('post_list')


def QA_list_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Employ_post.objects.get(id=data['post_id'])
        QA_list = post.question_set.all()
        page_num = int(data["page_num"])
        QA_list = list(QA_list[5 * (page_num - 1):5 * page_num - 1].values("id", "title", "views"))

        context = {
            "QA_List": QA_list
        }
        return JsonResponse(context)


def QA_list(request,id):
    post = Employ_post.objects.get(id = id)
    context = {
        "post":post
    }
    return render(request, "Q&A/Q&A_p.html",context)

def create_question(request, post_id):  # Q&A 질문 작성(게시물 id)
    post = Employ_post.objects.get(id=post_id)
    if request.method == 'POST':
        print(request.POST)
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.employ_post_ref = post
            question.userable = request.user
            question.progress = "답변대기중"
            question.save()
            return redirect('post_detail', post_id, question.id)
        else:
            print(form.errors)
            return render(request, 'findwork_company_QnA/QnA_question_w.html',{"post":post})
    else:
        return render(request, 'findwork_company_QnA/QnA_question_w.html',{"post":post})

def update_question(request, id):
    # 해시태그 저장 함수 utls에서 찾아서 사용
    post = get_object_or_404(Postable, id=id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id)
        else:
            return render(request, 'findwork_company_QnA/QnA_question_w.html', {"post": post})

    else:
        return render(request, 'findwork_company_QnA/QnA_question_w.html', {"post": post})


def delete_question(request, question_id):  # Q&A 질문 삭제(질문 id)
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return redirect('QA_list')


def question_detail(request, post_id, question_id):
    post = Postable.objects.get(id=post_id)
    question = Question.objects.get(id=question_id)
    answers = question.answer_set.all()

    context = {
        "post": post,
        "question": question,
        "answers": answers
    }
    return render(request, "Q&A/Q&A_before.html", context)


def create_answer(request, post_id, question_id):  # Q&A 답변 작성(질문 id)
    post = Employ_post.objects.get(id = post_id)
    question = Question.objects.get(id=question_id)
    context = {
        "post": post,
        "question": question
    }
    if request.method == 'POST':

        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_ref = question
            answer.userable = request.user
            answer.save()
            question.progress = "답변완료"
            question.save()
            return render(request,'Q&A_sub.html', context)
        else:
            return render(request, 'findwork_company_QnA/QnA_answer_w.html',context)
    else:

        return render(request, 'findwork_company_QnA/QnA_answer_w.html',context)

def update_answer(request, id):
    # 해시태그 저장 함수 utls에서 찾아서 사용
    post = get_object_or_404(Postable, id=id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return render(request, 'Q&A_sub.html', {"post": post})
        else:
            return render(request, 'findwork_company_QnA/QnA_answer_w.html', {"post": post})

    else:
        return render(request, 'findwork_company_QnA/QnA_answer_w.html', {"post": post})


def delete_answer(request, answer_id):  # Q&A 답변 삭제?(답변 id)
    answer = get_object_or_404(Answer, id=answer_id)
    answer.delete()
    return redirect('QA_list')


def report_create_e(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Postable.objects.get(id=data['post_id'])
        content = data['content']
        new = report.objects.create(content=content, postable=post)

        return JsonResponse({})
    
def post_detail(request, post_id):
    if Employ_post.objects.filter(id=post_id).exists():
        return redirect('employ_post_detail', post_id)
    elif Job_post.objects.filter(id=post_id).exists():
        return redirect('job_post_detail', post_id)
    elif Freepost_e.objects.filter(id=post_id).exists():
        return redirect('employ_free_post_detail', post_id)
    elif Freepost_j.objects.filter(id=post_id).exists():
        return redirect('job_free_post_detail', post_id)
    elif Question.objects.filter(id=post_id).exists():
        return redirect('question_detail', post_id)

    "{{% url 'employ:post_detail post_id' %}}"
from django.shortcuts import render, redirect
from django.http import JsonResponse
from account.models import Employer
from employ.models import Postable, Employ_post, Freepost_e
from util.models import Hashtag, Interest, UserInterest
from job.models import Job_post, Freepost_j
import json
from django.db.models import Q
from account.models import Userable


# 메인화면
def main_view(request):
    employ_posts = Employ_post.objects.order_by('-created_at')[:5]  # 구인글 5개
    job_posts = Job_post.objects.order_by('-created_at')[:5]  # 구직글 5개
    context = {'employ_posts': employ_posts, 'job_posts': job_posts}

    return render(request, '메인화면 템플릿', context)


# 검색페이지(검색어 get parameter)
# 뷰만 띄움
def search_page(request, keyword, category, board_type, post_type, search_type):
    print(keyword)
    return render(request, 'main_view.html')


# 검색 결과
# 매개변수로 검색어랑 카테고리 pk로 받아서 검색
# ajax
# 구인 카테고리면 employ에서 구직이면 job에서 자유면 freepost

def toatl_page(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data["my_page"]:
            if request.user.is_authenticated:
                posts = Postable.objects.order_by('-created_at')
                return JsonResponse({'total_num': len(posts)//5+1})
        keyword = data['keyword']
        category = data['category']
        board_type = data['board_type']
        post_type = data['post_type']
        search_type = data['search_type']
        posts = []
        if category == "구직":

            if board_type == "구직":
                if search_type == "제목":
                    posts = list(Job_post.objects.filter(title__icontains=keyword).values())
                    ranks = list(Job_post.objects.filter(title__icontains=keyword).order_by("-views").values())[0:4]
                elif search_type == "내용":
                    posts = list(Job_post.objects.filter(content__icontains=keyword).values())
                elif search_type == "제목+내용":
                    posts = list(Job_post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).values())
                elif search_type == "해시태그":
                    posts = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Job_post.objects.filter(id=post.id).exists():
                                free = Job_post.objects.get(id=post.id)

                                posts.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "content": free.content,
                                    "created_at": free.created_at,
                                    "views": free.views,
                                    "userable_id": free.userable.id,
                                    "postable_ptr_id": free.id,
                                    "image": free.image.url,
                                })
                elif search_type == "회사이름":
                    employer = Employer.objects.filter(company__icontains=keyword)
                    posts = list(Job_post.objects.filter(title__in=employer).order_by("created_at").values("id","title","views"))

            else:
                if search_type == "제목":
                    posts = list(Freepost_j.objects.filter(title__icontains=keyword).values())

                elif search_type == "내용":
                    posts = list(Freepost_j.objects.filter(content__icontains=keyword).values())

                elif search_type == "제목+내용":
                    posts = list(
                        Freepost_j.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).values())

                elif search_type == "해시태그":
                    posts = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Freepost_j.objects.filter(id=post.id).exists():
                                free = Freepost_j.objects.get(id=post.id)

                                posts.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "content": free.content,
                                    "created_at": free.created_at,
                                    "views": free.views,
                                    "userable_id": free.userable.id,
                                    "postable_ptr_id": free.id,
                                    "image": free.image.url,
                                })
                elif search_type == "회사이름":
                    employer = Employer.objects.filter(company__icontains=keyword)
                    posts = list(Freepost_j.objects.filter(title__in=employer).order_by("created_at").values("id","title","views"))
                    ranks = list(Freepost_j.objects.filter(title__in=employer).order_by("-views").values("id","title","views"))[0:4]

        elif category == "구인":
            if board_type == "구인":
                if post_type == "관심분야":
                    # user = request.user
                    user = Userable.objects.get(id=3)
                    interest = list(UserInterest.objects.filter(userable=user).values_list("interest", flat=True))
                    employer = Employer.objects.filter(interest__in=interest)
                    if search_type == "제목":
                        posts = list(
                            Employ_post.objects.filter(title__icontains=keyword, userable__in=employer).values())

                    elif search_type == "내용":
                        posts = list(
                            Employ_post.objects.filter(content__icontains=keyword, userable__in=employer).values())

                    elif search_type == "제목+내용":
                        posts = list(Employ_post.objects.filter(Q(title__icontains=keyword, userable__in=employer)
                                                                | Q(content__icontains=keyword,
                                                                    userable__in=employer)).values())

                    elif search_type == "해시태그":
                        posts = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id, userable__in=employer).exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "content": free.content,
                                        "created_at": free.created_at,
                                        "views": free.views,
                                        "userable_id": free.userable.id,
                                        "postable_ptr_id": free.id,
                                        "image": free.image.url,
                                    })


                elif post_type == "경력":
                    if search_type == "제목":
                        posts = list(Employ_post.objects.filter(title__icontains=keyword, career='경력').values())

                    elif search_type == "내용":
                        posts = list(Employ_post.objects.filter(content__icontains=keyword, career='경력').values())

                    elif search_type == "제목+내용":
                        posts = list(Employ_post.objects.filter(Q(title__icontains=keyword, career='경력')
                                                                | Q(content__icontains=keyword, career='경력')).values())


                    elif search_type == "해시태그":
                        posts = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id, career="경력").exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "content": free.content,
                                        "created_at": free.created_at,
                                        "views": free.views,
                                        "userable_id": free.userable.id,
                                        "postable_ptr_id": free.id,
                                        "image": free.image.url,
                                    })

                elif post_type == "신입":
                    if search_type == "제목":
                        posts = list(Employ_post.objects.filter(title__icontains=keyword, career='신입').values())

                    elif search_type == "내용":
                        posts = list(Employ_post.objects.filter(content__icontains=keyword, career='신입').values())

                    elif search_type == "제목+내용":
                        posts = list(Employ_post.objects.filter(Q(title__icontains=keyword, career='신입')
                                                                | Q(content__icontains=keyword, career='신입')).values())

                    elif search_type == "해시태그":
                        posts = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id, career="신입").exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "content": free.content,
                                        "created_at": free.created_at,
                                        "views": free.views,
                                        "userable_id": free.userable.id,
                                        "postable_ptr_id": free.id,
                                        "image": free.image.url,
                                    })

            else:
                if search_type == "제목":
                    posts = list(Freepost_e.objects.filter(title__icontains=keyword).values())

                elif search_type == "내용":
                    posts = list(Freepost_e.objects.filter(content__icontains=keyword).values())

                elif search_type == "제목+내용":
                    posts = list(
                        Freepost_e.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).values())

                elif search_type == "해시태그":
                    post = []
                    hashtag = Hashtag.objects.get(name=keyword)

                    for post in hashtag.postable.all():
                        if Freepost_e.objects.filter(id=post.id, career="신입").exists():
                            free = Freepost_e.objects.get(id=post.id)

                            posts.append({
                                "id": free.id,
                                "title": free.title,
                                "content": free.content,
                                "created_at": free.created_at,
                                "views": free.views,
                                "userable_id": free.userable.id,
                                "postable_ptr_id": free.id,
                                "image": free.image.url,
                            })

        else:
            posts = list(Postable.objects.filter(title__contains=keyword).values())

        return JsonResponse({"total_pages" : len(posts)//5+1})

def search_posts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        keyword = data['keyword']
        category = data['category']
        board_type = data['board_type']
        post_type = data['post_type']
        search_type = data['search_type']
        page_num = data["page_num"]
        posts = []
        ranks = []
        if category == "구직":

            if board_type == "구직":
                if search_type == "제목":
                    print(1)
                    posts = list(Job_post.objects.filter(title__icontains=keyword).order_by("created_at").values("id","title","views"))
                    ranks = list(Job_post.objects.filter(title__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]
                elif search_type == "내용":
                    posts = list(Job_post.objects.filter(content__icontains=keyword).order_by("created_at").values())
                    ranks = list(Job_post.objects.filter(content__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]
                elif search_type == "제목+내용":
                    posts = list(Job_post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).values("id","title","views"))
                    ranks = list(Job_post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("-views").values("id","title","views"))[0:4]
                elif search_type == "해시태그":
                    posts = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Job_post.objects.filter(id=post.id).exists():
                                free = Job_post.objects.get(id=post.id)

                                posts.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "views": free.views,
                                    "created_at": free.created_at,
                                })
                    posts = sorted(posts , key= lambda x: x['created_at'], reverse=True)
                    posts = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in posts]
                    ranks = sorted(posts , key= lambda x: x['views'], reverse=True)
                elif search_type == "회사이름":
                    employer = Employer.objects.filter(company__icontains=keyword)
                    posts = list(Freepost_j.objects.filter(title__in=employer).order_by("created_at").values("id","title","views"))
                    ranks = list(Freepost_j.objects.filter(title__in=employer).order_by("-views").values("id","title","views"))[0:4]

            else:
                if search_type == "제목":
                    posts = list(Freepost_j.objects.filter(title__icontains=keyword).order_by("created_at").values("id","title","views"))
                    ranks = list(Freepost_j.objects.filter(title__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]

                elif search_type == "내용":
                    posts = list(Freepost_j.objects.filter(content__icontains=keyword).order_by("created_at").values("id","title","views"))
                    ranks = list(Freepost_j.objects.filter(content__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]

                elif search_type == "제목+내용":
                    posts = list(
                        Freepost_j.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("created_at").values("id","title","views"))
                    ranks = list(Freepost_j.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("-views").values("id","title","views"))[0:4]

                elif search_type == "해시태그":
                    posts = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Freepost_j.objects.filter(id=post.id).exists():
                                free = Freepost_j.objects.get(id=post.id)

                                posts.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "views": free.views,
                                    "created_at": free.created_at,
                                })
                    posts = sorted(posts , key= lambda x: x['created_at'], reverse=True)
                    posts = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in posts]
                    ranks = sorted(posts , key= lambda x: x['views'], reverse=True)
                elif search_type == "회사이름":
                    employer = Employer.objects.filter(company__icontains=keyword)
                    posts = list(Freepost_j.objects.filter(title__in=employer).order_by("created_at").values("id","title","views"))
                    ranks = list(Freepost_j.objects.filter(title__in=employer).order_by("-views").values("id","title","views"))[0:4]

        elif category == "구인":
            if board_type == "구인":
                if post_type == "관심분야":
                    # user = request.user
                    user = Userable.objects.get(id=3)
                    interest = list(UserInterest.objects.filter(userable=user).values_list("interest", flat=True))
                    employer = Employer.objects.filter(interest__in=interest)
                    if search_type == "제목":
                        posts = list(
                            Employ_post.objects.filter(title__icontains=keyword, userable__in=employer).order_by("created_at").values("id","title","views"))
                        ranks = list(Employ_post.objects.filter(title__icontains=keyword, userable__in=employer).order_by("-views").values("id","title","views"))[0:4]

                    elif search_type == "내용":
                        posts = list(
                            Employ_post.objects.filter(content__icontains=keyword, userable__in=employer).order_by("created_at").values("id","title","views"))
                        ranks = list(Employ_post.objects.filter(content__icontains=keyword, userable__in=employer).order_by("-views").values("id","title","views"))[0:4]

                    elif search_type == "제목+내용":
                        posts = list(Employ_post.objects.filter(Q(title__icontains=keyword, userable__in=employer)
                                                                | Q(content__icontains=keyword,
                                                                    userable__in=employer)).order_by("created_at").values("id","title","views"))
                        ranks = list(Employ_post.objects.filter(Q(title__icontains=keyword, userable__in=employer)
                                                                | Q(content__icontains=keyword,
                                                                    userable__in=employer)).order_by("-views").values("id","title","views"))[0:4]

                    elif search_type == "해시태그":
                        posts = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id, userable__in=employer).exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "views": free.views,
                                        "created_at": free.created_at,
                                    })
                        posts = sorted(posts , key= lambda x: x['created_at'], reverse=True)
                        posts = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in posts]
                        ranks = sorted(posts , key= lambda x: x['views'], reverse=True)


                elif post_type == "경력":
                    if search_type == "제목":
                        posts = list(Employ_post.objects.filter(title__icontains=keyword, career='경력').order_by("created_at").values("id","title","views"))
                        ranks = list(Employ_post.objects.filter(title__icontains=keyword, career='경력').order_by("-views").values("id","title","views"))[0:4]

                    elif search_type == "내용":
                        posts = list(Employ_post.objects.filter(content__icontains=keyword, career='경력').order_by("created_at").values("id","title","views"))
                        ranks = list(Employ_post.objects.filter(content__icontains=keyword, career='경력').order_by("-views").values("id","title","views"))[0:4]

                    elif search_type == "제목+내용":
                        posts = list(Employ_post.objects.filter(Q(title__icontains=keyword, career='경력')
                                                                | Q(content__icontains=keyword, career='경력')).order_by("created_at").values("id","title","views"))
                        ranks = list(Employ_post.objects.filter(Q(title__icontains=keyword, career='경력')
                                                                | Q(content__icontains=keyword, career='경력')).order_by("-views").values("id","title","views"))[0:4]


                    elif search_type == "해시태그":
                        posts = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id, career="경력").exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "views": free.views,
                                        "created_at": free.created_at,
                                    })
                        posts = sorted(posts , key= lambda x: x['created_at'], reverse=True)
                        posts = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in posts]
                        ranks = sorted(posts , key= lambda x: x['views'], reverse=True)

                elif post_type == "신입":
                    if search_type == "제목":
                        posts = list(Employ_post.objects.filter(title__icontains=keyword, career='신입').order_by("created_at").values("id","title","views"))
                        ranks = list(Employ_post.objects.filter(title__icontains=keyword, career='신입').order_by("-views").values("id","title","views"))[0:4]

                    elif search_type == "내용":
                        posts = list(Employ_post.objects.filter(content__icontains=keyword, career='신입').order_by("created_at").values("id","title","views"))
                        ranks = list(Employ_post.objects.filter(content__icontains=keyword, career='신입').order_by("-views").values("id","title","views"))[0:4]

                    elif search_type == "제목+내용":
                        posts = list(Employ_post.objects.filter(Q(title__icontains=keyword, career='신입')
                                                                | Q(content__icontains=keyword, career='신입')).order_by("created_at").values("id","title","views"))
                        ranks = list(Employ_post.objects.filter(Q(title__icontains=keyword, career='신입')
                                                                | Q(content__icontains=keyword, career='신입')).order_by("-views").values("id","title","views"))[0:4]

                    elif search_type == "해시태그":
                        posts = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id, career="신입").exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "views": free.views,
                                        "created_at": free.created_at,
                                    })
                        posts = sorted(posts , key= lambda x: x['created_at'], reverse=True)
                        posts = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in posts]
                        ranks = sorted(posts , key= lambda x: x['views'], reverse=True)

            else:
                if search_type == "제목":
                    posts = list(Freepost_e.objects.filter(title__icontains=keyword).order_by("created_at").values("id","title","views"))
                    ranks = list(Freepost_e.objects.filter(title__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]

                elif search_type == "내용":
                    posts = list(Freepost_e.objects.filter(content__icontains=keyword).order_by("created_at").values("id","title","views"))
                    ranks = list(Freepost_e.objects.filter(content__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]

                elif search_type == "제목+내용":
                    posts = list(
                        Freepost_e.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("created_at").values("id","title","views"))
                    ranks = list(Freepost_e.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("-views").values("id","title","views"))[0:4]

                elif search_type == "해시태그":
                    post = []
                    hashtag = Hashtag.objects.get(name=keyword)
                    for post in hashtag.postable.all():

                        if Freepost_e.objects.filter(id=post.id, career="신입").exists():
                            free = Freepost_e.objects.get(id=post.id)

                            posts.append({
                                "id": free.id,
                                "title": free.title,
                                "views": free.views,
                                "created_at": free.created_at,
                            })
                    posts = sorted(posts , key= lambda x: x['created_at'], reverse=True)
                    posts = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in posts]
                    ranks = sorted(posts , key= lambda x: x['views'], reverse=True)

        else:
            posts = list(Postable.objects.filter(title__contains=keyword).order_by("created_at").values("id","title","views"))
            ranks = list(Freepost_e.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("-views").values("id","title","views"))[0:4]

        return JsonResponse({'posts': posts[5*(page_num-1):5*page_num-1], 'ranks' : ranks})

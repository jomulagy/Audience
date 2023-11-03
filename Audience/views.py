from django.shortcuts import render, redirect
from django.http import JsonResponse
from account.models import Employer
from employ.models import Postable, Employ_post, Freepost_e
from util.models import Hashtag, Interest, UserInterest
from job.models import Job_post, Freepost_j
import json
from django.db.models import Q
from account.models import Userable

# 인트로
def intro_view(request):
    return render(request, 'intro.html')

# 메인화면
def main_view(request):
    employ_posts = Employ_post.objects.order_by('-created_at')[:5]  # 구인글 5개
    job_posts = Job_post.objects.order_by('-created_at')[:5]  # 구직글 5개
    context = {'employ_posts': employ_posts, 'job_posts': job_posts}

    return render(request, 'main.html', context)


# 검색페이지(검색어 get parameter)
# 뷰만 띄움
def search_page(request, keyword, category, board_type, post_type, search_type):

    return render(request, 'Post/search.html')

def post_list_page(request, category, board_type, post_type, search_type):
    context = {
        "category" : category + "자"
    }
    return render(request, 'Post/postList.html',context)

# 검색 결과
# 매개변수로 검색어랑 카테고리 pk로 받아서 검색
# ajax
# 구인 카테고리면 employ에서 구직이면 job에서 자유면 freepost

def total_page(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        if "my_page" in data:
            if request.user.is_authenticated:
                posts = Postable.objects.order_by('-created_at')
                return JsonResponse({'total_num': len(posts) // 5 + 1})
        keyword = data['keyword']
        category = data['category']
        board_type = data['board_type']
        post_type = data['post_type']
        search_type = data['search_type']
        if keyword:
            if category == "구직":

                if board_type == "구직":
                    posts_hashtag = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Job_post.objects.filter(id=post.id).exists():
                                free = Job_post.objects.get(id=post.id)

                                posts_hashtag.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "views": free.views,
                                    "created_at": free.created_at,
                                })
                    posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                    posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for
                                     dictionary in
                                     posts_hashtag]
                    employer = Employer.objects.filter(company__icontains=keyword)
                    total = {
                        "제목": {
                            "posts": list(
                                Job_post.objects.filter(title__icontains=keyword).order_by("-created_at").values("id",
                                                                                                                 "title",
                                                                                                                 "views")),
                        },
                        "내용": {
                            "posts": list(
                                Job_post.objects.filter(content__icontains=keyword).order_by("-created_at").values()),
                        },
                        "제목+내용": {
                            "posts": list(Job_post.objects.filter(
                                Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by(
                                "-created_at").values("id", "title", "views")),
                        },
                        "해시태그": {
                            "posts": posts_hashtag,
                        },
                        "회사이름": {
                            "posts": list(
                                Freepost_j.objects.filter(title__in=employer).order_by("-created_at").values("id",
                                                                                                             "title",
                                                                                                             "views")),
                        },
                    }
                    if search_type == "제목":
                        posts = total["제목"]["posts"]
                        print(posts)
                    elif search_type == "내용":
                        posts = total["내용"]["posts"]
                    elif search_type == "제목+내용":
                        posts = total["제목+내용"]["posts"]
                    elif search_type == "해시태그":
                        print(total["해시태그"])
                        posts = total["해시태그"]["posts"]
                    elif search_type == "회사이름":
                        posts = total["회사이름"]["posts"]
                    else:
                        posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + total["해시태그"][
                            "posts"] + total["회사이름"]["posts"]
                        seen = set()
                        posts = [d for d in posts if
                                 frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                else:
                    posts_hashtag = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Freepost_j.objects.filter(id=post.id).exists():
                                free = Freepost_j.objects.get(id=post.id)

                                posts_hashtag.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "views": free.views,
                                    "created_at": free.created_at,
                                })
                    posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                    posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for
                                     dictionary in
                                     posts_hashtag]
                    employer = Employer.objects.filter(company__icontains=keyword)
                    total = {
                        "제목": {
                            "posts": list(
                                Freepost_j.objects.filter(title__icontains=keyword).order_by("created_at").values("id",
                                                                                                                  "title",
                                                                                                                  "views")),
                        },
                        "내용": {
                            "posts": list(
                                Freepost_j.objects.filter(content__icontains=keyword).order_by("created_at").values(
                                    "id", "title", "views")),
                        },
                        "제목+내용": {
                            "posts": list(Freepost_j.objects.filter(
                                Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by(
                                "created_at").values("id", "title", "views")),
                        },
                        "해시태그": {
                            "posts": posts_hashtag,
                        },
                        "회사이름": {
                            "posts": list(
                                Freepost_j.objects.filter(title__in=employer).order_by("created_at").values("id",
                                                                                                            "title",
                                                                                                            "views")),
                        },
                    }
                    if search_type == "제목":
                        posts = total["제목"]["posts"]
                    elif search_type == "내용":
                        posts = total["내용"]["posts"]
                    elif search_type == "제목+내용":
                        posts = total["제목+내용"]["posts"]
                    elif search_type == "해시태그":
                        posts = total["해시태그"]["posts"]
                    elif search_type == "회사이름":
                        posts = total["회사이름"]["posts"]
                    else:
                        posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + total["해시태그"][
                            "posts"] + total["회사이름"]["posts"]
                        seen = set()
                        posts = [d for d in posts if
                                 frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]

            elif category == "구인":
                if board_type == "구인":

                    if post_type == "관심분야":
                        user = request.user
                        interest = list(UserInterest.objects.filter(userable=user).values_list("interest", flat=True))
                        employer = Employer.objects.filter(interest__in=interest)
                        posts_hashtag = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id, userable__in=employer).exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts_hashtag.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "views": free.views,
                                        "created_at": free.created_at,
                                    })
                        posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                        posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for
                                         dictionary in
                                         posts_hashtag]
                        total = {
                            "제목": {
                                "posts": list(Employ_post.objects.filter(title__icontains=keyword,
                                                                         userable__in=employer).order_by(
                                    "created_at").values("id", "title", "views")),
                            },
                            "내용": {
                                "posts": list(Employ_post.objects.filter(content__icontains=keyword,
                                                                         userable__in=employer).order_by(
                                    "created_at").values("id", "title", "views")),
                            },
                            "제목+내용": {
                                "posts": list(
                                    Employ_post.objects.filter(Q(title__icontains=keyword, userable__in=employer)
                                                               | Q(content__icontains=keyword,
                                                                   userable__in=employer)).order_by(
                                        "created_at").values("id", "title", "views")),
                            },
                            "해시태그": {
                                "posts": posts_hashtag,
                            },

                        }

                        if search_type == "제목":
                            posts = total["제목"]["posts"]
                        elif search_type == "내용":
                            posts = total["내용"]["posts"]
                        elif search_type == "제목+내용":
                            posts = total["제목+내용"]["posts"]
                        elif search_type == "해시태그":
                            posts = total["해시태그"]["posts"]
                        else:
                            posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + \
                                    total["해시태그"]["posts"]
                            seen = set()
                            posts = [d for d in posts if
                                     frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]

                    elif post_type == "경력":
                        posts_hashtag = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id, career="경력").exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts_hashtag.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "views": free.views,
                                        "created_at": free.created_at,
                                    })
                        posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                        posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for
                                         dictionary in
                                         posts_hashtag]
                        total = {
                            "제목": {
                                "posts": list(
                                    Employ_post.objects.filter(title__icontains=keyword, career='경력').order_by(
                                        "created_at").values("id", "title", "views")),
                            },
                            "내용": {
                                "posts": list(
                                    Employ_post.objects.filter(content__icontains=keyword, career='경력').order_by(
                                        "created_at").values("id", "title", "views")),
                            },
                            "제목+내용": {
                                "posts": list(Employ_post.objects.filter(Q(title__icontains=keyword, career='경력')
                                                                         | Q(content__icontains=keyword,
                                                                             career='경력')).order_by(
                                    "created_at").values("id", "title", "views")),
                            },
                            "해시태그": {
                                "posts": posts_hashtag,
                            },

                        }
                        if search_type == "제목":
                            posts = total["제목"]["posts"]
                        elif search_type == "내용":
                            posts = total["내용"]["posts"]
                        elif search_type == "제목+내용":
                            posts = total["제목+내용"]["posts"]
                        elif search_type == "해시태그":
                            posts = total["해시태그"]["posts"]
                        else:
                            posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + \
                                    total["해시태그"]["posts"]
                            seen = set()
                            posts = [d for d in posts if
                                     frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]

                    elif post_type == "신입":
                        posts_hashtag = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id, career="신입").exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts_hashtag.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "views": free.views,
                                        "created_at": free.created_at,
                                    })
                        posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                        posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for
                                         dictionary in
                                         posts_hashtag]
                        total = {
                            "제목": {
                                "posts": list(
                                    Employ_post.objects.filter(title__icontains=keyword, career='신입').order_by(
                                        "created_at").values("id", "title", "views")),
                            },
                            "내용": {
                                "posts": list(
                                    Employ_post.objects.filter(content__icontains=keyword, career='신입').order_by(
                                        "created_at").values("id", "title", "views")),
                            },
                            "제목+내용": {
                                "posts": list(Employ_post.objects.filter(
                                    Q(title__icontains=keyword, career='신입') | Q(content__icontains=keyword,
                                                                                 career='신입')).order_by(
                                    "created_at").values("id", "title", "views")),
                            },
                            "해시태그": {
                                "posts": posts_hashtag,
                            },

                        }
                        if search_type == "제목":
                            posts = total["제목"]["posts"]
                        elif search_type == "내용":
                            posts = total["내용"]["posts"]
                        elif search_type == "제목+내용":
                            posts = total["제목+내용"]["posts"]
                        elif search_type == "해시태그":
                            print(total["해시태그"])
                            posts = total["해시태그"]["posts"]
                        else:
                            posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + \
                                    total["해시태그"]["posts"]
                            seen = set()
                            posts = [d for d in posts if
                                     frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                    else:
                        posts_hashtag = []
                        if Hashtag.objects.filter(name=keyword).exists():
                            hashtag = Hashtag.objects.get(name=keyword)
                            for post in hashtag.postable.all():
                                if Employ_post.objects.filter(id=post.id).exists():
                                    free = Employ_post.objects.get(id=post.id)

                                    posts_hashtag.append({
                                        "id": free.id,
                                        "title": free.title,
                                        "views": free.views,
                                        "created_at": free.created_at,
                                    })
                        posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                        posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for
                                         dictionary in
                                         posts_hashtag]
                        total = {
                            "제목": {
                                "posts": list(
                                    Employ_post.objects.filter(title__icontains=keyword).order_by("created_at").values(
                                        "id", "title", "views")),
                            },
                            "내용": {
                                "posts": list(
                                    Employ_post.objects.filter(content__icontains=keyword, career='신입').order_by(
                                        "created_at").values("id", "title", "views")),
                            },
                            "제목+내용": {
                                "posts": list(Employ_post.objects.filter(
                                    Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by(
                                    "created_at").values("id", "title", "views")),
                            },
                            "해시태그": {
                                "posts": posts_hashtag,
                            },

                        }
                        if search_type == "제목":
                            posts = total["제목"]["posts"]
                            print(posts)
                        elif search_type == "내용":
                            posts = total["내용"]["posts"]
                        elif search_type == "제목+내용":
                            posts = total["제목+내용"]["posts"]
                        elif search_type == "해시태그":
                            print(total["해시태그"])
                            posts = total["해시태그"]["posts"]
                        else:
                            posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + \
                                    total["해시태그"]["posts"]
                            seen = set()
                            posts = [d for d in posts if
                                     frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                else:
                    posts_hashtag = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():

                            if Freepost_e.objects.filter(id=post.id).exists():
                                free = Freepost_e.objects.get(id=post.id)

                                posts_hashtag.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "views": free.views,
                                    "created_at": free.created_at,
                                })
                        posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                        posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for
                                         dictionary in
                                         posts_hashtag]
                        total = {
                            "제목": {
                                "posts": list(
                                    Freepost_e.objects.filter(title__icontains=keyword).order_by("created_at").values("id",
                                                                                                                      "title",
                                                                                                                      "views")),
                            },
                            "내용": {
                                "posts": list(
                                    Freepost_e.objects.filter(content__icontains=keyword).order_by("created_at").values(
                                        "id", "title", "views")),
                            },
                            "제목+내용": {
                                "posts": list(
                                    Freepost_e.objects.filter(
                                        Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by(
                                        "created_at").values("id", "title", "views")),
                            },
                            "해시태그": {
                                "posts": posts_hashtag,
                            },

                        }
                        if search_type == "제목":
                            posts = total["제목"]["posts"]
                        elif search_type == "내용":
                            posts = total["내용"]["posts"]
                        elif search_type == "제목+내용":
                            posts = total["제목+내용"]["posts"]
                        elif search_type == "해시태그":
                            print(total["해시태그"])
                            posts = total["해시태그"]["posts"]
                        else:
                            posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + total["해시태그"][
                                "posts"]
                            seen = set()
                            posts = [d for d in posts if
                                     frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
            else:
                posts_hashtag = []
                if Hashtag.objects.filter(name=keyword).exists():
                    hashtag = Hashtag.objects.get(name=keyword)
                    for post in hashtag.postable.all():

                        if Postable.objects.filter(id=post.id).exists():
                            free = Postable.objects.get(id=post.id)

                            posts_hashtag.append({
                                "id": free.id,
                                "title": free.title,
                                "views": free.views,
                                "created_at": free.created_at,
                            })
                    posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                    posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary
                                     in
                                     posts_hashtag]
                    total = {
                        "제목": {
                            "posts": list(
                                Postable.objects.filter(title__icontains=keyword).order_by("created_at").values("id",
                                                                                                                "title",
                                                                                                                "views")),
                        },
                        "내용": {
                            "posts": list(
                                Postable.objects.filter(content__icontains=keyword).order_by("created_at").values("id",
                                                                                                                  "title",
                                                                                                                  "views")),
                        },
                        "제목+내용": {
                            "posts": list(
                                Postable.objects.filter(
                                    Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by(
                                    "created_at").values("id", "title", "views")),
                        },
                        "해시태그": {
                            "posts": posts_hashtag,
                        },

                    }

                    posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + total["해시태그"][
                        "posts"]
                    seen = set()
                    posts = [d for d in posts if
                             frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]

        else:
            if category == "구직":

                if board_type == "구직":
                    posts = list(Job_post.objects.all().order_by("-created_at").values("id","title","views"))

                else:
                    posts = list(Freepost_j.objects.all().order_by("created_at").values("id","title","views"))

            elif category == "구인":
                if board_type == "구인":

                    if post_type == "관심분야":
                        user = request.user
                        interest = list(UserInterest.objects.filter(userable=user).values_list("interest", flat=True))
                        employer = Employer.objects.filter(interest__in=interest)
                        posts = list(Employ_post.objects.filter(userable__in=employer).order_by("created_at").values("id","title","views"))

                    elif post_type == "경력":
                        posts = list(Employ_post.objects.filter(career='경력').order_by("created_at").values("id","title","views"))

                    elif post_type == "신입":
                        posts = list(Employ_post.objects.filter(career='신입').order_by("created_at").values("id","title","views"))

                    else:
                        posts = list(Employ_post.objects.all().order_by("created_at").values("id","title","views"))

                else:
                    posts = list(Freepost_e.objects.all().order_by("created_at").values("id","title","views"))

            else:
                posts = list(Postable.objects.all().order_by("created_at").values("id", "title","views"))
        return JsonResponse({'total_pages': len(posts) // 5 + 1})

def search_posts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        keyword = data['keyword']
        category = data['category']
        board_type = data['board_type']
        post_type = data['post_type']
        search_type = data['search_type']
        page_num = data["page_num"]

        if category == "구직":

            if board_type == "구직":
                posts_hashtag = []
                if Hashtag.objects.filter(name=keyword).exists():
                    hashtag = Hashtag.objects.get(name=keyword)
                    for post in hashtag.postable.all():
                        if Job_post.objects.filter(id=post.id).exists():
                            free = Job_post.objects.get(id=post.id)

                            posts_hashtag.append({
                                "id": free.id,
                                "title": free.title,
                                "views": free.views,
                                "created_at": free.created_at,
                            })
                posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in
                         posts_hashtag]
                ranks_hashtag = sorted(posts_hashtag, key=lambda x: x['views'], reverse=True)[0:4]
                employer = Employer.objects.filter(company__icontains=keyword)
                total = {
                        "제목": {
                            "posts" : list(Job_post.objects.filter(title__icontains=keyword).order_by("-created_at").values("id","title","views")),
                            "ranks" : list(Job_post.objects.filter(title__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "내용": {
                            "posts" : list(Job_post.objects.filter(content__icontains=keyword).order_by("-created_at").values()),
                            "ranks" : list(Job_post.objects.filter(content__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "제목+내용": {
                            "posts" : list(Job_post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("-created_at").values("id","title","views")),
                            "ranks" : list(Job_post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "해시태그": {
                            "posts" : posts_hashtag,
                            "ranks" : ranks_hashtag
                        },
                        "회사이름": {
                            "posts" : list(Freepost_j.objects.filter(title__in=employer).order_by("-created_at").values("id","title","views")),
                            "ranks" : list(Freepost_j.objects.filter(title__in=employer).order_by("-views").values("id","title","views"))[0:4]
                        },
                }
                if search_type == "제목":
                    posts = total["제목"]["posts"]
                    ranks = total["제목"]["ranks"]
                elif search_type == "내용":
                    posts = total["내용"]["posts"]
                    ranks = total["내용"]["ranks"]
                elif search_type == "제목+내용":
                    posts = total["제목+내용"]["posts"]
                    ranks = total["제목+내용"]["ranks"]
                elif search_type == "해시태그":
                    print(total["해시태그"])
                    posts = total["해시태그"]["posts"]
                    ranks = total["해시태그"]["ranks"]
                elif search_type == "회사이름":
                    posts = total["회사이름"]["posts"]
                    ranks = total["회사이름"]["ranks"]
                else:
                    posts = total["제목"]["posts"]+total["내용"]["posts"]+total["제목+내용"]["posts"]+total["해시태그"]["posts"]+total["회사이름"]["posts"]
                    seen = set()
                    posts = [d for d in posts if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                    seen = set()
                    ranks = total["제목"]["ranks"]+total["내용"]["ranks"]+total["제목+내용"]["ranks"]+total["해시태그"]["ranks"]+total["회사이름"]["ranks"]
                    ranks = [d for d in ranks if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
            else:
                posts_hashtag = []
                if Hashtag.objects.filter(name=keyword).exists():
                    hashtag = Hashtag.objects.get(name=keyword)
                    for post in hashtag.postable.all():
                        if Freepost_j.objects.filter(id=post.id).exists():
                            free = Freepost_j.objects.get(id=post.id)

                            posts_hashtag.append({
                                "id": free.id,
                                "title": free.title,
                                "views": free.views,
                                "created_at": free.created_at,
                            })
                posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in
                         posts_hashtag]
                ranks_hashtag = sorted(posts_hashtag, key=lambda x: x['views'], reverse=True)[0:4]
                employer = Employer.objects.filter(company__icontains=keyword)
                total = {
                        "제목": {
                            "posts" : list(Freepost_j.objects.filter(title__icontains=keyword).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Freepost_j.objects.filter(title__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "내용": {
                            "posts" : list(Freepost_j.objects.filter(content__icontains=keyword).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Freepost_j.objects.filter(content__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "제목+내용": {
                            "posts" : list(Freepost_j.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Freepost_j.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "해시태그": {
                            "posts" : posts_hashtag,
                            "ranks" : ranks_hashtag
                        },
                        "회사이름": {
                            "posts" : list(Freepost_j.objects.filter(title__in=employer).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Freepost_j.objects.filter(title__in=employer).order_by("-views").values("id","title","views"))[0:4]
                        },
                }
                if search_type == "제목":
                    posts = total["제목"]["posts"]
                    ranks = total["제목"]["ranks"]
                elif search_type == "내용":
                    posts = total["내용"]["posts"]
                    ranks = total["내용"]["ranks"]
                elif search_type == "제목+내용":
                    posts = total["제목+내용"]["posts"]
                    ranks = total["제목+내용"]["ranks"]
                elif search_type == "해시태그":
                    print(total["해시태그"])
                    posts = total["해시태그"]["posts"]
                    ranks = total["해시태그"]["ranks"]
                elif search_type == "회사이름":
                    posts = total["회사이름"]["posts"]
                    ranks = total["회사이름"]["ranks"]
                else:
                    posts = total["제목"]["posts"]+total["내용"]["posts"]+total["제목+내용"]["posts"]+total["해시태그"]["posts"]+total["회사이름"]["posts"]
                    seen = set()
                    posts = [d for d in posts if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                    seen = set()
                    ranks = total["제목"]["ranks"]+total["내용"]["ranks"]+total["제목+내용"]["ranks"]+total["해시태그"]["ranks"]+total["회사이름"]["ranks"]
                    ranks = [d for d in ranks if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]

        elif category == "구인":
            if board_type == "구인":

                if post_type == "관심분야":
                    user = request.user
                    interest = list(UserInterest.objects.filter(userable=user).values_list("interest", flat=True))
                    employer = Employer.objects.filter(interest__in=interest)
                    posts_hashtag = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Employ_post.objects.filter(id=post.id, userable__in=employer).exists():
                                free = Employ_post.objects.get(id=post.id)

                                posts_hashtag.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "views": free.views,
                                    "created_at": free.created_at,
                                })
                    posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                    posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in
                             posts_hashtag]
                    ranks_hashtag = sorted(posts_hashtag, key=lambda x: x['views'], reverse=True)
                    total = {
                        "제목": {
                            "posts" : list(Employ_post.objects.filter(title__icontains=keyword, userable__in=employer).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(title__icontains=keyword, userable__in=employer).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "내용": {
                            "posts" : list(Employ_post.objects.filter(content__icontains=keyword, userable__in=employer).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(content__icontains=keyword, userable__in=employer).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "제목+내용": {
                            "posts" : list(Employ_post.objects.filter(Q(title__icontains=keyword, userable__in=employer)
                                                                | Q(content__icontains=keyword,
                                                                    userable__in=employer)).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(Q(title__icontains=keyword, userable__in=employer)
                                                                | Q(content__icontains=keyword,
                                                                    userable__in=employer)).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "해시태그": {
                            "posts" : posts_hashtag,
                            "ranks" : ranks_hashtag
                        },

                    }

                    if search_type == "제목":
                        posts = total["제목"]["posts"]
                        ranks = total["제목"]["ranks"]
                    elif search_type == "내용":
                        posts = total["내용"]["posts"]
                        ranks = total["내용"]["ranks"]
                    elif search_type == "제목+내용":
                        posts = total["제목+내용"]["posts"]
                        ranks = total["제목+내용"]["ranks"]
                    elif search_type == "해시태그":
                        print(total["해시태그"])
                        posts = total["해시태그"]["posts"]
                        ranks = total["해시태그"]["ranks"]
                    else:
                        posts = total["제목"]["posts"]+total["내용"]["posts"]+total["제목+내용"]["posts"]+total["해시태그"]["posts"]
                        seen = set()
                        posts = [d for d in posts if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                        seen = set()
                        ranks = total["제목"]["ranks"]+total["내용"]["ranks"]+total["제목+내용"]["ranks"]+total["해시태그"]["ranks"]
                        ranks = [d for d in ranks if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]

                elif post_type == "경력":
                    posts_hashtag = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Employ_post.objects.filter(id=post.id, career="경력").exists():
                                free = Employ_post.objects.get(id=post.id)

                                posts_hashtag.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "views": free.views,
                                    "created_at": free.created_at,
                                })
                    posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                    posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in
                             posts_hashtag]
                    ranks_hashtag = sorted(posts_hashtag, key=lambda x: x['views'], reverse=True)
                    total = {
                        "제목": {
                            "posts" : list(Employ_post.objects.filter(title__icontains=keyword, career='경력').order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(title__icontains=keyword, career='경력').order_by("-views").values("id","title","views"))[0:4]
                        },
                        "내용": {
                            "posts" : list(Employ_post.objects.filter(content__icontains=keyword, career='경력').order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(content__icontains=keyword, career='경력').order_by("-views").values("id","title","views"))[0:4]
                        },
                        "제목+내용": {
                            "posts" : list(Employ_post.objects.filter(Q(title__icontains=keyword, career='경력')
                                                                | Q(content__icontains=keyword, career='경력')).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(Q(title__icontains=keyword, career='경력')
                                                                | Q(content__icontains=keyword, career='경력')).order_by("created_at").values("id","title","views"))
                        },
                        "해시태그": {
                            "posts" : posts_hashtag,
                            "ranks" : ranks_hashtag
                        },

                    }
                    if search_type == "제목":
                        posts = total["제목"]["posts"]
                        ranks = total["제목"]["ranks"]
                    elif search_type == "내용":
                        posts = total["내용"]["posts"]
                        ranks = total["내용"]["ranks"]
                    elif search_type == "제목+내용":
                        posts = total["제목+내용"]["posts"]
                        ranks = total["제목+내용"]["ranks"]
                    elif search_type == "해시태그":
                        print(total["해시태그"])
                        posts = total["해시태그"]["posts"]
                        ranks = total["해시태그"]["ranks"]
                    else:
                        posts = total["제목"]["posts"]+total["내용"]["posts"]+total["제목+내용"]["posts"]+total["해시태그"]["posts"]
                        seen = set()
                        posts = [d for d in posts if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                        seen = set()
                        ranks = total["제목"]["ranks"]+total["내용"]["ranks"]+total["제목+내용"]["ranks"]+total["해시태그"]["ranks"]
                        ranks = [d for d in ranks if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]

                elif post_type == "신입":
                    posts_hashtag = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Employ_post.objects.filter(id=post.id, career="신입").exists():
                                free = Employ_post.objects.get(id=post.id)

                                posts_hashtag.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "views": free.views,
                                    "created_at": free.created_at,
                                })
                    posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                    posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in
                             posts_hashtag]
                    ranks_hashtag = sorted(posts_hashtag, key=lambda x: x['views'], reverse=True)
                    total = {
                        "제목": {
                            "posts" : list(Employ_post.objects.filter(title__icontains=keyword, career='신입').order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(title__icontains=keyword, career='신입').order_by("-views").values("id","title","views"))[0:4]
                        },
                        "내용": {
                            "posts" : list(Employ_post.objects.filter(content__icontains=keyword, career='신입').order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(content__icontains=keyword, career='신입').order_by("-views").values("id","title","views"))[0:4]
                        },
                        "제목+내용": {
                            "posts" : list(Employ_post.objects.filter(Q(title__icontains=keyword, career='신입') | Q(content__icontains=keyword, career='신입')).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(Q(title__icontains=keyword, career='신입')
                                                                | Q(content__icontains=keyword, career='신입')).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "해시태그": {
                            "posts" : posts_hashtag,
                            "ranks" : ranks_hashtag
                        },

                    }
                    if search_type == "제목":
                        posts = total["제목"]["posts"]
                        ranks = total["제목"]["ranks"]
                    elif search_type == "내용":
                        posts = total["내용"]["posts"]
                        ranks = total["내용"]["ranks"]
                    elif search_type == "제목+내용":
                        posts = total["제목+내용"]["posts"]
                        ranks = total["제목+내용"]["ranks"]
                    elif search_type == "해시태그":
                        print(total["해시태그"])
                        posts = total["해시태그"]["posts"]
                        ranks = total["해시태그"]["ranks"]
                    else:
                        posts = total["제목"]["posts"]+total["내용"]["posts"]+total["제목+내용"]["posts"]+total["해시태그"]["posts"]
                        seen = set()
                        posts = [d for d in posts if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                        seen = set()
                        ranks = total["제목"]["ranks"]+total["내용"]["ranks"]+total["제목+내용"]["ranks"]+total["해시태그"]["ranks"]
                        ranks = [d for d in ranks if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                else:
                    posts_hashtag = []
                    if Hashtag.objects.filter(name=keyword).exists():
                        hashtag = Hashtag.objects.get(name=keyword)
                        for post in hashtag.postable.all():
                            if Employ_post.objects.filter(id=post.id).exists():
                                free = Employ_post.objects.get(id=post.id)

                                posts_hashtag.append({
                                    "id": free.id,
                                    "title": free.title,
                                    "views": free.views,
                                    "created_at": free.created_at,
                                })
                    posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                    posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in
                             posts_hashtag]
                    ranks_hashtag = sorted(posts_hashtag, key=lambda x: x['views'], reverse=True)
                    total = {
                        "제목": {
                            "posts" : list(Employ_post.objects.filter(title__icontains=keyword).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(title__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "내용": {
                            "posts" : list(Employ_post.objects.filter(content__icontains=keyword, career='신입').order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(content__icontains=keyword, career='신입').order_by("-views").values("id","title","views"))[0:4]
                        },
                        "제목+내용": {
                            "posts" : list(Employ_post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("created_at").values("id","title","views")),
                            "ranks" : list(Employ_post.objects.filter(Q(title__icontains=keyword)
                                                                | Q(content__icontains=keyword)).order_by("-views").values("id","title","views"))[0:4]
                        },
                        "해시태그": {
                            "posts" : posts_hashtag,
                            "ranks" : ranks_hashtag
                        },

                    }
                    if search_type == "제목":
                        posts = total["제목"]["posts"]
                        ranks = total["제목"]["ranks"]
                    elif search_type == "내용":
                        posts = total["내용"]["posts"]
                        ranks = total["내용"]["ranks"]
                    elif search_type == "제목+내용":
                        posts = total["제목+내용"]["posts"]
                        ranks = total["제목+내용"]["ranks"]
                    elif search_type == "해시태그":
                        print(total["해시태그"])
                        posts = total["해시태그"]["posts"]
                        ranks = total["해시태그"]["ranks"]
                    else:
                        posts = total["제목"]["posts"]+total["내용"]["posts"]+total["제목+내용"]["posts"]+total["해시태그"]["posts"]
                        seen = set()
                        posts = [d for d in posts if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                        seen = set()
                        ranks = total["제목"]["ranks"]+total["내용"]["ranks"]+total["제목+내용"]["ranks"]+total["해시태그"]["ranks"]
                        ranks = [d for d in ranks if frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
            else:
                posts_hashtag = []
                if Hashtag.objects.filter(name=keyword).exists():
                    hashtag = Hashtag.objects.get(name=keyword)
                    for post in hashtag.postable.all():

                        if Freepost_e.objects.filter(id=post.id).exists():
                            free = Freepost_e.objects.get(id=post.id)

                            posts_hashtag.append({
                                "id": free.id,
                                "title": free.title,
                                "views": free.views,
                                "created_at": free.created_at,
                            })
                    posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                    posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in
                             posts_hashtag]
                    ranks_hashtag = sorted(posts_hashtag, key=lambda x: x['views'], reverse=True)
                    total = {
                            "제목": {
                                "posts" : list(Freepost_e.objects.filter(title__icontains=keyword).order_by("created_at").values("id","title","views")),
                                "ranks" : list(Freepost_e.objects.filter(title__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]
                            },
                            "내용": {
                                "posts" : list(Freepost_e.objects.filter(content__icontains=keyword).order_by("created_at").values("id","title","views")),
                                "ranks" : list(Freepost_e.objects.filter(content__icontains=keyword).order_by("-views").values("id","title","views"))[0:4]
                            },
                            "제목+내용": {
                                "posts" : list(
                                            Freepost_e.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("created_at").values("id","title","views")),
                                "ranks" : list(Freepost_e.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by("-views").values("id","title","views"))[0:4]
                            },
                            "해시태그": {
                                "posts" : posts_hashtag,
                                "ranks" : ranks_hashtag
                            },

                    }
                    if search_type == "제목":
                        posts = total["제목"]["posts"]
                        ranks = total["제목"]["ranks"]
                    elif search_type == "내용":
                        posts = total["내용"]["posts"]
                        ranks = total["내용"]["ranks"]
                    elif search_type == "제목+내용":
                        posts = total["제목+내용"]["posts"]
                        ranks = total["제목+내용"]["ranks"]
                    elif search_type == "해시태그":
                        print(total["해시태그"])
                        posts = total["해시태그"]["posts"]
                        ranks = total["해시태그"]["ranks"]
                    else:
                        posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + total["해시태그"][
                            "posts"]
                        seen = set()
                        posts = [d for d in posts if
                                 frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                        seen = set()
                        ranks = total["제목"]["ranks"] + total["내용"]["ranks"] + total["제목+내용"]["ranks"] + total["해시태그"][
                            "ranks"]
                        ranks = [d for d in ranks if
                                 frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]

        else:
            posts_hashtag = []
            if Hashtag.objects.filter(name=keyword).exists():
                hashtag = Hashtag.objects.get(name=keyword)
                for post in hashtag.postable.all():

                    if Postable.objects.filter(id=post.id).exists():
                        free = Postable.objects.get(id=post.id)

                        posts_hashtag.append({
                            "id": free.id,
                            "title": free.title,
                            "views": free.views,
                            "created_at": free.created_at,
                        })
                posts_hashtag = sorted(posts_hashtag, key=lambda x: x['created_at'], reverse=True)
                posts_hashtag = [{key: value for key, value in dictionary.items() if key != "created_at"} for dictionary in
                                 posts_hashtag]
                ranks_hashtag = sorted(posts_hashtag, key=lambda x: x['views'], reverse=True)
                total = {
                    "제목": {
                        "posts": list(
                            Postable.objects.filter(title__icontains=keyword).order_by("created_at").values("id", "title",
                                                                                                              "views")),
                        "ranks": list(
                            Postable.objects.filter(title__icontains=keyword).order_by("-views").values("id", "title",
                                                                                                          "views"))[0:4]
                    },
                    "내용": {
                        "posts": list(
                            Postable.objects.filter(content__icontains=keyword).order_by("created_at").values("id",
                                                                                                                "title",
                                                                                                                "views")),
                        "ranks": list(
                            Postable.objects.filter(content__icontains=keyword).order_by("-views").values("id", "title",
                                                                                                            "views"))[0:4]
                    },
                    "제목+내용": {
                        "posts": list(
                            Postable.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by(
                                "created_at").values("id", "title", "views")),
                        "ranks": list(
                            Postable.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by(
                                "-views").values("id", "title", "views"))[0:4]
                    },
                    "해시태그": {
                        "posts": posts_hashtag,
                        "ranks": ranks_hashtag
                    },

                }

                posts = total["제목"]["posts"] + total["내용"]["posts"] + total["제목+내용"]["posts"] + total["해시태그"][
                    "posts"]
                seen = set()
                posts = [d for d in posts if
                         frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]
                seen = set()
                ranks = total["제목"]["ranks"] + total["내용"]["ranks"] + total["제목+내용"]["ranks"] + total["해시태그"][
                    "ranks"]
                ranks = [d for d in ranks if
                         frozenset(d.items()) not in seen and not seen.add(frozenset(d.items()))]

        return JsonResponse({'posts': posts[5*(page_num-1):5*page_num-1], 'ranks': ranks})

def post_list(request):
    if request.method == "POST":
        data = json.loads(request.body)
        category = data['category']
        board_type = data['board_type']
        post_type = data['post_type']
        page_num = data["page_num"]

        if category == "구직":

            if board_type == "구직":
                posts = list(Job_post.objects.all().order_by("-created_at").values("id","title","views", "content"))
                ranks = list(Job_post.objects.all().order_by("-views").values("id","title","views", "content"))[0:4]

            else:
                posts = list(Freepost_j.objects.all().order_by("created_at").values("id","title","views", "content"))
                ranks = list(Freepost_j.objects.all().order_by("-views").values("id","title","views", "content"))[0:4]

        elif category == "구인":
            if board_type == "구인":

                if post_type == "관심분야":
                    user = request.user
                    interest = list(UserInterest.objects.filter(userable=user).values_list("interest", flat=True))
                    employer = Employer.objects.filter(interest__in=interest)
                    posts = list(Employ_post.objects.filter(userable__in=employer).order_by("created_at").values("id","title","views", "content"))
                    ranks = list(Employ_post.objects.filter(userable__in=employer).order_by("-views").values("id","title","views", "content"))[0:4]

                elif post_type == "경력":
                    posts = list(Employ_post.objects.filter(career='경력').order_by("created_at").values("id","title","views", "content"))
                    ranks = list(Employ_post.objects.filter(career='경력').order_by("-views").values("id","title","views", "content"))[0:4]

                elif post_type == "신입":
                    posts = list(Employ_post.objects.filter(career='신입').order_by("created_at").values("id","title","views", "content"))
                    ranks = list(Employ_post.objects.filter(career='신입').order_by("-views").values("id","title","views", "content"))[0:4]

                else:
                    posts = list(Employ_post.objects.all().order_by("created_at").values("id","title","views", "content"))
                    ranks = list(Employ_post.objects.all().order_by("-views").values("id","title","views", "content"))[0:4]

            else:
                posts = list(Freepost_e.objects.all().order_by("created_at").values("id","title","views", "content"))
                ranks = list(Freepost_e.objects.all().order_by("-views").values("id","title","views", "content"))[0:4]

        else:
            posts = list(Postable.objects.all().order_by("created_at").values("id", "title","views", "content"))
            ranks = list(Postable.objects.all().order_by("-views").values("id", "title", "views", "content"))[0:4]

        return JsonResponse({'posts': posts[5*(page_num-1):5*page_num-1], 'ranks': ranks})

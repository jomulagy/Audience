from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import re
import string
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import check_password
from django.views.generic import View

from .models import Userable, Applicant, Employer
from employ.models import Postable
from util.views import update_interest
from util.models import UserInterest
# 로그인
class UserLoginView(View):
    template_name = 'login_error.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('id')
        password = request.POST.get('pw')
        user = authenticate(request, username=username, password=password)

        # 성공
        if user is not None:
            login(request, user=user)
            return redirect('main:main_view')
        # 실패
        else:
            return render(request, 'login_error.html', {'error': True, 'username': username})

# 로그아웃
class UserLogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('intro_view')

# 회원가입
def signup_page(request):
    return render(request, 'sign_up.html')

# 구직자
def create_applicant(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        nickname = request.POST.get('nickname')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        interest = request.POST.getlist('interest')
        school = request.POST.get('school')
        career = request.FILES.get('career')

        context = {'username': username, 'name': name, 'nickname': nickname, 'age': age, 'career': career}

        email_pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, username):
            context["error"] = 'wrong_username_error'
            return render(request, 'sign_up_error_p.html', context)

        if password1 != password2:
            context["error"] = 'no_same_password_error'
            return render(request, 'sign_up_error_p.html', context)

        password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$'
        if not re.match(password_pattern, password1):
            context["error"] = 'wrong_password_error'
            return render(request, 'sign_up_error_p.html', context)

        if Userable.objects.filter(username=username).exists():
            context["error"] = 'username_duplicate_error'
            return render(request, 'sign_up_error_p.html', context)

        if Applicant.objects.filter(nickname=nickname).exists():
            context["error"] = 'nickname_duplicate_error'
            return render(request, 'sign_up_error_p.html', context)

        if not name:
            context["error"] = 'no_name_error'
            return render(request, 'sign_up_error_p.html', context)

        if not nickname:
            context["error"] = 'no_nickname_error'
            return render(request, 'sign_up_error_p', context)

        applicant = Applicant.objects.create_user(
            username=username, password=password1,
            name=name, nickname=nickname, gender=gender,
            age=age, school=school, type='구직자'
        )

        if career:
            file_path = 'applicant_career/' + career.name
            with open(file_path, 'wb') as f:
                for chunk in career.chunks():
                    f.write(chunk)

            applicant.profile_pic = file_path

        update_interest(applicant, interest)
        applicant.save()
        return render(request, 'signup_fin.html', {'id': applicant.username})

    else:
        return render(request, 'sign_up_error_p.html')


# 구인자
def create_employer(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        name = request.POST.get('name')
        company = request.POST.get('company')
        interest = request.POST.getlist('interest')
        image = request.FILES.get('image')

        context = {'username': username, 'name': name, 'company': company}

        email_pattern = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, username):
            context["error"] = 'wrong_username_error'
            return render(request, 'sign_up_error_c.html', context)

        if password1 != password2:
            context["error"] = 'no_same_password_error'
            return render(request, 'sign_up_error_c.html', context)
        password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$'
        if not re.match(password_pattern, password1):
            context["error"] = 'wrong_password_error'
            return render(request, 'sign_up_error_c.html', context)

        if Userable.objects.filter(username=username).exists():
            context["error"] = 'username_duplicate_error'
            return render(request, 'sign_up_error_c.html', context)

        if Employer.objects.filter(company=company).exists():
            context["error"] = 'company_duplicate_error'
            return render(request, 'sign_up_error_c.html', context)

        if not name:
            context["error"] = 'no_name_error'
            return render(request, 'sign_up_error_c.html', context)

        if not company:
            context["error"] = 'no_company_error'
            return render(request, 'sign_up_error_c', context)

        employer = Employer.objects.create_user(
            username=username, password=password1,
            name=name, company=company, type='구인자'
        )
        update_interest(employer, interest)
        if image:
            file_path = 'company_profile/' + image.name
            with open(file_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            employer.profile_pic = file_path

        employer.save()
        return render(request, 'signup_fin.html', {'id': employer.username})

    else:
        return render(request, 'sign_up_error_c.html')


# 회원가입 완료 view
def signup_finish(request):
    return render(request, 'signup_finish.html')

def search_id_pw(request):
    return render(request, 'find_id_pw.html')

# 아이디 찾기 tested
def search_username(request):  # ajax로 받기 (done)
    data = json.loads(request.body)
    name = data['name']
    subname = data['subname']

    # 성공
    is_applicant = Applicant.objects.filter(name=name, nickname=subname).exists()
    is_employer = Employer.objects.filter(name=name, company=subname).exists()
    if is_applicant:
        user = Applicant.objects.get(name=name, nickname=subname)
        return JsonResponse({'success': True, 'username': user.username})

    elif is_employer:
        user = Employer.objects.get(name=name, company=subname)
        return JsonResponse({'success': True, 'username': user.username})
    # 실패
    else:
        return JsonResponse({'success': False, 'error': f'"{name}", "{subname}" does not exist.'})


# 아이디/비밀번호 찾기 창 view 만들기
# email 대신 username 쓰기

# 비밀번호 찾기 tested
def search_password(request):  # ajax로 변경(done)
    data = json.loads(request.body)
    username = data['username']

    # 성공
    if Userable.objects.filter(username=username).exists():
        user = Userable.objects.get(username=username)

        pw_candidate = string.ascii_letters + string.digits + string.punctuation
        new_password = ""
        for i in range(10):
            new_password += random.choice(pw_candidate)

        user.set_password(new_password)
        user.save()

        subject = "From Audience"
        to = [username]
        from_email = "audience_likelion@naver.com"
        message = f'임시 비밀번호: {new_password}'
        EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
        return JsonResponse({'success': True})
    # 실패
    else:
        return JsonResponse({'success': False, 'error': f'"{username}" does not exist.'})

# 마이페이지
@login_required
def my_page(request):
    interest = UserInterest.objects.filter(userable=request.user)
    user_posts = Postable.objects.filter(userable=request.user)
    post = user_posts.order_by('-created_at')[:5]
    if request.user.type == "구직자":
        detail_user = Applicant.objects.get(id=request.user.id)
    else:
        detail_user = Employer.objects.get(id=request.user.id)
    return render(request, 'mypage.html', {'interest': interest, 'posts': post,
                                           'user_type': request.user.type, 'detail_user': detail_user})

def my_posts_detail(request):
    if request.user.is_authenticated:
        user = request.user
        post = Postable.objects.filter(userable=user)
        return render(request, 'my_library.html', {'post': post})

# 비밀번호 확인
def check_user_password(request):
    user = request.user
    password = request.POST.get('password')

    if request.method == "POST":
        if check_password(password, user.password):
            return redirect('update_account')
        else:
            return render(request, 'checkpw_error.html', {'error': 'no_match_password_error'})
    else:
        return render(request, 'checkpw_error.html')

# 아이디 중복 검사
def check_duplicate_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if Applicant.objects.filter(username=username).exists():
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

def check_duplicate_nickname(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        if Applicant.objects.filter(nickname=nickname).exists():
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

def check_duplicate_company(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        if Employer.objects.filter(company=company).exists:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

# 비면번호 변경
# render 사용해서 틀렸을 때 context에 error(key값으로 두 개) 넣어서 같은 페이지로 이동 (done)

def change_password(request):
    user = request.user
    password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$'

    if request.method == "POST":
        if check_password(password, user.password):
            if re.match(password_pattern, new_password):
                user.set_password(new_password)
                return render(request, 'changepw_complete.html')
            else:
                return render(request, 'changepw_error.html', {'error': 'wrong_password_error'})
        else:
            return render(request, 'changepw_error.html', {'error': 'no_match_password_error'})

    else:
        return render(request, 'changepw_error.html')


# 개인정보 수정

def update_account(request):
    user = request.user
    if request.method == "GET":
        if user.type == "구직자":
            detail_user = Applicant.objects.get(id=user.id)
            return render(request, 'change_p.html', {'detail_user': detail_user})
        else:
            detail_user = Employer.objects.get(id=user.id)
            return render(request, 'change_c.html', {'detail_user': detail_user})
    else:
        if user.type == "구직자":
            applicant = Applicant.objects.get(id=user.id)
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            age = request.POST.get('age')
            interest = request.POST.getlist('interest')
            school = request.POST.get('school')

            applicant.name = name
            applicant.gender = gender
            applicant.age = age
            applicant.school = school
            update_interest(applicant, interest)
            applicant.save()

            return render(request, 'change_complete.html')

        else:
            employer = Employer.objects.get(id=user.id)
            company = request.POST.get('company')
            interest = request.POST.getlist('interest')
            image = request.FILES.get('image')

            employer.company = company
            update_interest(employer, interest)
            if image:
                employer.image = image

            employer.save()

            return render(request, 'change_complete.html')

# 계정 삭제
@login_required
def delete_account(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if check_password(password2, request.user.password):
                request.user.delete()
                return redirect('account_login')
            else:
                return render(request, 'delete_error.html', {'error': 'no_match_password_error'})
        else:
            password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,20}$'
            if not re.match(password_pattern, request.POST.get('password1')):
                return render(request, 'delete_error.html', {'error': 'wrong_password_error'})
            else:
                return render(request, 'delete_error.html', {'error': 'no_match_password_error'})

    else:
        return render(request, 'delete_error.html')



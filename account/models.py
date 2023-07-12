from django.db import models
from django.contrib.auth.models import AbstractUser

class Userable(AbstractUser):
    first_name = None
    last_name = None
    username = models.CharField(max_length=16, unique=True, null=False, default='')     # 로그인 아이디
    name = models.CharField(max_length=16, null=False, default='')
    CHOICES = [
        ('선택', None), ('구직자', 'Applicant'), ('구인자', 'Employer')
    ]
    type = models.CharField(max_length=3, choices=CHOICES)

class Applicant(Userable):
    nickname = models.CharField(max_length=16, unique=True, null=False, default='')
    age = models.IntegerField(null=True)

    GENDER = [
        ('남자', 'male'), ('여자', 'female'), ('없음', '없음')
    ]
    gender = models.CharField(max_length=10, choices=GENDER)

    SCHOOL = [
        ('중졸', '중졸'), ('고졸', '고졸'), ('고졸', '고졸'), ('대학교 2,3년제', '대학교 2,3년제'),
        ('대학교 4년제', '대학교 4년제'), ('졸업 예정자', '졸업 예정자'), ('졸업자', '졸업자')
    ]
    school = models.CharField(max_length=10, choices=SCHOOL)

    career = models.ImageField(upload_to='applicant_career/', null=True)

class Employer(Userable):
    company = models.CharField(max_length=20, null=False, default='')
    age = models.IntegerField(null=True)
    image = models.ImageField(upload_to='company_profile/', null=True)


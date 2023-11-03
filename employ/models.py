from django.db import models

class Postable(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default = 0)
    userable = models.ForeignKey('account.Userable', on_delete=models.CASCADE, null=True)

class Employ_post(Postable):
    required_num = models.IntegerField(null=True)
    start_date = models.DateTimeField(max_length=20, null=True)
    end_date = models.DateTimeField(max_length=20, null=True)
    prefer_condition = models.CharField(max_length=30, null=True)
    image = models.ImageField(upload_to='post/employ/', null=True)
    CAREER_CHOICES = (('경력', '경력'), ('신입', '신입'))
    career = models.CharField(max_length=100, default='a', choices=CAREER_CHOICES, null=True)
    EMPLOY_SHAPE_CHOICES = (('인턴','인턴'),('정규직','정규직'),('비정규직','비정규직'))
    employ_shape = models.CharField(max_length=100, default='a', choices=EMPLOY_SHAPE_CHOICES , null=True)
    apply_method = models.CharField(max_length=50, null=True)

class Freepost_e (Postable):
    image = models.ImageField(upload_to="post/free_post_e", null=True, blank=True)


class Question(Postable):
    progress = models.CharField(max_length=100)
    employ_post_ref = models.ForeignKey(Employ_post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "post/question")


class Answer(Postable):
    image = models.ImageField(upload_to = "post/answer")

    question_ref = models.ForeignKey(Question, on_delete=models.CASCADE)



from django.db import models
from employ.models import Postable

# Create your models here.
class Job_post(Postable):
    image = models.ImageField(upload_to='post/job/')
    EMPLOY_SHAPE_CHOICES = (('인턴','인턴'),('정규직','정규직'),('비정규직','비정규직'))
    employ_shape = models.CharField(max_length=100, default='a', choices=EMPLOY_SHAPE_CHOICES )
    STARS = [
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
    ]
    rating = models.IntegerField(choices=STARS, null=True)
    search_company = models.CharField(max_length=20)


class Freepost_j(Postable):
    image = models.ImageField(upload_to = "free_post_j")

class report(models.Model):
    content = models.CharField(max_length=100)
    postable = models.ForeignKey('employ.Postable', on_delete=models.CASCADE)


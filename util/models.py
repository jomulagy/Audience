from django.db import models

class Like(models.Model):
    userable = models.ForeignKey('account.Userable', on_delete=models.CASCADE, null=True)
    postable = models.ForeignKey("employ.Postable", on_delete=models.CASCADE, null=True)

class Dislike(models.Model):
    userable = models.ForeignKey("account.Userable", on_delete=models.CASCADE, null=True)
    postable = models.ForeignKey("employ.Postable", on_delete=models.CASCADE, null=True)

class Interest(models.Model):
    name = models.CharField(max_length=16, null=False, default='')

class UserInterest(models.Model):
    interest = models.ForeignKey("util.Interest", on_delete=models.CASCADE, null=True)
    userable = models.ForeignKey("account.Userable", on_delete=models.CASCADE, null=True, related_name = "interest")

class Hashtag(models.Model):
    name = models.CharField(max_length=10, null=False, default='')
    postable = models.ManyToManyField('employ.Postable', related_name='posts')

class Rating(models.Model):
    STARS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    rate = models.IntegerField(choices=STARS, null=False, default='0')

class EmployerRating(models.Model):
    employer = models.ForeignKey("account.Employer", on_delete=models.CASCADE, null=True)
    applicant = models.ForeignKey("account.Applicant", on_delete=models.CASCADE, null=True)
    rating = models.ForeignKey("util.Rating", on_delete=models.CASCADE, null=True)
